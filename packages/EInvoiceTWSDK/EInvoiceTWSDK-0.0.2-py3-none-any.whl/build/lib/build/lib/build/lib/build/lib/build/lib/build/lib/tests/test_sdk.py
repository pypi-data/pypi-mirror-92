import os
import unittest
from uuid import uuid4
from EInvoiceTWSDK import InvoiceAPI, parse_invoice_string_from_qrcode, parse_invoice_string_from_barcode


class MyTestCase(unittest.TestCase):

    def test_get_winning_number(self):
        invoice_api = InvoiceAPI(os.getenv("EINVOICE_API_ID"))
        r = invoice_api.get_winning_number(inv_term="10910")
        self.assertEqual(r.get('code'), "200")

    def test_get_invoice_header(self):
        invoice_api = InvoiceAPI(os.getenv("EINVOICE_API_ID"))
        raw_str = "KH1440387611001035057000000390000003c000000002898467872rStxzKloUSiNojOjCAJA==:**********:1:1:1:"
        invoice_info = parse_invoice_string_from_qrcode(raw_str)
        r = invoice_api.get_invoice_header(inv_num=invoice_info.get('inv_num'),
                                           inv_date=invoice_info.get('inv_date_ad'),
                                           uuid=str(uuid4()))
        self.assertEqual(r.get('code'), "200")

    def test_get_invoice_detail_from_qrcode(self):
        invoice_api = InvoiceAPI(os.getenv("EINVOICE_API_ID"))
        raw_str_qrcode = "KH1440387611001035057000000390000003c000000002898467872rStxzKloUSiNojOjCAJA==:**********:1:1:1:"
        invoice_info = parse_invoice_string_from_qrcode(raw_str_qrcode)
        r = invoice_api.get_invoice_detail_from_qrcode(inv_num=invoice_info.get('inv_num'),
                                                       inv_date=invoice_info.get('inv_date_ad'),
                                                       encrypt=invoice_info.get('encrypt'),
                                                       seller_id=invoice_info.get('seller_id'),
                                                       uuid=str(uuid4()),
                                                       random_number=invoice_info.get('random_number'))
        self.assertEqual(r.get('code'), "200")

    def test_get_invoice_detail_from_barcode(self):
        invoice_api = InvoiceAPI(os.getenv("EINVOICE_API_ID"))
        raw_str_barcode = "11002KH144038765057"
        invoice_info = parse_invoice_string_from_barcode(raw_str_barcode)
        r = invoice_api.get_invoice_detail_from_barcode(inv_num=invoice_info.get('inv_num'),
                                                        inv_term=invoice_info.get('inv_term'),
                                                        inv_date="2021/01/03",
                                                        uuid=str(uuid4()),
                                                        random_number=invoice_info.get('random_number'))
        self.assertEqual(r.get('code'), "200")


if __name__ == '__main__':
    unittest.main()
