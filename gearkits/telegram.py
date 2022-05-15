''' TelegramBot '''
# pylint: disable=arguments-renamed,arguments-differ
from requests.sessions import Session


class TelegramBot(Session):
    ''' TelegramBot '''

    def __init__(self, token: str):
        super().__init__()
        self.url = f'https://api.telegram.org/bot{token}'

    def get(self, path: str, **kwargs):
        ''' GET '''
        return super().get(self.url+path, **kwargs)

    def post(self, path: str, **kwargs):
        ''' POST '''
        return super().post(self.url+path, **kwargs)

    def get_me(self):
        ''' Get me '''
        return self.post('/getMe')

    def send_message(self, chat_id: str, text: str,
                     parse_mode: str = 'Markdown', reply_markup=None):
        ''' Send message '''
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        if reply_markup is not None:
            data['reply_markup'] = reply_markup

        return self.post('/sendMessage', json=data)

    def set_webhook(self, url: str):
        ''' Set webhook '''
        return self.post('/setWebhook', json={'url': url})

    def get_webhook_info(self, url: str):
        ''' Get webhook info '''
        return self.post('/getWebhookInfo', json={'url': url})

    def delete_webhook(self):
        ''' delete webhook '''
        return self.post('/deleteWebhook')

    @staticmethod
    def is_command_start(data: dict) -> bool:
        ''' command start '''
        if data['message']['from']['is_bot']:
            return False

        if data['message']['text'].strip() == '/start':
            return True

        return False

    @staticmethod
    def is_command_start_linkme(data: dict) -> bool:
        ''' command start '''
        if 'message' not in data:
            return False

        if data['message']['from']['is_bot']:
            return False

        if data['message']['text'].strip() in ('/start linkme', '/linkme'):
            return True

        return False
