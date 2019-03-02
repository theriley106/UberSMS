def returnSpeech(speech, endSession=True):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
		"outputSpeech": {
		"type": "PlainText",
		"text": speech
			},
			"shouldEndSession": endSession
		  }
	}

def on_intent(intent_request, session):
	# This means the person asked the skill to do an action
	intent_name = intent_request["intent"]["name"]
	# This is the name of the intent (Defined in the Alexa Skill Kit)
	if intent_name == 'bookUber':
		slots = intent_request["intent"]["slots"]
		address = slots['address'].get("value", "")
		cityVal = slots['cityVal'].get("cityVal", "")
		state = slots['state'].get("state", "")
		address = "{} {} {}".format(address, cityVal, state)
		# whatDay intent
		return "Book an uber to: {}".format(str(address))
		# Return the response for what day



def lambda_handler(event, context):
	if event["request"]["type"] == "LaunchRequest":
		speech ="You just started up the skill"
		return returnSpeech(speech, False)
	elif event["request"]["type"] == "IntentRequest":
		speech = on_intent(event["request"], event["session"])
    	return returnSpeech(speech)

if __name__ == '__main__':
	pass
