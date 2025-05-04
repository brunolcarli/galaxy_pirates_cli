from src.queries import get_solar_system
from tabulate import tabulate


def show_solar_system(galaxy_id, solar_system_id):
    solar_system = get_solar_system(galaxy_id, solar_system_id)['data']['solarSystem']
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

    options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'explore_galaxy']]
    menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA)]
    print(tabulate(options_menu, menu_headers, tablefmt="simple"))
    