import requests, mongo
from bs4 import BeautifulSoup

URL = 'https://www.tesmanian.com'

# headers from https://curlconverter.com/python-httpclient/
HEADERS = {
    'cookie': "localization=US; cart_currency=USD; _y=be582d6d-3db2-435a-8af7-fdc577283007; _s=fe35e52b-a69b-4686-9ba5-3a880beb7ff6; _shopify_y=be582d6d-3db2-435a-8af7-fdc577283007; _shopify_s=fe35e52b-a69b-4686-9ba5-3a880beb7ff6; _orig_referrer=; _landing_page=%252F; _shopify_sa_p=; _gcl_au=1.1.710636476.1680258453; _gid=GA1.2.232707084.1680258454; shopify_pay_redirect=pending; __gads=ID%3De407240a979ebef2-22a40df8f0de00b8%3AT%3D1680258454%3ART%3D1680258454%3AS%3DALNI_MYd1fQ5GBHvXjvNJjuJBvwaVVHzpg; __gpi=UID%3D00000a37b43e1423%3AT%3D1680258454%3ART%3D1680258454%3AS%3DALNI_MY9x4hRphQ0sVs2Bs0Q7KUVKVyJcg; _secure_session_id=e925ac4d00c51e72c4c9d5d2f2fe3e86; customer_auth_session_created_at=2023-03-31%2B10%253A30%253A22%2BUTC; customer_auth_provider=shopify_core; cart_sig=2dffaa6a7984f861d3c5f5a2432a5fbc; secure_customer_sig=d879bc8faa0d7df1918c49ac9abc1c27; _uetsid=a6712f30cfae11ed95e4b77c2a343506; _uetvid=a6715df0cfae11ed9067a18531f054fa; _shopify_sa_t=2023-03-31T10%253A47%253A35.210Z; _ga=GA1.2.1138966400.1680258454; keep_alive=7e214462-444e-4cd4-aa56-ba52b85b31ae; _ga_CVP4R0PXQN=GS1.1.1680258453.1.1.1680260283.0.0.0",
    'authority': "www.tesmanian.com",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'accept-language': "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    'if-none-match': "cacheable:23694b8a8af7ed07e0d3e1264215c417",
    'referer': "https://www.tesmanian.com/account",
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': "iframe",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='v-stack gap-4 sm:gap-5')
    fresh = []
    for item in items:
        title_id = item.find('a', class_='text-sm').get('href').split("/")[-1]
        #print(f"id_: {title_id}")
        title_url = URL + item.find('a', class_='text-sm').get('href')
        #print(title_url)
        text = item.find('div', class_='v-stack gap-3 sm:gap-4').get_text(strip=True),
        text = ''.join(text)
        #print(text)
        date = item.find('span', class_='text-sm').get_text(strip=True),
        date = ''.join(date)
        #print(date)
        tesmanian = {"_id": {"title": title_id},
                   "date": date,
                   'url': title_url,
                   'text': text}
        try:
            mongo.db.Parser.insert_one(tesmanian)
            fresh.append(tesmanian)
        except Exception as E:
            #print(f"mongo:\n{E}")
            pass
    return fresh

def start_parcer():
    html, l = get_html(URL), []
    fresh = get_content(html.text)
    if fresh == []:
        return fresh
    else:
        for i in reversed(fresh):
            date = i['date']
            title = f"<a href='{i['url']}'>{i['text']}</a>"
            sms = f"{date}\n{title}"
            l.append(sms)
            #print(sms)
        return l

#html = get_html(URL)
#print(get_content(html.text))
#print(start_parcer())

