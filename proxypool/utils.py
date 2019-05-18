import requests
from requests.exceptions import ConnectionError

origin_headers = {
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

def get_page(url,other_header={}):
    '''
    :param other_header: other header information
    :return text
    '''
    headers = dict(origin_headers, **other_header) #what??
    print('getting page',url)
    try:
        response = requests.get(url,headers=headers)
        print('successfully get page',url,response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('error in getting page',url)
        return None

