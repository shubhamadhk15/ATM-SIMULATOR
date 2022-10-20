from twilio.rest import Client
import random

def sendOtp(receiver,purpose):
    OTP=str(random.randint(1000,9999))
    account_sid ='ACc2e8e2fe6627bc097395aed9419a4467'
    auth_token = 'b6b103b6fff55f5060ed2f84f937cf9b'
    client = Client(account_sid, auth_token)

    client.messages.create(
                        body="Your Velocity Bank OTP for "+purpose+' is '+OTP,
                        from_='+19292076630',
                        to='+91'+receiver
                    )
    return OTP