import asyncio
import requests
import logging
from aiogram import Bot, types, Dispatcher, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

API_TOKEN = '7935212447:AAF1QGQkSMwFLWqyWWlERoFTbMPy7z74IEE'
DISTRIBUTOR_BOT_TOKEN = '7979123656:AAGJyQVwkQg5tpZ-tPDt1xWAw0Qs8Z4-rLo'

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher with in-memory storage
bot = Bot(token=API_TOKEN)
distributor_bot = Bot(token=DISTRIBUTOR_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Initialize router
router = Router()

# Define states
class Form(StatesGroup):
    game_selection = State()

# GPLinks API key and URL shortening
def shorten_url(long_url):
    api_key = 'a0807d2977bb6f2990b75c13dd9f4c2505c1df52'  # Replace with your GPLinks API key
    api_url = 'https://gplinks.com/api'
    
    params = {
        'api': api_key,
        'url': long_url,
    }
    
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['shortenedUrl']
        else:
            print(f"GPLinks error: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"Failed to shorten URL. Status Code: {response.status_code}")
        return None

# Middleware for logging
class SimpleMiddleware:
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            print(f"Received message: {event.text}")
        result = await handler(event, data)
        print("Message processing completed.")
        return result

# Attach middleware to dispatcher
dp.message.middleware(SimpleMiddleware())

# Games data
games = {
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

# Start command handler
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer("Welcome! Click the button below to generate keys.", reply_markup=generate_keys_markup())

# Helper function to generate inline keyboard
def generate_keys_markup():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Generate Keys", callback_data="generate_keys")]
    ])
    return markup

# Callback query handler for game generation
@router.callback_query(F.data == 'generate_keys')
async def list_games(callback_query: types.CallbackQuery, state: FSMContext):
    game_list = "\n".join([f"{num}. {name['name']}" for num, name in games.items()])
    await bot.send_message(callback_query.from_user.id, f"Select a game by entering its number:\n\n{game_list}")
    await state.set_state(Form.game_selection)

# Handle game selection input from user
@router.message(F.text.regexp(r'^\d+$'), StateFilter(Form.game_selection))
async def handle_game_selection(message: types.Message, state: FSMContext):
    game_number = int(message.text)
    if game_number in games:
        selected_game = games[game_number]
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Get Key", callback_data=f"get_key_{game_number}")]
        ])
        await message.answer(f"You selected {selected_game['name']}. Click the button below to get the key.", reply_markup=markup)
    else:
        await message.answer("Invalid selection. Please choose a valid game number.")

# Callback query handler for getting the game key
@router.callback_query(lambda query: query.data.startswith("get_key_"))
async def process_get_key(callback_query: types.CallbackQuery):
    game_number = int(callback_query.data.split("_")[2])
    selected_game = games[game_number]
    
    # Create the long URL to trigger /start command on Key_Distribution_bot
    long_url = f"http://t.me/Key_Distributor_bot?start=game_{game_number}"
    
    # Shorten the URL using GPLinks
    shortened_url = shorten_url(long_url)
    
    if shortened_url:
        # Send the shortened URL to the user in the Get Key button
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Get Key", url=shortened_url)]
        ])
        await bot.send_message(callback_query.from_user.id, f"Click the button below to get your key for {selected_game['name']}:", reply_markup=markup)
        
        # Send game info to Key_Distribution_bot for processing
        await distributor_bot.send_message(chat_id='7116980283',  # Replace with your chat ID or distribution bot chat ID
                                           text=f"Game Selected: {selected_game['name']}\n"
                                                )
        
        # Trigger /start command on the Key_Distribution_bot
        await distributor_bot.send_message(chat_id='7116980283', text='/start')
    else:
        await bot.send_message(callback_query.from_user.id, "Failed to generate the shortened link. Please try again later.")

# Main function to start the bot
async def main():
    # Attach router to dispatcher
    dp.include_router(router)
    
    try:
        # Start polling
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# Run the bot
if __name__ == '__main__':
    asyncio.run(main())
