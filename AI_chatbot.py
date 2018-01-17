import sys, os
import random
import time

qgreet=['hello','hi','hellooo','hey','heyy']
rgreet= ['Hi! How are you?','Hey!',"Hello! What's up?"]
qans = ['nothing much','nothin','nothing, just tired','alright']
rans = ['Okay. How can I help you?']
qname=['what is your name','whats your name', 'whats your name?', 'what is your name?','Who are you','who r u',"who's this"]
rname=['My name is Chatbot','Chatbot']
qwhatsup=['how are you?','how are you','how do you do?','whats up','wassup']
rwhatsup=['I am good. Thank you for asking.', "I'm great",'I do great!','Okay']
print "Hi! I am a Chatbot!"
while(True):
	msg=raw_input('-').strip()
#	H=raw_input()
	msg=msg.lower()	
	if msg=='':
		print "Thanks. Come again!"
#		time.sleep(1)
#		os.system(sudo shutdown -h now)
		break
	elif msg in qname:
		print random.choice(rname)
	elif msg in qans:
		print random.choice(rans)
	elif msg in qgreet:
		print random.choice(rgreet)
	elif msg in qwhatsup:
		print random.choice(rwhatsup)
	else:
		print "Sorry! I can't understand."
