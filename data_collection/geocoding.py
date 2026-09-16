import re
import unicodedata

def sanitize_address_for_geocoding(address_raw: str, province: str = None, district: str = None) -> dict:
    """
    Sanitizes raw real-estate address text for geocoding while strictly preserving location information.
    
    Returns dict:
        - address_raw: Original raw input
        - sanitized_address: Core cleaned street/alley/ward location
        - geocoding_query: Formatted final query for geocoder
        - removed_tokens: List of removed marketing/spec terms
        - preserved_tokens: List of preserved geographic tokens
        - preservation_audit: Dict tracking status of house, street, ward, district, province, alley, project
    """
    if not address_raw or not isinstance(address_raw, str):
        address_raw = ""

    orig = address_raw
    text = address_raw

    removed_tokens = []

    # 1. Normalize Unicode & Punctuation symbols (preserve '/' when part of house numbers like 123/4B)
    text = unicodedata.normalize('NFC', text)
    # Replace double slashes // with space
    text = re.sub(r'//+', ' ', text)
    # Replace non-standard dashes, separators, emojis with space
    text = re.sub(r'[\\_–—|🔥✨⚡📌🔴⭐]', ' ', text)
    
    # 2. Extract and protect marketing words / specs to remove
    # Price patterns
    price_pattern = r'\b(giá\s*)?(\d+([.,]\d+)?\s*(tỷ|tỉ|triệu|tr|đồng|đ|tr/tháng)\b[^\,]*|nhỉnh\s*\d+\s*(tỷ|tỉ|đồng|đ)|chỉ\s*(hơn\s*)?\d+([.,]\d+)?\s*(tỷ|tỉ)|6\.x\s*tỷ|2tỷ\s*hơn|nhỉnh\s*\d+\s*đồng)'
    for m in re.finditer(price_pattern, text, flags=re.IGNORECASE):
        removed_tokens.append(m.group(0))
    text = re.sub(price_pattern, ' ', text, flags=re.IGNORECASE)

    # Dimensions & Area specs: dt 52m2, 30m2, (4x11), 10*9, 4x8.5m, 41x18m, 32m2 x 5 tầng, 35m2, 43m2
    dim_pattern = r'(\bdt\s*\d+m2?|\b\d+m2?\b|\(\d+x\d+\)|\b\d+[\*x]\d+([.,]\d+)?m?|\bngang\s*\d+m\b|\btrước\s*nhà\s*\d+([.,]\d+)?m\b)'
    for m in re.finditer(dim_pattern, text, flags=re.IGNORECASE):
        removed_tokens.append(m.group(0))
    text = re.sub(dim_pattern, ' ', text, flags=re.IGNORECASE)

    # Property specs & floor counts: 2 lầu 4pn 5wc, 5 tầng, 3 tầng, thang máy, full nội thất
    specs_pattern = r'\b(\d+\s*lầu|\d+\s*pn|\d+\s*wc|\d+\s*tầng|thang\s*máy|full\s*nội\s*thất|nội\s*thất\s*đầy\s*đủ|sẵn\s*thu\s*nhập|tặng\s*full\s*nội\s*thất)\b'
    for m in re.finditer(specs_pattern, text, flags=re.IGNORECASE):
        removed_tokens.append(m.group(0))
    text = re.sub(specs_pattern, ' ', text, flags=re.IGNORECASE)

    # Real-estate Marketing transaction prefixes & phrases
    marketing_phrases = [
        r'\bbán\s*nhà\s*riêng\s*chính\s*chủ\b',
        r'\bbán\s*nhà\s*chính\s*chủ\b',
        r'\bbán\s*nhà\s*đất\b',
        r'\bbán\s*nhà\b',
        r'\bbán\s*căn\s*hộ\b',
        r'\bbán\s*đất\b',
        r'\bsiêu\s*phẩm\b',
        r'\bcực\s*phẩm\b',
        r'\bchính\s*chủ\b',
        r'\bsổ\s*đẹp\b',
        r'\bsổ\s*đỏ\s*chính\s*chủ\b',
        r'\bnhà\s*đẹp\s*mới\s*xây\b',
        r'\bnhà\s*đẹp\b',
        r'\bnhà\s*mới\b',
        r'\bngõ\s*thông\s*tứ\s*tung\b',
        r'\bô\s*tô\s*tránh\b',
        r'\bô\s*tô\s*đỗ\s*cửa\b',
        r'\bô\s*tô\s*ngủ\s*trong\s*nhà\b',
        r'\bô\s*tô\s*vào\s*nhà\b',
        r'\bgần\s*ô\s*tô\b',
        r'\bphố\s*ô\s*tô\b',
        r'\bgara\s*4\s*ô\s*tô\b',
        r'\bkinh\s*doanh\b',
        r'\bở\s*sướng\b',
        r'\brẻ\s*nhất\b',
        r'\bphân\s*lô\b',
        r'\bsẵn\s*sàng\s*đón\s*tết\b',
        r'\bchủ\s*nhà\s*bán\s*lại\b',
        r'\bở\s*ngay\b',
        r'\bsát\s*quận\s*1\b',
        r'\btuần\s*lễ\b',
        r'\bhiếm\b',
        r'\bđộc\s*quyền\b',
        r'\btl\b',
        r'\bctl\b'
    ]
    for p in marketing_phrases:
        for m in re.finditer(p, text, flags=re.IGNORECASE):
            removed_tokens.append(m.group(0))
        text = re.sub(p, ' ', text, flags=re.IGNORECASE)

    # 3. Clean frontage / alley descriptions without losing actual alley number
    # "Hẻm xe hơi 8m" -> keep "Hẻm" if no number, but strip "xe hơi 8m"
    text = re.sub(r'\bhẻm\s*xe\s*hơi\s*\d+m\b', 'Hẻm', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhẻm\s*xe\s*hơi\b', 'Hẻm', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhxh\b', 'Hẻm', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmặt\s*tiền\s*\d+m\b', 'Mặt tiền', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmặt\s*tiền\b', '', text, flags=re.IGNORECASE)

    # 4. Clean extra punctuation except slash inside house numbers (e.g., 123/4B)
    text = re.sub(r'[,\.\-;\:\?\!\(\)]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Extract preservation tokens & audit
    preserved_tokens = [w for w in text.split() if w]
    
    # Audit preserved geographic features
    has_house_num = bool(re.search(r'\b\d+([/\-]\d+)*[a-zA-Z]?\b', text))
    has_street = bool(re.search(r'\b(đường|phố|trần|lê|nguyễn|phạm|hoàng|võ|lạc|quang|khuất|xuân|ngọc|tôn|ngô)\b', text, flags=re.IGNORECASE))
    has_ward = bool(re.search(r'\b(phường|p\.|p\b)\s*\d*\b', text, flags=re.IGNORECASE))
    has_alley = bool(re.search(r'\b(hẻm|ngõ|ngách)\b', text, flags=re.IGNORECASE))
    has_project = bool(re.search(r'\b(kđt|dự\s*án|khu\s*đô\s*thị|chung\s*cư)\b', text, flags=re.IGNORECASE))

    preservation_audit = {
        "house_number": "PRESERVED" if has_house_num else "NOT_PRESENT",
        "street": "PRESERVED" if has_street else "NOT_PRESENT",
        "ward": "PRESERVED" if has_ward else "NOT_PRESENT",
        "district": "PRESERVED" if district else "NOT_PRESENT",
        "province": "PRESERVED" if province else "NOT_PRESENT",
        "alley": "PRESERVED" if has_alley else "NOT_PRESENT",
        "project": "PRESERVED" if has_project else "NOT_PRESENT"
    }

    # 6. Format final geocoding query
    parts = []
    if text:
        parts.append(text)
    
    if district and district.strip():
        d_str = district.strip()
        if d_str.lower() not in text.lower():
            if d_str.isdigit():
                parts.append(f"Quận {d_str}")
            elif not d_str.lower().startswith(("quận", "huyện", "thành phố", "tp")):
                parts.append(f"Quận {d_str}" if d_str in ["1","2","3","4","5","6","7","8","9","10","11","12"] else d_str)
            else:
                parts.append(d_str)

    if province and province.strip():
        p_str = province.strip()
        if p_str.lower() not in text.lower():
            if p_str in ["Hồ Chí Minh", "HCMC", "TP.HCM"]:
                parts.append("Thành phố Hồ Chí Minh")
            elif p_str in ["Hà Nội", "HN"]:
                parts.append("Thành phố Hà Nội")
            else:
                parts.append(p_str)

    parts.append("Việt Nam")
    
    geocoding_query = ", ".join(parts)

    return {
        "address_raw": orig,
        "sanitized_address": text,
        "geocoding_query": geocoding_query,
        "removed_tokens": list(set(removed_tokens)),
        "preserved_tokens": preserved_tokens,
        "preservation_audit": preservation_audit
    }
