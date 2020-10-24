import json

# BALANCE FUNCTIONS

def withdraw(user, amount):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['balance'] -= amount
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def deposit(user, amount):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['balance'] += amount
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def get_balance(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    return playerstats[str(user)]['balance']

def get_inventory(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    return playerstats[str(user)]['inventory']

# MULTIPLIER AND level AND prestige FUNCTIONS

def get_multiplier(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    return playerstats[str(user)]['multiplier']

def get_level(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if playerstats[str(user)]['level'] >= 100:
        return 'MAX'

    return playerstats[str(user)]['level']

def add_multiplier(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['multiplier'] += 0.25
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def add_level(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['level'] += 1
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def level_can_happen(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if playerstats[str(user)]['level'] >= 100:
        return False

    if playerstats[str(user)]['balance'] >= round((5 * get_level(user)**3)/5):
        return True
    else:
        return False

def level_action(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if level_can_happen(user):
        playerstats[str(user)]['balance'] >= round((5 * get_level(user)**3)/5)
        withdraw(user, round((5 * get_level(user)**3)/5))
        add_level(user)
        add_multiplier(user)

def get_prestige(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    return playerstats[str(user)]['prestige']

        

           
        
    






