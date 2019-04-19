import yaml
import logging
from threading import Lock
import datetime
import time
from state import State

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = yaml.load(open('config.yml', 'r'))

# 
# database
# 

import csv


# 
# Database handling
# 

class RUser(object):

    def __init__(self, id, username, plan, addr, txid, amount, state, accepted=False, start_date=None):
        self.inited = False
        self.id = int(id)
        self.username = username
        self.plan = int(plan) if plan != '' else None
        self.txid = txid
        self.addr = addr
        self.amount = float(amount) if amount != '' else None
        self.accepted = accepted == "True" or accepted == True
        self.state = State(int(state))
        self.start_date = start_date
        self.lock = Lock()
        self.inited = True

    def expired(self):
        if self.start_date == None:
            return False
        end_date = self.start_date + datetime.timedelta(days=config['membership_lifespan'][self.plan])
        return datetime.datetime.now() > end_date

    # def __str__(self):
    #     return "RUser({}, {}, {}, {}, {}, {}, {}, {},)".format(self.id, self.name, self.invited_by, self.balance, self._has_joined, self.referrals, self.joined_referrals, self.chat_id)

    # def __repr__(self):
    #     return "RUser({}, {}, {}, {}, {}, {}, {}, {},)".format(self.id, self.name, self.invited_by, self.balance, self._has_joined, self.referrals, self.joined_referrals, self.chat_id)


    # def get_(self):
    #     return self._balance

    # def set_balance(self, value):
    #     self._balance = value
    #     self.save()

    # def save(self):
    #     if self.inited:
    #         save_db()

    # has_joined = property(get_has_joined, set_has_joined)
    # chat_id = property(get_chat_id, set_chat_id)
    # balance = property(get_balance, set_balance)

users = dict()
users_lock = Lock()

def add_user(user):
    users_lock.acquire()
    users[user.id] = user
    users_lock.release()

def save_loop():
    while True:
        time.sleep(5)
        save_db()


def save_db():
    db_file = open('data.csv', 'w')
    fieldnames = ['id', 'username', 'plan', 'addr', 'txid', 'amount', 'accepted', 'state', 'start_date']
    writer = csv.DictWriter(db_file, fieldnames=fieldnames)

    writer.writeheader()

    users_lock.acquire()
    for id in users:
        user = users[id]
        writer.writerow({
            'id': user.id,
            'username': user.username,
            'plan': user.plan,
            'addr': user.addr,
            'txid': user.txid,
            'amount': user.amount,
            'accepted': user.accepted,
            'state': int(user.state),
            'start_date': user.start_date
        })
    
    users_lock.release()

def parse_time(str):
    if str is None or str == '':
        return None
    return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")

def read_data():
    # read raw users
    db_file = open('data.csv', 'r')
    reader = csv.DictReader(db_file)

    for data in reader:
        data['start_date'] = parse_time(data['start_date'])
        users[int(data['id'])] = RUser(**data)
  
    logging.info("database successfully loaded")
    
read_data()
