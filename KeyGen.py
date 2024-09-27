import random
import time
import uuid
import httpx
import asyncio

class KeyGen:
    def __init__(self, app_token, promo_id, proxies, timing, attempts):
        self.app_token = app_token
        self.promo_id = promo_id
        self.proxies = proxies
        self.timing = timing
        self.attempts = attempts

    async def generate_client_id(self):
        timestamp = int(time.time() * 1000)
        random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
        return f"{timestamp}-{random_numbers}"

    async def login(self, client_id, retries=5):
        for attempt in range(retries):
            proxy = random.choice(self.proxies) if self.proxies else None
            async with httpx.AsyncClient(proxies=proxy) as client:
                try:
                    response = await client.post(
                        'https://api.gamepromo.io/promo/login-client',
                        json={'appToken': self.app_token, 'clientId': client_id, 'clientOrigin': 'deviceid'}
                    )
                    response.raise_for_status()
                    data = response.json()
                    print(f"Login Response: {data}")  # Add this log
                    return data['clientToken']
                except Exception as e:
                    print(f"Login attempt {attempt + 1} failed with error: {e}")
                    continue
            await asyncio.sleep(2)
        return None

    async def emulate_progress(self, client_token):
        proxy = random.choice(self.proxies) if self.proxies else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            response = await client.post(
                'https://api.gamepromo.io/promo/register-event',
                headers={'Authorization': f'Bearer {client_token}'},
                json={'promoId': self.promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'}
            )
            response.raise_for_status()
            data = response.json()
            print(f"Progress Emulation Response: {data}")  # Debug the progress response
            return data['hasCode']

    async def generate_key(self, client_token):
        proxy = random.choice(self.proxies) if self.proxies else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            response = await client.post(
                'https://api.gamepromo.io/promo/create-code',
                headers={'Authorization': f'Bearer {client_token}'},
                json={'promoId': self.promo_id}
            )
            response.raise_for_status()
            data = response.json()
            print(f"Generate Key Response: {data}")  # Debug the key generation response
            return data['promoCode']

    async def generate_keys(self, num_keys=4):
        keys = []  # List to store the generated keys
        client_id = await self.generate_client_id()
        print(f"Generated client ID: {client_id}")  # Log the client ID

        client_token = await self.login(client_id)
        if not client_token:
            print("Failed to login and retrieve client token.")
            return None

        for i in range(self.attempts):
            await asyncio.sleep(self.timing * (random.random() / 3 + 1))
            has_code = await self.emulate_progress(client_token)
            print(f"Progress attempt {i + 1}, hasCode: {has_code}")
            if has_code:
                break

        # Generate the specified number of keys
        for _ in range(num_keys):  # Change here to use num_keys parameter
            key = await self.generate_key(client_token)
            if key:
                print(f"Generated key: {key}")
                keys.append(key)  # Store each generated key
            else:
                print("Failed to generate key.")
    
        return keys  # Return the list of generated keys
