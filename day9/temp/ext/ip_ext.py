def check_ip(ip_address):
    """
    检查IP地址合法性,0.0.0.0 - 255.255.255.255 之间都为有效地址
    :param ip_address:
    :return:
    """
    import re
    pattern = "(2(5[0-5]|[0-4][0-9])|1\d{2}|[1-9]\d|[0-9])(\.(2(5[0-5]|[0-4][0-9])|1\d{2}|[1-9]\d|[0-9])){3}$"
    result = re.match(pattern, ip_address)
    return True if result else False


print(check_ip("0.0.7.255"))