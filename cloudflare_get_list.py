#get list of WAF - CloudFlare
#Nik 07/2023

import requests
import json
import warnings

ip = []
def request(url):


	payload={}
	headers = {
  	'X-Auth-Email': '<YOUR_EMAIL>', #CHANGE
  	'X-Auth-Key': '<GLOBAL_API_KEY>', #VERIFY CREDENTIAL SCOPE #CHANGE
  	'Content-Type': 'application/json'
	}

	warnings.filterwarnings("ignore", message="Unverified HTTPS request")

	response = requests.request("GET", url, headers=headers, data=payload, verify=False)
	response_decode = json.loads(response.text)
	response_text = response.text

	return  url, response_text, response_decode




def get_ip(url, response_text, response_decode):

	count = 0

	max = len(response_decode['result'])

	for item in range(max):

		ip.append((response_decode['result'][count]['ip']))
		count+=1

	try:
		next_page = response_decode['result_info']['cursors']['after']
		url = "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/rules/lists/<LIST_ID>/items?cursor=" #CHANGE
		next_page_url = url +  next_page

		return ip, next_page_url

	except KeyError:
		next_page_url = "finish"

		return ip,  next_page_url


def init():
	url = "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/rules/lists/<LIST_ID>/items?cursor=" #CHANGE
	ip_list = []
	while True:

		url, response_text, response_decode = request(url)
		ip, next_page_url = get_ip(url,response_text, response_decode)

		if next_page_url == "finish":

			break
		else:
			url = next_page_url
	print(ip)



init()