import telebot, shelve, datetime, sqlite3, SimpleQIWI, random
import files, config
from forex_python.converter import CurrencyRates
import requests

bot = telebot.TeleBot(config.token)
c = CurrencyRates()


def it_first():
    try:
        with open(files.working_log, encoding='utf-8') as f:
            return False
    except:
        return True


def main(chat_id):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Настроить ответы бота')
    user_markup.row('Настройка ассортимента', 'Загрузка нового товара')
    user_markup.row('Настройка платёжки')
    user_markup.row('Статистика', 'Рассылка')
    user_markup.row('Остальные настройки')
    bot.send_message(chat_id, """*Здравствуйте!*
Это первый запуск и вы сейчас находитесь в *админке.*
Чтобы бот был готов *для работы* с клиентами уже в ближайщее время, вам нужно добавить платёжку(или платёжки).
На выбор есть оплата криптовалютой *биткоин* и *рублями* на киви.
И потом загрузить 

На *данный* момент вы находитесь в админке бота. В следущий раз, чтоб в неё попасть нужно будет набрать /adm
Чтобы из неё выйти, нажмите /start
*Полный гайд по настройке бота*(рекомендую ознакомиться) - https://telegra.ph/Polnaya-nastrojka-bota-05-22
""", parse_mode='Markdown', reply_markup=user_markup)

    with shelve.open(files.payments_bd) as bd:
        bd['qiwi'] = '❌'
        bd['btc'] = '❌'

    log('First launch of bot')  # логгируется первый запускget_adminlist
    new_admin(chat_id)


def log(text):
    time = str(datetime.datetime.utcnow())[:22]
    try:
        with open(files.working_log, 'a', encoding='utf-8') as f:
            f.write(time + '    | ' + text + '\n')
    except:
        with open(files.working_log, 'w', encoding='utf-8') as f:
            f.write(time + '    | ' + text + '\n')


def check_message(message):
    with shelve.open(files.bot_message_bd) as bd:
        if message in bd:
            return True
        else:
            return False


def get_adminlist():
    admins_list = []
    with open(files.admins_list, encoding='utf-8') as f:
        for admin_id in f.readlines():admins_list.append(int(admin_id))        
    return admins_list


def user_loger(chat_id=0):
    if chat_id != 0:
        with open(files.users_list, encoding='utf-8') as f:
            if not str(chat_id) in f.read():
                with open(files.users_list, 'a', encoding='utf-8') as f: f.write(str(chat_id) + '\n')
    with open(files.users_list, encoding='utf-8') as f:
        return len(f.readlines())


def get_categories():
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, id FROM categories;")
    categories = []
    for name, id in cursor.fetchall():
        categories.append(name)
    return categories


def get_productcatalog():
    product_list = '*Current catalog:*\n'
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, description, price, stored FROM goods;")
    a = 0
    for name, description, price, stored in cursor.fetchall():
        a += 1
        good_amount = amount_of_goods(name)
        price_dollars = c.convert('RUB', 'USD', price)  # convert('USD', 'INR', 10)
        product_list += name + ' `-`' + '*' + str(
            price) + ' ₽ ' + f' (~{price_dollars:.2f}$)' + '*' + '   (We have - ' + str(good_amount) + ')\n'
    con.close()
    if a == 0:
        return None
    else:
        return product_list


def get_goods():
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, description FROM goods;")
    goods = []
    for name, price in cursor.fetchall(): goods.append(name)
    con.close()
    return goods


def get_categories_catalog(data):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, price, categories FROM goods;")
    goods = []
    prices = []
    stored = []
    for name, price, categories in cursor.fetchall():
        if data == categories:
            goods.append(name)
            prices.append(str(price))
            stored.append(amount_of_goods(name))
    con.close()
    return goods, prices, stored


def get_stored(name_good):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, stored FROM goods WHERE name = '" + name_good + "';")
    for name, stored in cursor.fetchall(): pass
    con.close()
    return stored


def amount_of_goods(name_good):
    stored = get_stored(name_good)
    try:
        with open(stored, encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0


def get_minimum(name_good):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, minimum FROM goods WHERE name = '" + name_good + "';")
    for name, minimum in cursor.fetchall(): pass
    con.close()
    return minimum


def order_sum(name_good, amount):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, price FROM goods WHERE name = '" + name_good + "';")
    for name, price in cursor.fetchall(): pass
    con.close()
    return int(price) * amount


def read_my_line(filename,
                 linenumber):  # первым аргументом передаётся название файла, вторым нужная для чтения строка(нумерация с нуля)
    with open(filename, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == linenumber:
                return line  # передаётся содержимое нужной строки


def normal_read_line(filename, linenumber):
    line = read_my_line(filename, linenumber)
    return line[:len(line) - 1]


def get_qiwidata():
    global phone, t0ken
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT number, token FROM qiwi_data;")
    a = 0
    for number, token in cursor.fetchall():
        if check_qiwi_valid(number, token) is True:
            phone = number
            t0ken = token
            a += 1
        elif check_qiwi_valid(number, token) is False:
            for id in get_adminlist():
                try:
                    bot.send_message(id, 'Забанили qiwi кошелёк 💢' + '\nНомер: ' + str(number) + '\nТокен: ' + token +
                                     '\nДанный кош удалён из базы данных!')
                except:
                    pass
            cursor.execute("DELETE FROM qiwi_data WHERE number = " + "'" + str(number) + "';")
            con.commit()
    con.close()
    if a == 0:
        return None
    else:
        return phone, t0ken


def check_qiwi_valid(phone, token):
    api = SimpleQIWI.QApi(token=token, phone=phone)
    try:
        a = api.balance
        return True
    except:
        return False


def get_sost(chat_id):
    with shelve.open(files.sost_bd) as bd:
        if str(chat_id) in bd: return True


def check_vklpayments(name):
    with shelve.open(files.payments_bd) as bd: return bd[name]


def get_goodformat(name_good):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT format, stored FROM goods WHERE name = '" + name_good + "';")
    for format, stored in cursor.fetchall():
        pass
    return format


def get_cryptonator_data():
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT merchant_id, secret FROM cryptonator_data;")
    a = 0
    for merchant, secret in cursor.fetchall():
        if check_cryptonator_valid(merchant) is True:
            merchant_id = merchant
            secret = secret
            a += 1
            return merchant_id, secret
        elif check_cryptonator_valid(merchant) is False:
            for id in get_adminlist(): bot.send_message(id, 'Данный невалид от cryptonator 💢' + '\nНужно заменить: ' +
                                                        str(
                                                            merchant) + '\nSecret: ' + secret + '\nДанный кош удалён из базы данных!')
            cursor.execute("DELETE FROM cryptonator_data WHERE number = " + "'" + str(merchant) + "';")
            con.commit()
            return None
    con.close()


def check_cryptonator_valid(merchant_id):
    try:
        payload = {f'merchant_id': {merchant_id}, 'item_name': 'test',
                   'invoice_currency': 'rur',
                   'invoice_amount': '500',
                   'language': 'en'}
        r = requests.get('https://www.cryptonator.com/api/merchant/v1/startpayment', params=payload)
        if r.status_code == 200:
            return True
    except:
        return False


def get_profit_statistic():
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT id, price FROM purchases;")
    price_amount = 0
    buyers_amount = 0
    for id, price in cursor.fetchall():
        price_amount += int(price)
        buyers_amount += 1
    return price_amount, buyers_amount


def get_amountblock():
    with open(files.blockusers_list, encoding='utf-8') as f: return len(f.readlines())


def new_blockuser(his_id):
    with open(files.blockusers_list, 'w', encoding='utf-8') as f: return f.write(str(his_id) + '\n')


def rasl(group, amount, text):
    good_send = 0
    lose_send = 0
    i = 0
    if group == 'all':
        try:
            while i < int(amount):
                if good_send + lose_send == user_loger(): break
                try:
                    chat_id = int(normal_read_line(files.users_list, i))
                    try:
                        bot.send_message(chat_id, text, parse_mode='Markdown')
                        good_send += 1
                        i += 1
                    except:
                        i += 1
                        lose_send += 1
                except:
                    pass


        except:
            pass

    elif group == 'buyers':
        con = sqlite3.connect(files.main_db)
        cursor = con.cursor()
        while i < int(amount):
            try:
                cursor.execute("SELECT id, username FROM purchases;")
                chat_id = int(cursor.fetchall()[i][0])
                i += 1
                try:
                    bot.send_message(chat_id, text, parse_mode='Markdown')

                    good_send += 1
                except:
                    lose_send += 1
            except:
                pass
        con.close()

    return 'Сообщение успешно получили ' + str(good_send) + ' юзеров!' + '\n' + str(
        lose_send) + ' пользователей заблокировали бота и попали в список заблокированых пользователей'


def del_id(file, chat_id):
    text = ''
    try:
        with open(file, encoding='utf-8') as f:
            for i in f.readlines():
                i = i[:len(i) - 1]
                if str(chat_id) == i:
                    pass
                else:
                    text += i + '\n'
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
    except:
        pass


def new_admin(his_id):
    with open(files.admins_list, encoding='utf-8') as f:
        if not str(his_id) in f.read():
            with open(files.admins_list, 'a', encoding='utf-8') as f:
                f.write(str(his_id) + '\n')


def get_description(name_good):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("SELECT name, description FROM goods WHERE name = '" + name_good + "';")
    for name, description in cursor.fetchall(): pass
    con.close()
    return description


def payments_checkvkl():
    active_payment = []
    if check_vklpayments('qiwi') == '✅' and get_qiwidata() is not None:
        active_payment.append('qiwi')
    elif check_vklpayments('qiwi') == '✅' and get_qiwidata() is None:
        for id in get_adminlist():
            try:
                bot.send_message(id,
                                 'В базе данных отсутствуют данные от qiwi! Он был автоматически выключен для приёма '
                                 'платежей.')
            except:
                pass
        with shelve.open(files.payments_bd) as bd:
            bd['qiwi'] = '❌'

    if check_vklpayments('btc') == '✅' and get_cryptonator_data() is not None:
        active_payment.append('btc')
    elif check_vklpayments('btc') == '✅' and get_cryptonator_data() is None:
        for id in get_adminlist():
            try:
                bot.send_message(id, 'В базе данных отсутствуют корректные данные от cryptonator! Он был автоматически '
                                     'выключен для приёма платежей.')
            except:
                pass
        with shelve.open(files.payments_bd) as bd:
            bd['btc'] = '❌'

    if len(active_payment) > 0:
        return active_payment
    else:
        return None


def generator_pw(n):  # аргументом количество символов в каждом блоке
    passwd = list('1234567890ABCDEFGHIGKLMNOPQRSTUVYXWZ')  # из этим символов генерируется id
    random.shuffle(passwd)
    pas = ''.join([random.choice(passwd) for x in range(n)])
    pass1 = ''.join([random.choice(passwd) for x in range(n)])
    pass2 = ''.join([random.choice(passwd) for x in range(n)])
    pass3 = ''.join([random.choice(passwd) for x in range(n)])
    pas = pas  # + '-' +  pass1 + '-' + pass2 + '-' + pass3
    return pas  # возращается сгенирированный пароль


def get_tovar(name_good):
    stored = get_stored(name_good)
    with open(stored, encoding='utf-8') as f:
        txt = f.read()
    text = txt.split('\n')[1:]
    d = read_my_line(stored, 0)
    d = d[:len(d) - 1]
    with open(stored, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text))
    return d


def new_buy(his_id, username, name_good, amount, price):
    con = sqlite3.connect(files.main_db)
    cursor = con.cursor()
    cursor.execute("INSERT INTO purchases VALUES(?, ?, ?, ?, ?)", (his_id, username, name_good, amount, price))
    con.commit()
    con.close()


# def new_buyer(his_id, username, payed):
    # con = sqlite3.connect(files.main_db)
    # cursor = con.cursor()
    # a = 0
    # cursor.execute("SELECT id, username FROM buyers WHERE id = '" + str(his_id) + "';")
    # for id, username in cursor.fetchall(): a += 1
    # if a == 0:
    #     cursor.execute("INSERT INTO buyers VALUES(?, ?, ?)", (his_id, username, payed))
    #     con.commit()
    # else:
    #     cursor.execute("SELECT id, payed FROM buyers WHERE id = '" + str(his_id) + "';")
    #     for id, hi_payed in cursor.fetchall():
    #         payed = int(hi_payed) + int(payed)
    #     cursor.execute("UPDATE buyers SET payed = '" + str(payed) + "' WHERE id = '" + str(his_id) + "';")
    #     con.commit()
    # con.close()
