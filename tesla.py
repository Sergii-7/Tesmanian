import mongo, user
from bs4 import BeautifulSoup

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='v-stack gap-4 sm:gap-5')
    fresh = []
    for item in items:
        title_id = item.find('a', class_='text-sm').get('href').split("/")[-1]
        #print(f"id_: {title_id}")
        title_url = user.URL + item.find('a', class_='text-sm').get('href')
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
    response = user.session.get(user.URL, cookies=user.cookies, headers=user.headers)
    fresh, l = get_content(response.text), []
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

#print(start_parcer())

