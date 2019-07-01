import vk
import json
import requests
import config

session = vk.Session()
api = vk.API(session, v=5.0)

def send_message(user_id, token, message, attachment=""):
	api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def pic_upload(img_url):
    vk_ph = config.vk_ph + img_url
    raw = requests.get(vk_ph).text
    data = json.loads(raw)
    attachment = ('photo'+str(data["owner_id"]) + '_' + str(data['id']))
    return attachment

def help_pic():
    attachment = config.help_id
    return attachment
