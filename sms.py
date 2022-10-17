import twilio
import random
OTP=random.randint(1000,9999)
print(OTP)
from twilio.rest import Client
account_sid ='ACc2e8e2fe6627bc097395aed9419a4467'
auth_token = 'b6b103b6fff55f5060ed2f84f937cf9b'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="This is your OTP: "+str(OTP),
                     from_='+19292076630',
                     to='+918240485958'
                 )

print(message.sid)