# 0 * * * * bash /home/ec2-user/muunilinst-igbc/src/run_bot.sh

# Accessing btc dir
cd /home/ec2-user/muunilinst-igbc/src

# Activating python
python3 btc_inserter.py
python3 btc_courier.py
