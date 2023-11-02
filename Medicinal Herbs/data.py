import json
HTML_CODE = ""
TITLES_LIST = []
ALL_INFO = {}
def set_info():
    TITLES_LIST.clear()
    ALL_INFO.clear()
    try:
        with open('info_update.json','r', encoding ='utf-8') as f:
                data = json.load(f)
        if data == {}:
            raise ValueError
    except:
        try:
            with open('info_original.json','r', encoding ='utf-8') as f:
                data = json.load(f)
        except:
            with open('info_original.json','w') as fileJSON:
                json.dump({},fileJSON,indent=4)
                data = ()

    for title in data:
        ###fix \xa0####
        fix_title = title.replace('\xa0',' ')
        ###############
        TITLES_LIST.append(fix_title)
        ALL_INFO[fix_title] = data[title]



def finde_seems_titles(user_text):
    # print(TITLES_LIST)


    fix_user_text = user_text.lower()
    fix_user_text = fix_user_text.split(' ')
    fix_user_text= list(filter(lambda s:s.isalpha(), fix_user_text))

    
    if len(fix_user_text) == 0:
        return TITLES_LIST
    else:
        seems_titles = []

        for title in TITLES_LIST:
            if user_text.lower() == title.lower():
                seems_titles.insert(0,title)
            else:
                for text_part in fix_user_text:
                    if title.lower().find(text_part) != -1:
                        seems_titles.append(title)
                        break

        return seems_titles

def change_html_code(title):
    global HTML_CODE
    HTML_CODE = ALL_INFO[title]