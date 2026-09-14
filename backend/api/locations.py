from fastapi import APIRouter
import src.features as features

router = APIRouter()

# Grouping districts according to src.features.DISTRICT_COORDINATES definition
HCMC_DISTRICTS = [
    "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 7", "Quận 8",
    "Quận 10", "Quận 11", "Quận 12", "Bình Thạnh", "Gò Vấp", "Tân Bình",
    "Tân Phú", "Bình Tân", "Thủ Đức", "Phú Nhuận", "Bình Chánh", "Hóc Môn",
    "Củ Chi", "Nhà Bè", "Cần Giờ"
]

HANOI_DISTRICTS = [
    "Hoàn Kiếm", "Ba Đình", "Đống Đa", "Hai Bà Trưng", "Cầu Giấy", "Thanh Xuân",
    "Tây Hồ", "Long Biên", "Hoàng Mai", "Nam Từ Liêm", "Bắc Từ Liêm", "Hà Đông",
    "Thanh Trì", "Gia Lâm", "Đông Anh", "Hoài Đức", "Đan Phượng", "Thường Tín",
    "Phúc Thọ", "Sơn Tây", "Thạch Thất", "Chương Mỹ", "Quốc Oai", "Mê Linh", "Sóc Sơn"
]


@router.get("/locations")
def get_locations():
    return {
        "provinces": [
            {
                "name": "TP. Hồ Chí Minh",
                "districts": HCMC_DISTRICTS
            },
            {
                "name": "Hà Nội",
                "districts": HANOI_DISTRICTS
            }
        ]
    }
