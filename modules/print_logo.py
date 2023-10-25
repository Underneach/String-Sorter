import colorama
import sys


def Print_Logo(app_version: str):
    print(
        colorama.Fore.LIGHTBLUE_EX +
        colorama.Style.BRIGHT +
        r'''
        
        
        
                 _____  _____  _____     _____  _                              _____               _               
                |  ___||  _  ||  _  |   /  ___|| |        ( )                 /  ___|             | |              
    ____ __  __ |___ \  \ V / | |/' |   \ `--. | |_  _ __  _  _ __    __ _    \ `--.   ___   _ __ | |_   ___  _ __ 
   | '__|\ \/ /     \ \ / _ \ |  /| |    `--. \| __|| '__|| || '_ \  / _` |    `--. \ / _ \ | '__|| __| / _ \| '__|
   | |    >  <  /\__/ /| |_| |\ |_/ /   /\__/ /| |_ | |   | || | | || (_| |   /\__/ /| (_) || |   | |_ |  __/| |   
   |_|   /_/\_\ \____/ \_____/ \___/    \____/  \__||_|   |_||_| |_| \__, |   \____/  \___/ |_|    \__| \___||_|   
                                                                       _/ |                                      
                                                                      |__/       ''' +
        colorama.Fore.LIGHTMAGENTA_EX +
        f'v{app_version} | Python {sys.version.split()[0]}'
        '\n\n\n\n'
    )
