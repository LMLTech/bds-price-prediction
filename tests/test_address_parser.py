"""
Regression tests for data_collection/parser.py to verify DOM-context-aware address extraction
and prevent sidebar/recommended-area false positives.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_collection.parser import parse_detail_page


class TestAddressParser(unittest.TestCase):
    """Regression test suite for address parser DOM context handling."""

    def test_sidebar_recommendation_bug_regression(self):
        """
        Test Case 1: Discovered bug regression.
        Verifies that a page with a sidebar recommendation containing 'Tân Phú, Hồ Chí Minh'
        or 'Hoài Đức, Hà Nội' extracts the property's actual address from the main listing container.
        """
        html_fixture = """
        <!DOCTYPE html>
        <html>
        <body>
            <div class="container dangtin">
                <div class="row">
                    <div class="col-lg-9 fix">
                        <div class="main-content">
                            <h1>Chính Chủ Bán HXH 182M Đường Lê Thị Bạch Cát, Phường 11, Quận 11: DT 4.15x20m</h1>
                            <div class="content">
                                <p>Cần bán gấp nhà Đường Lê Thị Bạch Cát, Phường 11, Quận 11.</p>
                            </div>
                        </div>
                        <div class="row mt-5">
                            <div class="address">Tân Phú, Hồ Chí Minh</div>
                            <div class="address">Quận 7, Hồ Chí Minh</div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        result = parse_detail_page(
            html_content=html_fixture,
            detail_url="https://batdongsan.vn/test-listing-r12345",
            original_title="Chính Chủ Bán HXH 182M Đường Lê Thị Bạch Cát, Phường 11, Quận 11",
            original_location="Quận 11, Hồ Chí Minh"
        )

        self.assertIsNotNone(result["address_raw"])
        self.assertNotIn("Tân Phú", result["address_raw"])
        self.assertIn("Lê Thị Bạch Cát", result["address_raw"])
        self.assertEqual(result["street"], "Đường Lê Thị Bạch Cát")
        self.assertEqual(result["district_detail"], "Quận 11")

    def test_generalized_sidebar_protection(self):
        """
        Test Case 2: Generalized sidebar protection.
        Verifies that parser ignores ANY arbitrary location string inside sidebar/recommendation
        containers and extracts the property's address from the main container.
        """
        html_fixture = """
        <!DOCTYPE html>
        <html>
        <body>
            <div class="container main-listing">
                <div class="left-detail">
                    <h1>Bán nhà mặt phố 45 Phố Huế, Phường Hàng Bài, Quận Hoàn Kiếm</h1>
                    <div class="content">
                        <p>Địa chỉ: 45 Phố Huế, Phường Hàng Bài, Quận Hoàn Kiếm</p>
                    </div>
                </div>
                <div class="sidebar box-right">
                    <div class="address">Quận Cầu Giấy, Hà Nội</div>
                    <div class="address">Huyện Đông Anh, Hà Nội</div>
                </div>
            </div>
        </body>
        </html>
        """

        result = parse_detail_page(
            html_content=html_fixture,
            detail_url="https://batdongsan.vn/test-listing-r67890",
            original_title="Bán nhà mặt phố 45 Phố Huế",
            original_location="Hoàn Kiếm, Hà Nội"
        )

        self.assertIsNotNone(result["address_raw"])
        self.assertNotIn("Cầu Giấy", result["address_raw"])
        self.assertNotIn("Đông Anh", result["address_raw"])
        self.assertIn("Phố Huế", result["address_raw"])
        self.assertEqual(result["province_detail"], "Hà Nội")

    def test_main_container_dedicated_address(self):
        """
        Test Case 3: Dedicated address tag inside main container.
        Verifies proper extraction when an explicit address element is present in the main container.
        """
        html_fixture = """
        <!DOCTYPE html>
        <html>
        <body>
            <div class="main-detail">
                <h1>Bán nhà 123 Nguyễn Trãi</h1>
                <div class="address">123 Nguyễn Trãi, Phường Bến Thành, Quận 1</div>
            </div>
            <div class="footer-recommendations">
                <div class="address">Thủ Đức, Hồ Chí Minh</div>
            </div>
        </body>
        </html>
        """

        result = parse_detail_page(
            html_content=html_fixture,
            detail_url="https://batdongsan.vn/test-listing-r11111",
            original_title="Bán nhà 123 Nguyễn Trãi",
            original_location="Quận 1, Hồ Chí Minh"
        )

        self.assertIsNotNone(result["address_raw"])
        self.assertIn("Nguyễn Trãi", result["address_raw"])
        self.assertNotIn("Thủ Đức", result["address_raw"])
        self.assertEqual(result["address_source"], "dedicated_address")


if __name__ == "__main__":
    unittest.main()
