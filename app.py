import os
from collections import Counter
import cmd
from random import choice
from tabulate import tabulate
import climage
from src.queries import (get_planet, get_hangar, get_ship_details, get_building_next_lv,
                         get_improve_steel_mine, get_improve_gold_mine, get_improve_water_farm,
                         get_improve_engine_power, get_improve_military_power, get_improve_shield_power,
                         get_build_ship, get_send_attack_mission, get_user_data, get_mission_reports)
from src.util import show_solar_system, banner, landpage
from settings import IMAGE_PATH, PLANET_PALETTE



def overview(user_metadata):
    user_data = get_user_data(*user_metadata)['data']['user']
    token = user_metadata[-1]
    username = user_data['username']
    current_planet = user_data['planets'][0]
    g, ss, p = current_planet['galaxy'], current_planet['solarSystem'], current_planet['position']
    planets = []
    for planet in user_data['planets']:
        planets.append([planet['id'], str([planet['galaxy'], planet['solarSystem'], planet['position']])])

    print('----------------------------------------------------------')
    print(f'Hello {username}  | {chr(0x1F310)} Main Pannel           ') 
    print('----------------------------------------------------------')


    print('----------------------------------------------------------\n')
    print(f'                 PLANET OVERVIEW     [{g}, {ss}, {p}]      ')
    print('----------------------------------------------------------\n')

    planet_pic = choice([img for img in os.listdir(IMAGE_PATH) if img.startswith('planet')])
    output = climage.convert(f'{IMAGE_PATH}{planet_pic}', is_16color=False, palette=choice(PLANET_PALETTE), width=24, is_8color=True, is_256color=False)

    headers = ['Steel', 'Water', 'Gold', 'Temperature (C˚)', 'Colonies']
    buildings = f'{chr(0x1F517)} Steel Mine Lv: {current_planet["steelMineLv"]}\n\n{chr(0x1F4A7)} Water Farm Lv: {current_planet["waterFarmLv"]}\n\n{chr(0x1F4B0)} Gold Mine Lv: {current_planet["goldMineLv"]}\n\n'
    infrastructure = f'{chr(0x2694)} Military Power: {current_planet["militaryPower"]}\n\n{chr(0x1F6E1)} Shield Power: {current_planet["shieldPower"]}\n\n{chr(0x1F680)} Engine power: {current_planet["enginePower"]}\n\n'

    overview = [
        [current_planet['steel'], current_planet['water'], current_planet['gold'], current_planet['temperature'], ''],
        [f'Name: {current_planet["name"]}', f'Size: ({current_planet["fieldsUsed"]}/{current_planet["size"]})', f'Coords: [{g}, {ss}, {p}]', f'ID: {current_planet["id"]}', ''],
        [buildings, infrastructure, f'Total ships landed:\n\n{chr(0x1F6E9)}: {len(current_planet["fleet"])} ships' , output, '\n'.join(f'{i[0]}: ' + str(i[1]) for i in planets)]
    ]

    print(tabulate(overview, headers=headers, tablefmt="fancy_grid"))

    options_menu = [['Available Commands', chr(0x15CC), 'overview','universe', 'hangar', 'fleet', 'missions', 'change_planet', 'infrastructure', 'farms']]

    menu_headers = ['COMMAND OPTIONS MENU', f'{chr(0x15CA)}', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA),chr(0x15CA),  chr(0x15CA), chr(0x15CA), chr(0x15CA)]
    print(tabulate(options_menu, menu_headers, tablefmt="simple"))
    print('-----------------------------------------------------------------------------------\n')



class GalaxyClient(cmd.Cmd):
    
    banner()

    auth = landpage()
    token = auth['token']
    user_metadata = [auth['user']['id'], auth['user']['username'], token]
    

    prompt = '> '
    selected_planet_id = auth['user']['planets'][0]['id']

    overview(user_metadata)

    ###################################
    # Overview and planets management
    ###################################

    def do_overview(self, *args):
        overview(self.user_metadata)


    def do_change_planet(self, planet_id):
        """
        Change the overview to another colonized planet
        """
        planet_id = int(planet_id)
        if planet_id < 0 or planet_id > len(self.planets) - 1:
            print('++'*20)
            print(f' {chr(0x1F6AB)} Invalid Planet {chr(0x1F6AB)}')
            print('++'*20)
            overview(self.user_metadata)
        
        self.selected_planet = self.planets[planet_id]
        overview(self.user_metadata)


    def do_farms(self, *args):
        """
        View farms and mine current levels and
        necessary resources for upgrading them
        """
        # g, ss, p = self.selected_planet
        # current_planet = get_planet(g, ss, p, self.token)['data']['solarSystem'][f'position{p}']
        user_planets = get_user_data(*self.user_metadata)['data']['user']['planets']
        current_planet = None
        for planet in user_planets:
            if planet['id'] == self.selected_planet_id:
                current_planet = planet
                break

        steel_mine_data = get_building_next_lv(current_planet['steelMineLv'], 'steel_mine', self.token)['data']['buildingNextLevel']
        water_farm_data = get_building_next_lv(current_planet['waterFarmLv'], 'water_farm', self.token)['data']['buildingNextLevel']
        gold_mine_data = get_building_next_lv(current_planet['goldMineLv'], 'gold_mine', self.token)['data']['buildingNextLevel']

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
        # g, ss, p = self.selected_planet
        # current_planet = get_planet(g, ss, p, self.token)['data']['solarSystem'][f'position{p}']
        user_planets = get_user_data(*self.user_metadata)['data']['user']['planets']
        current_planet = None
        for planet in user_planets:
            if planet['id'] == self.selected_planet_id:
                current_planet = planet
                break

        military_power = get_building_next_lv(current_planet['militaryPower'], 'military_power', self.token)['data']['buildingNextLevel']
        engine_power = get_building_next_lv(current_planet['enginePower'], 'engine_power', self.token)['data']['buildingNextLevel']
        shield_power = get_building_next_lv(current_planet['shieldPower'], 'shield_power', self.token)['data']['buildingNextLevel']

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
        hangar = get_hangar(self.token)['data']['hangar']
        print(tabulate(hangar, headers='keys', tablefmt="heavy_outline"))

        options_menu = [['Available Commands' ,chr(0x15CC), "overview", 'ship_details', 'build_ship']]

        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_ship_details(self, ship_id):
        """
        View ship attributes
        """
        hangar = get_ship_details(self.token)['data']['hangar']
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

        ship = get_build_ship(self.selected_planet_id, ship_id, self.token)

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
        user_planets = get_user_data(*self.user_metadata)['data']['user']['planets']
        current_planet = None
        for planet in user_planets:
            if planet['id'] == self.selected_planet_id:
                current_planet = planet
                break
        g, ss, p = current_planet['galaxy'], current_planet['solarSystem'], current_planet['position']

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

        upgrade = get_improve_steel_mine(self.selected_planet_id, self.token)

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

        upgrade = get_improve_gold_mine(self.selected_planet_id, self.token)

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

        upgrade = get_improve_water_farm(self.selected_planet_id, self.token)

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

        upgrade = get_improve_engine_power(self.selected_planet_id, self.token)

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

        upgrade = get_improve_shield_power(self.selected_planet_id, self.token)

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

        upgrade = get_improve_military_power(self.selected_planet_id, self.token)

        if 'errors' in upgrade:
            print(upgrade['errors'][0]['message'])
            self.do_infrastructure()

        else:
            print(f'Your military forces were upgraded to Lv: {upgrade["data"]["improveMilitaryPower"]["planet"]["militaryPower"]}')
            self.do_overview()


    ###################################
    #   MISSIONS
    ###################################
    def do_mission_reports(self, *args):
        mission_reports = get_mission_reports(self.user_metadata[0], self.token)
        rows = []
        for mission in mission_reports['data']['missionReports']:
            row = ''
            row += f"{mission['kind']} mission From {mission['originCoords']} to {mission['targetCoords']} State: {mission['state']}\n"
            row += f"Deploy: {mission['launchDatetime']} Arrival: {mission['arrivalDatetime']} Return: {mission['returnDatetime']}\n"
            fleet = Counter([i['name'] for i in mission['fleet']]).items()
            fleet = ''.join(f'{k} x {v}\n' for k, v in fleet)
            row += f"Fleet:\n {fleet}\n"
            row += f'Resources: \nSteel: {mission["steel"]} Water: {mission["water"]} Gold: {mission["gold"]}\n'
            rows.append(row)

        for row in rows:
            print(row)
            print('-----------------------------------------------------------------------------------')

        options_menu = [['Available Commands' ,chr(0x15CC),"overview", 'universe', 'hangar', 'farms', 'infrastructure']]
        menu_headers = ['COMMAND OPTIONS MENU', chr(0x15CA), chr(0x15CA), chr(0x15CA), chr(0x15CA)]
        print(tabulate(options_menu, menu_headers, tablefmt="simple"))
        print('-----------------------------------------------------------------------------------\n')


    def do_send_attack_mission(self, *args):
        """
        Send a fleet to attack and loot another planet.
        """
        # g, ss, p = self.selected_planet
        # current_planet = get_planet(g, ss, p, self.token)['data']['solarSystem'][f'position{p}']
        user_planets = get_user_data(*self.user_metadata)['data']['user']['planets']
        current_planet = None
        for planet in user_planets:
            if planet['id'] == self.selected_planet_id:
                current_planet = planet
                break
        # g, ss, p = current_planet['galaxy'], current_planet['solarSystem'], current_planet['position']
        available_ships = {i['id']: i['name'] for i in current_planet['fleet']}

        if not available_ships:
            print(f'{chr(0x274C)} You dont have any ships available in this planet to launch an assault mission! {chr(0x274C)}')
            self.do_send_attack_mission()
            return

        print('Insert the target planet coordinates:\n')

        target_planet_galaxy = input('Insert the target planet Galaxy: ')
        if not target_planet_galaxy or not target_planet_galaxy.strip().isdigit():
            print(f'{chr(0x274C)}  Invalid galaxy please insert correct target planet galaxy (Single number) {chr(0x274C)}')
            self.do_send_attack_mission()
            return
        target_planet_galaxy = int(target_planet_galaxy)

        target_planet_ss = input('Insert the target planet Solar System: ')
        if not target_planet_ss or not target_planet_ss.strip().isdigit():
            print(f'{chr(0x274C)}  Invalid Solar System please insert correct target planet solar system (Single number) {chr(0x274C)}')
            self.do_send_attack_mission()
            return
        target_planet_ss = int(target_planet_ss)

        target_planet_position = input('Insert the target planet position in the solar system: ')
        if not target_planet_position or not target_planet_position.strip().isdigit():
            print(f'{chr(0x274C)}  Invalid planet position please insert correct target planet solar system position (Single number) {chr(0x274C)}')
            self.do_send_attack_mission()
            return
        target_planet_position = int(target_planet_position)

        target_coords = [target_planet_galaxy, target_planet_ss, target_planet_position]
        origin_coords = [current_planet['galaxy'], current_planet['solarSystem'], current_planet['position']]
        if target_coords == origin_coords:
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

        mission = get_send_attack_mission(self.selected_planet_id, target_coords, fleet_ids, self.token)

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
        user_planets = get_user_data(*self.user_metadata)['data']['user']['planets']
        current_planet = None
        for planet in user_planets:
            if planet['id'] == self.selected_planet_id:
                current_planet = planet
                break
        g, ss = current_planet['galaxy'], current_planet['solarSystem']
        show_solar_system(g, ss, self.token)


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

        show_solar_system(galaxy_id, solar_system_id, self.token)

    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    GalaxyClient().cmdloop()
    GalaxyClient().do_overview()