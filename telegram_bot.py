import os

import telebot

from parsing_tools import IPhone, MacBook, AirPods, Apple_Watch
from telebot.types import Message, ReplyKeyboardMarkup
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TOKEN'))



class Getting_Device:
    """Class countaining functions of selecting device parameters"""

    def __init__(self, device: object,
                 apple_watch: bool = False) -> None:
        self.device = device
        self.apple_watch = apple_watch
        self.model = str
        self.max_price = int
        if apple_watch:
            self.diagonal = int
        else:
            self.memory = int


    @staticmethod
    def get_card(product: dict) -> str:   # text of message with product
        return f'{product.get("text")}\n{product.get("link")}\n'\
            f'Price: {product.get("price")} rub'


    def choose_model(self, message: Message) -> None:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*self.device.models)
        bot.send_message(
            message.chat.id, 'Please, choose model', reply_markup=kb
        )
        bot.register_next_step_handler(message, self.input_max_price)


    def input_max_price(self, message: Message) -> None:
        self.model = message.text
        bot.send_message(
            message.chat.id, 'Enter the maximum allowable price (in rubles)'
        )
        if self.apple_watch:
            bot.register_next_step_handler(message, self.input_diag)
        else:
            bot.register_next_step_handler(message, self.choose_memory)
            

    def input_diag(self, message: Message) -> None:
        try:
            self.max_price = int(message.text)
        except ValueError:
            bot.reply_to(message, 'Incorrected input!')
        else:
            bot.send_message(
                message.chat.id, 'Enter the screen diagonal (in millimeters)'
            )
            bot.register_next_step_handler(message, self.get_devices)


    def choose_memory(self, message: Message) -> None:
        try:
            self.max_price = int(message.text)
        except ValueError:
            bot.reply_to(message, 'Incorrected input!')
        else:
            memory_buttons = [str(2 ** i) + ' Gb' for i in range(1, 12)]
            kb = ReplyKeyboardMarkup(resize_keyboard=True)
            kb.add(*memory_buttons)
            bot.send_message(
                message.chat.id, 'Choose the device memory', reply_markup=kb
            )
            bot.register_next_step_handler(message, self.get_devices)


    def get_devices(self, message: Message) -> None:
        try:
            if self.apple_watch:
                self.diagonal = int(message.text)
            else:
                self.memory = int(message.text.replace(' Gb', ''))
        except ValueError:
            bot.reply_to(message, 'Incorrected input!')
        else:
            bot.send_message(message.chat.id, 'Please, waiting...')

            if self.apple_watch:
                devices = self.device.get_products(
                    url=str(self.device.models.get(self.model)),
                    max_price=int(self.max_price),
                    desired_diagonal=self.diagonal
                )
            else:
                devices = self.device.get_products(
                    url=str(self.device.models.get(self.model)),
                    max_price=int(self.max_price),
                    desired_memory=self.memory
                )
                
            for i in devices:
                card = Getting_Device.get_card(i)
                bot.send_message(message.chat.id, card)

    
    def __del__(self) -> int:
        return 0



@bot.message_handler(commands=['start', 'search'])
def start(message: Message) -> None:
    start_buttons = ['IPhone', 'MacBook', 'AirPods', 'Apple Watch']
    kd = ReplyKeyboardMarkup(resize_keyboard=True)
    kd.add(*start_buttons)
    bot.send_message(
        message.chat.id, 'What do you want?', reply_markup=kd
    )


@bot.message_handler(func=lambda message: message.text == 'IPhone')
def get_iphones(message):
    iphone = IPhone()
    search = Getting_Device(iphone)
    search.choose_model(message)


@bot.message_handler(func=lambda message: message.text == 'MacBook')
def get_macbooks(message):
    macbook = MacBook()
    search = Getting_Device(macbook)
    search.choose_model(message)


@bot.message_handler(func=lambda message: message.text == 'AirPods')
def get_airpods(message: Message) -> None:
    bot.send_message(message.chat.id, 'Please, waiting...')

    search = AirPods()
    pods = search.get_products()

    for i in pods:
        card = Getting_Device.get_card(i)
        bot.send_message(message.chat.id, card)


@bot.message_handler(func=lambda message: message.text == 'Apple Watch')
def get_aw(message):
    aw = Apple_Watch()
    search = Getting_Device(aw, apple_watch=True)
    search.choose_model(message)



bot.infinity_polling()