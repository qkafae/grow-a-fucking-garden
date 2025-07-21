import os, json, time
from colorama import Fore, Style
from src.binaries.DynCache import DynCache

gamedir = os.path.join(os.path.expanduser("~"), ".gafg")
configPath = os.path.join(gamedir, "config.json")

global mode

main_logo = [
    r"   _____                                ______          _    _                _____               _            ",
    r"  / ____|                       /\     |  ____|        | |  (_)              / ____|             | |           ",
    r" | |  __ _ __ _____      __    /  \    | |__ _   _  ___| | ___ _ __   __ _  | |  __  __ _ _ __ __| | ___ _ __  ",
    r" | | |_ | '__/ _ \ \ /\ / /   / /\ \   |  __| | | |/ __| |/ / | '_ \ / _` | | | |_ |/ _` | '__/ _` |/ _ \ '_ \ ",
    r" | |__| | | | (_) \ V  V /   / ____ \  | |  | |_| | (__|   <| | | | | (_| | | |__| | (_| | | | (_| |  __/ | | |",
    r"  \_____|_|  \___/ \_/\_/   /_/    \_\ |_|   \__,_|\___|_|\_\_|_| |_|\__, |  \_____|\__,_|_|  \__,_|\___|_| |_|",
    r"                                                                      __/ |                                    ",
    r"                                                                     |___/                                     "
]

base_profile = {
    "mastery_xp": 0,
    "garden_size": 5,
    "garden": {
        
    },
    "coins": 0,
    "last_shop_refresh": None
}

plants = {
        "wheat": {
            "rarity": "common",
            "display": "Wheat",
            "color": (245, 222, 179),
            "time": 3
        },
        "carrot": {
            "rarity": "common",
            "display": "Carrot",
            "color": (237, 145, 33),
            "time": 5
        },
        "potato": {
            "rarity": "common",
            "display": "Potato",
            "color": (224, 189, 77),
            "time": 5
        }
}

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

def main():
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

    for k, v in plants.items():
        temp.set(k, v)

    print("> Loaded all plants")
    del plants
    time.sleep(.5)

    input(Fore.GREEN + "-- PRESS ANY KEY TO BEGIN --" + Style.RESET_ALL)