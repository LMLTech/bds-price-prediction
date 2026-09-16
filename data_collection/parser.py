"""
HTML Parser module for real estate detail pages.
Extracts raw address text, normalized address, street, ward, district, province,
address source provenance, address category, and automated semantic validation status.

Includes DOM-context-aware tree scope isolation to prevent sidebar/recommendation
false positives.
"""

import re
from typing import Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup


def parse_detail_page(
    html_content: str,
    detail_url: str,
    original_title: str = "",
    original_location: str = ""
) -> Dict[str, Optional[str]]:
    """
    Parses a single listing detail page HTML to extract detailed location information.

    Returns dict with keys:
    - address_raw
    - address_normalized
    - street
    - ward
    - district_detail
    - province_detail
    - address_source
    - address_category
    - validation_status
    """
    if not html_content:
        return {
            "address_raw": None,
            "address_normalized": None,
            "street": None,
            "ward": None,
            "district_detail": None,
            "province_detail": None,
            "address_source": "unknown",
            "address_category": "missing",
            "validation_status": "insufficient_information"
        }

    soup = BeautifulSoup(html_content, "html.parser")

    # Isolate main listing container & decompose sidebar/recommendation/footer widgets
    main_container = _isolate_main_listing_container(soup)

    # 1. Extract raw address text and provenance source from main container
    address_raw, source = _extract_raw_address_and_source(main_container, original_title, original_location)

    # 2. Extract breadcrumbs for district / province structural fallback
    breadcrumb_district, breadcrumb_province = _extract_breadcrumbs(main_container)

    # 3. Parse components (street, ward, district, province)
    street = _extract_street(address_raw, original_title, detail_url)
    ward = _extract_ward(address_raw, original_title, html_content)
    district_detail = _extract_district(address_raw, original_title, original_location) or breadcrumb_district
    province_detail = _extract_province(address_raw, original_title, original_location) or breadcrumb_province

    # 4. Normalize address text
    address_normalized = _normalize_address(address_raw, street, ward, district_detail, province_detail)

    # 5. Classify address category
    address_category = _classify_address_category(address_raw, street, ward, district_detail, province_detail)

    # 6. Automated semantic validation against original_location
    validation_status = _validate_location_consistency(
        original_location=original_location,
        address_raw=address_raw,
        district_detail=district_detail,
        province_detail=province_detail
    )

    return {
        "address_raw": address_raw,
        "address_normalized": address_normalized,
        "street": street,
        "ward": ward,
        "district_detail": district_detail,
        "province_detail": province_detail,
        "address_source": source,
        "address_category": address_category,
        "validation_status": validation_status
    }


def _isolate_main_listing_container(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Creates a scoped DOM tree isolating the main listing content
    by decomposing sidebar, recommendation, related news, and footer containers.
    """
    # Clone tree to avoid mutating original if passed elsewhere
    soup_clone = BeautifulSoup(str(soup), "html.parser")

    # Decompose non-listing containers
    noise_selectors = [
        "div.row.mt-5", "div.box-right", "div.sidebar", "footer",
        ".recommended-area", ".box-location", ".recommended",
        "div.related-news", "div.footer", ".box-item"
    ]
    for sel in noise_selectors:
        for noise_el in soup_clone.select(sel):
            noise_el.decompose()

    # Prefer specific main content subcontainers if present
    main_el = soup_clone.select_one("div.left-detail, div.main-content, div.col-lg-9, div.product-detail, .main-detail")
    if main_el:
        return BeautifulSoup(str(main_el), "html.parser")

    return soup_clone


def _extract_raw_address_and_source(
    container: BeautifulSoup,
    original_title: str,
    original_location: str
) -> Tuple[Optional[str], str]:
    """Finds raw address text strictly inside the main listing container."""

    # Priority 1: Search for explicit "Địa chỉ:", "Vị trí:" in main listing text
    for el in container.find_all(["p", "div", "li", "span"]):
        text = el.get_text(" ", strip=True)
        if re.search(r'(Địa chỉ|Vị trí|Nằm tại|Tọa lạc)\s*:', text, re.IGNORECASE):
            match = re.search(r'(?:Địa chỉ|Vị trí|Nằm tại|Tọa lạc)\s*:\s*([^.\n]+)', text, re.IGNORECASE)
            if match:
                val = match.group(1).strip()
                if len(val) > 5 and not any(w in val.lower() for w in ["trang chủ", "bán nhà"]):
                    return val, "dedicated_address"

    # Priority 2: Check dedicated address selectors within main listing container
    selectors = [
        "div.address", "span.address", "p.address", "div.location-info",
        ".product-address", ".listing-address", "div.detail-address"
    ]
    for sel in selectors:
        el = container.select_one(sel)
        if el and el.get_text(strip=True):
            text = el.get_text(strip=True)
            if len(text) > 5 and not text.startswith("http"):
                return text, "dedicated_address"

    # Priority 3: Check H1 title for explicit address patterns (e.g. "Đường Lê Thị Bạch Cát, Phường 11, Quận 11")
    h1_el = container.find("h1")
    if h1_el:
        h1_text = h1_el.get_text(strip=True)
        match = re.search(r'((?:Đường|Đ\.|Phố|Ngõ|Hẻm|Mặt tiền)\s+[^:,]+(?:,\s*(?:Phường|P\.|Xã)\s+[^:,]+)?(?:,\s*(?:Quận|Q\.|Huyện|TP|Thị xã)\s+[^:,]+)?)', h1_text, re.IGNORECASE)
        if match:
            return match.group(1).strip(), "title"

    # Priority 4: Search lines in description box
    desc_el = container.select_one("div.content, div.description, div.box-characteristics, div.detail-content")
    if desc_el:
        desc_text = desc_el.get_text("\n", strip=True)
        lines = [line.strip() for line in desc_text.split("\n") if line.strip()]
        for line in lines:
            if re.search(r'(đường|phố|phường|xã|quận|huyện|ngõ|hẻm)\b', line, re.IGNORECASE):
                if len(line) < 150 and not any(w in line.lower() for w in ["diện tích", "số phòng", "mức giá", "sổ đỏ"]):
                    return line, "description"

    # Priority 5: Fallback to full H1 title text
    if h1_el and h1_el.get_text(strip=True):
        return h1_el.get_text(strip=True), "title"

    # Priority 6: Fallback to original title + location
    if original_title:
        return f"{original_title} - {original_location}", "fallback"

    return original_location, "fallback"


def _extract_breadcrumbs(container: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
    """Extracts district and province from breadcrumb navigation if present."""
    bc_items = container.select("ul.breadcrumb li, div.breadcrumb a, ol.breadcrumb li, .breadcrumb-item")
    crumbs = [item.get_text(strip=True) for item in bc_items if item.get_text(strip=True)]
    
    district = None
    province = None

    for crumb in crumbs:
        if re.search(r'\b(Hồ Chí Minh|Hà Nội|TP HCM|TP.HCM|HCM)\b', crumb, re.IGNORECASE):
            province = "Hồ Chí Minh" if "Hồ Chí Minh" in crumb or "HCM" in crumb else "Hà Nội"
        elif re.search(r'\b(Quận|Huyện|Thị xã|Thành phố|Q\.|H\.)\b', crumb, re.IGNORECASE):
            if crumb not in ["Bán nhà", "Trang chủ", "Bán nhà riêng", "Bán căn hộ"]:
                district = crumb

    return district, province


def _extract_street(text: Optional[str], title: str, url: str) -> Optional[str]:
    """Extracts street name using regex patterns from address text, title, or URL slug."""
    combined = f"{text or ''} {title or ''}"
    
    match = re.search(
        r'\b(?:Đường|Đ\.|Phố|Hẻm|Ngõ|Mặt tiền|Tên đường)\s+([A-ZĐÀÁẢẠÃĂẰẮẲẶẴÂẦẤẨẬẪÈÉẺẸẼÊỀẾỂỆỄÌÍỈỊĨÒÓỎỌÕÔỒỐỔỘỖƠỜỚỞỢỠÙÚỦỤŨƯỪỨỬỰỮỲÝỶỤỸa-zđàáảạãăằắẳặẵâầấẩậẫèéẻẹẽêềếểệễìíỉịĩòóỏọõôồốổộỗơờớởợỡùúủụũưừứửựữỳýỷụỹ0-9\s\-]+?)(?=[,\.\-\n]|\b(?:Phường|P\.|Xã|Quận|Q\.|Huyện|DT|Giá)|$)',
        combined,
        re.IGNORECASE
    )
    if match:
        street_candidate = match.group(0).strip()
        if len(street_candidate.split()) <= 8:
            return street_candidate.title()

    words = title.split()
    upper_sequences = []
    current_seq = []
    for w in words:
        cleaned = re.sub(r'[^\w]', '', w)
        if cleaned.isupper() and len(cleaned) > 1 and not cleaned.isdigit():
            current_seq.append(w)
        else:
            if len(current_seq) >= 2:
                upper_sequences.append(" ".join(current_seq))
            current_seq = []
    if current_seq and len(current_seq) >= 2:
        upper_sequences.append(" ".join(current_seq))

    for seq in upper_sequences:
        if not re.search(r'\b(SỔ ĐỎ|CHÍNH CHỦ|GIÁ RẺ|GẤP|HOT|Ô TÔ|CẦN BÁN|DT|DIỆN TÍCH|TẦNG|MẶT TIỀN|CỰC PHẨM|SIÊU PHẨM)\b', seq, re.IGNORECASE):
            return seq.title()

    return None


def _extract_ward(text: Optional[str], title: str, html: str) -> Optional[str]:
    """Extracts ward name using regex patterns."""
    combined = f"{text or ''} {title or ''}"
    
    match = re.search(
        r'\b(?:Phường|P\.|Xã|Thị trấn|Tổ)\s+([A-ZĐÀÁẢẠÃĂẰẮẲẶẴÂẦẤẨẬẪÈÉẺẸẼÊỀẾỂỆỄÌÍỈỊĨÒÓỎỌÕÔỒỐỔỘỖƠỜỚỞỢỠÙÚỦỤŨƯỪỨỬỰỮỲÝỶỤỸa-zđàáảạãăằắẳặẵâầấẩậẫèéẻẹẽêềếểệễìíỉịĩòóỏọõôồốổộỗơờớởợỡùúủụũưừứửựữỳýỷụỹ0-9\s]+?)(?=[,\.\-\n]|\b(?:Quận|Q\.|Huyện|TP|Tỉnh|DT|Giá)|$)',
        combined,
        re.IGNORECASE
    )
    if match:
        ward_candidate = match.group(0).strip()
        if len(ward_candidate.split()) <= 5:
            return ward_candidate.title()

    return None


def _extract_district(text: Optional[str], title: str, original_location: str) -> Optional[str]:
    """Extracts district from address text, title, or original location."""
    combined = f"{text or ''} {title or ''} {original_location or ''}"
    
    match = re.search(
        r'\b(?:Quận|Q\.|Huyện|Thị xã|TP\.)\s+([A-ZĐÀÁẢẠÃĂẰẮẲẶẴÂẦẤẨẬẪÈÉẺẸẼÊỀẾỂỆỄÌÍỈỊĨÒÓỎỌÕÔỒỐỔỘỖƠỜỚỞỢỠÙÚỦỤŨƯỪỨỬỰỮỲÝỶỤỸa-z0-9\s]+?)(?=[,\.\-\n]|\b(?:Hồ Chí Minh|Hà Nội|Tỉnh|DT|Giá)|$)',
        combined,
        re.IGNORECASE
    )
    if match:
        district_candidate = match.group(0).strip()
        if len(district_candidate.split()) <= 4:
            return district_candidate.title()

    if original_location:
        parts = [p.strip() for p in original_location.split(",")]
        if len(parts) >= 2:
            return parts[0]

    return None


def _extract_province(text: Optional[str], title: str, original_location: str) -> Optional[str]:
    """Extracts province/city from address text, title, or original location."""
    combined = f"{text or ''} {title or ''} {original_location or ''}"
    
    if re.search(r'\b(Hồ Chí Minh|HCM|TP.HCM|TPHCM)\b', combined, re.IGNORECASE):
        return "Hồ Chí Minh"
    elif re.search(r'\b(Hà Nội|HN)\b', combined, re.IGNORECASE):
        return "Hà Nội"

    if original_location:
        parts = [p.strip() for p in original_location.split(",")]
        if len(parts) >= 2:
            return parts[-1]
        elif len(parts) == 1:
            return parts[0]

    return None


def _normalize_address(
    address_raw: Optional[str],
    street: Optional[str],
    ward: Optional[str],
    district: Optional[str],
    province: Optional[str]
) -> Optional[str]:
    """Cleans up raw address text into a standardized representation."""
    if not address_raw:
        return None

    norm = address_raw
    norm = re.sub(r'\s+', ' ', norm).strip()
    norm = re.sub(r'(?::\s*DT\b|,\s*Giá\b|:\s*Giá\b|,\s*DT\b).*$', '', norm, flags=re.IGNORECASE).strip()
    norm = re.sub(r'[\s,:\-–]+$', '', norm).strip()

    norm = re.sub(r'\bĐ\.\s*', 'Đường ', norm)
    norm = re.sub(r'\bP\.\s*', 'Phường ', norm)
    norm = re.sub(r'\bQ\.\s*', 'Quận ', norm)
    norm = re.sub(r'\bH\.\s*', 'Huyện ', norm)
    norm = re.sub(r'\bTP\.?\s*HCM\b', 'Hồ Chí Minh', norm, flags=re.IGNORECASE)
    norm = re.sub(r'\bHN\b', 'Hà Nội', norm)

    if len(norm) < 5 or "http" in norm:
        components = [c for c in [street, ward, district, province] if c]
        if components:
            return ", ".join(components)

    return norm


def _classify_address_category(
    address_raw: Optional[str],
    street: Optional[str],
    ward: Optional[str],
    district: Optional[str],
    province: Optional[str]
) -> str:
    """Classifies extracted address into structural granularity categories."""
    if not address_raw:
        return "missing"

    raw_lower = address_raw.lower()

    is_alley = bool(re.search(r'\b(hẻm|ngõ|ngách|hẻm xe hơi|hxh)\b', raw_lower))
    is_project = bool(re.search(r'\b(khu đô thị|kđt|khu dân cư|kdc|dự án|chung cư|căn hộ)\b', raw_lower))
    has_house_num = bool(re.search(r'\b\d+/\d*|\b\d+[a-z]?\s+(?:đường|phố|hẻm|ngõ)', raw_lower))
    has_street = bool(street or re.search(r'\b(đường|phố)\b', raw_lower))
    has_ward = bool(ward or re.search(r'\b(phường|xã|p\.)\b', raw_lower))
    has_district = bool(district or re.search(r'\b(quận|huyện|q\.)\b', raw_lower))

    if (has_house_num or is_alley) and has_street and has_ward and has_district:
        return "full_address"
    elif is_project:
        return "project_or_residential_area"
    elif is_alley:
        return "alley_or_lane"
    elif has_house_num and has_street:
        return "house_number_and_street"
    elif has_street and has_ward:
        return "street_and_ward"
    elif has_street:
        return "street_only"
    elif re.search(r'\b(gần|cạnh|đối diện|ngay)\b', raw_lower):
        return "landmark_only"
    
    return "unclear"


def _validate_location_consistency(
    original_location: str,
    address_raw: Optional[str],
    district_detail: Optional[str],
    province_detail: Optional[str]
) -> str:
    """Automated semantic validation comparing original coarse location vs extracted location."""
    if not address_raw:
        return "insufficient_information"

    orig_parts = [p.strip().lower() for p in original_location.split(",")]
    orig_district = orig_parts[0] if len(orig_parts) >= 2 else None
    orig_province = orig_parts[-1] if len(orig_parts) >= 1 else None

    ext_dist_lower = district_detail.lower() if district_detail else ""
    ext_prov_lower = province_detail.lower() if province_detail else ""

    if orig_province:
        if ("hồ chí minh" in orig_province or "hcm" in orig_province) and "hà nội" in ext_prov_lower:
            return "suspicious"
        if "hà nội" in orig_province and ("hồ chí minh" in ext_prov_lower or "hcm" in ext_prov_lower):
            return "suspicious"

    if orig_district and ext_dist_lower:
        clean_orig_dist = re.sub(r'\b(quận|huyện|q\.|h\.)\s*', '', orig_district).strip()
        clean_ext_dist = re.sub(r'\b(quận|huyện|q\.|h\.)\s*', '', ext_dist_lower).strip()

        if clean_orig_dist == clean_ext_dist or clean_orig_dist in ext_dist_lower:
            return "consistent"
        elif clean_orig_dist not in ext_dist_lower:
            if re.search(r'\b(quận|huyện)\s+[a-z0-9]+', address_raw.lower()):
                return "suspicious"
            return "partially_consistent"

    if ext_prov_lower or ext_dist_lower:
        return "partially_consistent"

    return "insufficient_information"
