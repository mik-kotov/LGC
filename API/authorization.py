import os
import json
import requests
from API import locators_api
from API import data
import os
import json
import requests
from API import locators_api
from API import data

TOKEN_FILE = 'auth_tokens.json'

def save_token(token_data):
    with open(TOKEN_FILE, 'w') as file:
        json.dump(token_data, file)


def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    return {}



class APIClient:

    def __init__(self, user_phone, user_card=None):
        self.headers = data.headers
        self.base_url = locators_api.URL_USER_SERVICE
        self.phone_number = f"+{user_phone}"
        self.tokens = self.load_or_get_tokens()
        self.user_card = user_card

    def get_anonim_auth_token(self):
        print("Запрашиваем анонимный токен")
        response = requests.get("https://api-service-dev.lgcity.dev/auth", headers=self.headers)
        response.raise_for_status()
        return response.json()['response']['access_token']

    def request_confirm_token(self):
        current_phone_request_body = {'phone': self.phone_number}
        headers_with_anon_auth_token = {**self.headers, 'X-Auth-Token': self.get_anonim_auth_token()}
        print("Запрашиваем код подтверждения")
        response = requests.post(self.base_url + locators_api.CONFIRM_CODE,
                                 headers=headers_with_anon_auth_token,
                                 data=json.dumps(current_phone_request_body))
        response.raise_for_status()
        return response.json()

    def get_user_auth_token(self):
        response = self.request_confirm_token()
        print("Запрашиваем токен авторизации")
        confirm_phone_code = response['debug']['trace']['phone_code']
        current_request_body = {'phone': self.phone_number, 'code': confirm_phone_code}
        response_user_auth_token = requests.post(self.base_url + locators_api.LOGIN,
                                                 headers=self.headers,
                                                 data=json.dumps(current_request_body))
        response_user_auth_token.raise_for_status()
        return response_user_auth_token.json()['data']['token']

    def load_or_get_tokens(self):
        tokens = load_tokens()
        if self.phone_number not in tokens:
            tokens[self.phone_number] = self.get_user_auth_token()
            save_token(tokens)
        return tokens

    def request_with_token(self, method, url, **kwargs):
        headers = kwargs.pop('headers', {})
        token = self.tokens.get(self.phone_number)
        if not token:
            print("Токен для номера телефона не найден. Получаем новый.")
            token = self.get_user_auth_token()
            self.tokens[self.phone_number] = token
            save_token(self.tokens)
        if locators_api.URL_USER_SERVICE in url:
            combined_headers = {**self.headers, 'Authorization': f'Bearer {token}', **headers}
        elif locators_api.URL_API_SERVICE in url:
            combined_headers = {**self.headers, 'X-Auth-Token': token, **headers}
        response = requests.request(method, url, headers=combined_headers, **kwargs)
        if response.status_code == 401:
            print("Получен ответ 401, обновляем токен")
            token = self.get_user_auth_token()
            self.tokens[self.phone_number] = token
            save_token(self.tokens)
            if locators_api.URL_USER_SERVICE in url:
                combined_headers['Authorization'] = f'Bearer {token}'
            elif locators_api.URL_API_SERVICE in url:
                combined_headers['X-Auth-Token'] = token
            response = requests.request(method, url, headers=combined_headers, **kwargs)
        return response

    def get(self, url, **kwargs):
        return self.request_with_token('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request_with_token('POST', url, **kwargs)

