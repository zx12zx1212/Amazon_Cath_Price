import requests
from bs4 import BeautifulSoup
import schedule


def lineNotifyMessage(product_list):
    str_list = []
    for i in product_list:
        tmp = i[0]
        str = '\n商品名稱：{}\n價格：{}\n'.format(tmp.strip(), i[1])
        str_list.append(str)
    headers = {
        "Authorization": "",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': str_list}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def amazon():
    tmp_list = []
    txt = open('url.txt', 'r')
    for line in txt.readlines():
        tmp = []
        url = line
        web_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'TE': 'Trailers'}

        request = requests.get(url, headers=web_header)

        response_soup = BeautifulSoup(request.text, 'html.parser')
        # 商品名稱
        result_list_1 = response_soup.find_all("div", id="titleSection")
        for result in result_list_1:
            conten_1 = result.find('span', id="productTitle")
            tmp.append(conten_1.text)

        # 價格
        result_list_2 = response_soup.find_all("table", class_="a-lineitem a-align-top")
        for result in result_list_2:
            conten = result.find('span', class_="a-offscreen")
            tmp.append(conten.text)
        tmp_list.append(tmp)
    txt.close()
    return tmp_list


def task():
    product_list = amazon()
    lineNotifyMessage(product_list)
    print("=======ING=======")


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(task)
    schedule.every().day.at("01:00").do(task)
    schedule.every().day.at("02:00").do(task)
    schedule.every().day.at("03:00").do(task)
    schedule.every().day.at("04:00").do(task)
    schedule.every().day.at("05:00").do(task)
    schedule.every().day.at("06:00").do(task)
    schedule.every().day.at("12:00").do(task)
    schedule.every().day.at("18:00").do(task)
    schedule.every().day.at("22:00").do(task)
    schedule.every().day.at("23:00").do(task)
    # schedule.every().minutes.do(task)
    while True:
        schedule.run_pending()
