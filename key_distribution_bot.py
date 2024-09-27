import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import KeyGen  # Import your KeyGen class

API_TOKEN = '7979123656:AAGJyQVwkQg5tpZ-tPDt1xWAw0Qs8Z4-rLo'  # Replace with your bot's API token

# Example game configurations (you should populate this with your actual game configurations)
game_configs = {
    1: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
        'timing': 25000 / 1000,
        'attempts': 20,
    },
    2: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
        'timing': 20000 / 1000,
        'attempts': 15,
    },
    3: {
        'name': 'Merge Away',
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4',
        'timing': 20000 / 1000,
        'attempts': 25,
    },
    4: {
        'name': 'Twerk Race 3D',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    5: {
        'name': 'Polysphere',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    6: {
        'name': 'Mow and Trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    7: {
        'name': 'Tile Trio',
        'appToken': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'promoId': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    8: {
        'name': 'Zoopolis',
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'promoId': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    9: {
        'name': 'Fluff Crusade',
        'appToken': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'promoId': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    10: {
        'name': 'Stone Age',
        'appToken': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'promoId': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
   11: {
        'name': 'Bouncemasters',
        'appToken': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'promoId': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'timing': 20000 / 1000,
        'attempts': 20,
    },
    12: {
        'name': 'Hide Ball',
        'appToken': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'promoId': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'timing': 40000 / 1000,
        'attempts': 20,
    },
    13: {
        'name': 'Pin Out Master',
        'appToken': 'd2378baf-d617-417a-9d99-d685824335f0',
        'promoId': 'd2378baf-d617-417a-9d99-d685824335f0',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    14: {
        'name': 'Count Masters',
        'appToken': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'promoId': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    15: {
        'name': 'Infected Frontier',
        'appToken': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'promoId': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    16: {
        'name': 'Among Waterr',
        'appToken': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'promoId': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
    17: {
        'name': 'Factory World',
        'appToken': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'promoId': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'timing': 30000 / 1000,
        'attempts': 20,
    },
}

proxies = []

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Use in-memory storage for FSM
dp = Dispatcher(storage=storage)

ADMIN_IDS = [7116980283, 940961498]


@dp.message(F.text.startswith('/start game_'))  # Handle commands like /start game_1, game_2, etc.
async def handle_start(message: types.Message):

    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        await message.answer("You do not have permission to use this command.")
        return
    
    game_info = message.text.split('_')[1] if '_' in message.text else None

    if game_info and game_info.isdigit():
        game_number = int(game_info)
        if game_number in game_configs:
            game_config = game_configs[game_number]

            keys = await generate_key(game_config)  # No need to loop since keys[] is returned

            if keys:
                # Join all keys into a single message
                keys_message = "\n".join([f"Key {i+1}: {key}" for i, key in enumerate(keys)])
                
                # Send all keys in one message
                await bot.send_message(message.from_user.id, f"Your generated keys for {game_config['name']}:\n\n{keys_message}")
            else:
                await bot.send_message(message.from_user.id, "Failed to generate a key. Please try again later.")
        else:
            await bot.send_message(message.from_user.id, "Invalid game number. Please try again.")
    else:
        await bot.send_message(message.from_user.id, "No valid game information received.")


async def generate_key(game_config, num_keys=4):  # Defaults to 4 keys
    key_gen = KeyGen.KeyGen(
        app_token=game_config['appToken'],
        promo_id=game_config['promoId'],
        proxies=proxies,
        timing=game_config['timing'],
        attempts=game_config['attempts']
    )
    
    # The KeyGen class now returns the list of keys directly
    return await key_gen.generate_keys(num_keys=num_keys)

# Async main function to start the bot
async def main():
    try:
        # Start polling
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())
