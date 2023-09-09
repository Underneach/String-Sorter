import colorama
import psutil
import sys


def Print_Logo(app_version: str):
    print(f'Python {colorama.Fore.LIGHTCYAN_EX}{sys.version.split(" ")[0]}{colorama.Style.RESET_ALL}  Psutil {colorama.Fore.LIGHTCYAN_EX}{psutil.__version__}{colorama.Style.RESET_ALL}  ')
    print(
        colorama.Fore.LIGHTYELLOW_EX +
        colorama.Style.BRIGHT +
        '''\n\n\n
                 _____  _____  _____     _____  _                              _____               _               
                |  ___||  _  ||  _  |   /  ___|| |        ( )                 /  ___|             | |              
    ____ __  __ |___ \  \ V / | |/' |   \ `--. | |_  _ __  _  _ __    __ _    \ `--.   ___   _ __ | |_   ___  _ __ 
   | '__|\ \/ /     \ \ / _ \ |  /| |    `--. \| __|| '__|| || '_ \  / _` |    `--. \ / _ \ | '__|| __| / _ \| '__|
   | |    >  <  /\__/ /| |_| |\ |_/ /   /\__/ /| |_ | |   | || | | || (_| |   /\__/ /| (_) || |   | |_ |  __/| |   
   |_|   /_/\_\ \____/ \_____/ \___/    \____/  \__||_|   |_||_| |_| \__, |   \____/  \___/ |_|    \__| \___||_|   
                                                                       _/ |                                      
                                                                      |__/                                ''' +
        colorama.Fore.LIGHTMAGENTA_EX +
        f'v{app_version}' +
        '\n\n\n'
    )
