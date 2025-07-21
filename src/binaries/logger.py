from colorama import  Fore, Style

def sucess(s):
    print(Fore.GREEN + s + Style.RESET_ALL)

def warn(s):
    print(Fore.YELLOW + s + Style.RESET_ALL)

def error(s):
    print(Fore.RED + s + Style.RESET_ALL)