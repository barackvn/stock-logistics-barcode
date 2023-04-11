# © 2019 Wassim Ghannoum <wassim@mediaengagers.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo.exceptions import ValidationError
from odoo.tests import common

_logger = logging.getLogger(__name__)


class TestGS1Barcode(common.TransactionCase):
    def test_decode(self):
        GS = "\x1D"
        PREFIX = ""
        # AI 01 (GTIN, fixed length)
        gtin = "03400933816759"
        # AI 17 (expiry date) - day 0 will be replaced with day 31
        expiry = "140500"
        # AI 10 (lot number, variable length)
        lot = "B04059A"
        # AI 310 (Net Weight in Kg, 5 decimals)
        weight = "006385"
        barcode = f"{PREFIX}01{gtin}"
        barcode += f"17{expiry}"
        barcode += f"10{lot}{GS}"
        barcode += f"3105{weight}"
        expiry = "140501"
        barcode += f"15{expiry}"
        result = self.env["gs1_barcode"].decode(barcode)
        assert len(result) == 5, "The barcode should decode to 5 AIs"
        assert result.get("01") == gtin, f"The GTIN should be {gtin}"
        assert result.get("17") == "2014-05-31"
        assert result.get("10") == lot, f"The lot should be {lot}"
        assert result.get("310") == 0.06385, f"The weight should be {weight}"
        # AI 311 (expiry date) - day 0 will be replaced with day 31
        expiry = "140515"
        # AI 11 (lot number, variable length)
        lot = "B04059A"
        weight = "006385"
        barcode = f"{PREFIX}01{gtin}"
        barcode += f"11{expiry}"
        result = self.env["gs1_barcode"].decode(barcode)
        assert len(result) == 2, "The barcode should decode to 4 AIs"
        assert result.get("11") == "2014-05-15"
        gtin = "03400933816759"
        # AI 17 (expiry date) - day 0 will be replaced with day 31
        expiry = "140522"
        # AI 10 (lot number, variable length)
        lot = "B04059A"
        # AI 310 (Net Weight in Kg, 5 decimals)
        weight = "006385"
        barcode = f"{PREFIX}01{gtin}17"
        barcode += f"{expiry}10{lot}{GS}3105{weight}"
        result = self.env["gs1_barcode"].decode(barcode)
        assert len(result) == 4, "The barcode should decode to 4 AIs"
        assert result.get("01") == gtin, f"The GTIN should be {gtin}"
        assert result.get("17") == "2014-05-22"
        assert result.get("10") == lot, f"The lot should be {lot}"
        try:
            self.env["gs1_barcode"].decode(barcode)
        except ValidationError as exc:
            _logger.error(exc)
