import telebot
from telebot import types
import telebot, shelve, sqlite3
import config, adminka
import forex_python.converter
import time
from time import sleep


# Обьяснил как долбоёбу
bot: object = telebot.TeleBot(config.token)
in_admin = []
id = (config.id)
site = (config.site)
channel = (config.channel)
op = (config.op)

@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    bot.send_message(id,
                     str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Написал: " + str(message.text))
    keyboard: object = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="Москва", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Воронеж", callback_data="button2")
    button3 = types.InlineKeyboardButton(text="Норильск", callback_data="button3")
    button4 = types.InlineKeyboardButton(text="Томск", callback_data="button4")
    button5 = types.InlineKeyboardButton(text="Краснодар", callback_data="button5")
    button6 = types.InlineKeyboardButton(text="Красноярск", callback_data="button6")
    button7 = types.InlineKeyboardButton(text="Иркутск", callback_data="button7")
    button8 = types.InlineKeyboardButton(text="Улан-Удэ", callback_data="button8")
    button9 = types.InlineKeyboardButton(text="Бийск", callback_data="button9")
    button10 = types.InlineKeyboardButton(text="Борисоглебцк", callback_data="button10")
    button11 = types.InlineKeyboardButton(text="Пермь", callback_data="button11")
    button12 = types.InlineKeyboardButton(text="Екатеринбург", callback_data="button12")
    button13 = types.InlineKeyboardButton(text="Сургут", callback_data="button13")
    button14 = types.InlineKeyboardButton(text="Сочи", callback_data="button14")
    button15 = types.InlineKeyboardButton(text="Ханты-Мансийский", callback_data="button15")
    button16 = types.InlineKeyboardButton(text="Абакан", callback_data="button16")
    button17 = types.InlineKeyboardButton(text="Оренбург", callback_data="button17")
    button18 = types.InlineKeyboardButton(text="Нижний Новгород", callback_data="button18")
    keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13, button14, button15, button16, button17, button18)
    bot.send_message(message.chat.id, "Привет, " + str(
        message.chat.first_name) + ".\nДобро пожаловать в наш бот удовольствий.\nИНФO-канал: " + str(
        channel) + "\nОператор: " + str(op) + "\nПожалуйста, выберите город:", reply_markup=keyboard)

def button(message, city):
    keyboard1 = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton(text="Ленинский", callback_data="ray1")
    button3 = types.InlineKeyboardButton(text="Московский", callback_data="ray2")
    bot.send_message(id, str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Выбрал: " + str(name))
    keyboard1.add(button2)
    keyboard1.add(button3)
    bot.send_message(message.chat.id, "Вы выбрали " + str(city) + ".\nТеперь выберите Район:",
                     reply_markup=keyboard1)
def button(message, ray):
    keyboard2 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="СК синее", callback_data="blue")
    button2 = types.InlineKeyboardButton(text="Гашиш на реагенте", callback_data="red")
    button3 = types.InlineKeyboardButton(text="Гашиш печать ROLEX", callback_data="yellow")
    bot.send_message(id, str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Выбрал: " + str(ray))
    keyboard2.add(button1)
    keyboard2.add(button2)
    keyboard2.add(button3)
    bot.send_message(message.chat.id, "Вы выбрали город " + str(ray) + ".\nТеперьвыберите товар:",
                     reply_markup=keyboard2)


def blue(message, name):
    keyboard3 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="0.3г - 900р", callback_data="b3")
    button2 = types.InlineKeyboardButton(text="0.5г - 1200р", callback_data="b5")
    button3 = types.InlineKeyboardButton(text="1г - 2200р", callback_data="b1")
    bot.send_message(id, str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Выбрал: " + str(name))
    keyboard3.add(button1)
    keyboard3.add(button2)
    keyboard3.add(button3)
    bot.send_message(message.chat.id, "Вы выбрали " + str(name) + ".\nТеперь выберите количество:",
                     reply_markup=keyboard3)


def red(message, name):
    keyboard3 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="0.3г - 650р", callback_data="r3")
    button2 = types.InlineKeyboardButton(text="0.6г - 1100р", callback_data="r6")
    button3 = types.InlineKeyboardButton(text="1г - 1500р", callback_data="r1")
    bot.send_message(id, str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Выбрал: " + str(name))
    keyboard3.add(button1)
    keyboard3.add(button2)
    keyboard3.add(button3)
    bot.send_message(message.chat.id, "Вы выбрали " + str(name) + ".\nТеперь выберите количество:",
                     reply_markup=keyboard3)


def yellow(message, name):
    keyboard3 = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton(text="0.6г - 950р", callback_data="y6")
    button3 = types.InlineKeyboardButton(text="1.1г - 1350р", callback_data="y11")
    bot.send_message(id, str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Выбрал: " + str(name))
    keyboard3.add(button2)
    keyboard3.add(button3)
    bot.send_message(message.chat.id, "Вы выбрали " + str(name) + ".\nТеперь выберите количество:",
                     reply_markup=keyboard3)


def buy(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Оплатить", url=site, callback_data="by")
    keyboard.add(button1)
    bot.send_message(message.chat.id, "Для оплаты нажмите на кнопку:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message = call.message
    if call.message:
        if call.data == "button1":
            button(call.message, "Москва")
        elif call.data == "button2":
            button(call.message, "Воронеж")
        elif call.data == "button3":
            button(call.message, "Норильск")
        elif call.data == "button4":
            button(call.message, "Томск")
        elif call.data == "button5":
            button(call.message, "Краснодар")
        elif call.data == "button6":
            button(call.message, "Красноярск")
        elif call.data == "button7":
            button(call.message, "Иркутск")
        elif call.data == "button8":
            button(call.message, "Улан-Удэ")
        elif call.data == "button9":
            button(call.message, "Бийск")
        elif call.data == "button10":
            button(call.message, "Борисоглебцк")
        elif call.data == "button11":
            button(call.message, "Пермь")
        elif call.data == "button12":
            button(call.message, "Екатеринбург")
        elif call.data == "button13":
            button(call.message, "Сургут")
        elif call.data == "button14":
            button(call.message, "Сочи")
        elif call.data == "button15":
            button(call.message, "Ханты-Мансийский")
        elif call.data == "button16":
            button(call.message, "Абакан")
        elif call.data == "button17":
            button(call.message, "Оренбург")
        elif call.data == "button18":
            button(call.message, "Нижний Новгород")
        elif call.data == "ray1":
            button(call.message, "Ленинский")
        elif call.data == "ray2":
            button(call.message, "Московский")
        elif call.data == "blue":
            blue(call.message, "СК синее")
        elif call.data == "blue":
            blue(call.message, "СК синее")
        elif call.data == "red":
            red(call.message, "Гашиш на реагенте")
        elif call.data == "yellow":
            yellow(call.message, "Гашиш печать ROLEX")
        elif call.data == "b3":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: СК синее 0.3г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали СК синее 0.3г\nК оплате:900р.\nКоментарий: " + str(message.chat.id))
            buy(message)
        elif call.data == "b5":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: СК синее 0.5г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали СК синее 0.5г\nК оплате:1200р.\nКоментарий: " + str(message.chat.id))
            buy(message)
        elif call.data == "b1":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: СК синее 1г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали СК синее 1г\nК оплате:2200р.\nКоментарий: " + str(message.chat.id))
            buy(message)
        elif call.data == "r3":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: Гашиш на реагенте 0.3г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали Гашиш на реагенте0.3г\nК оплате: 650р.\nКоментарий: " + str(
                                 message.chat.id))
            buy(message)
        elif call.data == "r6":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: Гашиш на реагенте 0.6г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали Гашиш на реагенте0.6г\nК оплате: 1100р.\nКоментарий: " + str(
                                 message.chat.id))
            buy(message)
        elif call.data == "r1":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: Гашиш на реагенте 1г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали Гашиш на реагенте 1г\nКоплате: 1500р.\nКоментарий: " + str(
                                 message.chat.id))
            buy(message)
        elif call.data == "y6":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: Гашиш печать ROLEX 0.6г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали Гашиш печать ROLEX0.6г\nК оплате: 950р.\nКоментарий: " + str(
                                 message.chat.id))
            buy(message)
        elif call.data == "y11":
            bot.send_message(id, str(message.chat.first_name) + " [ " + str(
                message.chat.id) + " ] |Оплачивает: Гашиш на реагенте 1.1г")
            bot.send_message(message.chat.id,
                             "QIWI\nВы выбрали Гашиш печать ROLEX1.1г\nК оплате: 1350р.\nКоментарий: " + str(
                                 message.chat.id))
            buy(message)


@bot.message_handler(content_types=['text'])
def message_send(message):
    if '/start' == message.text:
        if message.chat.first_name:
            if dop.get_sost(message.chat.id) is True:
                with shelve.open(files.sost_bd) as bd: del bd[str(message.chat.id)]
            if message.chat.id in in_admin: in_admin.remove(message.chat.id)
            if message.chat.id == config.admin_id and dop.it_first() is True:
                in_admin.append(message.chat.id)
                dop.main(message.chat.id)
            elif dop.it_first() is True and message.chat.id not in dop.get_adminlist():
                print("no ready")
            elif dop.check_message('start') is True:
                buttons = []
                keyboard_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                if config.reviews_channel != '':
                    reviews = types.KeyboardButton(text='💌Наши отзывы')
                    buttons.append(reviews)
                if config.support != '':
                    support = types.KeyboardButton(text='👨🏻‍💻Оператор')
                    buttons.append(support)
                if config.rules != '':
                    rules = types.KeyboardButton(text='📖Правила')
                    buttons.append(rules)

                tmp = types.KeyboardButton(text='🔥Перейти к покупкам')

                try:
                    bot.send_message(message.chat.id, '💁🏻‍Добро пожаловать в магазин ',
                                     reply_markup=keyboard_start, parse_mode='Markdown')
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Каталог',
                                                               callback_data='Перейти к каталогу товаров'))
                    with shelve.open(files.bot_message_bd) as bd:
                        start_message = bd['start']
                    start_message = start_message.replace('name', message.from_user.first_name)
                    bot.send_message(message.chat.id, start_message, reply_markup=key, parse_mode='Markdown')
                except:
                    pass
            elif dop.check_message('start') is False and message.chat.id in dop.get_adminlist():
                bot.send_message(message.chat.id,
                                 'Приветствие ещё не добавлено!\nЧтобы его добавить, перейдите в админку по команде /adm и *настройте ответы бота*',
                                 parse_mode='Markdown')

            dop.user_loger(chat_id=message.chat.id)  # логгирование юзеровs
        elif not message.chat.first_name:
            with shelve.open(files.bot_message_bd) as bd:
                start_message = bd['userfalse']
            start_message = start_message.replace('uname', message.from_user.first_name)
            try:
                bot.send_message(message.chat.id, start_message, parse_mode='Markdown')
            except:
                pass

    elif '/adm' == message.text:
        if not message.chat.id in in_admin:
            in_admin.append(message.chat.id)
        adminka.in_adminka(message.chat.id, message.text, message.chat.username, message.from_user.first_name)

    elif message.chat.id in in_admin:
        adminka.in_adminka(message.chat.id, message.text, message.chat.username, message.from_user.first_name)

    elif '/help' == message.text:
        try:
            if dop.check_message('help') is True:
                with shelve.open(files.bot_message_bd) as bd:
                    help_message = bd['help']
                help_message = help_message.replace('name', message.from_user.first_name)
                bot.send_message(message.chat.id, help_message)

            elif dop.check_message('help') is False and message.chat.id in dop.get_adminlist():
                bot.send_message(message.chat.id,
                                 'Сообщение с помощью ещё не добавлено!\nЧтобы его добавить, перейдите в админку по команде /adm и *настройте ответы бота*',
                                 parse_mode='Markdown')
        except:
            pass
    elif '💌Наши отзывы' == message.text:
        bot.send_message(message.chat.id,
                         f'🔗*Наша группа с отзывами* - {config.reviews_channel}',
                         parse_mode='Markdown')
    elif '🔥Перейти к покупка' == message.text:
        bot.send_message(message.chat.id,
                         f'Для покупки товара нажмите /start* - {config.support}',
                         parse_mode='Markdown')
    elif '👨🏻‍💻Оператор' == message.text:
        if '_' in config.support:
            support = config.support.replace('_', '\_')
            bot.send_message(message.chat.id,
                             f'🔗*Связь с поддержкой* - {support}',
                             parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id,
                             f'🔗*Связь с поддержкой* - {config.support}', parse_mode='Markdown')
    elif '📖Правила' == message.text:
        bot.send_message(message.chat.id,
                         f'{config.rules}',
                         parse_mode='Markdown')

    elif dop.get_sost(message.chat.id) is True:
        with shelve.open(files.sost_bd) as bd:
            sost_num = bd[str(message.chat.id)]
        if sost_num == 22:
            key = telebot.types.InlineKeyboardMarkup()
            try:
                amount = int(message.text)  # проверяется, числительно ли это
                with open('data/Temp/' + str(message.chat.id) + 'good_name.txt', encoding='utf-8') as f:
                    name_good = f.read()
                if dop.get_minimum(name_good) <= amount <= dop.amount_of_goods(name_good):
                    sum = dop.order_sum(name_good, amount)
                    if dop.check_vklpayments('qiwi') == '✅' and dop.check_vklpayments('btc') == '✅':
                        if sum >= 80:
                            key.add(telebot.types.InlineKeyboardButton(text='🥝Qiwi', callback_data='Qiwi'),
                                    telebot.types.InlineKeyboardButton(text='💰Криптовалюта', callback_data='btc'))
                        elif sum >= 80:
                            key.add(telebot.types.InlineKeyboardButton(text='🥝Qiwi', callback_data='Qiwi'))
                            key.add(telebot.types.InlineKeyboardButton(
                                text='Выбрать больше товара для оплаты криптовалютой', callback_data='Купить'))

                    elif dop.check_vklpayments('qiwi') == '✅':
                        key.add(telebot.types.InlineKeyboardButton(text='🥝Qiwi', callback_data='Qiwi'))
                        key.add(telebot.types.InlineKeyboardButton(text='💰Криптовалюта', callback_data='btc'))
                    elif dop.check_vklpayments('btc') == '✅' and sum >= 80:
                        key.add(telebot.types.InlineKeyboardButton(text='💰Криптовалюта', callback_data='btc'))
                        key.add(telebot.types.InlineKeyboardButton(text='🥝Qiwi', callback_data='Qiwi'))
                    elif dop.check_vklpayments('btc') == '✅' and sum >= 80:
                        key.add(
                            telebot.types.InlineKeyboardButton(text='Выбрать больше товара для оплаты криптовалютой',
                                                               callback_data='Купить'))
                    key.add(
                        telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
                    price_dollars = c.convert('RUB', 'USD', sum)
                    bot.send_message(message.chat.id, 'Вы *выбрали*: ' + name_good + '\n*Количество*: ' + str(
                        amount) + '\n*Цена* заказа: ' + str(sum) + f'₽ ({price_dollars:.2f}$)'
                                                                   '\nВыберите, через что будете оплачивать',
                                     parse_mode='Markdown', reply_markup=key)
                    with open('data/Temp/' + str(message.chat.id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(str(amount) + '\n')  # записывается количество выбраных товаров
                        f.write(str(sum) + '\n')  # записывается стоимость выбранных товаров
                elif dop.get_minimum(name_good) >= amount:
                    key.add(
                        telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
                    bot.send_message(message.chat.id,
                                     'Выберите больше пожалуйста!\nМинимальное количество к покупке - *' + str(
                                         dop.get_minimum(name_good)) + '*', parse_mode='Markdown', reply_markup=key)
                elif amount >= dop.amount_of_goods(name_good):
                    bot.send_message(message.chat.id,
                                     'Выберите меньше пожалуйста!\nМаксимальное количество к покупке - *' + str(
                                         dop.amount_of_goods(name_good)) + '*', parse_mode='Markdown', reply_markup=key)
            except:
                key.add(telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
                bot.send_message(message.chat.id, 'Введите строго в цифрах!', reply_markup=key)

def inline(callback):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    the_categories = dop.get_categories()
    the_goods = dop.get_goods()
    if callback.message.chat.id in in_admin:
        adminka.ad_inline(callback.data, callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'Перейти к каталогу товаров':
        cursor.execute("SELECT name, id FROM categories;")
        key = telebot.types.InlineKeyboardMarkup(row_width=2)
        names = [name for name, _ in cursor.fetchall()]
        key.add(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in names])
        key.add(telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Вернуться в начало'))

        if dop.get_productcatalog() is None:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
                                      text='Ничего не было еще добавлено в бот')
        else:
            try:
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                      text='*Выберите город:*', reply_markup=key, parse_mode='Markdown')
            except:
                pass
    elif callback.data in the_categories:
        cursor.execute("SELECT name, categories FROM goods;")
        key = telebot.types.InlineKeyboardMarkup(row_width=1)
        names, prices, stored = dop.get_categories_catalog(callback.data)
        for name, price, store in zip(names, prices, stored):
            button = name + f' |Цена - {price}₽ |Доступно - {store}'
            if len(button) < 60:
                try:
                    key.add(telebot.types.InlineKeyboardButton(text=button,
                                                               callback_data=name))
                except:
                    pass
            elif len(button) > 60:
                for admin_id in dop.get_adminlist():
                    try:
                        bot.send_message(admin_id,
                                         f'Позиция *{name}* имеет слишком длинное название!\nМакс длина строки 30 символов!',
                                         parse_mode='Markdown')
                    except:
                        pass

        key.add(telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text=f'*Категория* {callback.data}', reply_markup=key, parse_mode='Markdown')
        except:
            pass
    elif callback.data in the_goods:
        with open('data/Temp/' + str(callback.message.chat.id) + 'good_name.txt', 'w', encoding='utf-8') as f:
            f.write(callback.data)
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton(text='Купить', callback_data='Купить'))
        key.add(telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text=dop.get_description(callback.data), reply_markup=key)
        except:
            pass

    elif callback.data == 'Вернуться в начало':
        if callback.message.chat.id:
            if dop.get_sost(callback.message.chat.id) is True:
                with shelve.open(files.sost_bd) as bd: del bd[str(callback.message.chat.id)]
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Каталог',
                                                       callback_data='Перейти к каталогу товаров'))
            with shelve.open(files.bot_message_bd) as bd:
                start_message = bd['start']
            start_message = start_message.replace('name', callback.from_user.first_name)
            try:
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                      text=start_message, reply_markup=key)
            except:
                pass
        elif not callback.message.chat.username:
            with shelve.open(files.bot_message_bd) as bd:
                start_message = bd['userfalse']
            start_message = start_message.replace('uname', callback.from_user.first_name)
            bot.send_message(callback.message.chat.id, start_message, parse_mode='Markdown')

    elif callback.data == 'Купить':
        with open('data/Temp/' + str(callback.message.chat.id) + 'good_name.txt', encoding='utf-8') as f:
            name_good = f.read()

        if dop.amount_of_goods(name_good) == 0:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
                                      text='Невозможно к покупке в настоящий момент')
        elif dop.payments_checkvkl() is None:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
                                      text='Платежные методы не настроены, Вы не можете купить товар')
        else:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Ленинский️', callback_data='1'))
            key.add(telebot.types.InlineKeyboardButton(text='Московский', callback_data='1'))
            key.add(telebot.types.InlineKeyboardButton(text='Back⬅️', callback_data='Перейти к каталогу товаров'))
            try:
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                      text='Введите *район * \n*Доступные районы* к '
                                           'покупке:' + str(
                                          dop.get_minimum(name_good)) + '\n*Максимально* возможно: ' + str(
                                          dop.amount_of_goods(name_good)) + '```\n\nВнимание оплата криптовалютой '
                                                                            'доступна при заказе от 80₽```',
                                      reply_markup=key, parse_mode='Markdown')
            except:
                pass
            with shelve.open(files.sost_bd) as bd:
                bd[str(callback.message.chat.id)] = 22

    elif callback.data == 'btc' or callback.data == 'Qiwi':
        if callback.data == 'Qiwi':
            with open('data/Temp/' + str(callback.message.chat.id) + 'good_name.txt', encoding='utf-8') as f:
                name_good = f.read()
            amount = dop.normal_read_line('data/Temp/' + str(callback.message.chat.id) + '.txt', 0)
            sum = dop.normal_read_line('data/Temp/' + str(callback.message.chat.id) + '.txt', 1)

            payments.creat_bill_qiwi(callback.message.chat.id, callback.id, callback.message.message_id, sum, name_good,
                                     amount)
        elif callback.data == 'btc':
            sum = dop.normal_read_line('data/Temp/' + str(callback.message.chat.id) + '.txt', 1)
            with open('data/Temp/' + str(callback.message.chat.id) + 'good_name.txt', encoding='utf-8') as f:
                name_good = f.read()
            amount = dop.normal_read_line('data/Temp/' + str(callback.message.chat.id) + '.txt', 0)
            payments.creat_bill_btc(callback.message.chat.id, callback.id, callback.message.message_id, sum,
                                    name_good, amount, callback.message.from_user.first_name,
                                    callback.from_user.username)
    elif callback.data == 'Проверить оплату':
        username = callback.from_user.username
        if callback.from_user.username is None:
            username = 'без username'
        payments.check_oplata_qiwi(callback.message.chat.id, username, callback.id,
                                   callback.message.from_user.first_name, callback.message.message_id)
    # elif callback.data == 'Обновить':
    #     try:
    #         if callback.message.chat.id in payments.he_client:
    #             bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
    #                                       text='Все и так отлично работает!')
    #             pass
    #         else:
    #             payments.he_client.append(callback.message.chat.id)
    #             bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
    #                                       text='Обновил состояние!')
    #     except:
    #         pass
    elif callback.data == 'Проверить оплату btc':
        username = callback.from_user.username
        if callback.from_user.username is None:
            username = 'без username'
        payments.check_oplata_btc(callback.message.chat.id, username, callback.id,
                                  callback.message.from_user.first_name, callback.message.message_id)

    elif dop.get_sost(callback.message.chat.id) is True:
        with shelve.open(files.sost_bd) as bd:
            sost_num = bd[str(callback.message.chat.id)]
        if sost_num == 12:
            pass
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~работа с файлами~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def echo_all(message):
    bot.send_message(id,
                     str(message.chat.first_name) + " [ " + str(message.chat.id) + " ] |Написал: " + str(message.text))
    bot.send_message(message.chat.id, "Вы что-то делаете не так, пожалуйста нажмите -/start")

@bot.message_handler(content_types=['document'])
def handle_docs_log(message):
    if message.chat.id in in_admin:
        if shelve.open(files.sost_bd)[str(message.chat.id)] == 12:
            adminka.new_files(message.document.file_id, message.chat.id)
while True:
    bot.polling(none_stop=True)
    if __name__ == '__main__':
        bot.infinity_polling()
