import cmd
from src.queries import get_solar_system, get_planet
from tabulate import tabulate
import climage




class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    username = input('username: ')
    print('----------------------------------------------------------')
    print(f'Hello {username}  | {chr(0x1F310)} Main Pannel           ') 
    print('----------------------------------------------------------')

    planets = (
        ['COORD', [9, 102, 8]],
        ['COORD', [7, 10, 2]]
    )
    g,ss, p = planets[0][1]
    current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

    print('----------------------------------------------------------\n')
    print(f'                 PLANET OVERVIEW     [{g}, {ss}, {p}]                      ')
    print('----------------------------------------------------------\n')

    output = climage.convert('planet3.png', is_16color=False, palette='solarized', width=24, is_8color=True, is_256color=False)
    buildings = f'{chr(0x1F517)} Steel Mine Lv: {current_planet["steelMineLv"]}\n\n{chr(0x1F4A7)} Water Farm Lv: {current_planet["waterFarmLv"]}\n\n{chr(0x1F4B0)} Gold Mine Lv: {current_planet["goldMineLv"]}\n\n'
    infrastructure = f'{chr(0x2694)} Military Power: {current_planet["militaryPower"]}\n\n{chr(0x1F6E1)} Shield Power: {current_planet["shieldPower"]}\n\n{chr(0x1F680)} Engine power: {current_planet["enginePower"]}\n\n'
    overview = [
        [current_planet['steel'], current_planet['water'], current_planet['gold'], current_planet['temperature'], ''],
        [f'Name: {current_planet["name"]}', f'Size: ({current_planet["fieldsUsed"]}/{current_planet["size"]})', f'Coords: [{g}, {ss}, {p}]', f'ID: {current_planet["id"]}', ''],
        [buildings, infrastructure, f'Total ships landed:\n\n{chr(0x1F6E9)}: {len(current_planet["fleet"])} ships' ,output, '\n'.join(str(i[1]) for i in planets)]
    ]

    print(tabulate(overview, headers=['Steel', 'Water', 'Gold', 'Temperature (C˚)', 'Colonies'], tablefmt="fancy_grid"))

    options_menu = [['Available Commands' ,chr(0x15CC),"universe", 'hangar', 'fleet', 'missions', 'Change-planet']]

    menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA),chr(0x15CA),  chr(0x15CA)]
    print(tabulate(options_menu, menu_headers, tablefmt="simple"))
    print('-----------------------------------------------------------------------------------\n')





    def do_universe(self):
        print('Universe')
        print('not implemented')


    def do_ss(self, coords):
        print(coords.split())
        g, ss, *_ = coords.split()
        solar_system = get_solar_system(g, ss)
        print(tabulate(solar_system, headers='keys'))
    
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    HelloWorld().cmdloop()