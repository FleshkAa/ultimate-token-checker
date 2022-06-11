__version__='1.1'
"""
█▀▀ █   █▀▀ █▀▀ █  █ █ █ █▀▀█ 
█▀▀ █   █▀▀ ▀▀█ █▀▀█ █▀▄ █▄▄█ 
▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀  ▀ ▀ ▀ ▀  ▀
    © Copyright 2022

https://discord.com/users/906838008261664790
https://github.com/fleshkaa/
Licensed under the GNU GPLv3
"""
import os
import requests
clear=lambda: os.system('cls') if os.name=='nt' else os.system('clear')

'''
checker_py=requests.get('https://raw.githubusercontent.com/FleshkAa/ultimate-token-checker/main/checker.py').text
requirements_txt=requests.get('https://raw.githubusercontent.com/FleshkAa/ultimate-token-checker/main/requirements.txt').text

if checker_py.split('\n')[0].split('=')[1]!=__version__:
    while True:
        inp=input('The checker has been updated, would you like to automatically update it? (Y/N)')
        if inp.lower()=='y':
           with open(__file__,'w') as f: f.write(checker_py)
           with open('requirements.txt','w') as f: f.write(requirements_txt)
           __import__("sys").exit(input("The checker has been successfully updated! Re-run the file to use it"))
        elif inp.lower()=='n':
            break
        else:
            continue
'''
#raw link didnt updated at this why

try:
    import grequests
    from discord import Permissions as perms
    from colorama import Fore as fore
    from datetime import datetime
    import time
except:
    if os.name=='nt': os.system('py -3 -m pip install -r requirements.txt')
    else: os.system('python3 -m pip install -r requirements.txt')

    import grequests
    import requests
    from discord import Permissions as perms
    from colorama import Fore as fore
    from datetime import datetime
    import time



if os.name=='nt': os.system('title Ultimate Token Checker by FleshkA#9009')
__import__("colorama").init()

userheaders=lambda token: {"Authorization":token,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"}
botheaders=lambda token: {"Authorization": f"Bot {token}"}


def check(token):
    try:
        headers=userheaders(token)
        resp=requests.get('https://discord.com/api/v9/users/@me',headers=headers)
        tokentype='User'
    except Exception as e:
        print(e)
        try:
            headers=botheaders(token)
            resp=requests.get('https://discord.com/api/v9/users/@me',headers=headers)
            tokentype='Bot'
        except:
            return f'{fore.RED}{fore.RED}{resp.status_code} Error |{fore.RESET} Invalid token\n {fore.RESET}'

    guilds=requests.get('https://discord.com/api/v9/users/@me/guilds',headers=headers).json()
    json=resp.json()


    if resp.status_code==401:
        return f'{fore.RED}{resp.status_code} Error |{fore.RESET} Invalid token\n {fore.RESET}'

    elif 'You need to verify your account in order to perform this action.' in str(guilds):
        return f'{fore.RED}{resp.status_code} Error |{fore.RESET} Locked account\n {fore.RESET}'

    if tokentype=='User':
        payments=requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources",headers=headers).json()
        nitro=requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers).json()

        if payments != []:
            valid=len([payment for payment in payments if not payment['invalid']])
            payments=f'This token has {valid} valid payment methods' if valid != 0 else 'This token has no payment sources'
            paymentss=valid != 0
        else:
            payments='This token has no payment sources'
            paymentss=False

        if len(nitro)>0:
            def convert(date):
                date=str(date)
                return {
                        'day': f'{date[8]}{date[9]}',
                        'month': f'{date[5]}{date[6]}',
                        'year': f'{date[0]}{date[1]}{date[2]}{date[3]}'
                        }
            def days(date):
                return int((date['year'])*365)+int((date['month'])*30)+int(date['day'])

            start=convert(nitro[0]["current_period_start"])
            end=convert(nitro[0]["current_period_end"])
            nnitro=f'''
{fore.GREEN}Start date (DD.MM.YYYY): {fore.YELLOW}{start['day']}.{start['month']}.{start['year']}
{fore.GREEN}End date (DD.MM.YYYY): {fore.YELLOW}{end['day']}.{end['month']}.{end['year']}
{fore.GREEN}Days left: {fore.YELLOW}{days(convert(str(datetime.now())))-days(start)}
            '''.strip()
        else:
            nnitro=''

    if json['avatar'] is not None:
        avatar=f"https://cdn.discordapp.com/avatars/{json['id']}/{json['avatar']}.png?size=1024"
        if json['avatar'].startswith('a_'): avatar=f"https://cdn.discordapp.com/avatars/{json['id']}/{json['avatar']}.gif?size=1024"
    else:
        avatar='https://cdn.discordapp.com/embed/avatars/0.png'
    
    if tokentype=='User':
        if paymentss:
            with open('payments.txt','a') as f:
                if token not in open('payments.txt').read(): f.write(f'{token}\n')
        if nitro:
            with open('nitros.txt','a') as f:
                if token not in open('nitros.txt').read(): f.write(f'{token}\n')

        with open('valids.txt','a') as f:
            if token not in open('valids.txt').read(): f.write(f'{token}\n')

    elif tokentype=='Bot':
        with open('bots.txt','a') as f:
            if token not in open('bots.txt').read(): f.write(f'{token}\n')

    creation_date=datetime.utcfromtimestamp(((int(json['id']) >> 22) + 1420070400000) / 1000)

    if tokentype=='User': return f"""
{fore.RED}------------------------------------------------------------
{fore.GREEN}Username: {fore.YELLOW}{json['username']}#{json['discriminator']}
{fore.GREEN}ID: {fore.YELLOW}{json['id']}
{fore.GREEN}Token type: {fore.YELLOW}User
{fore.GREEN}Bio: {fore.YELLOW}{json['bio'] if json['bio'] else None}
{fore.GREEN}Email: {fore.YELLOW}{json['email'] if json['email'] else None}
{fore.GREEN}Phone: {fore.YELLOW}{json['phone'] if json['phone'] else None}
{fore.GREEN}2FA: {fore.YELLOW}{json['mfa_enabled']}
{fore.GREEN}Friends count: {fore.YELLOW}{len(requests.get('https://discord.com/api/v9/users/@me/relationships',headers=userheaders(token)).json())}
{fore.GREEN}Created at (DD.MM.YYYY): {fore.YELLOW}{creation_date.strftime('%d.%m.%Y')} ({(datetime.now()-creation_date).days} days)
{fore.GREEN}Avatar: {fore.CYAN}{avatar} 
{fore.RED}------------------------------------------------------------
{fore.GREEN}Servers count: {fore.YELLOW}{len(guilds)}
{fore.GREEN}With owner permissions: {fore.YELLOW}{len([guild for guild in guilds if guild['owner']==True])}
{fore.GREEN}With administrator permissions: {fore.YELLOW}{len([guild for guild in guilds if perms(int(guild['permissions'])).administrator and not guild['owner']])}
{fore.RED}------------------------------------------------------------
{fore.GREEN}Nitro: {fore.YELLOW}{len(nitro)>0}\n{nnitro}
{fore.RED}------------------------------------------------------------
{fore.GREEN}{payments}\n{fore.RESET}
    """.strip()


    elif tokentype=='Bot': return f"""
{fore.RED}------------------------------------------------------------
{fore.GREEN}Username: {fore.YELLOW}{json['username']}#{json['discriminator']}
{fore.GREEN}ID: {fore.YELLOW}{json['id']}
{fore.GREEN}Token type: {fore.YELLOW}Bot
{fore.GREEN}Verified: {fore.YELLOW}{(json['public_flags'] << 16) > 0}
{fore.GREEN}Bio: {fore.YELLOW}{json['bio'] if json['bio'] else None}
{fore.GREEN}Created at (DD.MM.YYYY): {fore.YELLOW}{creation_date.strftime('%d.%m.%Y')} ({(datetime.now()-creation_date).days} days)
{fore.GREEN}Avatar: {fore.CYAN}{avatar} 
{fore.RED}------------------------------------------------------------
{fore.GREEN}Servers count: {fore.YELLOW}{len(guilds)}
{fore.GREEN}With administrator permissions: {fore.YELLOW}{len([guild for guild in guilds if perms(int(guild['permissions'])).administrator and not guild['owner']])}
{fore.RED}------------------------------------------------------------
{fore.RESET}
    """.strip()


def parse(tokens):
    try:
        tokens=open(tokens,'r').read().strip().split('\n')
    except FileNotFoundError as e:
        return f"{fore.RED} Error | {fore.RESET}No such file or directory: {fore.CYAN}{tokens}{fore.RESET}\n"

    dir_name=f"parsed-tokens\\parsed-{datetime.now().astimezone().strftime('%Y-%m-%d-%H-%M-%S')}"

    if not os.path.exists(dir_name): os.system(f'mkdir {dir_name}')

    valids=open(dir_name + r'\valids.txt','a')
    payments=open(dir_name + r'\payments.txt','a')
    bots=open(dir_name + r'\bots.txt','a')
    nitros=open(dir_name+r'\nitro.txt','a')


    intvalids=0
    intpayments=0
    intinvalids=0
    intbots=0
    intnitro=0

    for token in tokens:
        res=requests.get('https://discord.com/api/v9/users/@me',headers=userheaders(token))
        valid=res.status_code==200
        if 'You need to verify your account in order to perform this action.' in str(requests.get('https://discord.com/api/v9/users/@me/guilds',headers=userheaders(token)).json()): valid=False
        elif 'message' in res.json(): valid=False

        if valid:
            nitro=len(requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions',headers=userheaders(token)).json()) > 0
            payment=requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources',headers=userheaders(token)).json()
            if len(payment)>0: payment=len([payment for paymentt in payment if not payment['invalid']])>0
            else: payment=False

        else:
            res=requests.get('https://discord.com/api/v9/users/@me',headers=botheaders(token))
            bot=res.status_code==200
            if 'message' in res.json(): bot=False

    
        if valid:
            if payment: 
                valids.write(f'{token}\n')
                payments.write(f'{token}\n')
                print(f'{fore.GREEN}[+] {fore.YELLOW}{token} {fore.GREEN} | {res.json()["username"]}#{res.json()["discriminator"]} ({fore.YELLOW}{res.json()["id"]}{fore.GREEN}){fore.CYAN} | Payment found')
                intpayments+=1

            elif nitro:
                valids.write(f'{token}\n')
                nitros.write(f'{token}\n')
                print(f'{fore.GREEN}[+] {fore.YELLOW}{token} {fore.GREEN} | {res.json()["username"]}#{res.json()["discriminator"]} ({fore.YELLOW}{res.json()["id"]}{fore.GREEN}){fore.CYAN} | Nitro found')
                intnitro+=1

            else:
                valids.write(f'{token}\n')
                print(f'{fore.GREEN}[+] {fore.YELLOW}{token}{fore.GREEN}  | {res.json()["username"]}#{res.json()["discriminator"]} ({fore.YELLOW}{res.json()["id"]}{fore.GREEN}){fore.CYAN} | Valid user token')
                intvalids+=1

        elif bot:
            bots.write(f'{token}\n')
            print(f'{fore.GREEN}[+] {fore.YELLOW}{token}{fore.GREEN}  | {res.json()["username"]}#{res.json()["discriminator"]} ({fore.YELLOW}{res.json()["id"]}{fore.GREEN}){fore.CYAN} | Valid bot token')
            intbots+=1

        else:
            print(f'{fore.RED}[-] {fore.YELLOW}{token}{fore.RED} | Invalid token')
            intinvalids+=1


    return f'\n{fore.RED}---------------------------\n{fore.GREEN}All checked: {fore.YELLOW}{intvalids+intpayments+intinvalids+intbots+intnitro}\n{fore.GREEN}Valid: {fore.YELLOW}{intvalids+intpayments+intnitro}\n{fore.GREEN}Bots: {fore.YELLOW}{intbots}\n{fore.GREEN}With payments: {fore.YELLOW}{intpayments}\n{fore.GREEN}With nitro: {fore.YELLOW}{intnitro}\n{fore.GREEN}Invalid: {fore.YELLOW}{intinvalids}\n{fore.MAGENTA}All tokens was saved to {fore.CYAN}{os.getcwd()}\\{dir_name}{fore.MAGENTA} directory\n{fore.RED}---------------------------{fore.RESET}'

def fast_parse(tokens):
    try:
        tokens=open(tokens,'r').read().strip().split('\n')
    except FileNotFoundError as e:
        return f"{fore.RED} Error | {fore.RESET}No such file or directory: {fore.CYAN}{tokens}{fore.RESET}\n"

    dir_name=f"fast-parsed-tokens"
    file_name=r'\parsed-valids-' + datetime.now().astimezone().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'
    if not os.path.exists(dir_name): os.system(f'mkdir {dir_name}')

    valids=open(dir_name + file_name,'a')
    intvalids=0
    intinvalids=0
    position=0

    for res in grequests.map([grequests.get('https://discord.com/api/v9/users/@me',headers={"Authorization": token, "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"}) for token in tokens]):
        position+=1
        if res.status_code==200:
            valids.write(f'{tokens[position-1]}\n')
            print(f'{fore.GREEN}[+] {fore.YELLOW}{tokens[position-1]} | {res.json()["username"]}#{res.json()["discriminator"]} ({fore.YELLOW}{res.json()["id"]}{fore.GREEN}){fore.CYAN} | Valid user token')
            intvalids+=1
        else:
            print(f'{fore.RED}[-] {fore.YELLOW}{tokens[position-1]}{fore.RED} | Invalid user token')
            intinvalids+=1

    return f'\n{fore.RED}---------------------------\n{fore.GREEN}All checked: {fore.YELLOW}{intvalids+intinvalids}\n{fore.GREEN}Valid: {fore.YELLOW}{intvalids}\n{fore.GREEN}Invalid: {fore.YELLOW}{intinvalids}\n{fore.MAGENTA}All tokens was saved to {fore.CYAN}{os.getcwd()}\\{dir_name + file_name}{fore.MAGENTA} file\n{fore.RED}---------------------------{fore.RESET}'





while True:
    print(f'''
{fore.CYAN}
█  █ █   ▀▀█▀▀  ▀  █▀▄▀█ █▀▀█ ▀▀█▀▀ █▀▀  
█  █ █     █    █  █ ▀ █ █▄▄█   █   █▀▀  
 ▀▀▀ ▀▀▀   ▀    ▀  ▀   ▀ ▀  ▀   ▀   ▀▀▀  

▀▀█▀▀ █▀▀█ █ █ █▀▀ █▀▀▄ 
  █   █  █ █▀▄ █▀▀ █  █ 
  ▀   ▀▀▀▀ ▀ ▀ ▀▀▀ ▀  ▀ 

█▀▀ █  █ █▀▀ █▀▀ █ █ █▀▀ █▀▀█ 
█   █▀▀█ █▀▀ █   █▀▄ █▀▀ █▄▄▀ 
▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀ ▀▀
https://github.com/FleshkAa/ultimate-token-checker

{fore.RED}-------------------------------------
{fore.GREEN}1 - {fore.YELLOW}Token check one at a time
{fore.GREEN}2 - {fore.YELLOW}Check all token from .txt file (tokens must be distributed via Enter button on keyboard)
{fore.GREEN}3 - {fore.YELLOW}[BETA] Fast check all tokens from .txt file (cant check to bot,nitro, payment)
{fore.RED}-------------------------------------{fore.RESET}
    '''.strip())
    choice=int(input(f'Choice: '))
    clear()
    print(f'{fore.YELLOW}Enter #quit to return this choice{fore.RESET}')

    while choice==1:
        token=input("Token: ")

        if token=='#quit':
            break

        else:
            print(check(token))

    while choice==2:
        path=input(f'Path to tokens: ')

        if path=='#quit': 
            break

        else:
            print(parse(path))

    while choice==3:
        path=input(f'Path to tokens: ')

        if path=='#quit': 
            break

        else:
            print(fast_parse(path))
