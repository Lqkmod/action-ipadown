import requests
import os
import re
import sys
from rich.console import Console
from time import sleep
import requests, threading, time
from datetime import datetime
from pystyle import Write,Colors
import requests, re, os, sys, time
os.system("cls" if os.name == "nt" else "clear")
def banner():
    banner = ('''
              \033[1;91mDeveloper Tool: \033[1;37mKHANG DINO                  \033[1;91mBy: \033[1;37mDINO TOOL
\x1b[1;35m==================================================================================
\033[1;91m[\033[1;32m</>\033[1;91m] => \033[1;32mTool Get Token EAAD6V7 Bằng Cookie
\033[1;91m[\033[1;32m</>\033[1;91m] => \033[1;32mFacebook Admin Tool: https://www.facebook.com/lequockhang666?mibextid=LQQJ4d
\033[1;91m[\033[1;32m</>\033[1;91m] 
\033[1;91m[\033[1;32m</>\033[1;91m] => \033[1;32mĐã Update Ngày: 27/8/2024
\033[1;91m[\033[1;32m</>\033[1;91m] => \033[1;32mChúc Năm Mới Hai Ta Luôn Bên Nhau Mãi Mãi Và Yêu Nhau Nhiều Hơn <3
\033[1;91m[\033[1;32m</>\033[1;91m] => \033[1;91mTool Coppyright DINO TOOL
\x1b[1;35m==================================================================================
''')
    for i in banner:
      sys.stdout.write(i)
      sys.stdout.flush()
      time.sleep(0.000)
banner()
do = "\033[1;91m"
xanhbien = "\033[32;5;245m\033[1m\033[38;5;39m"
vang = "\033[0;33m"
trang = "\033[1;37m"
xanhla = "\033[1;32m"
Xb = "\033[1;36m"
tim = "\x1b[1;35m"
console = Console()


def change_cookies_fb(cookies: str):
    result = {}
    try:
        for i in cookies.split(';'):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result
    except(Exception,):
        for i in cookies.split('; '):
            result.update({i.split('=')[0]: i.split('=')[1]})
        return result


def clear():
    try:
        if "linux" in sys.platform.lower():
            os.system("clear")
        elif "win" in sys.platform.lower():
            os.system("cls")
        else:
            os.system("clear")
    except (Exception,):
        os.system("cls")


class GETTOKEN:
    def __init__(self, cookie_re: str):
        self.cookies = change_cookies_fb(cookie_re)

        self.facebook_android = [
            "275254692598279"
        ]
    def run(self):
        get_data = requests.get(
            "https://www.facebook.com/v2.3/dialog/oauth", params={
                'redirect_uri': 'fbconnect://success',
                'scope': 'email,publish_actions,publish_pages,user_about_me,user_actions.books,user_actions.music,user_actions.news,user_actions.video,user_activities,user_birthday,user_education_history,user_events,user_games_activity,user_groups,user_hometown,user_interests,user_likes,user_location,user_notes,user_photos,user_questions,user_relationship_details,user_relationships,user_religion_politics,user_status,user_subscriptions,user_videos,user_website,user_work_history,friends_about_me,friends_actions.books,friends_actions.music,friends_actions.news,friends_actions.video,friends_activities,friends_birthday,friends_education_history,friends_events,friends_games_activity,friends_groups,friends_hometown,friends_interests,friends_likes,friends_location,friends_notes,friends_photos,friends_questions,friends_relationship_details,friends_relationships,friends_religion_politics,friends_status,friends_subscriptions,friends_videos,friends_website,friends_work_history,ads_management,create_event,create_note,export_stream,friends_online_presence,manage_friendlists,manage_notifications,manage_pages,photo_upload,publish_stream,read_friendlists,read_insights,read_mailbox,read_page_mailboxes,read_requests,read_stream,rsvp_event,share_item,sms,status_update,user_online_presence,video_upload,xmpp_login',
                'response_type': 'token,code',
                'client_id': '356275264482347',
            }, cookies=self.cookies, headers={
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'dnt': '1',
                'dpr': '1.25',
                'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                'viewport-width': '1038',
            }
        ).text
        fb_dtsg = re.search('DTSGInitData",,{"token":"(.+?)"', get_data.replace('[]', '')).group(1)
        
        print(f"{xanhla}Đang Get Token")
        sleep(0)
        app_id = ''
        type_access_token = '1'
        if type_access_token == '1' or type_access_token == '01':
            app_id = self.facebook_android[0]
        else:
            exit()
        response = requests.post(
            f'https://www.facebook.com/dialog/oauth/business/cancel/?app_id={app_id}&version=v12.0&logger_id'
            f'=&user_scopes[0]=user_birthday&user_scopes[1]=user_religion_politics&user_scopes[2]=user_relationships&user_scopes[3]=user_relationship_details&user_scopes[4]=user_hometown&user_scopes[5]=user_location&user_scopes[6]=user_likes&user_scopes[7]=user_education_history&user_scopes[8]=user_work_history&user_scopes[9]=user_website&user_scopes[10]=user_events&user_scopes[11]=user_photos&user_scopes[12]=user_videos&user_scopes[13]=user_friends&user_scopes[14]=user_about_me&user_scopes[15]=user_posts&user_scopes[16]=email&user_scopes[17]=manage_fundraisers&user_scopes[18]=read_custom_friendlists&user_scopes[19]=read_insights&user_scopes[20]=rsvp_event&user_scopes[21]=xmpp_login&user_scopes[22]=offline_access&user_scopes[23]=publish_video&user_scopes[24]=openid&user_scopes[25]=catalog_management&user_scopes[26]=user_messenger_contact&user_scopes[27]=gaming_user_locale&user_scopes[28]=private_computation_access&user_scopes[29]=instagram_business_basic&user_scopes[30]=user_managed_groups&user_scopes[31]=groups_show_list&user_scopes[32]=pages_manage_cta&user_scopes[33]=pages_manage_instant_articles&user_scopes[34]=pages_show_list&user_scopes[35]=pages_messaging&user_scopes[36]=pages_messaging_phone_number&user_scopes[37]=pages_messaging_subscriptions&user_scopes[38]=read_page_mailboxes&user_scopes[39]=ads_management&user_scopes[40]=ads_read&user_scopes[41]=business_management&user_scopes[42]=instagram_basic&user_scopes[43]=instagram_manage_comments&user_scopes[44]=instagram_manage_insights&user_scopes[45]=instagram_content_publish&user_scopes[46]=publish_to_groups&user_scopes[47]=groups_access_member_info&user_scopes[48]=leads_retrieval&user_scopes[49]=whatsapp_business_management&user_scopes[50]=instagram_manage_messages&user_scopes[51]=attribution_read&user_scopes[52]=page_events&user_scopes[53]=business_creative_transfer&user_scopes[54]=pages_read_engagement&user_scopes[55]=pages_manage_metadata&user_scopes[56]=pages_read_user_content&user_scopes[57]=pages_manage_ads&user_scopes[58]=pages_manage_posts&user_scopes[59]=pages_manage_engagement&user_scopes[60]=whatsapp_business_messaging&user_scopes[61]=instagram_shopping_tag_products&user_scopes[62]=read_audience_network_insights&user_scopes[63]=user_about_me&user_scopes[64]=user_actions.books&user_scopes[65]=user_actions.fitness&user_scopes[66]=user_actions.music&user_scopes[67]=user_actions.news&user_scopes[68]=user_actions.video&user_scopes[69]=user_activities&user_scopes[70]=user_education_history&user_scopes[71]=user_events&user_scopes[72]=user_friends&user_scopes[73]=user_games_activity&user_scopes[74]=user_groups&user_scopes[75]=user_hometown&user_scopes[76]=user_interests&user_scopes[77]=user_likes&user_scopes[78]=user_location&user_scopes[79]=user_managed_groups&user_scopes[80]=user_photos&user_scopes[81]=user_posts&user_scopes[82]=user_relationship_details&user_scopes[83]=user_relationships&user_scopes[84]=user_religion_politics&user_scopes[85]=user_status&user_scopes[86]=user_tagged_places&user_scopes[87]=user_videos&user_scopes[88]=user_website&user_scopes[89]=user_work_history&user_scopes[90]=email&user_scopes[91]=manage_notifications&user_scopes[92]=manage_pages&user_scopes[93]=publish_actions&user_scopes[94]=publish_pages&user_scopes[95]=read_friendlists&user_scopes[96]=read_insights&user_scopes[97]=read_page_mailboxes&user_scopes[98]=read_stream&user_scopes[99]=rsvp_event&user_scopes[100]=read_mailbox&user_scopes[101]=business_creative_management&user_scopes[102]=business_creative_insights&user_scopes[103]=business_creative_insights_share&user_scopes[104]=whitelisted_offline_access&redirect_uri=fbconnect%3A%2F%2Fsuccess&response_types[0]=token&response_types[1]=code&display=page&action=finish&return_scopes=false&return_format[0]=access_token&return_format[1]=code&tp=unspecified&sdk=&selected_business_id=&set_token_expires_in_60_days=false',
            cookies=self.cookies,
            headers={
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'dnt': '1',
                'dpr': '1.25',
                'origin': 'https://www.facebook.com',
                'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                'viewport-width': '1038',
            },
            data={
                'fb_dtsg': str(fb_dtsg)
            },
        )
        access_token = re.findall(r'access_token=([^"]*)&data_access_expiration_time', response.text)[0]
        Login = requests.get("https://graph.facebook.com/me/?fields=id,name&access_token="+access_token).json()
        if "error" in Login or "errors" in Login:
            if int(Login["error"]["code"]) == 190:
                print("Code: 190, Cookies Đã Bị Đăng Xuất Khỏi Chrome")
            else:
                print(Login["error"]["message"])
        else:
            print("=======================================")
            print(f"Cookie: {Login['id']} | Facebook: {Login['name']}")
            print("=======================================")
            time.sleep(1)
            open("token.txt", "a+").write('{}\n'.format(access_token))
            print("\n")
            print(access_token+"\n")
            input("ENTERDETATTOOL")

def main():
    cookie_input = console.input("NHẬP COOKIES FACEBOOK : ")
    cookie_re = re.sub(r"\s+", "", cookie_input, flags=re.UNICODE)
    GETTOKEN(cookie_re).run()


if __name__ == '__main__':
    main()
