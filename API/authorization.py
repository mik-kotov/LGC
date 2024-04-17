from API import configuration
import requests
from API import data
import json

def get_anonim_auth_token():
    print("Запрашиваем анонимный токен")
    get_anon_token_response = requests.get("https://api-service-dev.lgcity.dev/auth",
                        headers=data.headers)

    return get_anon_token_response.json()['response']['access_token']

def request_confirm_token ():
    current_phone_request_body = {'phone': data.current_phone}
    headers_with_anon_auth_token = {**data.headers, 'X-Auth-Token': get_anonim_auth_token()}
    print("Запрашиваем код подтверждения на номер телефона")
    response_confirm_token = requests.post(configuration.URL_USER_SERVICE + configuration.CONFIRM_CODE,
                                          headers=headers_with_anon_auth_token,
                                          data=json.dumps(current_phone_request_body))
    return response_confirm_token.json()


def user_auth_token():
    response = request_confirm_token()
    print("Запрашиваем токен авторизации")
    confirm_phone_code = response['debug']['trace']['phone_code']
    current_request_body = {'phone': data.current_phone, 'code': confirm_phone_code}
    response_user_auth_token = requests.post(configuration.URL_USER_SERVICE + configuration.LOGIN,
                                             headers=data.headers,
                                             data=json.dumps(current_request_body))
    user_auth_token = response_user_auth_token.json()['data']['token']
    return user_auth_token

headers_with_user_auth_token = {**data.headers, 'X-Auth-Token': user_auth_token()}
