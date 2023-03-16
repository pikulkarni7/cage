import os
import random
import string
from twilio.rest import Client


account_sid = "AC0703eda2b5c0c002a05ca7431e6c0862"
auth_token = "6691700f744df1fbb9be601cc6434e93"
twilio_phone_number = "+15076691935"


# account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
# twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")


def generate_otp(length=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_string(s):
    return s

def send_otp_via_sms(phone_number, otp):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Your OTP is: {}".format(otp),
        from_=twilio_phone_number,
        to=phone_number
    )
    return message.sid

def send_msg_via_sms(phone_number,msg):
    client = Client(account_sid, auth_token)
    # message=msg
    message = client.messages.create(
        body="Your Message is: {}".format(msg),
        from_=twilio_phone_number,
        to=phone_number
    )

    return message.sid


recipient_phone_number = "+16693880796" 
msg=generate_string("13.37°C is the temperature in San Francisco and it feels like 12.54°C.")
print("Generated OTP:", msg)

message_sid=send_msg_via_sms(recipient_phone_number,msg)

print("Message sent with SID:", message_sid)
