import requests
from datetime import datetime
from urllib.parse import urlencode
from .exceptions import ParameterError, EInvoiceApiError

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'HIGH:!DH:!aNULL'
)


class CustomAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(CustomAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(CustomAdapter, self).proxy_manager_for(*args, **kwargs)


class InvoiceAPI:
    def __init__(self, app_id, api_key=None, timeout=10, stage="PROD"):
        self.app_id = app_id
        self.api_key = api_key
        if stage == "PROD":
            self.endpoint = "https://api.einvoice.nat.gov.tw"
        else:
            self.endpoint = "https://wwwtest.einvoice.nat.gov.tw"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.mount(self.endpoint, CustomAdapter())

    def _request(self, url: str, query_dict: dict):
        if query_dict:
            r = self.session.post(url + "?" + urlencode(query_dict))
        else:
            r = self.session.post(url)

        result = r.json()
        if result.get('code') == "200":
            return result
        else:
            if query_dict.get('appID'):
                query_dict.update({"appID": "xxxxxxxxxx" + query_dict["appID"][10:]})
            raise EInvoiceApiError(status_code=r.status_code, sub_code=result.get('code'), message=result.get('msg'),
                                   request_url=url + "?" + urlencode(query_dict))

    def get_winning_number(self, inv_term, version="0.2"):
        url = self.endpoint + "/PB2CAPIVAN/invapp/InvApp"
        query_dict = {
            "version": version,
            "action": "QryWinningList",
            "invTerm": inv_term,
            "appID": self.app_id
        }
        return self._request(url, query_dict)

    def get_invoice_header(self, inv_num, inv_date, uuid, version="0.5", inv_type="QRCode", generation="V2"):
        if inv_type not in ["QRCode", "Barcode"]:
            raise ParameterError(parameter_name="type", message="type should be 'QRCode' or 'Barcode'")
        try:
            datetime.strptime(inv_date, "%Y/%m/%d")
        except ValueError:
            raise ParameterError(parameter_name="inv_date", message="inv_date should be `%Y/%m/%d`")

        url = self.endpoint + "/PB2CAPIVAN/invapp/InvApp"
        query_dict = {
            "version": version,
            "type": inv_type,
            "invNum": inv_num,
            "action": "qryInvHeader",
            "generation": generation,
            "invDate": inv_date,
            "UUID": uuid,
            "appID": self.app_id
        }
        # print(url + "?" + urlencode(query_dict))
        return self._request(url, query_dict)

    def get_invoice_detail_from_qrcode(self, inv_num, inv_date, encrypt, seller_id, uuid, random_number, version="0.5", generation="V2"):
        url = self.endpoint + "/PB2CAPIVAN/invapp/InvApp"
        query_dict = {
            "version": version,
            "type": "QRCode",
            "invNum": inv_num,
            "action": "qryInvDetail",
            "generation": generation,
            "invDate": inv_date,
            "encrypt": encrypt,
            "sellerID": seller_id,
            "UUID": uuid,
            "randomNumber": random_number,
            "appID": self.app_id
        }
        # print(url + "?" + urlencode(query_dict))
        return self._request(url, query_dict)

    def get_invoice_detail_from_barcode(self, inv_num, inv_term, inv_date, uuid, random_number, version="0.5", generation="V2"):
        url = self.endpoint + "/PB2CAPIVAN/invapp/InvApp"
        query_dict = {
            "version": version,
            "type": "Barcode",
            "invNum": inv_num,
            "action": "qryInvDetail",
            "generation": generation,
            "invTerm": inv_term,
            "invDate": inv_date,
            "UUID": uuid,
            "randomNumber": random_number,
            "appID": self.app_id
        }
        # print(url + "?" + urlencode(query_dict))
        return self._request(url, query_dict)

