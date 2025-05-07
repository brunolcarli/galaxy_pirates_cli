import getpass
from time import sleep
from random import choice
from src.queries import get_solar_system, get_login, get_register
from tabulate import tabulate
from settings import LOGO_PALETTE, BEELZEWARE_PALETTE, VERSION
import climage


def banner():
    """
    Shows developer banner and game logo on game init
    """
    sleep(1)
    print(climage.convert('static/images/bzw.png', is_unicode=True, palette=choice(BEELZEWARE_PALETTE), **climage.color_to_flags(climage.color_types.color8), width=64))
    sleep(2.5)
    print(climage.convert('static/images/logo.png', is_unicode=True, palette=choice(LOGO_PALETTE), **climage.color_to_flags(climage.color_types.color8), width=64))
    sleep(2.5)

    print(f'Galaxy Pirates version {VERSION} - 2025')

    sleep(1)



def show_solar_system(galaxy_id, solar_system_id, token):
    solar_system = get_solar_system(galaxy_id, solar_system_id, token)['data']['solarSystem']
    headers = ['Planet Position', 'Planet ID', 'Planet Name', 'Planet coordinates', 'Gravity Field']
    rows = []
    for pos, value in enumerate(solar_system.values()):
        position = pos + 1
        coords = f'[{galaxy_id}, {solar_system_id}, {position}]'
        if value is None:
            planet_id = ''
            planet_name = ''
        else:
            planet_id = value['id']
            planet_name = f'{chr(0x1FA90)} ' + value['name']

        rows.append([position, planet_id, planet_name, coords, ''])
    

    print('---------------------------------------------------------------------------------------')
    print('                                  GALAXY OVERVIEW                                      ')
    print('-------------------------------------------------------------------------------------\n')

    print(tabulate(
        [
            ['---', '---', '---', '---', f'{chr(0x1F30C)}', '', '   Galaxies   ', '1 to 9', '', '', f'{chr(0x1F30C)}', '---', '---', '---', '---'],
            ['---', '---', '---', '---', f'{chr(0x2600)}', '', '   Solar Systems   ', '1 to 500', '', '', f'{chr(0x2600)}', '---', '---', '---', '---'],
        ]
    ))

    print(tabulate(rows, headers, tablefmt="double_outline"))
    print('-----------------------------------------------------------------------------------\n')

    options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'explore_galaxy', 'fleet']]
    menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA)]
    print(tabulate(options_menu, menu_headers, tablefmt="simple"))



def login():
    print('Confirm your username and account...\n\n')
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    authentication = get_login(username, password)
    if 'errors' in authentication:
        print(authentication['errors'][0]['message'])
        return False
    
    return authentication['data']['signIn']



def register():
    print('Register a username and password...\n\n')
    username = input('Username: ')
    username = username.strip()
    while not username:
        print('Username cannot be empty')
        username = input('Username: ')
        username = username.strip()

    
    password = getpass.getpass('Password: ')
    password = password.strip()
    while not password:
        print('Password cannot be empty')
        password = getpass.getpass('Password: ')
        password = password.strip()

    planet_name = input("Please give your new planet a name: ")

    if not planet_name.strip():
        planet_name = 'Colony'

    registration = get_register(username, password, planet_name)

    if 'errors' in registration:
        print(registration['errors'][0]['message'])
        return False

    return True


def landpage():
    """
    Initial screen that gives the option to create an account or log in the game
    """
    headers = ['- - - - ', 'GALAXY PIRATES', '- - - -']
    rows = [['Select an option'], ['1  -> Login | '], ['2  -> Register']]

    while True:
        print(tabulate(rows, headers, tablefmt="double_outline"))
        option = input('> ')

        if option.strip() == '1':
            auth = login()
            if auth == False:
                continue
            else:
                return auth
            
        elif option.strip() == '2':
            reg = register()
            if reg == True:
                print('Registration success, please use the login option to start.')
                continue
            else:
                print('Something wrong happened, please try again.')
                continue

        else:            
            print('Please insert 1 for login or 2 for create a account.')
