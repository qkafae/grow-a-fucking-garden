import argparse as ap
import sys, json, os
from colorama import Fore, Style

from src.binaries.game import game
from src.binaries import logger
from resources.garden import *
from resources.logo import *
from resources.plants import *
from resources.profile import *
from resources.shop import *

script_version = {
    "name": "Grow A Fucking Garden [CLI]",
    "version": "0.1.0 (Alpha)",
    "description": "Grow A Garden but it's a CLI",
    "author": "kafae"
}

base_config = {
    "cache": True, # or False
    "position": "centered", # or "standard"
    "keybinds": {
        "up": [
            "w",
            "up"
        ],
        "down": [
            "s",
            "down"
        ],
        "interact": [
            "e"
        ]
    }
}

global config
config = {}

gamedir = os.path.join(os.path.expanduser("~"), ".gafg")
configPath = os.path.join(gamedir, "config.json")

def editConfig(k, v):
    cfg = loadConfig()
    cfg[k] = v

    with open(configPath, "w") as f:
        json.dump(cfg, f, indent=4)

def loadConfig():
    with open(configPath, "r") as f:
        return json.load(f)

def quickStart():
    upd = False
    if not (os.path.isdir(gamedir)):
        os.makedirs(gamedir)
        with open(configPath, "w") as f:
            json.dump(base_config, f, indent=4)
        logger.sucess("Created necessary game files")
    else:
        if not (os.path.isfile(configPath)):
            with open(configPath, "w") as f:
                json.dump(base_config, f, indent=4)
            upd = True
        elif not (os.path.isdir(os.path.join(gamedir, "profiles"))):
            os.makedirs(os.path.join(gamedir, "profiles"))
            upd = True
        elif not (os.path.isdir(os.path.join(gamedir, "temp"))):
            os.makedirs(os.path.join(gamedir, "temp"))
            upd = True
        
        if (upd):
            logger.sucess("Updated/Created necessary game files")
        else:
            logger.warn("No updates were made to game files")



def showVersion():
    for k in script_version:
        print(Fore.GREEN + f"[{k}]" + Style.RESET_ALL + f": {script_version[k]}" )                

def main():
    parser = ap.ArgumentParser(description="Grow a fucking garden, also in CLI")
    parser.add_argument(
        "--quickstart",
        action="store_true",
        help="Setup the necessary files"
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Launch the game"
    )
    parser.add_argument(
        "--version", 
        action="store_true",
        help="Check the version"
        )
    parser.add_argument(
        "--enablecache",
        action="store_true",
        help="Enable caching of game files"
    )
    parser.add_argument(
        "--disablecache",
        action="store_true",
        help="Disable caching of game files"
    )
    parser.add_argument(
        "--standardui",
        action="store_true",
        help="Set the game ui to the standard (top left corner) position on screen"
    )
    parser.add_argument(
        "--centeredui",
        action="store_true",
        help="Set the game ui to a centered position on screen"
    )

    args = parser.parse_args()

    if (args.version):
        showVersion()
    elif (args.quickstart):
        quickStart()
    elif (args.launch):
        if (os.path.isdir(gamedir) and os.path.isfile(configPath) and os.path.isdir(os.path.join(gamedir, "profiles")) and os.path.isdir(os.path.join(gamedir, "temp"))):
            game.initialize()
        else:
            logger.error("Game files not found or is corrupted! Please run --quickstart")
    elif (args.enablecache):
        if not (os.path.isfile(configPath)):
            logger.error("Config file not found or is corrupted! Please run --quickstart")
            return
        editConfig("cache", True)
        logger.sucess("Sucessfully enabled caching")
    elif (args.disablecache):
        if not (os.path.isfile(configPath)):
            logger.error("Config file not found or is corrupted! Please run --quickstart")
            return
        editConfig("cache", False)
        logger.sucess("Sucessfully disabled caching")
    else:
        parser.print_help()