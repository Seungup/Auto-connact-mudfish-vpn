import ctypes
import psutil
from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess
import time
import os
import sys
from multiprocessing import Process
import getpass
import re
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
 
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

def iv():

    return chr(0) * 16

class AESCipher(object):

    def __init__(self, key):
        self.key = key

    def encrypt(self, message):

        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv().encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv().encode("utf8"))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')
    
def mud_check(ps_name):
    state = "VPN" if ps_name == "mudrun.exe" else "League of Legends"
    ps_state = ps_name in (p.name() for p in psutil.process_iter())
    if ps_state == False:
        state = "No"

    else:
        if state == "VPN":
            print()
            print("{} state : Ready".format(state))
            state = "Yes"

    return state

def mud_vpn_start():
    key = 'abcdefghijklmnopqrstuvwxyz123456'
    print()
    print("System : Now take a Mud ID and PW")
    mod = sys.modules[__name__]
    with open('info.txt') as f:
        a = 0
        for line in f:
            setattr(mod, 'info_{}'.format(a), line)
            a += 1
        mud_id = re.sub('###mud_id = ', '', info_0)
        mud_pw = re.sub('###mud_pw = ', '', info_1)
    print()
    print("VPN state : start selenium in background..")
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("window-size={}x{}".format(screen_width, screen_height))
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    print()
    print("VPN state : mud service now login..")
    driver.get('http://127.0.0.1:8282')
    driver.find_element_by_name('username').send_keys(AESCipher(key).decrypt(mud_id))
    driver.find_element_by_name('password').send_keys(AESCipher(key).decrypt(mud_pw))
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div/table/tbody/tr/td/button').click()
    try:
        req = driver.page_source
        soup=BeautifulSoup(req, 'html.parser')
        information_list = soup.select("body > div.mud-body > div > aside > div > div.panel-body > center > a > strong")
        for information in information_list:
            if information.text == "연결하기":
                state = "Connected"

            elif information.text == "연결끊기":
                state = "Shutdown VPN"
            else:
                state = "error"

        driver.find_element_by_xpath('/html/body/div[2]/div/aside/div/div[2]/center/a').click()
        print()
        print("VPN state : {}.".format(state))
        if state == "ShutDown VPN":
            driver.quit()
            exit()
        else:
            driver.quit()
            return state
    except:
        print()
        print("System : Login Failed")
        os.remove(r"info.txt")
        restart()
        exit()

def restart():
    print("Restart")
    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)

    time.sleep(1)
    print("Rescanning")
    os.execvp(executable, args)

def mudstart():
    print("*** START MUD SERVICE ***")
    subprocess.call(["C:\Program Files (x86)\Mudfish Cloud VPN\mudrun.exe"], shell=True)

def main():
    os.system('cls')
    try:
        mod = sys.modules[__name__]
        with open('info.txt') as f:
            a = 0
            for line in f:
                setattr(mod, 'info_{}'.format(a), line)
                a += 1
            mud_id = re.sub('###mud_id = ', '', info_0)
            mud_pw = re.sub('###mud_pw = ', '', info_1)
    except:
        try:
            key = 'abcdefghijklmnopqrstuvwxyz123456'
            mud_id_input = str(input("미꾸라지 VPN 아이디 : "))
            mud_pw_input = getpass.getpass("미꾸라지 VPN 비밀번호 : ")
            info_flie = open("info.txt", "w")
            info_flie.write("""###mud_id = {}
###mud_pw = {}""".format(AESCipher(key).encrypt(mud_id_input),
                                     AESCipher(key).encrypt(mud_pw_input)))
        except:
            key = 'abcdefghijklmnopqrstuvwxyz123456'
            mud_id_input = str(input("미꾸라지 VPN 아이디 : "))
            mud_pw_input = getpass.getpass("미꾸라지 VPN 비밀번호 : ")
            info_flie = open("info.txt", "w")
            info_flie.write("""###mud_id = {}
###mud_pw = {}""".format(AESCipher(key).encrypt(mud_id_input),
                                        AESCipher(key).encrypt(mud_pw_input)))
        info_flie.close()
    if mud_check("mudrun.exe") == "No":
        print("*** NO MUD SERVICE ***")
        print("make a multi process..")
        p1 = Process(target=restart)
        p2 = Process(target=mudstart)
        print("start a multi functions now")
        p1.start()
        p2.start()



    else:
        if mud_vpn_start() == "Connected":
            print()
            print("[JP] League of Legends start")
            subprocess.call(["D:\GAME\League_JP\LeagueClient.exe"], shell=True)
            while True:
                if mud_check(ps_name='LeagueClientUx.exe') == "No":
                    print()
                    print("[JP] League of Legends Client shutdown detected.")
                    print()
                    print("Automatically VPN shutdown now")
                    mud_vpn_start()
                    break
                else:
                    print("wphiu")
                    continue

if __name__ == '__main__':    
    main()




