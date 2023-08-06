
def parse_invoice_string_from_qrcode(raw_str: str) -> dict:
    """
    :param raw_str: string from invoice's qrcode
    :return: the result dict
        inv_num: 發票字軌 (10)：記錄發票完整十碼號碼。
        inv_date: 發票開立日期 (7)：記錄發票三碼民國年份二碼月份二碼日期。
        random_number: 隨機碼 (4)：記錄發票上隨機碼四碼。
        sales_figure: 銷售額 (8), 記錄發票上未稅之金額總計八碼，原始數據將金額轉換以十六進位方式記載，回傳值已轉回十進位。若營業人銷售系統無法順利將稅項分離計算，則以00000000 記載。
        total: 記錄發票上含稅總金額總計八碼，原始數據將金額轉換以十六進位方式記載，回傳值已轉回十進位。。
        buyer_id: 記錄發票上買受人統一編號，若買受人為一般消費者則以 00000000 記載。
        seller_id: 賣方統一編號 (8)：記錄發票上賣方統一編號。
        encrypt: 將發票字軌十碼及隨機碼四碼以字串方式合併後使用 AES 加密並採用 Base64 編碼轉換
    :rtype: dict
    """
    data = {
        "inv_num": raw_str[0:10],
        "inv_date": raw_str[10:17],
        "inv_date_ad": _parse_roc_to_ad(raw_str[10:17]),
        "random_number": raw_str[17:21],
        "sales_figure": int(raw_str[21:29], 16),
        "total": int(raw_str[29:37], 16),
        "buyer_id": raw_str[37:45],
        "seller_id": raw_str[45:53],
        "encrypt": raw_str[53:77]
    }
    return data


def parse_invoice_string_from_barcode(raw_str: str) -> dict:
    """
    :param raw_str: string from invoice's barcode
    :return: the result dict
        inv_term: 發票年期別 (5)：記錄發票字軌所屬民國年份(3 碼)及期別之雙數月份(2 碼)
        inv_num: 發票字軌 (10)：記錄發票完整十碼號碼。
        random_number: 隨機碼 (4)：記錄發票上隨機碼四碼。
    :rtype: dict
    """
    data = {
        "inv_term": raw_str[0:5],
        "inv_num": raw_str[5:15],
        "random_number": raw_str[15:19]
    }
    return data


def parse_inv_date_to_inv_term(inv_date: str) -> str:
    """
    :param inv_date:
    :return: inv_term 發票期別(發票民國年月,年分為民國年,月份必須為雙數月)
    """
    ymd = inv_date.split("/")

    # term
    if int(ymd[1]) % 2 == 0:
        term = ymd[1].zfill(2)
    else:
        term = str(int(ymd[1]) + 1).zfill(2)

    # year
    if len(ymd[0]) == 4:
        "yyyy/MM/dd"
        year = str(int(ymd[0]) - 1911)
    elif len(ymd[0]) == 3:
        "yyy(roc)/MM/dd"
        year = ymd[0]
    else:
        raise ValueError

    return "{yyy}{term}".format(yyy=year, term=term)


def _parse_roc_to_ad(roc_date: str) -> str:
    return "{year}/{month}/{date}".format(year=str(int(roc_date[0:3]) + 1911),
                                          month=roc_date[3:5],
                                          date=roc_date[5:7])
