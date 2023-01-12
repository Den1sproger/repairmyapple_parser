import telebot

from parsing_tools import IPhone, MacBook, AirPods, Apple_Watch
from telebot.types import Message, ReplyKeyboardMarkup



TOKEN = '5320242884:AAFvo5kvfeHoHZZNa6xbvhvuHMGZmjbkdF8'



bot = telebot.TeleBot(TOKEN)


model = str
max_price = int
diagonal = int
memory = int



def get_card(product: dict) -> str:
    return f'{product.get("text")}\n{product.get("link")}\n'\
           f'Price: {product.get("price")} rub'


@bot.message_handler(commands=['start', 'search'])
def start(message: Message) -> None:
    start_buttons = ['IPhone', 'MacBook', 'AirPods', 'Apple Watch']
    kd = ReplyKeyboardMarkup(resize_keyboard=True)
    kd.add(*start_buttons)
    bot.send_message(
        message.chat.id, 'What do you want?', reply_markup=kd
    )



@bot.message_handler(func=lambda message: message.text == 'IPhone')
def choose_iph_model(message: Message) -> None:
    global search
    search = IPhone()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    bot.send_message(
        message.chat.id, 'Please, choose model', reply_markup=kb
    )
    bot.register_next_step_handler(message, input_mp_iph)


def input_mp_iph(message: Message) -> None:
    global model
    model = message.text
    bot.send_message(
        message.chat.id, 'Enter the maximum allowable price (in rubles)'
    )
    bot.register_next_step_handler(message, choose_iph_memory)


def choose_iph_memory(message: Message) -> None:
    global max_price
    try:
        max_price = int(message.text)
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        memory_buttons = [str(2 ** i) + ' Gb' for i in range(1, 12)]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*memory_buttons)
        bot.send_message(
            message.chat.id, 'Choose the device memory', reply_markup=kb
        )
        bot.register_next_step_handler(message, get_iphones)


def get_iphones(message: Message) -> None:
    global model, max_price, memory
    try:
        memory = int(message.text.replace(' Gb', ''))
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        bot.send_message(message.chat.id, 'Please, waiting...')

        search = IPhone()
        iphones = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_memory=memory
        )

        for i in iphones:
            card = get_card(i)
            bot.send_message(message.chat.id, card)
    finally:
        model, max_price, memory = '', 0, 0



@bot.message_handler(func=lambda message: message.text == 'MacBook')
def choose_mb_model(message: Message) -> None:
    search = MacBook()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    bot.send_message(
        message.chat.id, 'Please, choose model', reply_markup=kb
    )
    bot.register_next_step_handler(message, input_mp_mcbk)

def input_mp_mcbk(message: Message) -> None:
    global model
    model = message.text
    bot.send_message(
        message.chat.id, 'Enter the maximum allowable price (in rubles)'
    )
    bot.register_next_step_handler(message, choose_mb_memory)


def choose_mb_memory(message: Message) -> None:
    global max_price
    try:
        max_price = int(message.text)
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        memory_buttons = [str(2 ** i) + ' Gb' for i in range(1, 12)]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*memory_buttons)
        bot.send_message(
            message.chat.id, 'Choose the device memory', reply_markup=kb
        )
        bot.register_next_step_handler(message, get_macbooks)


def get_macbooks(message: Message) -> None:
    global model, max_price, memory
    try:
        memory = int(message.text.replace(' Gb', ''))
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        bot.send_message(message.chat.id, 'Please, waiting...')
        search = MacBook()
        macbooks = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_memory=memory
        )

        for i in macbooks:
            card = get_card(i)
            bot.send_message(message.chat.id, card)
    finally:
        model, max_price, memory = '', 0, 0


@bot.message_handler(func=lambda message: message.text == 'AirPods')
def get_airpods(message: Message) -> None:
    bot.send_message(message.chat.id, 'Please, waiting...')

    search = AirPods()
    pods = search.get_products()

    for i in pods:
        card = get_card(i)
        bot.send_message(message.chat.id, card)



@bot.message_handler(func=lambda message: message.text == 'Apple Watch')
def choose_aw_model(message: Message) -> None:
    search = Apple_Watch()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*search.models)
    bot.send_message(
        message.chat.id, 'Please, choose model', reply_markup=kb
    )
    bot.register_next_step_handler(message, input_mp_aw)


def input_mp_aw(message: Message) -> None:
    global model
    model = message.text
    bot.send_message(
        message.chat.id, 'Enter the maximum allowable price (in rubles)'
    )
    bot.register_next_step_handler(message, input_diag)


def input_diag(message: Message) -> None:
    global max_price
    try:
        max_price = int(message.text)
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        bot.send_message(
            message.chat.id, 'Enter the screen diagonal (in millimeters)'
        )
        bot.register_next_step_handler(message, get_watches)

def get_watches(message: Message) -> None:
    global model, max_price, diagonal
    try:
        diagonal = int(message.text)
    except ValueError:
        bot.reply_to(message, 'Incorrected input!')
    else:
        bot.send_message(message.chat.id, 'Please, waiting...')
        search = Apple_Watch()
        watches = search.get_products(
            url=str(search.models.get(model)),
            max_price=int(max_price),
            desired_diagonal=diagonal
        )

        for i in watches:
            card = get_card(i)
            bot.send_message(message.chat.id, card)
    finally:
        model, max_price, diagonal = '', 0, 0



bot.infinity_polling()