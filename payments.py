import SimpleQIWI, telebot, time, shelve, requests
import dop, config, files
import hashlib
import forex_python.converter

bot = telebot.TeleBot(config.token)
c = forex_python.converter.CurrencyRates()


def creat_bill_qiwi(chat_id, callback_id, message_id, sum, name_good, amount):
    if dop.amount_of_goods(name_good) < int(amount): bot.answer_callback_query(callback_query_id=callback_id,
                                                                                show_alert=True,
                                                                                text='Выберите меньшее число товаров к покупке')
    if dop.payments_checkvkl() is None:
        bot.answer_callback_query(callback_query_id=callback_id, show_alert=True,
                                  text='Недоступна оплата Qiwi!')
    else:
        phone, token = dop.get_qiwidata()
        api = SimpleQIWI.QApi(token=token, phone=phone)
        comm = 'bill|' + dop.generator_pw(10) + '|'
        with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
            f.write(str(phone) + '\n')
            f.write(token + '\n')
            f.write(str(amount) + '\n')
            f.write(str(sum) + '\n')
            f.write(comm)
        key = telebot.types.InlineKeyboardMarkup()
        rurl = 'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D=' + str(phone) + '&amountInteger=' + str(
            sum) + '&amountFraction=0&extra%5B%27comment%27%5D=' + comm + '&currency=643&blocked[0]=account&blocked[1]=sum&blocked[2]=comment'
        url_button = telebot.types.InlineKeyboardButton("Оплатить в браузере", rurl)
        b1 = telebot.types.InlineKeyboardButton(text='Проверить оплату', callback_data='Проверить оплату')
        # b2 = telebot.types.InlineKeyboardButton(text='Обновить(если зависла проверка оплаты)', callback_data='Обновить')
        key.add(b1, url_button)
        # key.add(b2)
        key.add(telebot.types.InlineKeyboardButton(text='❌Отменить заказ', callback_data='Перейти к каталогу товаров'))
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text='Чтобы купить ' + name_good + ' количеством ' + str(
                                      amount) + '\nНадо пополнить qiwi кошелек `' + str(phone) + '` на сумму `' + str(
                                      sum) + '` *₽*\nПри переводе обязательно укажите комментарий\n `' + comm + '`\nБез него платёж не зачислится.' +
                                      '\nВо избежание проблем оплачивайте по ссылке в кнопке',
                                  parse_mode='Markdown', reply_markup=key)
        # bot.send_message(message.chat.id, '`' + comm + '`', parse_mode='Markdown', reply_markup=key)
        # bot.send_message(chat_id, '`' + comm + '`')
        except:
            pass


def check_oplata_qiwi(chat_id, username, callback_id, first_name, message_id):
    with open('data/Temp/' + str(chat_id) + 'good_name.txt', encoding='utf-8') as f:
        name_good = f.read()
    phone = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 0)
    token = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 1)
    amount = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 2)
    price = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 3)
    comm = dop.read_my_line('data/Temp/' + str(chat_id) + '.txt', 4)
    api = SimpleQIWI.QApi(phone=phone, token=token)
    comment = api.bill(int(price), comm, currency=643)
    api.start()
    time.sleep(1)
    try:
        if api.check(comment):
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='Платеж прошел успешно!\nСейчас вы получите товар')
                text = ''
                for i in range(int(amount)):
                    if dop.get_goodformat(name_good) == 'file':
                        bot.send_document(chat_id, dop.get_tovar(name_good))
                    elif dop.get_goodformat(name_good) == 'text':
                        text += dop.get_tovar(name_good) + '\n'
                if dop.get_goodformat(name_good) == 'text':
                    bot.send_message(chat_id, text)
                if dop.check_message('after_buy') is True:
                    with shelve.open(files.bot_message_bd) as bd: after_buy = bd['after_buy']
                    after_buy = after_buy.replace('username', username)
                    after_buy = after_buy.replace('name', first_name)
                    bot.send_message(chat_id, after_buy)
                dop.new_buy(chat_id, username, name_good, amount, price)
                for admin_id in dop.get_adminlist():
                    try:
                        bot.send_message(admin_id, '<b>Юзер</b>\nID: <code>' + str(chat_id)
                                         + '</code>\nUsername: @' + username + '\nКупил <b>' + name_good + '</b>\nНа сумму '
                                         + str(price) + ' р', parse_mode='HTML')
                    except:
                        pass
            except Exception as e:
                try:
                    with open('error_log.txt', 'w', encoding='utf-8') as f:
                        f.write(str(e))
                except:
                    pass
        else:
            bot.answer_callback_query(callback_query_id=callback_id, show_alert=True,
                                      text='Статус - неоплачено! Я жду Вашего платежа')
    except Exception as e:
        try:
            with open('error_log.txt', 'w', encoding='utf-8') as f:
                f.write(str(e))
        except:
            pass
    api.stop()


def creat_bill_btc(chat_id, callback_id, message_id, sum, name_good, amount, firstname, username):
    if dop.amount_of_goods(name_good) < int(amount): bot.answer_callback_query(callback_query_id=callback_id,
                                                                                show_alert=True,
                                                                                text='Выберите меньшее число товаров к покупке')
    if dop.get_cryptonator_data() is None:
        bot.answer_callback_query(callback_query_id=callback_id, show_alert=True,
                                  text='Недоступна оплата криптовалютой!')
    else:
        merchant_id, secret = dop.get_cryptonator_data()
        sum = int(sum)  # прибавляется комиссия в btc
        r = requests.get('https://blockchain.info/tobtc?currency=RUB&value=' + str(sum))
        btc_price = float(r.json())
        price_dollars = c.convert('RUB', 'USD', sum)  # сколько сатох нужно юзеру оплатить
        payload = {f'merchant_id': {merchant_id},
                   'item_name': {name_good},
                   'order_id': chat_id,
                   'invoice_currency': 'usd',
                   'invoice_amount': f'{price_dollars:.2f}',
                   'language': 'en'}
        r = requests.get('https://www.cryptonator.com/api/merchant/v1/startpayment', params=payload)
        with open('data/Temp/' + str(chat_id) + '.txt', 'w', encoding='utf-8') as f:
            f.write(str.replace(r.url, 'https://www.cryptonator.com/merchant/invoice/', '') + '\n')
            f.write(str(amount) + '\n')
            f.write(str(sum) + '\n')
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton(text='Оплатить', url=f'{r.url}', callback_data='Оплатить btc'),
                telebot.types.InlineKeyboardButton(text='Проверить оплату', callback_data='Проверить оплату btc'))
        # b2 = telebot.types.InlineKeyboardButton(text='Обновить(если зависла проверка оплаты)', callback_data='Обновить')
        # key.add(b2)
        key.add(telebot.types.InlineKeyboardButton(text='❌Отменить заказ', callback_data='Перейти к каталогу товаров'))
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text=f'Чтобы купить *' + name_good + '* ' + str(amount) + ' шт совершите платеж\n\n'
                                                                                            '*Не нажимайте* ❌Отменить заказ *если вы оплатили*',
                                  parse_mode='Markdown', reply_markup=key)

        except:
            pass


def check_oplata_btc(chat_id, username, callback_id, first_name, message_id):
    try:
        with open('data/Temp/' + str(chat_id) + 'good_name.txt', encoding='utf-8') as f:
            name_good = f.read()
    except:
        pass
    invoice_id = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 0)
    amount = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 1)
    price = dop.normal_read_line('data/Temp/' + str(chat_id) + '.txt', 2)
    merchant_id, secret = dop.get_cryptonator_data()
    secret_hash = hashlib.sha1(f'{merchant_id}&{invoice_id}&{secret}'.encode('utf-8')).hexdigest()
    r = requests.post('https://www.cryptonator.com/api/merchant/v1/getinvoice', data={'merchant_id': {merchant_id},
                                                                                      'invoice_id': {invoice_id},
                                                                                      'secret_hash': {secret_hash}})
    try:
        if r.json()['status'] == 'paid':
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text='Платеж прошел успешно!\nСейчас вы получите товар')
                text = ''
                for i in range(int(amount)):
                    if dop.get_goodformat(name_good) == 'file':
                        bot.send_document(chat_id, dop.get_tovar(name_good))
                    elif dop.get_goodformat(name_good) == 'text':
                        text += dop.get_tovar(name_good) + '\n'
                if dop.get_goodformat(name_good) == 'text':
                    bot.send_message(chat_id, text)
                if dop.check_message('after_buy') is True:
                    with shelve.open(files.bot_message_bd) as bd: after_buy = bd['after_buy']
                    after_buy = after_buy.replace('username', username)
                    after_buy = after_buy.replace('name', first_name)
                    bot.send_message(chat_id, after_buy)
                dop.new_buy(chat_id, username, name_good, amount, price)
                for admin_id in dop.get_adminlist():
                    try:
                        bot.send_message(admin_id, '<b>Юзер</b>\nID: <code>' + str(chat_id)
                                         + '</code>\nUsername: @' + username + '\nКупил <b>' + name_good + '</b>\nНа сумму '
                                         + str(price) + ' р', parse_mode='HTML')
                    except:
                        pass
            except Exception as e:
                with open('data/error_log' + '.txt', 'w', encoding='utf-8') as f:
                    f.write(str(e) + '\n')  # записывает ошибки

        elif r.json()['status'] == 'confirming':
            bot.answer_callback_query(callback_query_id=callback_id, show_alert=True,
                                      text='Статус - подтверджается платеж! Ожидайте')
        else:
            bot.answer_callback_query(callback_query_id=callback_id, show_alert=True,
                                      text='Статус - неоплачено! Я жду Вашего платежа')
    except:
        pass
