export VENV=./venv

python3 -m venv $VENV

$VENV/bin/pip install pyyaml
$VENV/bin/pip install python-telegram-bot
$VENV/bin/pip install requests
$VENV/bin/pip install -I telethon==0.19.1.5
$VENV/bin/pip install block-io==1.1.6

chmod +x tgbot.py
chmod +x setup.py

./setup.py
