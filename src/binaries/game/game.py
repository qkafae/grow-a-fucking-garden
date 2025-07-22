import os, json, time, platform, glob, re
import questionary as que
from colorama import Fore, Style

from src.binaries.DynCache import DynCache
from src.binaries import logger

from resources.garden import *
from resources.logo import *
from resources.plants import *
from resources.profile import *
from resources.shop import *

##########################################################################################################################

gamedir = os.path.join(os.path.expanduser("~"), ".gafg")
configPath = os.path.join(gamedir, "config.json")
profilesPath = os.path.join(gamedir, "profiles")

global mode, sessions

##########################################################################################################################

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def editConfig(k, v):
    cfg = loadConfig()
    cfg[k] = v

    with open(configPath, "w") as f:
        json.dump(cfg, f, indent=4)

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

##########################################################################################################################

def initialize():
    clear()

    global seeds

    for l in main_logo:
        print(Fore.LIGHTGREEN_EX + l + Style.RESET_ALL)

    print("> Starting Grow A Fucking Garden")
    time.sleep(.5)
    print("> Loading resources")
    time.sleep(.5)

    global temp, plants
    if (getConfig("cache")):
        temp = DynCache()
        mode = Fore.GREEN + "Cache" + Style.RESET_ALL
    else:
        temp = DynCache(use_memory = False, temp_dir = os.path.join(gamedir, "temp"))
        mode = Fore.RED + "Disk" + Style.RESET_ALL
    
    print(f"> Current mode: {mode}")
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

def getMenu():
    menu = []
    for i in range(len(getProfile()["garden"])):
        if (getProfile()["garden"][i]["crop"] == None):
            menu.append(f"Empty Slot {i + 1}")
        else:
            menu.append(temp.get(getProfile()["garden"][i]["crop"])["display"])

    menu.append("-------Market-------")
    menu.append("Upgrades")
    menu.append("Shop")
    menu.append("Mastery")
    menu.append("--------Menu--------")
    menu.append("Switch Profiles")
    menu.append("Quit")        
    
    return menu

##########################################################################################################################

def game(session = None):
    clear()
    if (len(getProfile()["garden"]) > getProfile()["garden_size"]):
        tmp = getProfile()
        del tmp["garden"][getProfile()["garden_size"]:]
        temp.set("profile", tmp)

    for i in getMenu():
        print(i)
                