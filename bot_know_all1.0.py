import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import random
import json
import pymorphy2
import urllib.request 
import requests
import wikipedia


#ключ 6931969120c41f8b698fd2df75872e665f443495e9413fc975c52cb000e367e1bcfde04f2a35445f85f55
#181727795

USERS = {}

#token = '18b21fd284c1dc3b756bb051569f24c7b30c2a2c3c8ebc44695bd062fb13b6c9ac7b1782bd9835791e3de'
token = '6931969120c41f8b698fd2df75872e665f443495e9413fc975c52cb000e367e1bcfde04f2a35445f85f55'



def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1, 2147483647)})

def write_msg2(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1, 2147483647), "keyboard": keyboard})
    

def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": True,
    "buttons": [

        [get_button(label="расскажи о...", color="positive")],
        [get_button(label="мини-досье на...", color="positive")],
        [get_button(label="поиграем в ассоциации", color="positive")]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def menu():
    global keyboard
    keyboard = {
        "one_time": True,
        "buttons": [

            [get_button(label="расскажи о...", color="positive")],
            [get_button(label="мини-досье на...", color="positive")],
            [get_button(label="поиграем в ассоциации", color="positive")]

        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

def auth(idd):
    global USERS
    if idd not in USERS.keys():
        print('!important')
        USERS[idd] = {'act': 'menu', 'word': '', 'first': True}
    return (idd, USERS[idd]['act'])    

def birth(dict_info):
    keys = dict_info.keys()
    ans = ''
    date = []
    if 'bdate' in keys:
        date = [int(i) for i in dict_info['bdate'].split('.')]
        months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        ans = str(date[0]) + ' ' + months[date[1] - 1] + ' '
    if len(date) > 2 and 'bdate' in keys:
        ans += str(date[2]) + 'г'
    elif 'schools' in keys:
        if not 'bdate' in keys: 
            ans = 'в '
        ans += str(dict_info['schools'][0]['year_from'] - 6) + '-' + str(dict_info['schools'][0]['year_from'] - 7) + 'гг'
    return ans    
    
def wiki_menu():
    global keyboard
    keyboard = {
        "one_time": True,
        "buttons": [
        [get_button(label='расскажи подробнее', color="positive")],
        [get_button(label='дай ссылку на Wiki', color="positive")],
        [get_button(label='назад в меню', color="default")]]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    
def words_menu():
    global keyboard
    keyboard = {
        "one_time": True,
        "buttons": [
        [get_button(label='назад в меню', color="default")]]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))    

def nomn_case(word):
    morph = pymorphy2.MorphAnalyzer()
    txt = morph.parse(word)[0]
    w = txt.inflect({'sing', 'nomn'})
    return w.word[0].upper() + w.word[1:]
def loct_case(word):
    morph = pymorphy2.MorphAnalyzer()
    txt = morph.parse(word)[0]
    w = txt.inflect({'sing', 'loct'})
    return w.word[0].upper() + w.word[1:]

def gent_case(word):
    morph = pymorphy2.MorphAnalyzer()
    txt = morph.parse(word)[0]
    w = txt.inflect({'sing', 'gent'})
    return w.word[0].upper() + w.word[1:]

def verb_past(word, sex):
    if sex == 1:
        morph = pymorphy2.MorphAnalyzer()
        txt = morph.parse(word)[0]
        w = txt.inflect({'past', 'femn'}).word
    else:
        morph = pymorphy2.MorphAnalyzer()
        txt = morph.parse(word)[0]
        w = txt.inflect({'past', 'mask'}).word
    print(w) 
    return w

def info_about_vk(user_id):
    dict_info = vk.method('users.get', {'user_ids': user_id, 'fields': ' photo_id, verified, sex, bdate, city, country, home_town, has_photo, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me'})[0]
    ans = dict_info['first_name'] + ' ' + dict_info['last_name']
    print(dict_info)
    
    if dict_info['sex'] == 1:
        ans += ' (' + 'ж' + ')\n'
    else:
        ans += ' (' + 'м' + ')\n'
        
    birthday = birth(dict_info)
    if birthday:
        ans += verb_past('родиться', dict_info['sex']) + ' ' + birthday + '\n'
    
    if 'home_town' in dict_info.keys() and dict_info['home_town']:
        ans += 'в ' + loct_case(dict_info['home_town'])
        ans += '.\n'
    print(dict_info['city'])
    ans += 'сейчас в ' + loct_case(dict_info['city']["title"]) 
    ans += ' ('+ dict_info['country']["title"] + ')'
    ans += '.\n'
    
    if ('mobile_phone' in dict_info.keys() and
        'home_phone' in dict_info.keys() and
        dict_info["mobile_phone"] and dict_info["home_phone"]):
        ans += 'можно связаться по номеру: ' + dict_info["mobile_phone"]
        ans += ',\n'
        ans += 'а также по номеру: ' + dict_info["home_phone"]
    elif ('mobile_phone' in dict_info.keys() and
          dict_info["mobile_phone"]):
        ans += 'можно связаться по номеру: ' + dict_info["mobile_phone"]
        ans += '.\n'        
    elif ('home_phone' in dict_info.keys() and
          dict_info["home_phone"]):
        ans += 'можно связаться по номеру: ' + dict_info["mobile_phone"]
        ans += '.\n'
    return ans

def tell_about(what):
    thing = nomn_case(what)
    try:
        complete_content = wikipedia.summary(thing)
        ans = complete_content
    except wikipedia.exceptions.PageError:
        ans = 'эээ? не знаю, извини :('
    except wikipedia.exceptions.DisambiguationError:
        ans = 'может что-то другое в виду имелось? уточни'
        menu()
    #print(complete_content.content)    
    #vk.method('users.get', {'user_ids': user_id, })
    return ans

def tell_more(what):
    thing = nomn_case(what)
    try:
        complete_content = wikipedia.page(thing)
        ans = complete_content.content
    except wikipedia.exceptions.PageError:
        ans = 'эээ? не знаю, извини :('
    except wikipedia.exceptions.DisambiguationError:
        ans = 'может что-то другое в виду имелось?'
    return ans    

def wiki_url(what):
    thing = nomn_case(what)
    try:
        complete_content = wikipedia.page(thing)
        ans = complete_content.url
    except wikipedia.exceptions.PageError:
        ans = 'эээ? не знаю, извини :('
    except wikipedia.exceptions.DisambiguationError:
        ans = 'может что-то другое в виду имелось?'
    return ans
#6954926

# авторизация
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
menu()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            current_user, act = auth(event.user_id)
            request = event.text.lower()
            new_mes = str(current_user) + ' ' + request
            print(new_mes)
            print(USERS[current_user]['word'])
            print(type(USERS[current_user]['word']))
            
            if USERS[current_user]['first']:
                USERS[current_user]['first'] = False
                msg = 'привет! я бот-всезнайка, дружу с Википедией и люблю интеллектуальные игры\n'
                msg += 'можем поиграть в одну из них. ещё я могу рассказать о чём-нибудь (или ком-нибудь)'
                write_msg2(current_user, msg, keyboard)
            # меню
            elif request == 'меню' or request == 'назад в меню' or request == 'привет' or request == 'здравствуй':
                USERS[current_user]['act'] = 'menu'
                menu()
                write_msg2(current_user, '...', keyboard)
                
            elif act == 'menu' and request == 'расскажи о...':
                USERS[current_user]['act'] = 'wiki'
                write_msg(current_user, 'о чём рассказать?')
                
            elif act == 'menu' and request == 'поиграем в ассоциации':
                USERS[current_user]['act'] = 'play'
                write_msg(current_user, 'обожаю эту игру, могу играть вечно! пока ты не попросишься в меню, буду отвечать))\nзагадывай')
            
            elif act == 'menu' and request == "мини-досье на...":
                USERS[current_user]['act'] = 'user_info'
                msg = 'на кого?\n'
                msg += 'впиши число после "id" из ссылки на страницу пользователя или краткий адрес страницы (после "vk.com/" в ссылке)'
                write_msg(current_user, msg)
                
            #Википедия    
            elif act == 'wiki' and request == 'расскажи подробнее':
                # он про все отвечает, но про некоторые слова долго думает
                what = USERS[current_user]['word']
                wikipedia.set_lang("ru")
                
                ans = tell_more(what)
                ans = ans.replace('== Примечания ==', '')
                ans = ans.replace('== См. также ==', '== Рекомендрую почитать про ==')
                ans += '\n' + 'что-то может отображаться некорректно, в случае чего, ссылка на Википедию: ' + wiki_url(what)
                ans = ans.split('\n')
                ans = '\n'.join(ans)
                anss = []
                while ans:
                    num = 4096
                    if len(ans) < num:
                        num = len(ans)
                        anss.append(ans[:num])
                        if len(ans) > num:
                            ans = ans[num:]
                        else:
                            ans = ''
                        for i in anss:
                            write_msg(current_user, i)
                print('!!!', USERS[current_user]['word'])    
                write_msg2(current_user, 'что теперь?', keyboard)
                
                            
            elif act == 'wiki' and request == 'дай ссылку на wiki':
                what = USERS[current_user]['word']
                write_msg(current_user, wiki_url(what))
                write_msg2(current_user, 'что теперь?', keyboard)                
            
            elif act == 'wiki':
                if request[:2] == 'о ':
                    what = request[2:]
                elif request[:4] == 'про ':
                    what = request[4:]
                else:
                    what = request
                USERS[current_user]['word'] = what
                wikipedia.set_lang("ru")
                
                ans = tell_about(what)
                if ans == 'эээ? не знаю, извини :(' or ans == 'может что-то другое в виду имелось? уточни':
                    menu()
                    USERS[current_user]['act'] = 'menu'
                    write_msg(current_user, ans)
                    write_msg2(current_user, 'о другом спросишь или, хочешь, поиграем?', keyboard)
                else:    
                    ans = ans.replace('== Примечания ==', '')
                    ans = ans.split('\n')
                    ans = '\n'.join(ans)
                    print(ans)  
                    anss = []
                    while ans:
                        num = 4096
                        if len(ans) < num:
                            num = len(ans)
                        anss.append(ans[:num])
                        if len(ans) > num:
                            ans = ans[num:] 
                        else:
                            ans = ''
                        for i in anss:
                            write_msg(current_user, i)
                            wiki_menu() 
                            write_msg2(current_user, 'что теперь?', keyboard)
                
            elif act == 'wiki_long':
                if 10:
                    if request[:2] == 'о ':
                        what = request[2:]
                    elif request[:4]  == 'про ':
                        what = request[4:]  
                    else:
                        what = request
                        wikipedia.set_lang("ru")
                        
                        ans = tell_more(what)
                        ans = ans.replace('== Примечания ==', '')
                        ans = ans.replace('== См. также ==', '== Рекомендрую почитать про ==')
                        ans += '\n' + 'что-то может отображаться некорректно, в случае чего, ссылка на Википедию: ' + wiki_url(what)
                        ans = ans.split('\n')
                        ans = '\n'.join(ans)
                        anss = []
                        while ans:
                            num = 4096
                            if len(ans) < num:
                                num = len(ans)
                                anss.append(ans[:num])
                                if len(ans) > num:
                                    ans = ans[num:]
                                else:
                                    ans = ''
                                    for i in anss:
                                        write_msg(current_user, i) 
            
            #игра    
            elif act == 'play' and request != 'назад в меню':
                x = request.split()[0]
                req = 'https://api.wordassociations.net/associations/v1.0/json/search?apikey=45197842-3902-45e1-bc7b-bb5fd308657a&text='
                req += x
                req += '&pos=noun&type=response&lang=ru&limit=2'
                response = requests.get(req)
                json_response = response.json()
                print(json_response['response'])
                my_ans = json_response['response'][0]['items'][random.randint(0, 1)]['item']
                ans = nomn_case(my_ans).lower()
                words_menu()
                write_msg2(current_user, ans, keyboard)
                                        
            #досье
            elif act == 'user_info':
                msg = info_about_vk(request)
                USERS[current_user]['act'] = 'menu'
                menu()
                write_msg2(current_user, msg, keyboard)
                
            #<3    
            else:
                write_msg(current_user, "сам ты " + request)
                
               