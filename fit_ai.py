import requests

class FitAI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def authenticate(self):
        """Получение токена авторизации."""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '61313eb5-5b82-4ed5-a93f-cb4c77731c1c',
            'Authorization': f'Basic {self._encode_credentials()}'
        }
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
        else:
            raise Exception(f"Authentication failed: {response.text}")

    def _encode_credentials(self):
        import base64
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def generate_plan(self, goal, level):
        return f"План для цели: {goal}, уровень подготовки: {level}"

    async def ask_question(self, question):
        """Отправка вопроса в GigaChat."""
        import aiohttp

        if not self.access_token:
            raise Exception("Authentication required. Call authenticate() first.")

        url = "https://api.gigachat.com/chat"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        data = {
            "question": question
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("answer", "Извините, я не могу сейчас ответить.")
                    else:
                        return f"Ошибка при соединении с сервером: {response.status}"
            except aiohttp.ClientError as e:
                return f"Ошибка: {str(e)}"

# Пример использования
# fit_ai = FitAI(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")
# fit_ai.authenticate()
# print(fit_ai.generate_plan("Похудение", "Новичок"))
# asyncio.run(fit_ai.ask_question("Как мне начать тренировки?"))
