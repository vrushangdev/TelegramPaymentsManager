#!./env/bin/python
# -*- coding: utf-8 -*-
 
from telegram.ext import *
from telegram import *
import telegram
import logging
import json
import _thread
import time
import copy
import requests
import uuid
import urllib
import data
import yaml
import _thread
from enum import IntEnum
import datetime
import time
from state import State
from data import RUser
import invite_username

config = yaml.load(open('config.yml', 'r'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot: Bot = None

# 
# 
# 

def get_address():
    url = 'https://www.blockonomics.co/api/new_address';
    headers = {'Authorization': "Bearer " + config['blockonomics_key']}
    r = requests.post(url, headers=headers)
    return r.json()['address']

def check_btc_tx(tx, addr, amount):
    url = 'https://blockchain.info/rawtx/{}'.format(tx)
    r = requests.get(url)
    if r.content == b'Transaction not found':
        return False, False, False
    else:
        json = r.json()
        for out in json['out']:
            if out['addr'] == addr:
                v = out['value'] / 10**8
                mp = amount
                mpa = mp - 0.02 * mp
                mpb = mp + 0.02 * mp
                ok = v > mpa and v < mpb
                if ok:
                    return True, True, True
                else:
                    return True, True, v
        return True, False, False


def check_neo_tx(tx, addr, amount):
    return True, True, True
    url = 'https://neoscan.io/api/main_net/v1/get_transaction/{}'.format(tx)
    r = requests.get(url)
    print(r.json())
    return 

    if r.content == b'"Internal server error"':
        return False, False, False
    else:
        json = r.json()
        for out in json['vouts']:
            if out['address_hash'] == addr:
                v = out['value'] 
                mp = amount
                mpa = mp - 0.02 * mp
                mpb = mp + 0.02 * mp
                ok = v > mpa and v < mpb
                if ok:
                    return True, True, True
                else:
                    return True, True, v
        return True, False, False

def check_if_in_group(user_id):
    try:
        ans = bot.get_chat_member(chat_id="@{}".format(config['group_username']), user_id=user_id)
        return ans['status'] != 'left'
    except:
        return False

# 
# STATES
# 

class StateFilter(BaseFilter):
    def __init__(self, state):
        self.state = state

    def filter(self, message: Message):
        user = message.from_user.id
        return user in data.users and data.users[user].state == self.state

#  
# COMMANDS
# 

@run_async
def start(bot: Bot, update: Update):
    user = update.message.from_user

    if user.username is None:
        update.message.reply_text("Please set up a username and re-run /start to use this bot")
        return

    if user.id not in data.users:
        data.add_user(RUser(user.id, user.username, '', None, None, '', State.START))
    else:
        data.users[user.id].state = State.START

    update.message.reply_text(config['start_messages'], reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("Got it!", callback_data="gotit"),
    ]]))

@run_async
def cancel(bot: Bot, update: Update):
    user = data.users[update.message.from_user.id]
    user.addr = None
    user.plan = None
    user.txid = None
    user.accepted = False
    state = State.CANCELED

    update.message.reply_text("Canceled!")
    

@run_async
def getchatid(bot: Bot, update: Update):
    print(update.message.chat.id)

# 
# CALLBACK QUERIES
# 

@run_async
def select_plan(bot: Bot, update: Update):
    id = update.callback_query.from_user.id
    message = update.callback_query.message
    data.users[id].state = State.SELECT_PLAN

    bot.edit_message_text(chat_id=message.chat_id,
                          message_id=message.message_id,
                          text=config['select_plan_message'],
                          reply_markup=InlineKeyboardMarkup([
            [ InlineKeyboardButton(config['name'][i], callback_data="plan:{}".format(i)) ] for i in config['name']
        ]))

@run_async
def select_payment(bot: Bot, update: Update):
    id = update.callback_query.from_user.id
    message = update.callback_query.message

    # set plan
    d = update.callback_query.data
    plan = int(d.split(':')[1])
    data.users[id].plan = plan
    
    bot.edit_message_text(chat_id=message.chat_id,
                          message_id=message.message_id,
                          text=config['select_payment_message'],
                          parse_mode="HTML",
                          reply_markup=InlineKeyboardMarkup([
                              [ InlineKeyboardButton("bitcoin", callback_data="payment:btc") ],
                              [ InlineKeyboardButton("NEO", callback_data="payment:neo") ]
        ]))

@run_async
def pay(bot: Bot, update: Update):
    id = update.callback_query.from_user.id
    message = update.callback_query.message
    d = update.callback_query.data
    payment_method = d.split(':')[1]
    
    user = data.users[id]
    if payment_method == 'btc':
        addr = get_address()
        user.addr = addr
        user.amount = config['price_btc'][user.plan]
        user.state = State.PAY_BTC
    elif payment_method == 'neo':
        addr = config['neo_address']
        user.addr = addr
        user.amount = config['price_neo'][user.plan]
        user.state = State.PAY_NEO

    bot.edit_message_text(chat_id=message.chat_id,
                        message_id=message.message_id,
                        text=config['pay_message'].format(amount=user.amount, address=addr, currency=payment_method),
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup([[]]))

@run_async
def verify_pay(bot: Bot, update: Update):
    user = data.users[update.message.from_user.id]
    user.txid = update.message.text

    if user.state == State.PAY_BTC:
        exists, recipient, amount = check_btc_tx(user.txid, user.addr, user.amount)
    else:
        exists, recipient, amount = check_neo_tx(user.txid, user.addr, user.amount)

    if not exists:
        update.message.reply_text(config['not_done'])
    else:
        if not recipient:
            update.message.reply_text("wrong address")
        else:
            if amount == True or user.amount - amount < 0:
                user.accepted = True
                user.state = State.ACCEPTED
                user.start_date = datetime.datetime.now()
                update.message.reply_text(config['welcome'])
                invite_username.invite(user.username)
                print("@{} has paid".format(user.username))
                if user.amount - amount < 0:
                    user.amount = user.amount - amount
                    bot.send_message(chat_id=user.id,
                                    text=config['refund_msg'].format(amount=user.amount, address=user.addr),
                                    parse_mode="HTML",
                                    reply_markup=InlineKeyboardMarkup([[]]))
            else:
                user.amount = user.amount - amount
                update.message.reply_text(config['wrong_amount'].format(user.amount))
                addr = get_address()
                user.addr = addr
                bot.send_message(chat_id=user.id,
                                text=config['pay_message'].format(amount=user.amount, address=addr),
                                parse_mode="HTML",
                                reply_markup=InlineKeyboardMarkup([[]]))

# 
# MAIN FUNCTIONS
# 

def checker():
    # users_lock.acquire()
    for user in data.users.values():
        if user.expired() and check_if_in_group(user.id):
            logging.info("Kick @{} ({})".format(user.username, user.id))
            bot.send_message(chat_id=user.id, text=config['expired_msg'])
            bot.kick_chat_member(config['chat_id'], user.id)
        
    # users_lock.release()

def checker_loop():
    while True:
        try:
            checker()
        except:
            pass
        time.sleep(180)

def init_bot():
    global bot

    updater = Updater(config["bot_token"])
    bot = updater.bot

    # updater.dispatcher.add_handler(MessageHandler(MenuFilter(0) & Filters.private, help))


    updater.dispatcher.add_handler(CallbackQueryHandler(select_plan, pattern="gotit"))
    updater.dispatcher.add_handler(CallbackQueryHandler(select_payment, pattern=r"plan:(.*)"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern=r"payment:(.*)"))


    updater.dispatcher.add_handler(CommandHandler('start', start,
                                                  pass_args = False,
                                                  filters=Filters.private))

    updater.dispatcher.add_handler(CommandHandler('cancel', cancel,
                                                  pass_args = False,
                                                  filters=Filters.private))

    updater.dispatcher.add_handler(CommandHandler('getchatid', getchatid))
                                                  
    updater.dispatcher.add_handler(MessageHandler(StateFilter(State.CANCELED), start))

    updater.dispatcher.add_handler(MessageHandler(StateFilter(State.PAY_BTC), verify_pay))
    updater.dispatcher.add_handler(MessageHandler(StateFilter(State.PAY_NEO), verify_pay))
    updater.dispatcher.add_handler(MessageHandler(StateFilter(State.START), start))


    logging.info("Telegram Bot successfully started")

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # for user in data.users.values():
    #     user.accepted = True
    #     user.state = State.ACCEPTED
    #     user.start_date = datetime.datetime.now()

    _thread.start_new_thread(data.save_loop, ())
    _thread.start_new_thread(checker_loop, ())
    init_bot()
