"# TelegramPaymentsManager" 

# telegram bot token from @BotFather
bot_token: 94597063:AAED1S0qJN-yorSdXWKegIA9ToknAOtxa8Y # modify this
group_username: <group>
chat_id: <chat id>

# 1. open https://my.telegram.org/ and login with your phone number.
# 2. Click under API Development tools.
# 3. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
# 4. Click on Create application at the end.
# 5. Copy and paste the api id and hash here

api_id: 123456
api_hash: 02cae2c8b4c4a0bb68d101ab2eb8ff24

# payment

blockonomics_key: vxnihOj3wv3S8F8hE2IwTtn87oQWBNos0dcFg255cmA
neo_address: <neo address>

# plans

price_btc:
  1: 0.128
  2: 0.05
  3: 0.10

price_neo:
  1: 0.1282
  2: 0.052
  3: 0.102

name:
  1: 0.128 btc
  2: 0.05 btc
  3: 0.10 btc

# in days
membership_lifespan: 
  1: 1
  2: 10
  3: 100

# message texts
start_messages: |
  Before we begin, let me answer you the most common questions.
  As you might have realized we are one of (if not the) most accurate telegram channels in existence. You are here because you've seen the proof on our free channel or on our website.
  Now, regarding exchanges: it's around the place - you should have account at: Binance, Poloniex, gate io, Huobi among others.
  If you don't have an account, well... go and register, Sherlock!
  How many signals a week? - approx 1-4 - depending on when we have something strong.
  Now, I will ask you a few questions to make sure you choose the right package, ok?


select_plan_message: |
  Select your plan!

select_payment_message: |
  Select payment method

pay_message: |
  Pay {amount} {currency} to the following address:

  <pre>{address}</pre>

  Paste your transaction id here...

welcome: |
  Warm welcome to the community :blush:.

  Keep two things in mind.

  1. The path to 10x ROI is not a straight line. There will be days when we're in the red and there will be days in the green. Brace yourself. This is not a ride for the emotional.

  2. With high quality coins with solid backers ,developers,and premium research/ information from top industry expert's . it's almost certain to deliver high ROI. And since we are at the super early adopter stage, there's a very high certainty of high returns. So we only advise buys on high quality altcoins. You may see other coins doing well. Even if a coin does well, if it's a risky coin, we will not touch it. Grade A coins will always out perform questionable coins over time.

  Any Other query ? 

  I am here to help.

not_done: |
  payment is not done yet, plase send it again later

wrong_amount: |
  wrong amount payed, pay {} BTC

refund_msg: |
  For Refunds Of Additional BTC Contact @me  

expired_msg: |
  Your subscription ahs expired
  
