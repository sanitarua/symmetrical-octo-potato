import telebot, sqlite3, shelve
import os
import config, dop, files

bot = telebot.TeleBot(config.token)
block_symbols = ['/', '\\', ':', '*', '?', '«', '<', '>', '|', '"']


def global_markup():
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Настройка платёжки')
    user_markup.row('Статистика', 'Рассылка')
    user_markup.row('Остальные настройки')
    return user_markup


def catalog_markup():
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Добавить категорию', 'Удалить категорию')
    user_markup.row('Изменить название категории')
    user_markup.row('Добавить новую позицию в категорию', 'Удалить позицию')
    user_markup.row('Изменить название позиции'), user_markup.row('Переместить позицию в другую категорию')
    user_markup.row('Поменять описание позиции', 'Поменять цену')
    user_markup.row('Выгрузить товар позиции')
    user_markup.row('Вернуться в главное меню')
    return user_markup


def in_adminka(chat_id, message_text, username, name_user):
    global message
    if chat_id in dop.get_adminlist():
        if message_text == 'Вернуться в главное меню' or message_text == '/adm':
            if dop.get_sost(chat_id) is True:
                with shelve.open(files.sost_bd) as bd: del bd[str(chat_id)]
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Настройка платёжки')
            user_markup.row('Статистика', 'Рассылка')
            user_markup.row('Остальные настройки')
            bot.send_message(chat_id, 'Вы вошли в админку бота!\nЧтобы выйти из неё, нажмите /start',
                             reply_markup=user_markup)

        elif message_text == 'Настроить ответы бота':
            if dop.check_message('start') is True:
                start = 'Изменить'
            else:
                start = 'Добавить'
            if dop.check_message('after_buy'):
                after_buy = 'Изменить'
            else:
                after_buy = 'Добавить'
            if dop.check_message('help'):
                help = 'Изменить'
            else:
                help = 'Добавить'
            if dop.check_message('userfalse'):
                userfalse = 'Изменить'
            else:
                userfalse = 'Добавить'
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            user_markup.row(start + ' приветствие пользователя')
            user_markup.row(after_buy + ' сообщение после оплаты товара')
            user_markup.row(help + ' ответ на команду help', userfalse + ' сообщение если нету username')
            # user_markup.row(userfalse + ' сообщение если нету username')
            user_markup.row('Вернуться в главное меню')
            bot.send_message(chat_id,
                             'Выберите, какое сообщение вы хотите изменить.\nПосле выбора, вы получите небольшую инструкцию',
                             reply_markup=user_markup)

        elif ' приветствие пользователя' in message_text or ' сообщение после оплаты товара' in message_text or ' ответ на команду help' in message_text or ' сообщение если нету username' in message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            if ' приветствие пользователя' in message_text:
                message = 'start'
                bot.send_message(chat_id,
                                 'Введите новое привественное сообщение! В тексте вы можете использовать слова `username`  и `name`. Они автоматически заменяться на имя пользователя',
                                 parse_mode='MarkDown', reply_markup=key)
            elif ' сообщение после оплаты товара' in message_text:
                message = 'after_buy'
                bot.send_message(chat_id,
                                 'Введите новое сообщение, которое бот будет слать юзеру после покупки! В тексте вы можете использовать слова `username`  и `name`. Они автоматически заменяться на имя пользователя',
                                 parse_mode='MarkDown', reply_markup=key)
            elif ' ответ на команду help' in message_text:
                bot.send_message(chat_id,
                                 'Введите новое сообщение с помощью! Туда впринципе, можно поместить что угодно! В тексте вы можете использовать слова `username`  и `name`. Они автоматически заменяться на имя пользователя',
                                 parse_mode='MarkDown', reply_markup=key)
                message = 'help'
            elif ' сообщение если нету username' in message_text:
                bot.send_message(chat_id,
                                 'Введите новое сообщение которое будет отправляться если у пользователя нету `username`. В тексте вы можете использовать `uname`. Оно автоматически заменится на имя пользователя',
                                 parse_mode='MarkDown', reply_markup=key)
                message = 'userfalse'
            with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                f.write(message)
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 1

        elif 'Настройка ассортимента' == message_text:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            goodz = 'Созданые товары:\n\n'
            a = 0
            cursor.execute("SELECT name, description, format, minimum, price, stored FROM goods;")
            for name, description, format, minimum, price, stored in cursor.fetchall():
                a += 1
                amount = dop.amount_of_goods(name)
                goodz += '*Имя:* ' + name + '|*Цена:* ' + str(price) + '\n'
            con.close()
            if a == 0:
                goodz = 'Позиций ещё не создано!'
            else:
                pass
            bot.send_message(chat_id, goodz, reply_markup=catalog_markup(), parse_mode='Markdown')
        elif 'Добавить категорию' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id, 'Введите название новой категории', reply_markup=key)
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 23

        elif 'Удалить категорию' == message_text:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT * FROM categories;")
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            a = 0
            for name, id in cursor.fetchall():
                user_markup.row(name)
                a += 1

            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!', reply_markup=global_markup())
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id,
                                 'Какую категорию нужно удалить?',
                                 parse_mode='Markdown', reply_markup=user_markup)
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 24
            con.close()
        elif 'Изменить название категории' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id, 'Выбрано Изменить название категории', reply_markup=key)
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT * FROM categories;")
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            a = 0
            for name, id in cursor.fetchall():
                user_markup.row(name)
                a += 1
            bot.send_message(chat_id, 'Выберите категорию у которой хотите изменить название:',
                             reply_markup=user_markup)
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 26
        elif "Добавить новую позицию в категорию" == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id,
                             'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                             reply_markup=key, parse_mode='Markdown')
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 2

        elif 'В виде файла' == message_text or 'В виде текста' == message_text:
            if 'В виде файла' == message_text:
                with open('data/Temp/' + str(chat_id) + 'good_format.txt', 'w', encoding='utf-8') as f:
                    f.write('file')
                bot.send_message(chat_id,
                                 'Вы выбрали товар в виде файла\nТеперь введите минимальное количество товара, которое можно купить(т.е меньше этого числа купить не получиться)```\n\nВнимание оплата криптовалютой доступна если заказ будет больше 80р```',
                                 parse_mode='Markdown')
            elif 'В виде текста' == message_text:
                with open('data/Temp/' + str(chat_id) + 'good_format.txt', 'w', encoding='utf-8') as f:
                    f.write('text')
                bot.send_message(chat_id,
                                 'Вы выбрали товар в виде текста!\nТеперь введите минимальное количество товара, которое можно купить(т.е меньше этого числа купить не получиться)')
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 4

        elif 'Удалить позицию' == message_text:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            a = 0
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!', reply_markup=catalog_markup())
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id,
                                 'Какую позицию нужно удалить?Будьте осторожны, при удаление, весь загруженый товар удалиться!',
                                 parse_mode='Markdown', reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 6
            con.close()
        elif 'Изменить название позиции' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            a = 0
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!')
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'У какой позиции вы хотите поменять название?', parse_mode='Markdown',
                                 reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 28
            con.close()
        elif 'Переместить позицию в другую категорию' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            a = 0
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!')
            else:

                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'Какую позицию вы хотите переместить?', parse_mode='Markdown',
                                 reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 30
            con.close()
        elif 'Поменять описание позиции' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            a = 0
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!')
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'У какой позиции вы хотите поменять описание?', parse_mode='Markdown',
                                 reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 7
            con.close()

        elif 'Поменять цену' == message_text:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            a = 0
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!', reply_markup=catalog_markup())
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'У какой позиции вы хотите изменить цену?', parse_mode='Markdown',
                                 reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 9
            con.close()
        elif 'Выгрузить товар позиции' == message_text:
            if chat_id == config.admin_id:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("SELECT name, price FROM goods;")
                a = 0
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                for name, price in cursor.fetchall():
                    a += 1
                    user_markup.row(name)
                if a == 0:
                    bot.send_message(chat_id, 'Никаких позиций ещё не создано!')
                else:
                    user_markup.row('Вернуться в главное меню')
                    bot.send_message(chat_id, 'Выгрузка позиции заключается в отправке Вам всех загруженных товаров '
                                              'позиции и удаления их в базе, но при этом позиция остается в каталоге!',
                                     parse_mode='Markdown')
                    bot.send_message(chat_id, 'У какой позиции вы хотите выгрузить товар?', parse_mode='Markdown',
                                     reply_markup=user_markup)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 33
            else:
                bot.send_message(chat_id, 'Вам *запрещен* доступ к выгрузке товара! Вы не основатель бота', parse_mode='Markdown')


        elif 'Загрузка нового товара' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT name, price FROM goods;")
            a = 0
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            for name, price in cursor.fetchall():
                a += 1
                user_markup.row(name)
            if a == 0:
                bot.send_message(chat_id, 'Никаких позиций ещё не создано!')
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'Товары какой позиции вы хотите загрузить?', parse_mode='Markdown',
                                 reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 11
            con.close()

        elif 'Настройка платёжки' == message_text:
            if chat_id == config.admin_id:
                with shelve.open(files.payments_bd) as bd:
                    da_qiwi = bd['qiwi']
                    da_btc = bd['btc']
                if da_qiwi == '❌' and da_btc == '❌':
                    da_all = ''
                elif da_qiwi == '✅' and da_btc == '✅':
                    da_qiwi = ''
                    da_btc = ''
                    da_all = '✅'
                else:
                    da_all = ''

                key = telebot.types.InlineKeyboardMarkup()
                b1 = telebot.types.InlineKeyboardButton(text='Оплата через qiwi ' + da_qiwi,
                                                        callback_data='Оплата через qiwi')
                b2 = telebot.types.InlineKeyboardButton(text='Оплата через cryptonator ' + da_btc,
                                                        callback_data='Оплата через cryptonator')
                b3 = telebot.types.InlineKeyboardButton(text='Оплата и рублями и биткоинами ' + da_all,
                                                        callback_data='Оплата и рублями и биткоинами')
                b4 = telebot.types.InlineKeyboardButton(text='Отключить оплату',
                                                        callback_data='Отключить оплату')
                key.add(b1, b2)
                key.add(b3)
                key.add(b4)
                bot.send_message(chat_id, 'Настройка принятия платежей', reply_markup=key)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Добавить новый киви кошелёк', 'Удалить киви кошелёк', 'Показать добавленые киви кошельки')
                user_markup.row('Добавить/заменить данные от Cryptonator', 'Удалить данные от Cryptonator',
                                'Показать добавленые ключи от Cryptonator')
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, """*QIWI кошельков* вы можете добавить *неограниченое* количество.
    Если используемый кошелёк вдруг заблокируют, вам придёт об этом уведомление, а деньги будут приниматься на другой кошелёк.
    
    Биткоины на биржу можно принимать только на один аккаунт.
    
    Гайды по настройке обоих платёжек есть, их можно получить при добавление соотвествующей платёжки""",
                                 reply_markup=user_markup, parse_mode='Markdown')
            else:
                bot.send_message(chat_id, 'Вам *запрещена* работа с платежками!\nВы не основатель бота',
                                 parse_mode='Markdown', reply_markup=global_markup())

        elif 'Добавить новый киви кошелёк' == message_text and chat_id == config.admin_id:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id,
                             'Отправьте *номер* киви кошелька. Его вводите *без плюса*. Напрмер 7946 или 3756\n\nВалидность номера узнать не получиться, поэтому вводите его без ошибок! В противном случае, деньги будут зачисляться не на ваш кошелёк',
                             reply_markup=key, parse_mode='Markdown')
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 14

        elif 'Удалить киви кошелёк' == message_text and chat_id == config.admin_id:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id, 'Отправьте номер киви кошелька, который нужно удалить из базы данных',
                             reply_markup=key)
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 16

        elif 'Показать добавленые киви кошельки' == message_text and chat_id == config.admin_id:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT number, token FROM qiwi_data;")
            msg = ''
            for number, token in cursor.fetchall():
                msg += '*Номер:* ' + str(number) + '\n*Токен:* ' + str(token) + '\n\n'
            bot.send_message(chat_id, 'Список кошельков в базе:\n' + msg, parse_mode='MarkDown')
            con.close()

        elif 'Добавить/заменить данные от Cryptonator' == message_text and chat_id == config.admin_id:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id,
                             'Введите *Merchant id* от биржи *coinbase*\nИнструкция по получению\nhttps://telegra.ph/Polucheniya-dannyh-ot-Cryptonator-05-22',

                             reply_markup=key, parse_mode='Markdown')
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 17

        elif 'Удалить данные от Cryptonator' == message_text and chat_id == config.admin_id:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT merchant_id, secret FROM cryptonator_data;")
            a = 0
            for i in cursor.fetchall(): a += 1
            if a == 0:
                bot.send_message(chat_id, 'Ключи от биржи не добавлены! Удалять нечего')
            elif a > 0:
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton(text='Удалить', callback_data='Удалить ключи из бд'))
                key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                           callback_data='Вернуться в главное меню админки'))
                bot.send_message(chat_id, 'Подтвердите или отмените удаление', reply_markup=key)
            con.close()

        elif 'Показать добавленые ключи от Cryptonator' == message_text and chat_id == config.admin_id:
            con = sqlite3.connect(files.main_db)
            cursor = con.cursor()
            cursor.execute("SELECT merchant_id, secret FROM cryptonator_data;")
            msg = ''
            for api_key, private_key in cursor.fetchall():
                msg += '*Merchant_id:* ' + str(api_key) + '\n*Secret:* ' + str(private_key)
            con.close()
            bot.send_message(chat_id, 'Список ключей:\n' + msg, parse_mode='Markdown')

        elif 'Статистика' == message_text:
            amount_users = dop.user_loger()  # получение числа юзеров
            profit, buyers = dop.get_profit_statistic()  # получение дохода, получение количества покупателей
            lock = dop.get_amountblock()  # получение количества юзеров заблокировавших бот
            bot.send_message(chat_id, '*Статистика*\n\n*Количество юзеров зашедших в бота:* ' + str(
                amount_users) + '\n*Юзеров, которые заблокировали бота: *' + str(lock) + '\n*Доход с продаж:* ' + str(
                profit) + ' ₽\n*Количество покупателей:* ' + str(buyers), parse_mode='MarkDown')

        elif 'Рассылка' == message_text:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('По всем юзерам', 'Только купившим')
            user_markup.row('Вернуться в главное меню')
            bot.send_message(chat_id, 'Выберите, по какой группе пользователей вы хотите сделать рассылку',
                             reply_markup=user_markup)

        elif 'По всем юзерам' == message_text or 'Только купившим' == message_text:
            amount = ''
            if 'По всем юзерам' == message_text:
                with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                    f.write('all\n')
                amount = dop.user_loger()  # получение числа юзер
            elif 'Только купившим' == message_text:
                with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                    f.write('buyers\n')
                price, amount = dop.get_profit_statistic()  # получение количество покупателей
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id,
                             'По скольким юзерам нужно сделать рассылку? Введите числом. Максимально возможно ' +
                             str(amount))
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 19

        elif 'Остальные настройки' == message_text:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Добавить нового админа', 'Удалить админа')
            user_markup.row('Вернуться в главное меню')
            bot.send_message(chat_id, 'Выберите, что желаете сделать', reply_markup=user_markup)

        elif 'Добавить нового админа' == message_text:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                       callback_data='Вернуться в главное меню админки'))
            bot.send_message(chat_id, 'Введите id нового админа')
            with shelve.open(files.sost_bd) as bd:
                bd[str(chat_id)] = 21

        elif 'Удалить админа' == message_text:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            a = 0
            for admin_id in dop.get_adminlist():
                a += 1
                if int(admin_id) != config.admin_id: user_markup.row(str(admin_id))
            if a == 1:
                bot.send_message(chat_id, 'Вы ещё не добавляли админов!')
            else:
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, 'Выбери id админа, которого нужно удалить', reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 22















        elif dop.get_sost(chat_id) is True:
            with shelve.open(files.sost_bd) as bd:
                sost_num = bd[str(chat_id)]
            if sost_num == 1:
                with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                    what_message = f.read()  # достаётся сообщение, ответ на которое нужно изменить
                if what_message == 'start':
                    bot.send_message(chat_id, 'Добавлено новое привественное сообщение')
                    shelve.open(files.bot_message_bd)['start'] = message_text
                elif what_message == 'after_buy':
                    bot.send_message(chat_id, 'Добавлено новое сообщение после покупки')
                    shelve.open(files.bot_message_bd)['after_buy'] = message_text
                elif what_message == 'help':
                    bot.send_message(chat_id, 'Добавлено новое сообщение помощи')
                    shelve.open(files.bot_message_bd)['help'] = message_text
                elif what_message == 'userfalse':
                    bot.send_message(chat_id, 'Добавлено новое сообщение если нету username!')
                    shelve.open(files.bot_message_bd)['userfalse'] = message_text

                if 'start' in shelve.open(files.bot_message_bd):
                    start = 'Изменить'
                else:
                    start = 'Добавить'
                if 'after_buy' in shelve.open(files.bot_message_bd):
                    after_buy = 'Изменить'
                else:
                    after_buy = 'Добавить'
                if 'help' in shelve.open(files.bot_message_bd):
                    help = 'Изменить'
                else:
                    help = 'Добавить'
                if 'userfalse' in shelve.open(files.bot_message_bd):
                    userfalse = 'Изменить'
                else:
                    userfalse = 'Добавить'
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row(start + ' приветствие пользователя')
                user_markup.row(after_buy + ' сообщение после оплаты товара')
                user_markup.row(help + ' ответ на команду help')
                user_markup.row(userfalse + ' сообщение если нету username')
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, message_text, reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]

            elif sost_num == 2:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute('select exists(select 1 from goods where lower(name)=?)', (message_text.lower(),))
                query = cursor.fetchone()[0]
                if any([i in message_text for i in block_symbols]):
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Вы использовали запрещенные символы, введите название без них:')
                    bot.send_message(chat_id,
                                     'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                     parse_mode='Markdown', reply_markup=key)
                elif query:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Товар с таким названием уже существует')
                    bot.send_message(chat_id,
                                      'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                         parse_mode='Markdown', reply_markup=key)
                elif len(message_text) > 30:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Название слишком длинное, макс длина строки 30 символов, пробелы учитываются!')
                    bot.send_message(chat_id,
                                      'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                         parse_mode='Markdown', reply_markup=key)

                else:
                    with open('data/Temp/' + str(chat_id) + 'good_name.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Введите описание для ' + message_text, reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 3

            elif sost_num == 3:
                with open('data/Temp/' + str(chat_id) + 'good_description.txt', 'w', encoding='utf-8') as f:
                    f.write(message_text)
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('В виде файла', 'В виде текста')
                bot.send_message(chat_id,
                                 'В каком виде будет выдавать товар?\n*В виде файла*? *Например*: zip-архивы(логи), txt-документы(базы)\n\nИли *в виде текст*? *Например:* аккаунты и тд',
                                 reply_markup=user_markup, parse_mode='Markdown')
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]

            elif sost_num == 4:
                try:
                    message = int(message_text)
                    if message >= 0:
                        with open('data/Temp/' + str(chat_id) + 'good_minimum.txt', 'w', encoding='utf-8') as f:
                            f.write(str(message_text))
                        key = telebot.types.InlineKeyboardMarkup()
                        key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                   callback_data='Вернуться в главное меню админки'))
                        bot.send_message(chat_id, 'Минимальное число к покупке - ' + str(
                            message_text) + '\nТеперь введите цену за одну штуку товара в рублях.```\n\nВнимание оплата криптовалютой доступна если заказ будет больше 80р```',
                                         reply_markup=key, parse_mode='Markdown')
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 5
                    else:
                        bot.send_message(chat_id, 'Нельзя выбирать отрицательное число! Введите его заново!')
                except:
                    bot.send_message(chat_id, 'Минимальное количество вводить строго в цифрах! Введите его заново')

            elif sost_num == 5:
                try:
                    price = int(message_text)
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM categories;")
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    a = 0
                    for name, id in cursor.fetchall():
                        user_markup.row(name)
                        a += 1

                    if a == 0:
                        bot.send_message(chat_id, 'Никаких позиций ещё не создано!', reply_markup=global_markup())
                    else:
                        bot.send_message(chat_id,
                                         'В какую категорию хотите добавить?',
                                         parse_mode='Markdown', reply_markup=user_markup)
                    with open('data/Temp/' + str(chat_id) + 'good_price.txt', 'w', encoding='utf-8') as f:
                        f.write(str(message_text))
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 25

                except:
                    bot.send_message(chat_id, 'Цену за штуку вводить строго в цифрах! Введите её заново')

            elif sost_num == 6:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                    f.write(message_text)
                cursor.execute("SELECT description FROM goods WHERE name = " + "'" + message_text + "'")
                for i in cursor.fetchall(): a += 1
                if a == 0:
                    bot.send_message(chat_id,
                                     'Выбранное позиции не обнаружено! Выберите её, нажав на соотвествующую кнопку')
                else:
                    key = telebot.types.ReplyKeyboardMarkup(True, False)
                    key.row('Да', 'Нет')
                    key.row('Вернуться в главное меню')
                    bot.send_message(chat_id, 'Вы точно уверены в своем выборе?\nЭто не обратимый процесс',
                                     parse_mode='Markdown', reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 32
                con.close()

            elif sost_num == 7:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                cursor.execute("SELECT description FROM goods WHERE name = " + "'" + message_text + "';")
                for i in cursor.fetchall(): a += 1

                if a == 0:
                    bot.send_message(chat_id, 'Позиции с таким названием нет!\nВыберите заново!')
                else:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    bot.send_message(chat_id, 'Теперь напишите новое описание:', reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 8
                con.close()

            elif sost_num == 8:
                with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                    name = f.read()
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("UPDATE goods SET description = '" + message_text + "' WHERE name = '" + name + "';")
                con.commit()
                con.close()
                bot.send_message(chat_id, 'Описание успешно изменено!', reply_markup=catalog_markup())
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]

            elif sost_num == 9:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                cursor.execute("SELECT description FROM goods WHERE name = " + "'" + message_text + "';")
                for i in cursor.fetchall(): a += 1
                if a >= 1:
                    with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Теперь напишите новую цену', reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 10
                else:
                    bot.send_message(chat_id, 'Позиции с таким названием  нет!\nВыберите заново!')
                con.close()

            elif sost_num == 10:
                try:
                    message_text = int(message_text)
                    with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                        name = f.read()
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("UPDATE goods SET price = '" + str(message_text) + "' WHERE name = '" + name + "';")
                    con.commit()
                    con.close()
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row('Добавить категорию', 'Удалить категорию')
                    user_markup.row('Добавить новую позицию в категорию', 'Удалить позицию')
                    user_markup.row('Поменять описание позиции', 'Поменять цену')
                    user_markup.row('Вернуться в главное меню')
                    bot.send_message(chat_id, 'Цена успешно изменена!')
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                except:
                    bot.send_message(chat_id, 'Цена должна быть строго числом\nНапишите цену заново!')

            elif sost_num == 11:
                if message_text in dop.get_goods():
                    with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Остановить загрузку',
                                                               callback_data='Остановить загрузку'))
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    type = dop.get_goodformat(message_text)
                    if type == 'file':
                        bot.send_message(chat_id,
                                         'Загружайте файлы в бота!\nКогда все файлы загрузяться, нажмите остановить загрузку!',
                                         reply_markup=key)
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 12
                    elif type == 'text':
                        bot.send_message(chat_id,
                                         'Загружайте нужные данные в текстовом формате!\nКаждая строка = это один товар.\nПосле отправки боту всего текста, нажмите остановить загрузку',
                                         reply_markup=key)
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 13
                else:
                    bot.send_message(chat_id, 'Такой позиции в боте не создано!')

            elif sost_num == 13:
                try:
                    with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                        good_name = f.read()
                    stored = dop.get_stored(good_name)
                    with open(stored, 'a', encoding='utf-8') as f:
                        f.write(message_text + '\n')
                except:
                    pass
            elif sost_num == 14:
                try:
                    message = int(message_text)
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("SELECT number, token FROM qiwi_data WHERE number = " + str(message_text) + ";")
                    if len(cursor.fetchall()) > 0:
                        bot.send_message(chat_id, 'Такой номер уже есть в базе данных!')
                    elif 15 >= len(message_text) >= 10:
                        with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                            f.write(message_text)
                        bot.send_message(chat_id,
                                         'Теперь введите токен\n\n*Гайд по получению токена - *https://telegra.ph/Kak-poluchit-token-ot-kivi-koshelka-08-31',
                                         parse_mode='Markdown')
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 15
                    else:
                        bot.send_message(chat_id, 'Вы ввели неправильный номер!')
                    con.close()
                except:
                    bot.send_message(chat_id,
                                     'В номере не должно быть букв!\n\nОтправьте *номер* киви кошелька. Его вводите *без плюса*. Напрмер 7904 или 3757',
                                     parse_mode='Markdown')

            elif sost_num == 15:
                with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                    phone = f.read()
                if dop.check_qiwi_valid(phone, message_text) is False:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id,
                                     'Введённые данные не валидные! Либо, вы не дали нужных привелегий\n\nВведите номер от киви заново, либо вернитесь в главное меню',
                                     reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 14

                elif dop.check_qiwi_valid(phone, message_text) is True:
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO qiwi_data VALUES(?, ?)", (phone, message_text))
                    con.commit()
                    cursor.close()
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row('Добавить новый киви кошелёк', 'Удалить киви кошелёк',
                                    'Показать добавленые киви кошельки')
                    user_markup.row('Добавить/заменить данные от биржи', 'Удалить данные от биржи',
                                    'Показать добавленые ключи от  биржи')
                    user_markup.row('Вернуться в главное меню')
                    bot.send_message(chat_id,
                                     '*Токен* валидный\nДанные добавлены в базу данных! Деньги будут приходить на номер этого кошелька',
                                     parse_mode='Markdown', reply_markup=user_markup)
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]

            elif sost_num == 16:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("SELECT number, token FROM qiwi_data WHERE number = " + str(message_text) + ";")
                a = 0
                for i in cursor.fetchall(): a += 1
                if a == 0:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Номера `' + message_text + '` не найдено в базе данных!',
                                     reply_markup=key, parse_mode='Markdown')
                elif a > 0:
                    cursor.execute("DELETE FROM qiwi_data WHERE number = '" + str(message_text) + "';")
                    con.commit()
                    bot.send_message(chat_id, 'Киви кошелёк успешно удалён из базы!')
                con.close()

            elif sost_num == 17:
                with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                    f.write(message_text)
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                           callback_data='Вернуться в главное меню админки'))
                bot.send_message(chat_id,
                                 'Введите *Secret*\n\nhttps://prnt.sc/sj50x4 только эти значения вам понадобятся',
                                 reply_markup=key, parse_mode='Markdown')
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 18

            elif sost_num == 18:
                with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                    merchant_id = f.read()
                if dop.check_cryptonator_valid(merchant_id) is True:
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM cryptonator_data")
                    con.commit()
                    cursor.execute("INSERT INTO cryptonator_data VALUES(?, ?)", (merchant_id, message_text))
                    con.commit()
                    con.close()
                    bot.send_message(chat_id, 'Данные *валидные* и добавлены в базу!', parse_mode='Markdown')
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                elif dop.check_cryptonator_valid(merchant_id) is False:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id,
                                     'Данные не валид!\n\nВведите корректный Merchant_id\n\nИнструкция по получению\nhttps://telegra.ph/Polucheniya-dannyh-ot-Cryptonator-05-22',
                                     reply_markup=key, parse_mode='MarkDown')
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 17

            elif sost_num == 19:
                try:
                    if int(message_text) > 0:
                        with open('data/Temp/' + str(chat_id) + '.txt', 'a', encoding='utf-8') as f:
                            f.write(message_text)
                        key = telebot.types.InlineKeyboardMarkup()
                        key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                   callback_data='Вернуться в главное меню админки'))
                        group = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 0)
                        if group == 'all':
                            group = 'по всем'
                        elif group == 'buyers':
                            group = 'по покупателям'
                        bot.send_message(chat_id,
                                         'Вы выбрали рассылку ' + group + '\nПо ' + message_text + ' юзерам\nТеперь введите любой текст рассылки. Он будет разослан ровно в таком же виде, в каком вы его отправите')
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 20
                    elif int(message_text) < 1:
                        bot.send_message(chat_id, 'Для рассылки выбирать строго положительное число! Введите заново')
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 19
                except:
                    bot.send_message(chat_id, 'Количество юзеров для рассылки введите числом заново!')

            elif sost_num == 20:
                group = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 0)
                amount_users = dop.read_my_line('data/lists/chatid_list.txt', 0)
                message_text = dop.rasl(group, amount_users, message_text)  # получаются итоги рассылки

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('По всем юзерам', 'Только купившим')
                user_markup.row('Вернуться в главное меню')
                bot.send_message(chat_id, message_text, reply_markup=user_markup)
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]

            elif sost_num == 21:
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('Добавить нового админа', 'Удалить админа')
                user_markup.row('Вернуться в главное меню')
                if message_text.isdigit():
                    dop.new_admin(message_text)
                    bot.send_message(chat_id, 'Новый админ успешно добавлен', reply_markup=user_markup)
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                else:
                    bot.send_message(chat_id, '**Внимание вводить только числом**\nВведите id админа:',
                                     reply_markup=user_markup, parse_mode='Markdown')

            elif sost_num == 22:
                with open(files.admins_list, encoding='utf-8') as f:
                    if str(message_text) in f.read():
                        dop.del_id(files.admins_list, message_text)
                        bot.send_message(chat_id, 'Админ успешно удалён из списка')
                        with shelve.open(files.sost_bd) as bd:
                            del bd[str(chat_id)]
                    else:
                        bot.send_message(chat_id, 'Такого id в списках админов не обнаружено! Выберите правильный id!')
                        with shelve.open(files.sost_bd) as bd:
                            bd[str(chat_id)] = 22
            elif sost_num == 23:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("INSERT INTO categories VALUES (?, ?)", (message_text, '1'))
                con.commit()
                cursor.close()
                bot.send_message(chat_id, 'Спасибо категория добавлена', global_markup())
            elif sost_num == 24:
                con = sqlite3.connect(files.main_db)
                a = 0
                cursor = con.cursor()
                cursor.execute("SELECT id FROM categories WHERE name = " + "'" + message_text + "'")
                for i in cursor.fetchall(): a += 1
                if a == 0:
                    bot.send_message(chat_id,
                                     'Выбранной категории не обнаружено! Выберите её, нажав на соотвествующую кнопку')
                else:
                    cursor.execute("DELETE FROM categories WHERE name = " + "'" + message_text + "';")
                    con.commit()
                    cursor.close()
                    bot.send_message(chat_id, 'Спасибо категория удалена', reply_markup=global_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                con.close()
            elif sost_num == 25:
                category = message_text
                with open('data/Temp/' + str(chat_id) + 'good_category.txt', 'w', encoding='utf-8') as f:
                    f.write(message_text)
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton(text='Добавить товар в магазин',
                                                           callback_data='Добавить товар в магазин'))
                key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                           callback_data='Вернуться в главное меню админки'))
                with open('data/Temp/' + str(chat_id) + 'good_name.txt', encoding='utf-8') as f:
                    name = f.read()
                with open('data/Temp/' + str(chat_id) + 'good_description.txt', encoding='utf-8') as f:
                    description = f.read()
                with open('data/Temp/' + str(chat_id) + 'good_format.txt', encoding='utf-8') as f:
                    format = f.read()
                with open('data/Temp/' + str(chat_id) + 'good_minimum.txt', encoding='utf-8') as f:
                    minimum = f.read()
                with open('data/Temp/' + str(chat_id) + 'good_price.txt', encoding='utf-8') as f:
                    price = f.read()
                with open('data/Temp/' + str(chat_id) + 'good_category.txt', encoding='utf-8') as f:
                    category = f.read()
                bot.send_message(chat_id,
                                 "Вы решили добавить следущий товар:\n*Название:* " + name + '\n*Описание:* ' + description + '\n*Формат товара:* ' + format + '\n*Минимальная количество к  покупке:* ' + minimum + '\n*Цена за единицу:* ' + price + ' руб' + '\n*Категория*: ' + category,
                                 reply_markup=key, parse_mode='MarkDown')
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]
            elif sost_num == 26:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                cursor.execute("SELECT name FROM categories WHERE name = " + "'" + message_text + "';")
                for i in cursor.fetchall(): a += 1

                if a == 0:
                    bot.send_message(chat_id, 'Категории с таким названием нет!\nВыберите заново!')
                else:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    bot.send_message(chat_id, 'Теперь напишите новое название', reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 27
                con.close()

            elif sost_num == 27:
                with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                    name = f.read()
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("UPDATE categories SET name = '" + message_text + "' WHERE name = '" + name + "';")
                cursor.execute(
                    "UPDATE goods SET categories = '" + message_text + "' WHERE categories = '" + name + "';")
                con.commit()
                con.close()
                bot.send_message(chat_id, 'Название успешно изменено!', reply_markup=catalog_markup())
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]
            elif sost_num == 28:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                cursor.execute("SELECT description FROM goods WHERE name = " + "'" + message_text + "';")
                for i in cursor.fetchall(): a += 1
                if a == 0:
                    bot.send_message(chat_id, 'Позиции с таким названием нет!\nВыберите заново!')
                else:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(message_text)
                    bot.send_message(chat_id, 'Теперь напишите новое название:', reply_markup=key)
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 29
                con.close()

            elif sost_num == 29:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute('select exists(select 1 from goods where lower(name)=?)', (message_text.lower(),))
                query = cursor.fetchone()[0]
                if any([i in message_text for i in block_symbols]):
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                               callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Вы использовали запрещенные символы, введите название без них:')
                    bot.send_message(chat_id,
                                     'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                     parse_mode='Markdown', reply_markup=key)
                elif query:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Товар с таким названием уже существует')
                    bot.send_message(chat_id,
                                      'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                         parse_mode='Markdown', reply_markup=key)
                elif len(message_text) > 30:
                    key = telebot.types.InlineKeyboardMarkup()
                    key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                                callback_data='Вернуться в главное меню админки'))
                    bot.send_message(chat_id, 'Название слишком длинное, макс длина строки 30 символов, пробелы учитываются!')
                    bot.send_message(chat_id,
                                      'Введите название нового товара: \nИзбегайте символов ```/ / \ : * ? " « < > |```\nИзбегайте *эмодзи*\n*Они запрещены в названии файла* ',
                                         parse_mode='Markdown', reply_markup=key)
                else:
                    with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
                        name = f.read()
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("UPDATE goods SET name = '" + message_text + "' WHERE name = '" + name + "';")
                    # new_stored = f'data/goods/{message_text}.txt'
                    cursor.execute("UPDATE goods SET stored = '" + 'data/goods/' + message_text + '.txt' + "' WHERE name = '" + message_text + "';")
                    try:
                        os.rename(f'data/goods/{name}.txt', f'data/goods/{message_text}.txt')
                    except:
                        pass
                    con.commit()
                    con.close()
                    bot.send_message(chat_id, 'Название успешно изменено!', reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                
            elif sost_num == 30:
                f = open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8')
                f.write(message_text)
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                a = 0
                cursor.execute("SELECT name FROM goods WHERE name = " + "'" + message_text + "';")
                for i in cursor.fetchall(): a += 1
                if a == 0:
                    bot.send_message(chat_id, 'Позиции с таким названием нет!\nВыберите заново!')
                else:
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM categories;")
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    a = 0
                    for name, id in cursor.fetchall():
                        user_markup.row(name)
                        a += 1
                    con.close()
                    con = sqlite3.connect(files.main_db)
                    cursor = con.cursor()
                    cursor.execute("SELECT categories from goods WHERE name = " + "'" + message_text + "';")
                    bot.send_message(chat_id, f'В какую категорию вы хотите переместить?\n'
                                              f'На данный момент *{message_text}* в категории {cursor.fetchone()[0]}',
                                     reply_markup=user_markup, parse_mode='Markdown')
                    with shelve.open(files.sost_bd) as bd:
                        bd[str(chat_id)] = 31
                con.close()
            elif sost_num == 31:
                f = open('data/Temp/' + str(chat_id) + '.txt', 'r', encoding='utf-8')
                name = f.read()
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                cursor.execute("UPDATE goods SET categories = '" + message_text + "' WHERE name = '" + name + "';")
                con.commit()
                con.close()
                bot.send_message(chat_id, 'Позиция успешно перемещена!', reply_markup=catalog_markup())
                with shelve.open(files.sost_bd) as bd:
                    del bd[str(chat_id)]
            elif sost_num == 32:
                con = sqlite3.connect(files.main_db)
                cursor = con.cursor()
                f = open('data/Temp/' + str(chat_id) + '.txt', 'r', encoding='utf-8')
                query_for_delete = f.read()
                if message_text == 'Да':
                    try:
                        os.remove(f'data/goods/{query_for_delete}.txt')
                    except:
                        pass
                    cursor.execute("DELETE FROM goods WHERE name = " + "'" + query_for_delete + "';")
                    con.commit()
                    bot.send_message(chat_id, 'Позиция успешно удалена!', reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                elif message_text == 'Нет':
                    bot.send_message(chat_id, 'Вы вошли в админку бота!\nЧтобы выйти из неё, нажмите /start',
                                     reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                elif message_text == 'Вернуться в главное меню':
                    bot.send_message(chat_id, 'Вы вошли в админку бота!\nЧтобы выйти из неё, нажмите /start',
                                     reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
            elif sost_num == 33:
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton(text='Отменить и вернуться в главное меню админки',
                                                           callback_data='Вернуться в главное меню админки'))
                with open('data/Temp/' + str(chat_id) + 'admin.txt', 'w', encoding='utf-8') as f:
                    f.write(message_text)
                bot.send_message(chat_id, f'Какое количество вы хотите выгрузить? Количество товара - ' +
                                 str(dop.amount_of_goods(message_text)), reply_markup=key)
                with shelve.open(files.sost_bd) as bd:
                    bd[str(chat_id)] = 34

            elif sost_num == 34:
                try:
                    text = ''
                    name_good = open('data/Temp/' + str(chat_id) + 'admin.txt', 'r', encoding='utf-8').read()
                    amount = message_text
                    for i in range(int(amount)):
                        if dop.get_goodformat(name_good) == 'file':
                            bot.send_document(chat_id, dop.get_tovar(name_good))
                        elif dop.get_goodformat(str(name_good)) == 'text':
                            text += dop.get_tovar(name_good) + '\n'
                    if dop.get_goodformat(name_good) == 'text':
                        bot.send_message(chat_id, text)
                    bot.send_message(chat_id, 'Товар был успешно выгружен в количестве - ' + amount + '\nОстаток - ' +
                                 str(dop.amount_of_goods(name_good)), reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]
                except Exception as e:
                    bot.send_message(chat_id, 'Ошибка при выгрузке - попробуйте еще раз!\n Код ошибки - ' + str(e), reply_markup=catalog_markup())
                    with shelve.open(files.sost_bd) as bd:
                        del bd[str(chat_id)]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#                                                                                                                 BуB0ор
def ad_inline(callback_data, chat_id, message_id):
    if 'Вернуться в главное меню админки' == callback_data:
        if dop.get_sost(chat_id) is True:
            with shelve.open(files.sost_bd) as bd: del bd[str(chat_id)]
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Настроить ответы бота')
        user_markup.row('Настройка ассортимента', 'Загрузка нового товара')
        user_markup.row('Настройка платёжки')
        user_markup.row('Статистика', 'Рассылка')
        user_markup.row('Остальные настройки')
        bot.delete_message(chat_id, message_id)  # удаляется старое сообщение
        bot.send_message(chat_id, 'Вы вошли в админку бота!\nЧтобы выйти из неё, нажмите /start',
                         reply_markup=user_markup)

    elif callback_data == 'Добавить товар в магазин':
        with open('data/Temp/' + str(chat_id) + 'good_name.txt', encoding='utf-8') as f:
            name = f.read()
        with open('data/Temp/' + str(chat_id) + 'good_description.txt', encoding='utf-8') as f:
            description = f.read()
        with open('data/Temp/' + str(chat_id) + 'good_format.txt', encoding='utf-8') as f:
            format = f.read()
        with open('data/Temp/' + str(chat_id) + 'good_minimum.txt', encoding='utf-8') as f:
            minimum = f.read()
        with open('data/Temp/' + str(chat_id) + 'good_price.txt', encoding='utf-8') as f:
            price = f.read()
        with open('data/Temp/' + str(chat_id) + 'good_category.txt', encoding='utf-8') as f:
            category = f.read()
        con = sqlite3.connect(files.main_db)
        cursor = con.cursor()
        cursor.execute("INSERT INTO goods VALUES(?, ?, ?, ? , ?, ?, ?)",
                       (name, description, format, minimum, price, 'data/goods/' + name + '.txt', category))
        con.commit()
        con.close()
        bot.delete_message(chat_id, message_id)  # удаляется старое сообщение
        bot.send_message(chat_id, 'Товар был успешно добавлен', reply_markup=catalog_markup())

        with open('data/goods/' + name + '.txt', 'w', encoding='utf-8') as f:
            pass  # создаёся файл для товара

    elif callback_data == 'Остановить загрузку':
        good_name = open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8').read()
        bot.delete_message(chat_id, message_id)  # удаляется старое сообщение
        con = sqlite3.connect(files.main_db)
        cursor = con.cursor()
        cursor.execute("SELECT name, price FROM goods;")
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        for name, price in cursor.fetchall():
            user_markup.row(name)
        user_markup.row('Вернуться в главное меню')
        bot.send_message(chat_id,
                         'Товары были успешно загружены! Теперь количество ' + good_name + ' составляет ' + str(
                             dop.amount_of_goods(good_name)) + '\nЧтобы вернуться в главное меню админки нажмите /adm',
                         reply_markup=user_markup)

    elif callback_data == 'Оплата через qiwi' or callback_data == 'Оплата через cryptonator' or callback_data == 'Оплата и рублями и биткоинами' or callback_data == 'Отключить оплату':
        with shelve.open(files.payments_bd) as bd:
            if callback_data == 'Оплата и рублями и биткоинами':
                bd['qiwi'] = '✅'
                bd['btc'] = '✅'
            elif callback_data == 'Оплата через qiwi':
                bd['qiwi'] = '✅'
                bd['btc'] = '❌'
            elif callback_data == 'Оплата через cryptonator':
                bd['qiwi'] = '❌'
                bd['btc'] = '✅'
            elif callback_data == 'Отключить оплату':
                bd['qiwi'] = '❌'
                bd['btc'] = '❌'
            da_qiwi = bd['qiwi']
            da_btc = bd['btc']

            if da_qiwi == '❌' and da_btc == '❌':
                da_qiwi = '❌'
                da_btc = '❌'
                da_all = ''
            elif da_qiwi == '✅' and da_btc == '✅':
                 da_qiwi = ''
                 da_btc = ''
                 da_all = '✅'
            else:
                da_all = ''

        key = telebot.types.InlineKeyboardMarkup()
        b1 = telebot.types.InlineKeyboardButton(text='Оплата через qiwi ' + da_qiwi, callback_data='Оплата через qiwi')
        b2 = telebot.types.InlineKeyboardButton(text='Оплата через cryptonator' + da_btc,
                                                callback_data='Оплата через cryptonator')
        b3 = telebot.types.InlineKeyboardButton(text='Оплата и рублями и биткоинами' + da_all,
                                                callback_data='Оплата и рублями и биткоинами')
        b4 = telebot.types.InlineKeyboardButton(text='Отключить оплату',
                                                callback_data='Отключить оплату')
        key.add(b1, b2)
        key.add(b3)
        key.add(b4)
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Настройте', reply_markup=key)
        except:
            pass

    elif callback_data == 'Удалить ключи из бд':
        con = sqlite3.connect(files.main_db)
        cursor = con.cursor()
        cursor.execute("DELETE FROM cryptonator_data")
        con.commit()
        con.close()
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Ключи успешно удалены из базы данных!')
        except:
            pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~работа с файлами~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#                                                                                                           ВyВо0р
def new_files(document_id, chat_id):
    try:
        with open('data/Temp/' + str(chat_id) + '.txt', encoding='utf-8') as f:
            good_name = f.read()
        stored = dop.get_stored(good_name)
        with open(stored, 'a', encoding='utf-8') as f:
            f.write(document_id + '\n')
    except:
        pass
