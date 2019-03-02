import os
import re
import time
phoneNumber = "(256) 294-7054"
os.system("rm tmp")
os.system("touch tmp")

MESSAGES = [None]

def start_messages():
	os.system("adb shell am start -p com.google.android.apps.messaging -c android.intent.category.LAUNCHER 1")

def dumpUiAutomator():
	os.system("adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') tmp")
	return open('tmp', 'r').read()

def findBounds():
	Ui = dumpUiAutomator()
	Ui = Ui.partition('text="{}" resource-id="com.google.android.apps.messaging:id/conversation_name" class="android.widget.TextView" package="com.google.android.apps.messaging" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="'.format(phoneNumber))[2]
	Ui = Ui.partition('"')[0]
	Ui = re.findall('(\d+)', str(Ui))
	return Ui

def findBounds():
	Ui = dumpUiAutomator()
	Ui = Ui.partition('text="{}" resource-id="com.google.android.apps.messaging:id/conversation_name" class="android.widget.TextView" package="com.google.android.apps.messaging" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="'.format(phoneNumber))[2]
	Ui = Ui.partition('"')[0]
	Ui = re.findall('(\d+)', str(Ui))
	return Ui

def sendMessage(text):
	os.system("adb shell input tap 800 2600")
	os.system('adb shell input text "{}"'.format(text))
	os.system('adb shell input keyevent 4')
	os.system("adb shell input tap 1300 2600")


if __name__ == '__main__':
	'''start_messages()
				bounds = findBounds()
				time.sleep(1)
				os.system('adb shell input tap {} {}'.format(bounds[0], bounds[2]))
				time.sleep(1)
				os.system('adb shell input tap {} {}'.format(bounds[0], bounds[2]))
				'''
	for i in range(10):
		e = dumpUiAutomator()
		for val in str(e).split('<node index="0" text="'):
			if '"com.google.android.apps.messaging:id/message_text"' in str(val):
				MESSAGES[0] = ((val.partition('"')[0]))
		print MESSAGES[0]
	sendMessage('TESTING')
	for i in range(10):
		e = dumpUiAutomator()
		for val in str(e).split('<node index="0" text="'):
			if '"com.google.android.apps.messaging:id/message_text"' in str(val):
				MESSAGES[0] = ((val.partition('"')[0]))
		print MESSAGES[0]
