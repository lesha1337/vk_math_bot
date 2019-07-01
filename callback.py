from flask import Flask, request, json
from config import *
import vk
import vkapi
import branching
import time

app = Flask(__name__)

@app.route('/posting/', methods=['POST'])
def processing():
    data = json.loads(request.data) #распаковка запроса
    for elem in data:
        print(elem, ':', data[elem])
    # return confirmation_token

    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new':
        init_text = data['object']['body'].lower()

        session = vk.Session()
        api = vk.API(session, v=5.0)
        if abs(data['object']['date'] - int(time.time())) < 60*2: #1: #timestamp 2 min
            user_id = data['object']['user_id']
            text = (data['object']['body']).lower()
            
            try:
                data = branching.getAnswer(text)
            except Exception as e:
                print('exception  on getting data ', e)
                data = branching.help_answer()
            
            if data == None:
                message, attachment = branching.help_answer()
            else:
                message, attachment = data

            if init_text.find('привет') == 0:
                message = 'Привет!\n' + message

            api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    return 'ok'


app.run(port=5014, threaded=True, host='0.0.0.0')