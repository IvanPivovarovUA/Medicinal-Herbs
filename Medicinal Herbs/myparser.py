from bs4 import BeautifulSoup
import json
import requests
# https://liktravy.ua/useful/recipes
# https://liktravy.ua/useful/recipes?page=2
info = {}
URL = 'https://liktravy.ua/useful/recipes'
URL_short = 'https://liktravy.ua'

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
}

def conver_tag_list_on_text(title,tag_list):
    convert_text = '<h1>' + title + '</h1>'
    for item in tag_list:
        convert_text += "<p> - " + item.text + "</p>"
    
    return convert_text 

def get_item_info(url):
    url = URL_short + url
    print(url)
    reg = requests.get(url,headers)
    soup = BeautifulSoup(reg.text,'lxml')
    # with open('test.html','r',encoding="utf-8") as fileHTML:
    #     src = fileHTML.read()
    # soup = BeautifulSoup(src,'lxml')

    print(soup.find('h1',class_='h1'))
    text = ''
    
    text += '<h1>' + soup.find('h1',class_='h1').text + '</h1>'
    text += '<p>' + soup.find('div',class_='for-text_field').text + '</p>'

    text += conver_tag_list_on_text(
        'ІНГРЕДІЄНТИ',
        soup.find('div',class_='list-ingredient').find_all('li')
    )

    text += conver_tag_list_on_text(
        'СПОСІБ ПРИГОТУВАННЯ',
        soup.find('div',class_='list').find_all('li')
    )

    text += conver_tag_list_on_text(
        'ЕФЕКТ',
        soup.find('div',class_='additional-field-in-recipe').find_all('li')
    )

        

    return text
def add_item_list(url):
    url = URL_short + url
    print(url)
    reg = requests.get(url,headers)
    soup = BeautifulSoup(reg.text,'lxml')


    bottom_class = soup.find_all('div',class_='bottom')

    for div in bottom_class[:-1]:
        # print(a.find('a'))
        info[div.find('a').text] = str(get_item_info(div.find('a').get('href')))
    # info['rrrrrrrrrrrrrrrrrrrrrc'] = get_item_info('tesrt')

def load_site_info():
    try:
        print(URL)
        reg = requests.get(URL,headers)
        soup = BeautifulSoup(reg.text,'lxml')

        pages_urls  = soup.find('ul',class_='pagination').find_all('a')

        for page in pages_urls:
            add_item_list(page.get('href') )

        # add_item_list('rws')
        with open('info_update.json','w') as fileJSON:
            json.dump(info,fileJSON,indent=4)
        
        print(info)
        return True
    except:
        print('Parser Error!')
        with open('info_update.json','w') as fileJSON:
            json.dump({},fileJSON,indent=4)

        return False
