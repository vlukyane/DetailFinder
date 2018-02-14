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
    ans = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=ans).json()
    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    r = request.get_json()
    chat_id = r['message']['chat']['id']
    message = r['message']['text']
    if request.method == 'POST':

        flag = 'Hello' in message
        if flag:
            send_message(chat_id, text='HI! What would you want to find?')

        if not flag:
            file_work.make_new_part_num(message)
            response = file_work.data_proc()
            if response[0] == 'S':
                send_message(chat_id, text=response)
            else:
                for next_ans in response:
                    full_ans = ''
                    for info_param in next_ans:
                        full_ans += ' ' + str(info_param)
                    send_message(chat_id, text=full_ans)
        return jsonify(r)
    return '<h1>Bot greets you</h1>'


if __name__ == '__main__':
    thread1 = MyThreadForObserver(file_work)
    thread2 = MyThreadForBot()
    thread1.start()
    thread2.start()


