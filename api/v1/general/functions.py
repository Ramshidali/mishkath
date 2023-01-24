import requests
import random
import requests
import string
from cryptography.fernet import Fernet

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers


def generate_serializer_errors(args):
    message = ""
    # print (args)
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += "%s : %s | " %(key,error_message)
    return message[:-3]


def get_user_token(request,user_name,password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"username": "' + user_name + '", "password":"' + password + '"}'
    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    web_host = request.get_host()
    request_url = protocol + web_host + "/api/auth/token/"

    response = requests.post(request_url, headers=headers, data=data)
    # print(response)
    return(response)

def get_auto_id(model):
    auto_id = 1
    try:
        latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
        if latest_auto_id:
            for auto in latest_auto_id:
                auto_id = auto.auto_id + 1
    except:
        pass
    return auto_id


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()


def get_user_token(request, user_name, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"username": "' + user_name + '", "password":"' + password + '"}'
    print(data, "--data")
    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    web_host = request.get_host()
    request_url = protocol + web_host + "/api/v1/auth/token/"

    print(request_url, "--------request_url")

    response = requests.post(request_url, headers=headers, data=data)
    print(response, "------response2")
    return (response)


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')