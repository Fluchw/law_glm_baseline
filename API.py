import requests

def API(api_name, args):
    domain = "comm.chatglm.cn"
    url = f"https://{domain}/law_api/{api_name}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 8A9B4ED694D6453CB8377D8DD6698366C06B50D10FD97550'
    }
    rsp = requests.post(url, json=args, headers=headers)
    return rsp.json()

