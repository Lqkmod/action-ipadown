import requests
import threading
import os
import random
import string
from datetime import datetime

# Danh sách các URL API để lấy proxy
urls = [
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
]

# Danh sách tổng hợp proxy
proxy_list = []

# Lặp qua từng URL để lấy proxy
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        proxy_list.extend(response.text.splitlines())

# Hàm kiểm tra proxy
def check_proxy(proxy, live_proxies):
    try:
        # Sử dụng proxy để kết nối tới một trang web
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        
        # Nếu kết nối thành công, lưu proxy vào danh sách live_proxies
        if response.status_code == 200:
            live_proxies.append(proxy)
    except:
        # Nếu kết nối thất bại, bỏ qua proxy đó
        pass

# Danh sách các proxy còn hoạt động
live_proxies = []

# Sử dụng threading để kiểm tra proxy nhanh hơn
threads = []

for proxy in proxy_list:
    t = threading.Thread(target=check_proxy, args=(proxy, live_proxies))
    t.start()
    threads.append(t)

# Đợi tất cả các thread hoàn thành
for t in threads:
    t.join()

# Tạo tên file ngẫu nhiên
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
file_name = f"live_{timestamp}_{random_str}.txt"

# Ghi danh sách proxy live vào file mới tạo
with open(file_name, "w") as file:
    for proxy in live_proxies:
        file.write(proxy + "\n")

print(f"{len(live_proxies)} proxy còn hoạt động đã được lưu vào file {file_name}")