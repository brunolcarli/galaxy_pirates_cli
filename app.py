import cmd
from src.queries import get_solar_system, get_planet, get_hangar, get_ship_details, get_building_next_lv, get_improve_steel_mine, get_improve_gold_mine, get_improve_water_farm
from tabulate import tabulate
import climage


planets = (
    ['COORD', [9, 102, 8]],
    ['COORD', [7, 10, 2]]
)


def overview(username, selected_planet):
    print('----------------------------------------------------------')
    print(f'Hello {username}  | {chr(0x1F310)} Main Pannel           ') 
    print('----------------------------------------------------------')

    g, ss, p = selected_planet
    current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

    print('----------------------------------------------------------\n')
    print(f'                 PLANET OVERVIEW     [{g}, {ss}, {p}]      ')
    print('----------------------------------------------------------\n')

    output = climage.convert('planet3.png', is_16color=False, palette='solarized', width=24, is_8color=True, is_256color=False)
    buildings = f'{chr(0x1F517)} Steel Mine Lv: {current_planet["steelMineLv"]}\n\n{chr(0x1F4A7)} Water Farm Lv: {current_planet["waterFarmLv"]}\n\n{chr(0x1F4B0)} Gold Mine Lv: {current_planet["goldMineLv"]}\n\n'
    infrastructure = f'{chr(0x2694)} Military Power: {current_planet["militaryPower"]}\n\n{chr(0x1F6E1)} Shield Power: {current_planet["shieldPower"]}\n\n{chr(0x1F680)} Engine power: {current_planet["enginePower"]}\n\n'
    overview = [
        [current_planet['steel'], current_planet['water'], current_planet['gold'], current_planet['temperature'], ''],
        [f'Name: {current_planet["name"]}', f'Size: ({current_planet["fieldsUsed"]}/{current_planet["size"]})', f'Coords: [{g}, {ss}, {p}]', f'ID: {current_planet["id"]}', ''],
        [buildings, infrastructure, f'Total ships landed:\n\n{chr(0x1F6E9)}: {len(current_planet["fleet"])} ships' ,output, '\n'.join(f'{j}: ' + str(i[1]) for j, i in enumerate(planets))]
    ]

    print(tabulate(overview, headers=['Steel', 'Water', 'Gold', 'Temperature (C˚)', 'Colonies'], tablefmt="fancy_grid"))

    options_menu = [['Available Commands' ,chr(0x15CC), 'overview','universe', 'hangar', 'fleet', 'missions', 'change_planet', 'infrastructure', 'farms']]

    menu_headers = ['COMMAND OPTIONS MENU', f'{chr(0x15CA)}', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA),chr(0x15CA),  chr(0x15CA), chr(0x15CA), chr(0x15CA)]
    print(tabulate(options_menu, menu_headers, tablefmt="simple"))
    print('-----------------------------------------------------------------------------------\n')



class GalaxyClient(cmd.Cmd):
    """Simple command processor example."""
    username = input('username: ')
    selected_planet = planets[0][1]
    overview(username, selected_planet)

    def do_overview(self, *args):
        overview(self.username, self.selected_planet)


    def do_change_planet(self, planet_id):
        """
        Change the overview to another colonized planet
        """
        planet_id = int(planet_id)
        if planet_id < 0 or planet_id > len(planets) - 1:
            print('++'*20)
            print(f' {chr(0x1F6AB)} Invalid Planet {chr(0x1F6AB)}')
            print('++'*20)
            overview(self.username, self.selected_planet)
        
        self.selected_planet = planets[planet_id][1]
        overview(self.username, self.selected_planet)


    def do_hangar(self, *args):
        """
        View hangar ships
        """
        hangar = get_hangar()['data']['hangar']
        print(tabulate(hangar, headers='keys', tablefmt="heavy_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'ship_detais']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_ship_details(self, ship_id):
        """
        View ship attributes
        """
        hangar = get_ship_details()['data']['hangar']
        ship_id = int(ship_id)

        if ship_id > len(hangar) or ship_id < 1:
            print('++'*20)
            print(f' {chr(0x1F6AB)} Invalid Ship ID {chr(0x1F6AB)}')
            print('++'*20)
            self.do_hangar()

        ship_info = hangar[ship_id]
        headers = ['Attribute', 'Description']
        columns = [[k, v] for k, v in ship_info.items()]
        print(tabulate(columns, headers=headers, tablefmt="double_outline"))

        # TODO build ship

    def do_farms(self, *args):
        """
        View farms and mine current levels and
        necessary resources for upgrading them
        """
        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        steel_mine_data = get_building_next_lv(current_planet['steelMineLv'], 'steel_mine')['data']['buildingNextLevel']
        water_farm_data = get_building_next_lv(current_planet['waterFarmLv'], 'water_farm')['data']['buildingNextLevel']
        gold_mine_data = get_building_next_lv(current_planet['goldMineLv'], 'gold_mine')['data']['buildingNextLevel']

        headers = ['Building', 'LV', 'Required Steel', 'Required Gold', 'Required Water']
        rows = [
            [steel_mine_data['name'], steel_mine_data['lv'], steel_mine_data['steel'], steel_mine_data['gold'], steel_mine_data['water']],
            [water_farm_data['name'], water_farm_data['lv'], water_farm_data['steel'], water_farm_data['gold'], water_farm_data['water']],
            [gold_mine_data['name'], gold_mine_data['lv'], gold_mine_data['steel'], gold_mine_data['gold'], gold_mine_data['water']],
        ]
        print(tabulate(rows, headers=headers, tablefmt="double_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'improve_steel_mine', 'improve_gold_mine', 'improve_water_farm']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_improve_steel_mine(self, *args):
        """
        Upgrade a steel mine building if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the steel mine? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of steel mine.')
            self.do_farms()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_steel_mine(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_farms()

        else:
            print(f'Your steel mine was upgraded to Lv: {upgrade["data"]["improveSteelMine"]["planet"]["steelMineLv"]}')
            self.do_overview()

    def do_improve_gold_mine(self, *args):
        """
        Upgrade a gold mine building if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the gold mine? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of gold mine.')
            self.do_farms()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_gold_mine(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_farms()

        else:
            print(f'Your gold mine was upgraded to Lv: {upgrade["data"]["improveGoldMine"]["planet"]["goldMineLv"]}')
            self.do_overview()

    def do_improve_water_farm(self, *args):
        """
        Upgrade a water farm building if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the water farm? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of water farm.')
            self.do_farms()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_water_farm(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_farms()

        else:
            print(f'Your water farm was upgraded to Lv: {upgrade["data"]["improveWaterFarm"]["planet"]["waterFarmLv"]}')
            self.do_overview()


    def do_infrastructure(self, *args):
        """
        View infrastructure current levels and
        necessary resources for upgrading them
        """
        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        military_power = get_building_next_lv(current_planet['militaryPower'], 'military_power')['data']['buildingNextLevel']
        engine_power = get_building_next_lv(current_planet['enginePower'], 'engine_power')['data']['buildingNextLevel']
        shield_power = get_building_next_lv(current_planet['shieldPower'], 'shield_power')['data']['buildingNextLevel']

        headers = ['Building', 'LV', 'Required Steel', 'Required Gold', 'Required Water']
        rows = [
            [military_power['name'], military_power['lv'], military_power['steel'], military_power['gold'], military_power['water']],
            [engine_power['name'], engine_power['lv'], engine_power['steel'], engine_power['gold'], engine_power['water']],
            [shield_power['name'], shield_power['lv'], shield_power['steel'], shield_power['gold'], shield_power['water']],
        ]
        print(tabulate(rows, headers=headers, tablefmt="double_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'improve_military_power', 'improve_engine_power', 'improve_shield_power']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_universe(self):
        """ """
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
    GalaxyClient().cmdloop()
    GalaxyClient().do_overview()