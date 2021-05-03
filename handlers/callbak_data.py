from aiogram import types
from misc import dp, bot
from .sqlit import proverka_channel,cheak_partner_channels


name_channel_1 = 'nikolacinema'
name_channel_2 = 'filmsmarket'
name_channel_3 = 'Alitopprodaj'


@dp.callback_query_handler(text_startswith='start_watch')  # Нажал кнопку Начать смотреть
async def start_watch(call: types.callback_query):
    name_channel = call.data[12:]
    channel_teacher = cheak_partner_channels(name_channel) # Проверка на наличие учителя 0 - если нету учителя
    if channel_teacher == 0:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
        markup.add(bat_a)

        await bot.send_message(call.message.chat.id, '❌ ДОСТУП ЗАКРЫТ ❌\n\n '
                                                         '👉Для доступа к приватному каналу нужно быть подписчиком <b>Кино-каналов.</b>\n\n'
                                                         'Подпишись на <b>каналы</b> ниже 👇 и нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                         f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                         f'<b>Канал 2</b> - https://t.me/{name_channel_2}\n'
                                                         f'<b>Канал 3</b> - https://t.me/{name_channel_3}', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
    else:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'theck{name_channel}kod1{channel_teacher}')
        markup.add(bat_a)
        await bot.send_message(call.message.chat.id, '❌ ДОСТУП ЗАКРЫТ ❌\n\n '
                                                     '👉Для доступа к приватному каналу нужно быть подписчиком <b>Кино-каналов.</b>\n\n'
                                                     'Подпишись на <b>каналы</b> ниже 👇 и нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                     f'<b>Канал 2</b> - https://t.me/{channel_teacher}\n'
                                                     f'<b>Канал 3</b> - https://t.me/{name_channel_3}',
                               parse_mode='html', reply_markup=markup, disable_web_page_preview=True)





@dp.callback_query_handler(text_startswith='check')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, '⏳ Ожидайте. Идёт проверка подписки.')
    name_channel = call.data[5:]

    proverka1 = (await bot.get_chat_member(chat_id=f'@{name_channel_1}', user_id=call.message.chat.id)).status
    proverka2 = (await bot.get_chat_member(chat_id=f'@{name_channel_2}', user_id=call.message.chat.id)).status
    proverka3 = (await bot.get_chat_member(chat_id=f'@{name_channel_3}', user_id=call.message.chat.id)).status

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
    markup.add(bat_a)

    if proverka1 == 'creator' or proverka2 == 'creator' or proverka3 == 'creator' or (proverka1 == 'member'  and proverka2 == 'member' and proverka3 == 'member'): #Человек прошел все 3 проверки
        if name_channel == '':
            ######  Человек перещел без реферальной ссылке    #####
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/nikolacinema')  # Cсылка на приват канал # ВАЖНО!!!!!
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',parse_mode='html', reply_markup=markup_2)


            ###########   Человек перешел по реферальной ссылке    ##########

        else:
            status = proverka_channel(name_channel) ## Возвращает 1, если телеграмм канал проверен. 0 - Если нет

            if status == 0:
                markup_2 = types.InlineKeyboardMarkup()
                bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                                   url=f'https://t.me/nikolacinema')  # ВАЖНО!!!!!
                markup_2.add(bat_b)
                await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                             'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                       parse_mode='html', reply_markup=markup_2)
            else:
                markup_2 = types.InlineKeyboardMarkup()
                bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤', url=f'https://t.me/{name_channel}') # Cсылка на приват канал
                markup_2.add(bat_b)
                await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                             'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',parse_mode='html',reply_markup=markup_2)



    else:
        await bot.send_message(call.message.chat.id, '❌Вы не подписались на каналы ниже\n\n'
                                                     'Проверьте еще раз подписку на всех каналах. И нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                     f'<b>Канал 2</b> - https://t.me/{name_channel_2}\n'
                                                     f'<b>Канал 3</b> - https://t.me/{name_channel_3}\n', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)

@dp.callback_query_handler(text_startswith='theck')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check_teacher(call: types.callback_query):
    await bot.send_message(call.message.chat.id, '⏳ Ожидайте. Идёт проверка подписки.')
    #p10 kod1 t3
    channel = call.data[5:]
    channel = channel.split('kod1')

    channel_people =channel[0] # канал ученика
    channel_teacher = channel[1] # канал учителя


    proverka1 = (await bot.get_chat_member(chat_id=f'@{name_channel_1}', user_id=call.message.chat.id)).status
    proverka2 = (await bot.get_chat_member(chat_id=f'@{channel_teacher}', user_id=call.message.chat.id)).status
    proverka3 = (await bot.get_chat_member(chat_id=f'@{name_channel_3}', user_id=call.message.chat.id)).status



    if proverka1 == 'creator' or proverka2 == 'creator' or proverka3 == 'creator' or (proverka1 == 'member' and proverka2 == 'member' and proverka3 == 'member'):  # Человек прошел все 3 проверки
        status = proverka_channel(channel_people)  ## Возвращает 1, если телеграмм канал проверен. 0 - Если нет
        if status == 0:
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/nikolacinema')  # ВАЖНО!!!!!
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                   parse_mode='html', reply_markup=markup_2)
        else:
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/{channel_people}')  # Cсылка на приват канал
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                   parse_mode='html', reply_markup=markup_2)
    else: #Не прошел проверку
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤',
                                           callback_data=f'theck{channel_people}kod1{channel_teacher}')
        markup.add(bat_a)
        await bot.send_message(call.message.chat.id, '❌Вы не подписались на каналы ниже\n\n'
                                                     'Проверьте еще раз подписку на всех каналах. И нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                     f'<b>Канал 2</b> - https://t.me/{channel_teacher}\n'
                                                     f'<b>Канал 3</b> - https://t.me/{name_channel_3}\n',
                               parse_mode='html', reply_markup=markup, disable_web_page_preview=True)