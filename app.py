from collections import Counter
import cmd
from src.queries import (get_planet, get_hangar, get_ship_details, get_building_next_lv,
                         get_improve_steel_mine, get_improve_gold_mine, get_improve_water_farm,
                         get_improve_engine_power, get_improve_military_power, get_improve_shield_power,
                         get_build_ship, get_send_attack_mission)
from src.util import show_solar_system, banner
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

    output = climage.convert('static/images/planet3.png', is_16color=False, palette='solarized', width=24, is_8color=True, is_256color=False)
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
    
    banner()


    username = input('username: ')
    prompt = '> '
    selected_planet = planets[0][1]
    overview(username, selected_planet)

    ###################################
    # Overview and planets management
    ###################################

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

    ###################################
    # Fleet management
    ###################################

    def do_hangar(self, *args):
        """
        View hangar ships
        """
        hangar = get_hangar()['data']['hangar']
        print(tabulate(hangar, headers='keys', tablefmt="heavy_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC), "overview", 'ship_details', 'build_ship']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_ship_details(self, ship_id):
        """
        View ship attributes
        """
        hangar = get_ship_details()['data']['hangar']
        ship_id = int(ship_id)

        if ship_id > len(hangar) or ship_id < 0:
            print('++'*20)
            print(f' {chr(0x1F6AB)} Invalid Ship ID {chr(0x1F6AB)}')
            print('++'*20)
            self.do_hangar()

        ship_info = hangar[ship_id]
        headers = ['Attribute', 'Description']
        columns = [[k, v] for k, v in ship_info.items()]
        print(tabulate(columns, headers=headers, tablefmt="double_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'hangar', 'build_ship']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_build_ship(self, ship_id):
        """
        Build a ship by its id.
        """
        ship_id = int(ship_id)
        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        ship = get_build_ship(current_planet['id'], ship_id)

        if 'errors' in ship:
            print(ship['errors'][0]['message'])
            self.do_hangar()

        else:
            print(f'You have acquired a new spaceship: {ship["data"]["buildShip"]["ship"]["name"]}')
            self.do_overview()

    def do_fleet(self, *args):
        """
        Show fleet landed on the current planet.
        """
        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']
        print(f'Viewing fleet at planet {current_planet["id"]} - {current_planet["name"]} [{g}, {ss}, {p}]\n')
        headers = ['SHIP ID', 'SHIP NAME']
        rows = [[ship['id'], ship['name']] for ship in current_planet['fleet']]
        print(tabulate(rows, headers, tablefmt="fancy_grid"))

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'universe', 'hangar', 'farms', 'infrastructure', 'send_attack_mission']]
        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    ###################################
    # Resource and infrastructure upgrade
    ###################################

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


    def do_improve_engine_power(self, *args):
        """
        Upgrade a engines power if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the engine power? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of engine power.')
            self.do_infrastructure()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_engine_power(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_infrastructure()

        else:
            print(f'Your engines were upgraded to Lv: {upgrade["data"]["improveEnginePower"]["planet"]["enginePower"]}')
            self.do_overview()


    def do_improve_shield_power(self, *args):
        """
        Upgrade shields power if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the shield power? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of shield power.')
            self.do_infrastructure()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_shield_power(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_infrastructure()

        else:
            print(f'Your shields were upgraded to Lv: {upgrade["data"]["improveShieldPower"]["planet"]["shieldPower"]}')
            self.do_overview()


    def do_improve_military_power(self, *args):
        """
        Upgrade military power if able to cover
        required resource amount for upgrading it.
        """
        print('Are you sure you want to upgrade the military power? Resources spent cannot be recovered after confirmation!')
        confirmation = input('Confirm operation [y/n] ')
        if confirmation.lower()[:1] != 'y':
            print('Canceled upgrade of military power.')
            self.do_infrastructure()

        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        upgrade = get_improve_military_power(current_planet['id'])

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_infrastructure()

        else:
            print(f'Your military forces were upgraded to Lv: {upgrade["data"]["improveMilitaryPower"]["planet"]["militaryPower"]}')
            self.do_overview()


    ###################################
    #   MISSIONS
    ###################################

    def do_send_attack_mission(self, *args):
        """
        Send a fleet to attack and loot another planet.
        """
        g, ss, p = self.selected_planet
        current_planet = get_planet(g, ss, p)['data']['solarSystem'][f'position{p}']

        available_ships = {i['id']: i['name'] for i in current_planet['fleet']}

        if not available_ships:
            print(f'{chr(0x274C)}  IYou dont have any ships available in this planet to launch an assault mission! {chr(0x274C)}')
            self.do_send_attack_mission()
            return

        target_planet = input('Insert the target planet ID: ')
        if not target_planet or not target_planet.strip().isdigit():
            print(f'{chr(0x274C)}  Invalid planet ID please inser correct target planet ID {chr(0x274C)}')
            self.do_send_attack_mission()
            return
        
        target_planet = int(target_planet)
        if target_planet == current_planet['id']:
            print(f'{chr(0x274C)}  Cannot attack your own planet {chr(0x274C)}')
            self.do_send_attack_mission()
            return


        fleet_ids = []
        print('Insert each ship correct ID to join fleet!')
        print('Insert "ok" to finish fleet setup!')
        while True:
            ship_id = input('Ship ID: ')

            if ship_id.strip().lower() == 'ok':
                break

            if not ship_id.strip().isdigit():
                print(f'{chr(0x274C)} Ship ID must be a integer number {chr(0x274C)}')
                continue
            
            ship_id = int(ship_id.strip())
            if ship_id not in available_ships.keys():
                print(f'{chr(0x274C)} Invalid ship ID for this planet {chr(0x274C)}')
                continue
            
            fleet_ids.append(ship_id)

        ship_names = Counter([available_ships[ship] for ship in fleet_ids])
        print('Confirm the following fleet:')
        print(tabulate(ship_names.items(), headers=['Ship name', 'Count'], tablefmt="fancy_grid"))

        confirm_and_deploy = input(f'Deploy fleet containing {len(fleet_ids)} ships?\n [y/n]')
        if not confirm_and_deploy.strip().lower() == 'y':
            self.do_overview()
            return

        
        mission = get_send_attack_mission(current_planet['id'], target_planet, fleet_ids)

        if 'errors' in mission:
            print(mission['errors'][0]['message'])
            self.do_overview()
            return
        
        mission = mission['data']['sendAttackMission']['mission']
        headers = ['Mission Type', 'Origin', 'Target', 'Deploy datetime (UTC)', 'Arrival datetime (UTC)', 'Return datetime (UTC)']
        rows = [
            [
                mission['kind'],
                f'[{mission["originGalaxy"]}, {mission["originSolarSystem"]}, {mission["originPosition"]}]',
                f'[{mission["targetGalaxy"]}, {mission["targetSolarSystem"]}, {mission["targetPosition"]}]',
                mission['launchDatetime'],
                mission['arrivalDatetime'],
                mission['returnDatetime']
            ]
        ]

        print(tabulate(rows, headers, tablefmt="fancy_grid"))
        
        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'universe', 'hangar', 'farms', 'infrastructure']]
        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    ##################################
    # Other
    ##################################


    def do_universe(self, *args):
        """
        Explore the universe galaxies and solar systems
        """
        g, ss, p = self.selected_planet
        show_solar_system(g, ss)


    def do_explore_galaxy(self, coords):
        """
        Explore available galaxies and solar systems in the universe.
        """
        try:
            galaxy_id, solar_system_id, *_ = coords.split()
            galaxy_id = int(galaxy_id.strip())
            solar_system_id = int(solar_system_id.strip())
        except:
            print(f'\n {chr(0x274C)} Invalid arguments {chr(0x274C)}')
            print(f'{chr( 0x274C)} Command arguments must be like: "explore_galaxy 4 102" {chr( 0x274C)}\n')
            self.do_universe()
            return

        if galaxy_id < 1 or galaxy_id > 9:
            print(tabulate([[f'GALAXY {galaxy_id} IS OUT OF RANGE'], ['Galaxies limits are from 1 to 9']]))
            self.do_universe()
        
        if solar_system_id < 1 or solar_system_id > 500:
            print(tabulate([[f'SOLAR SYSTEM {solar_system_id} IS OUT OF RANGE'], ['Solar systems limits are from 1 to 500']]))
            self.do_universe()

        show_solar_system(galaxy_id, solar_system_id)

    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    GalaxyClient().cmdloop()
    GalaxyClient().do_overview()