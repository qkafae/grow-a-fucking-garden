import os, json, time, platform, glob, re, time, threading, keyboard
import questionary as que
from colorama import Fore, Style

from src.binaries.DynCache import DynCache
from src.binaries import logger
from src.binaries.buffer import Buffer

from resources.garden import *
from resources.logo import *
from resources.plants import *
from resources.profile import *
from resources.shop import *
from resources.rarity import *
from resources.npc import *

##########################################################################################################################

space = "                   "

gamedir = os.path.join(os.path.expanduser("~"), ".gafg")
configPath = os.path.join(gamedir, "config.json")
profilesPath = os.path.join(gamedir, "profiles")

buffer = Buffer()
inGame = False
maxpos = 0
pos = 0

global mode, sessions

##########################################################################################################################

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def loadConfig():
    with open(configPath, "r") as f:
        return json.load(f)
    
def getConfig(k):
    return loadConfig()[k]

def quit(session = None):
    clear()
    if (temp.key_exists("profile")):
        print("> Saving profile")
        time.sleep(.5)
        profile = temp.get("profile")
        with open(session, "w") as f:
            json.dump(profile, f, indent=4)
        print("> Saved profile")
        temp.clear("profile")
        time.sleep(.5)
        
    print("> Clearing cache")
    temp.clear("plants")
    time.sleep(.5)
    print("> Sucessfully cleared cache")

    input(Fore.RED + "-- Press any key to quit --" + Style.RESET_ALL)
    clear()
    return

def getProfile():
    return temp.get("profile")

def rgb(c, s):
    r, g, b = c
    return f"\033[38;2;{r};{g};{b}m" + s + Style.RESET_ALL

def intToTime(i):
    fmt = []
    hrs = i // 3600
    min = (i % 3600) // 60
    sec = i % 60
    
    if hrs > 0:
        fmt.append(f"{hrs}hr")
        if min > 0 or sec > 0:
            if min > 0:
                fmt.append(f"{min}m")
            if sec > 0:
                fmt.append(f"{sec}s")
    elif min > 0:
        fmt.append(f"{min}m")
        if sec > 0:
            fmt.append(f"{sec}s")
    else:
        fmt.append(f"{sec}s")
    
    return " ".join(fmt)

def getStatus(t):
    t -= time.time()
    t = int(t)
    if (t <= 0):
        return Fore.GREEN + "Done" + Style.RESET_ALL
    else:
        return intToTime(t)

##########################################################################################################################

def initialize():
    clear()

    global seeds, rarity

    for l in main_logo:
        print(Fore.LIGHTGREEN_EX + l + Style.RESET_ALL)

    print(" ")
    print("> Starting Grow A Fucking Garden")
    time.sleep(.5)
    print("> Loading resources")
    time.sleep(.5)

    global temp, plants
    if (getConfig("cache")):
        temp = DynCache()
        mode = Fore.GREEN + "Cache to memory" + Style.RESET_ALL
    else:
        temp = DynCache(use_memory = False, temp_dir = os.path.join(gamedir, "temp"))
        mode = Fore.RED + "Cache to disk disk" + Style.RESET_ALL
    
    print(f"> Current mode: {mode}")
    time.sleep(.5)

    for k,v in rarity.items():
        temp.set(k, v)

    print("> Analysed rarities")
    del rarity
    time.sleep(.5)

    for k, v in seeds.items():
        temp.set(k, v)

    print("> Planted the seeds")
    del seeds
    time.sleep(.5)

    for k, v in plants.items():
        temp.set(k, v)

    print("> Watered the plants")    
    del plants
    time.sleep(.5)

    input(Fore.GREEN + "-- PRESS ANY KEY TO BEGIN --" + Style.RESET_ALL)
    profilesMenu()

##########################################################################################################################

def profilesMenu():
    clear()
    profileOptions = []
    for f in [os.path.basename(f) for f in (glob.glob(os.path.join(profilesPath, "*.json")))]:
        profileOptions.append({
            "name": f.removesuffix(".json"), 
            "value": f
        })
    profileOptions.append({
        "name": "-- New Profile --", 
        "value": "new"
    })
    profileOptions.append({
        "name": "-- Quit --",
        "value": "quit"
    })
    
    profile = que.select(
        "Select a profile:",
        choices=profileOptions,
        use_arrow_keys=True,
        qmark="",
    ).ask()

    match (profile):
        case "quit":
            quit()
        case "new":
            done = False
            print("> Creating new profile")
            while not (done):
                print("Your profile name must match these requirements:")
                print("  - No spaces")
                print("  - Only letters, numbers, underscores (_), hyphens (-)")
                print("  - Less than or equal to 32 charaters")
                name = input("Your new profile name: ")
                clear()
                if not (re.fullmatch(r'^[A-Za-z0-9_-]+$', name)) or (len(name) > 32):
                    logger.error("Invalid name formatting")
                else:
                    done = True
            
            newpath = os.path.join(profilesPath, name + ".json")
            with open(newpath, "w") as f:
                json.dump(base_profile, f, indent=4)
            
            profilesMenu()
        case None:
            return
        case _:
            fix = False
            print("> Loading profile")
            session = os.path.join(profilesPath, profile)
            with open(session, "r") as f:
                loaded = json.load(f)

            for k in base_profile:
                if not (k in loaded):
                    fix = True
                    loaded[k] = base_profile[k]
                elif (type(base_profile[k]) != type(loaded[k])):
                    fix = True
                    loaded[k] = base_profile[k]

            if (fix):
                logger.warn("Profile is outdated or corrupted! Fixing it right now")
            
            temp.set("profile", loaded)
            time.sleep(.5)
            print("> Loaded profile")

            input(Fore.GREEN + "-- Press any key to start the game --" + Style.RESET_ALL)
            game(session)

##########################################################################################################################

up = getConfig("keybinds")["up"]
down = getConfig("keybinds")["down"]
interact = getConfig("keybinds")["interact"]

def inputWorker():
    global inGame, up, down, pos, maxpos
    while (inGame):
        event = keyboard.read_event()
        if (event.event_type == keyboard.KEY_DOWN):
            if (event.name in up):
                pos = max(0, pos - 1)
            elif (event.name in down):
                pos = min(maxpos, pos + 1)
            elif (event.name in interact):
                if (inGarden):
                    if (pos == maxpos):
                        return
                    
                elif (inMarket):
                    if (pos == 0):
                        inMarket = False
                        inGarden = True
                    elif (pos == maxpos):
                        return
                    
            refreshGarden()
        
keystrokeThread = threading.Thread(target=inputWorker)

##########################################################################################################################

def gardenMenu():
    global garden_logo, space
    menu = [
        f"{Fore.YELLOW}[Coins 🪙]{Style.RESET_ALL} {getProfile()["coins"]}",
        space
    ]

    for l in garden_logo:
        menu.append(l)

    menu.append(space)

    for i in range(len(getProfile()["garden"])):
        if (getProfile()["garden"][i]["crop"] == None):
            menu.append(f"Empty Slot {i + 1}")
        else:
            rarity_prefix = rgb(temp.get(temp.get(getProfile()["garden"][i]["crop"])["rarity"])["color"], temp.get(temp.get(getProfile()["garden"][i]["crop"])["rarity"])["abbrv"])
            crop_w_rgb = rgb(temp.get(getProfile()["garden"][i]["crop"])["color"], temp.get(getProfile()["garden"][i]["crop"])["display"])
            menu.append(f"[{i + 1}] [{rarity_prefix}] " + crop_w_rgb + f" ({getStatus(getProfile()["garden"][i]["time_until_growth"])})")

    menu.append(space)
    menu.append(rgb((220,208,192), "🧺 Path to The Market"))

    return menu

def refreshGarden():
    global buffer, pos, maxpos
    menu = gardenMenu()
    maxpos = len(menu) - 1
    menu[pos] += " 👨‍🌾"
    for i in menu:
        buffer.write(i)
    buffer.flush()

##########################################################################################################################

def marketMenu():
    global shop_logo, npcs, space
    menu = [
        Fore.GREEN + "🌱 Path to Your Garden" + Style.RESET_ALL,
        space,
        f"{Fore.YELLOW}[Coins 🪙]{Style.RESET_ALL} {getProfile()["coins"]}",
        space
    ]

def refreshMarket():
    return

##########################################################################################################################


inGarden = True
inMarket = False

def game(session = None):
    global inGarden, inMarket

    clear()
    if (len(getProfile()["garden"]) > getProfile()["garden_size"]):
        tmp = getProfile()
        del tmp["garden"][getProfile()["garden_size"]:]
        temp.set("profile", tmp)

    global inGame
    inGame = True

    keystrokeThread.start()

    while(inGarden):
        refreshGarden()
        time.sleep(1)

    while (inMarket):
        refreshMarket()
        time.sleep(1)
    
                