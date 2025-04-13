import os
import threading
import queue
import time

try:
    from user_agent import generate_user_agent
except ImportError:
    os.system('pip install user_agent')
    from user_agent import generate_user_agent
    
import requests, random
from time import sleep
n = 0
done = 0
bad = 0
blc = 0
err = 0
os.system('cls' if os.name == 'nt' else 'clear')

TK = input('[+] توكن  : ')
ID = input('[+] ايدي : ')
usersx = []
chars = 'abcdefghijklmnopqrstuvwxyz1234567890_'
user_len = int(input("[+] طول اليوزر  : "))
user_count = int(input("[+] عدد اليوزرات الي تريد تفحصها  : "))

for x in range(0, user_count):
    users = ""
    for x in range(0, user_len):
        users_char = random.choice(chars)
        users = users + users_char
    usersx.append(users)
user_queue = queue.Queue()
for user in usersx:
    user_queue.put(user)
def send_telegram_message(text):
    try:
        tele = f'https://api.telegram.org/bot{TK}/sendMessage?chat_id={ID}&text={text}'
        requests.get(tele)
    except:
        pass

def check_user(user):
    global done, bad, blc, err
    url = 'https://accounts.api.playstation.com/api/v1/accounts/onlineIds'
    hed = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language':'en-US,en;q=0.9,ar;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'46',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'accounts.api.playstation.com',
        'Origin':'https://id.sonyentertainmentnetwork.com',
        'Referer':'https://id.sonyentertainmentnetwork.com/',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'cross-site',
        'User-Agent': generate_user_agent()
    }
    dat = {
        'onlineId': user,
        'reserveIfAvailable': False
    }
    try:
        check = requests.post(url,headers=hed,json=dat)
        if check.status_code == 200 or check.status_code == 201:
            done += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'\n[-] متاح : {done}\n[-] غلط : {bad}\n[-] مبند : {blc}\n[-] خطأ : {err}')
            with open('Sony.txt','a') as f:
                f.write(f'{user}\n')
            send_telegram_message(f'❖ Sony User : {user} \n❖ Free By : @vipQvip')
        elif check.status_code == 429 or check.status_code == 406:
            blc += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'\n[-] متاح : {done}\n[-] غلط : {bad}\n[-] مبند : {blc}\n[-] خطأ : {err}')
        else:
            bad += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'\n[-] متاح : {done}\n[-] غلط : {bad}\n[-] مبند : {blc}\n[-] خطأ : {err}')
    except:
        err += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n[-] متاح : {done}\n[-] غلط : {bad}\n[-] مبند : {blc}\n[-] خطأ : {err}')

num_threads = 20 
threads = []

def worker():
    while True:
        try:
            user = user_queue.get(timeout=1)  
            check_user(user)
            user_queue.task_done()
        except queue.Empty:
            break  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  
            pass 
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
user_queue.join()
send_telegram_message('❖ Done Check All Users \n❖ Free By : @vipQvip')
for t in threads:
    t.join()

print("Finished checking usernames.")