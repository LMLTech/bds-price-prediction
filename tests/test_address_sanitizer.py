from data_collection.geocoding import sanitize_address_for_geocoding

def test_1_marketing_prefix():
    raw = "Bán nhà đẹp mới xây // An Dương Vương, p An Lạc dt 52m2 2 lầu 4pn 5wc"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Bình Tân")
    assert "Bán nhà" not in res["sanitized_address"]
    assert "An Dương Vương" in res["sanitized_address"]
    assert "An Lạc" in res["sanitized_address"]

def test_2_marketing_suffix():
    raw = "Đường Lê Văn Sỹ, Phường 13, Quận 3 giá nhỉnh 5 tỷ"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Quận 3")
    assert "nhỉnh 5 tỷ" not in res["sanitized_address"]
    assert "Lê Văn Sỹ" in res["sanitized_address"]

def test_3_frontage_description():
    raw = "Mặt tiền 4m đường Nguyễn Trãi, Thanh Xuân"
    res = sanitize_address_for_geocoding(raw, province="Hà Nội", district="Thanh Xuân")
    assert "4m" not in res["sanitized_address"]
    assert "Nguyễn Trãi" in res["sanitized_address"]

def test_4_alley_preservation():
    raw = "Hẻm 123 đường Lê Văn Sỹ"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Quận 3")
    assert "Hẻm 123" in res["sanitized_address"]
    assert "Lê Văn Sỹ" in res["sanitized_address"]

def test_5_house_number_protection():
    raw = "123/4B Nguyễn Trãi, Phường 2"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Quận 5")
    assert "123/4B" in res["sanitized_address"]
    assert "Nguyễn Trãi" in res["sanitized_address"]

def test_6_administrative_context():
    raw = "Quang Trung, Phường 11, Gò Vấp"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Gò Vấp")
    assert "Quang Trung" in res["geocoding_query"]
    assert "Phường 11" in res["geocoding_query"]
    assert "Thành phố Hồ Chí Minh" in res["geocoding_query"]

def test_7_project_preservation():
    raw = "Bán nhà đất dịch vụ KĐT Văn Khê, 50m2, 5 tầng, nhỉnh 8 tỷ"
    res = sanitize_address_for_geocoding(raw, province="Hà Nội", district="Hà Đông")
    assert "KĐT Văn Khê" in res["sanitized_address"] or "Văn Khê" in res["sanitized_address"]
    assert "nhỉnh 8 tỷ" not in res["sanitized_address"]

def test_8_already_clean_address():
    raw = "Đường Lê Văn Sỹ, Phường 13, Quận 3, Hồ Chí Minh"
    res = sanitize_address_for_geocoding(raw, province="Hồ Chí Minh", district="Quận 3")
    assert "Lê Văn Sỹ" in res["sanitized_address"]
    assert "Phường 13" in res["sanitized_address"]
