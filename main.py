from flask import Flask
from flask import request
from flask import jsonify
import observer
import config
import requests
import threading


app = Flask(__name__)
file_work = observer.Watcher()
URL = 'https://api.telegram.org/bot' + config.token


class MyThreadForObserver(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)

    def run(self):
        file_work.run()


class MyThreadForBot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app.run()


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + '/sendMessage'
    ans = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    r = requests.post(url, json=ans).json()
    return r


def send_photo(chat_id, urls_to_image):
    url = URL + '/sendMediaGroup'
    image_set = set()
    for some_img_inf in urls_to_image:
        image_set.add(some_img_inf)

    del urls_to_image[:]
    for item in image_set:
        urls_to_image.append(make_append(item))
    image_set.clear()
    ans = {'chat_id': chat_id, 'media': urls_to_image}
    requests.post(url, json=ans).json()


def make_append(raw_input):
    return {'type': 'photo', 'media': raw_input}


@app.route('/', methods=['POST', 'GET'])
def index():
    r = request.get_json()
    if "message" in r:
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        if request.method == 'POST':

            flag = 'Hello' in message
            if flag:
                send_message(chat_id, text='HI! What would you want to find?')
            if not flag:
                file_work.make_new_part_num(message.lower())
                response = file_work.data_proc()
                if response[0] == 'S':
                    send_message(chat_id, text=response)

                else:
                    response_stack = []
                    response_album_stack = []
                    prev_brand = 'not prev'
                    for next_ans in response:
                        full_ans = '<b>' + next_ans[0] + ' ' + str("{0:.2f}".format(next_ans[1])) + '</b>'
                        full_ans += ' (Brand: ' + str(next_ans[2]) + ', '
                        full_ans += 'Qty: ' + str(next_ans[3]) + ', '
                        full_ans += 'Case Qty: ' + str(next_ans[4]) + ', '
                        if next_ans[5] == 0:
                            full_ans += 'Weight: ' + 'Weight Unknown' + ', '
                        else:
                            full_ans += 'Weight: ' + str("{0:.2f}".format(next_ans[5])) + ', '
                        full_ans += 'HT: ' + str(next_ans[6]) + 'd)'

                        if prev_brand != 'not prev' and str(next_ans[2]) != prev_brand:
                            send_message(chat_id, text=str(prev_brand) + ' ' + message)
                            print(response_album_stack)
                            if len(response_album_stack) == 0:
                                send_message(chat_id, text='Sorry, there is no such image of this Brand')
                            send_photo(chat_id, response_album_stack)
                            for mess in response_stack:
                                send_message(chat_id, text=mess)
                            del response_stack[:]
                            del response_album_stack[:]

                        prev_brand = str(next_ans[2])
                        response_album_stack.append(next_ans[7])
                        response_stack.append(full_ans)

                    if len(response_stack) > 0:
                        send_message(chat_id, text=str(prev_brand) + ' ' + message)
                        print(response_album_stack)
                        if len(response_album_stack) == 0:
                            send_message(chat_id, text='Sorry, there is no such image of this Brand')
                        send_photo(chat_id, response_album_stack)
                        for mess in response_stack:
                            send_message(chat_id, text=mess)

            return jsonify(r)
        return jsonify(r)
    return jsonify(r)

if __name__ == '__main__':
    thread1 = MyThreadForObserver(file_work)
    thread2 = MyThreadForBot()
    thread1.start()
    thread2.start()
