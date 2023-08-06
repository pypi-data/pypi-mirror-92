from unittest import TestCase
import os
from uuid import uuid4
from EInvoiceTWSDK import parse_inv_date_to_inv_term


class Test(TestCase):
    def test_parse_inv_date_to_inv_term(self):
        self.assertEqual(parse_inv_date_to_inv_term("2021/01/01"), "11002")
        self.assertEqual(parse_inv_date_to_inv_term("2021/02/01"), "11002")
        self.assertEqual(parse_inv_date_to_inv_term("110/03/01"), "11004")
        self.assertEqual(parse_inv_date_to_inv_term("110/04/01"), "11004")
