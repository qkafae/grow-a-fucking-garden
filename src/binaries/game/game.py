import os, json
from colorama import Fore, Style
from resources import resource_handler as resources

gamedir = os.path.join(os.path.expanduser("~"), ".gafg")
configPath = os.path.join(gamedir, "config.json")

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

resources = {}

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
    print("> Loading resources")