import webview
import threading
import time
from pypresence import Presence
from pynput import keyboard
import bs4

def toggle_fullscreen():
    master_window.toggle_fullscreen()


def listener_start():
    with keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+#': toggle_fullscreen}) as h:
        h.join()

#This function isn't used right now, may potentially use it to add a leaderboard of some kind based on username
def user_fetch():
    username = ''
    while True:
        evaluation = master_window.evaluate_js('document.documentElement.outerHTML')
        soup = bs4.BeautifulSoup(evaluation, 'html.parser')
        user = soup.find('div', {'id': 'menu'})
        user = user.find('div', {'class': 'text'})
        user = user.string
        if username == '' and user != None:
            username = user
            break
    return username

def rpc_wpm():
    config = []
    with open('config.txt', 'r') as f:
        for line in f:
            option = line.split('=')[1]
            config.append(option)
    temp_wpm = ''
    user = user_fetch()
    print(user)
    while True:
        time.sleep(0.5)
        evaluation = master_window.evaluate_js('document.documentElement.outerHTML')
        soup=bs4.BeautifulSoup(evaluation, 'html.parser')
        livewpm = soup.find('div', {'id' : 'liveWpm'})
        livewpm = livewpm.string
        wpm = soup.find('div', {'class' : 'bottom'})
        wpm = wpm.string
        if config[0].strip() == 'True':
            if config[1].strip() == 'live':
                RPC.update(state=f"Currently typing at {livewpm} wpm", large_image='monkeytype', small_image='monkeytype',
                           details='Aping out on monkeytype.com Desktop')
            elif config[1].strip() == 'end':
                if wpm != '-':
                    RPC.update(state=f"Just got {wpm} wpm", large_image='monkeytype', small_image='monkeytype',
                       details='Aping out on monkeytype.com Desktop')
            elif config[1].strip() == 'both':
                if wpm != '-' and wpm != temp_wpm:
                    RPC.update(state=f"Just got {wpm} wpm!", large_image='monkeytype', small_image='monkeytype',
                               details='Aping out on monkeytype.com Desktop')
                    temp_wpm = wpm
                    time.sleep(5)
                else:
                    RPC.update(state=f"Currently typing at {livewpm} wpm", large_image='monkeytype',small_image='monkeytype',details='Aping out on monkeytype.com Desktop')


def create_new_window():
    child_window = webview.create_window('monkeytype', background_color='#333333', frameless=True)
    child_window.load_url('https://www.monkeytype.com/')
    master_window.load_url('https://www.monkeytype.com/')
    child_window.hide()
    rpct = threading.Thread(target=rpc_wpm)
    rpct.start()

if __name__ == '__main__':
    try:
        #If you would like to use my already set-up presence then download the built file. Otherwise, you will have to go to Discord applications website
        #create your own, and inside the ID here
        RPC = Presence('')
        RPC.connect()
        RPC.update(state="Just loaded MTDesktop", large_image='monkeytype', small_image='monkeytype',details='Aping out on monkeytype.com Desktop')
    except:
        pass
    t1 = threading.Thread(target=listener_start)
    main_t = threading.Thread(target=create_new_window)
    t1.start()
    main_t.start()
    master_window = webview.create_window('monkeytype', background_color='#333333')
    webview.start()
