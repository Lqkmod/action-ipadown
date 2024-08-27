
while(True):
	try:import requests; break
	except:import os; os.system('pip install requests')
token=input('ACCESS TOKEN: ')
list_page=requests.get(F'https://graph.facebook.com/me/accounts?access_token={token}&limit=100000000000000000000000000000000000000000000000000000000000000000').json()['data']
for page in list_page:
	try:
		access_token=page['access_token']
		with open('access_token_page.txt', 'a+', encoding='utf-8') as f:f.write(F'{access_token}\n')
		print(access_token)
	except:pass