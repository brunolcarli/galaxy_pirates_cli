import requests
from settings import API_URL


def get_build_ship(planet_id, ship_id):
    query = f'''
    mutation buildship{{
        buildShip(input: {{
            planetId: {planet_id}
            shipId: {ship_id}
        }}){{
            ship {{
                id
                name
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_improve_shield_power(planet_id):
    query = f'''
    mutation {{
        improveShieldPower(input: {{planetId: {planet_id} }}){{
            planet{{
                shieldPower
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_improve_engine_power(planet_id):
    query = f'''
    mutation {{
        improveEnginePower(input: {{planetId: {planet_id} }}){{
            planet{{
                enginePower
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_improve_military_power(planet_id):
    query = f'''
    mutation {{
        improveMilitaryPower(input: {{planetId: {planet_id} }}){{
            planet{{
                militaryPower
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()



def get_improve_water_farm(planet_id):
    query = f'''
    mutation {{
        improveWaterFarm(input: {{planetId: {planet_id} }}){{
            planet{{
                waterFarmLv
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_improve_gold_mine(planet_id):
    query = f'''
    mutation {{
        improveGoldMine(input: {{planetId: {planet_id} }}){{
            planet{{
                goldMineLv
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_improve_steel_mine(planet_id):
    query = f'''
    mutation {{
        improveSteelMine(input: {{planetId: {planet_id} }}){{
            planet{{
                steelMineLv
            }}
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_building_next_lv(building_lv, building_type):
    query = f'''
    query {{
        buildingNextLevel(currentLevel: {building_lv} buildingType: "{building_type}") {{
            name
            lv
            steel
            gold
            water
        }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_hangar():
    query = '''
    query ships{
        hangar {
            id
            name
            description
        }    
    }
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_ship_details():
    query = '''
    query ships{
        hangar {
            id
            name
            description
            integrity
            description
            offensePower
            shieldPower
            cargoSpace
            speed
            cost {
                steel
                water
                gold
            }
            requirements {
                militaryPower
                shieldPower
                enginePower
            }
        }    
    }
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_planet(galaxy, solar_system, position):
    query = f'''
    query {{ solarSystem(galaxy_Id: {galaxy} galaxyPosition: {solar_system}) {{
        position{position}{{
            id
            name
            galaxy
            solarSystem
            position
            steel
            water
            gold
            temperature
            size
            fieldsUsed
            steelMineLv
            waterFarmLv
            goldMineLv
            militaryPower
            shieldPower
            enginePower
            fleet{{
                id
                name
            }}
        }}
     }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_solar_system(galaxy, solar_system):
    query = f'''
    query {{ solarSystem(galaxy_Id: {galaxy} galaxyPosition: {solar_system}) {{
        position1{{ id name galaxy solarSystem position }}
        position2{{ id name galaxy solarSystem position }}
        position3{{ id name galaxy solarSystem position }}
        position4{{ id name galaxy solarSystem position }}
        position5{{ id name galaxy solarSystem position }}
        position6{{ id name galaxy solarSystem position }}
        position7{{ id name galaxy solarSystem position }}
        position8{{ id name galaxy solarSystem position }}
        position9{{ id name galaxy solarSystem position }}
        position10{{ id name galaxy solarSystem position }}
        position11{{ id name galaxy solarSystem position }}
        position12{{ id name galaxy solarSystem position }}
        position13{{ id name galaxy solarSystem position }}
        position14{{ id name galaxy solarSystem position }}
        position15{{ id name galaxy solarSystem position }}
     }}
    }}
    '''
    return requests.post(API_URL, json={'query': query}).json()


def get_send_attack_mission(origin_planet_id, target_planet_id, fleet_ids):
    # TODO include speed
    query = f'''
    mutation {{
        sendAttackMission(input: {{
            originPlanet: {origin_planet_id}
            targetPlanet: {target_planet_id}
            fleet: {fleet_ids}
            speed: 1
        }}){{
            mission {{
                kind
                originGalaxy
                originSolarSystem
                originPosition
                targetGalaxy
                targetSolarSystem
                targetPosition
                launchDatetime
                arrivalDatetime
                returnDatetime
                distance
            }}
        }}
    }}
    '''

    return requests.post(API_URL, json={'query': query}).json()


def get_planet_spy(galaxy, solar_system, position):
    ...
    # TODO


def get_planets(coords):
    ...
    # TODO