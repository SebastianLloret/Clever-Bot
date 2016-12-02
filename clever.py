'''
Python script to chat with cleverbot via Alexa
'''
import cleverbot
# Initialize the client
cleverbot_client = cleverbot.Cleverbot()
# Create the JSON return for Alexa functionality
def build_speechlet_response(title, output, speech, reprompt_text, should_end_session):
    return {
        # What Alexa will say to the user
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        # What Alexa will put in the companion app's card
        'card': {
            'type': 'Simple',
            'title': title,
            'content': "User: " + speech + "\nBot: " + output
        },
        # What Alexa will say if she doesn't hear an input
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        # Should we terminate the session?
        'shouldEndSession': should_end_session
    }
# Initialize session info
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
# How will we handle inputs?
def lambda_handler(event, context):
    session_attributes = {}
    # If the user launches Clever Bot
    if event["request"]["type"] == "LaunchRequest":
        return build_response(session_attributes, build_speechlet_response("Conversation Log", "What would you like me to tell Cleverbot?", "", "", False))

    # If the intent matches GetMessageIntent, then:
    elif event["request"]["type"] == "IntentRequest":
        if event["request"]["intent"]["name"] == "GetMessageIntent":
            # User speech equals the value of the message slot
            speech = event["request"]["intent"]["slots"]["message"]["value"]
            # Our bot will respond to the user input
            cleverResponse = cleverbot_client.ask(speech)
            # Return the build_response
            return build_response(session_attributes, build_speechlet_response("Conversation Log", cleverResponse, speech, "I didn't hear you, could you say that again?", False))

        # If the intent matches the built-in stop, then:
        elif event["request"]["intent"]["name"] == "AMAZON.StopIntent":
            # End the session
            return build_response(session_attributes, build_speechlet_response("Conversation Log", "Goodbye!", "stop", "", True))
