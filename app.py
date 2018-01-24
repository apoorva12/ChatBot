import os
import sys
import json
from datetime import datetime
import random
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

def find_in_omdb(st):
	api_key = '7fc5af0e'
	site = 'http://www.omdbapi.com/?t='+st+'&apikey=7fc5af0e'
	r = requests.get(site)
	p = r.json()
	if str(p['Response'])=='False':
		return 'try again'
	else:
		return str(p['Year'])

def generate(text):
	qgreet=['hello','hi','hellooo','hey','heyy']
	rgreet= ['Hi! How are you?','Hey!',"Hello! What's up?"]
	qans = ['nothing much','nothin','nothing, just tired','alright']
	rans = ['Okay. How can I help you?']
	qname=['what is your name','whats your name', 'whats your name?', 'what is your name?','Who are you','who r u',"who's this"]
	rname=['My name is Chatbot','Chatbot']
	qwhatsup=['how are you?','how are you','how do you do?','whats up','wassup']
	rwhatsup=['I am good. Thank you for asking.', "I'm great",'I do great!','Okay']
	msg=text.lower()	
	if msg=='':
		return "Thanks. Come again!"
	elif msg in qname:
		return random.choice(rname)
	elif msg in qans:
		return random.choice(rans)
	elif msg in qgreet:
		return random.choice(rgreet)
	elif msg in qwhatsup:
		return random.choice(rwhatsup)
	else:
		return find_in_omdb(msg)
	

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
		    ms=generate(message_text)
                    send_message(sender_id, ms)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
