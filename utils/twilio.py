from twilio.rest import Client


TWILIO_ACCOUNT_SID = "AC0703eda2b5c0c002a05ca7431e6c0862"
TWILIO_AUTH_TOKEN = "6691700f744df1fbb9be601cc6434e93"
TWILIO_PHONE_NUMBER = "+15076691935"


def notify_twilio(data, phone_number):
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body = format(data),
            from_= TWILIO_PHONE_NUMBER,
            to = phone_number
        )

        print("Message sent with SID: ", message.sid)
        return message.sid
    
    except Exception as e:
        print(e)
        return None
    