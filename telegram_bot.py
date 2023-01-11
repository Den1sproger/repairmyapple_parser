from parsing_tools import IPhone, MacBook, AirPods, Apple_Watch
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold, hlink



TOKEN = '5320242884:AAFvo5kvfeHoHZZNa6xbvhvuHMGZmjbkdF8'



bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
ds = Dispatcher(bot=bot, storage=MemoryStorage())

model = str
max_price = int
diagonal = int
memory = int



class User_answers(StatesGroup):
    iphone_model = State()
    mac_model = State()
    watch_model = State()
    max_price_iphone = State()
    max_price_mac = State()
    max_price_watch = State()
    iphone_memory = State()
    mac_memory = State()
    diagonal = State()


def get_card(product: dict) -> str:
    return f'{hlink(product.get("text"), product.get("link"))}\n'\
           f'{hbold("Price: ")} {product.get("price")} rub'


@ds.message_handler(commands=['search'])
async def start(message: types.Message) -> None:
    start_buttons = ['IPhone', 'MacBook', 'AirPods', 'Apple Watch']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('What do you want?', reply_markup=keyboard)



@ds.message_handler(Text(equals='IPhone'))
async def input_iph_model(message: types.Message) -> None:
    global search
    search = IPhone()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    await User_answers.iphone_model.set()
    await message.answer(f'Please, choose model', reply_markup=kb)


@ds.message_handler(state=User_answers.iphone_model)
async def input_mp_iph(message: types.Message, state: FSMContext) -> None:
    global model
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        model = proxy['text']
    await User_answers.max_price_iphone.set()
    await message.answer('Enter the maximum allowable price (in rubles)')


@ds.message_handler(state=User_answers.max_price_iphone)
async def choose_iph_memory(message: types.Message, state: FSMContext) -> None:
    global max_price
    async with state.proxy() as proxy:
        proxy['text'] = message.text
    try:
        max_price = int(proxy['text'])
    except ValueError:
        await message.answer('Incorrected input!')
    else:
        memory_buttons = [str(2 ** i) + ' Gb' for i in range(1, 12)]
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*memory_buttons)
        await User_answers.iphone_memory.set()
        await message.answer('Choose the device memory', reply_markup=kb)


@ds.message_handler(state=User_answers.iphone_memory)
async def get_iphones(message: types.Message, state: FSMContext) -> None:
    global model, max_price, memory
    async with state.proxy() as proxy:
        proxy['text'] = message.text
    try:
        memory = int(proxy['text'].replace(' Gb', ''))
    except ValueError:
        await message.answer('Incorrected input!')
    else:
        await message.answer('Please, waiting...')
        search = IPhone()
        iphones = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_memory=memory
        )

        for i in iphones:
            card = get_card(i)
            await message.answer(card)

        model = ''
        max_price = 0
        memory = 0

        await state.finish()


@ds.message_handler(Text(equals='MacBook'))
async def input_mb_model(message: types.Message) -> None:
    search = MacBook()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    await User_answers.mac_model.set()
    await message.answer(f'Please, choose model', reply_markup=kb)


@ds.message_handler(state=User_answers.mac_model)
async def input_mp_mb(message: types.Message, state: FSMContext) -> None:
    global model
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        model = proxy['text']
    await User_answers.max_price_mac.set()
    await message.answer('Enter the maximum allowable price (in rubles)')


@ds.message_handler(state=User_answers.max_price_mac)
async def choose_mb_memory(message: types.Message, state: FSMContext) -> None:
    global max_price
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        try:
            max_price = int(proxy['text'])
        except ValueError:
            await message.answer('Incorrected input!')
        else:
            memory_buttons = [str(2 ** i) + ' Gb' for i in range(1, 12)]
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.add(*memory_buttons)
            await User_answers.mac_memory.set()
            await message.answer('Choose the device memory', reply_markup=kb)


@ds.message_handler(state=User_answers.mac_memory)
async def get_macbooks(message: types.Message, state: FSMContext) -> None:
    global model, max_price
    async with state.proxy() as proxy:
        proxy['text'] = message.text
    try:
        memory = int(proxy['text'].replace(' Gb', ''))
    except ValueError:
        await message.answer('Incorrected input!')
    else:
        await message.answer('Please, waiting...')
        search = MacBook()
        macbooks = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_memory=memory
        )

        for i in macbooks:
            card = get_card(i)
            await message.answer(card)

        model = ''
        max_price = 0
        memory = 0

        await state.finish()


@ds.message_handler(Text(equals='AirPods'))
async def get_airpods(message: types.Message) -> None:
    await message.answer('Please, waiting...')

    search = AirPods()
    pods = search.get_products()

    for i in pods:
        card = get_card(i)
        await message.answer(card)



@ds.message_handler(Text(equals='Apple Watch'))
async def input_aw_model(message: types.Message) -> None:
    search = Apple_Watch()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    await User_answers.watch_model.set()
    await message.answer(f'Please, choose model', reply_markup=kb)


@ds.message_handler(state=User_answers.watch_model)
async def input_mp_aw(message: types.Message, state: FSMContext) -> None:
    global model
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        model = proxy['text']
    await User_answers.max_price_watch.set()
    await message.answer('Enter the maximum allowable price (in rubles)')


@ds.message_handler(state=User_answers.max_price_watch)
async def input_diag(message: types.Message, state: FSMContext) -> None:
    global max_price
    async with state.proxy() as proxy:
        proxy['text'] = message.text
    try:
        max_price = int(proxy['text'])
    except ValueError:
        await message.answer('Incorrected input!')
    else:
        await User_answers.diagonal.set()
        await message.answer('Enter the screen diagonal (in millimeters)')


@ds.message_handler(state=User_answers.diagonal)
async def get_watches(message: types.Message, state: FSMContext) -> None:
    global model, max_price, diagonal
    async with state.proxy() as proxy:
        proxy['text'] = message.text
    try:
        diagonal = int(proxy['text'])
    except ValueError:
        await message.answer('Incorrected input!')
    else:
        await message.answer('Please, waiting...')
        search = Apple_Watch()
        watches = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_diagonal=diagonal
        )

        for i in watches:
            card = get_card(i)
            await message.answer(card)

        model = ''
        max_price = 0
        diagonal = 0

        await state.finish()



if __name__ == '__main__':
    executor.start_polling(dispatcher=ds, skip_updates=True)