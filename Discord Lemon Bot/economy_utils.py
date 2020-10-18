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

# MULTIPLIER AND PRESTIGE FUNCTIONS

def get_multiplier(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    return playerstats[str(user)]['multiplier']

def get_prestige(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if playerstats[str(user)]['prestige'] >= 100:
        return 'MAX'

    return playerstats[str(user)]['prestige']

def add_multiplier(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['multiplier'] += 0.25
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def add_prestige(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)
        playerstats[str(user)]['prestige'] += 1
    with open('./jsons/playerstats.json', 'w') as f:
        json.dump(playerstats, f, indent=4)

def prestige_can_happen(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if playerstats[str(user)]['prestige'] >= 100:
        return False

    if playerstats[str(user)]['balance'] >= round((5 * get_prestige(user)**3)/5):
        return True
    else:
        return False

def prestige_action(user):
    with open('./jsons/playerstats.json', 'r') as f:
        playerstats = json.load(f)

    if prestige_can_happen(user):
        playerstats[str(user)]['balance'] >= round((5 * get_prestige(user)**3)/5)
        withdraw(user, round((5 * get_prestige(user)**3)/5))
        add_prestige(user)
        add_multiplier(user)
        

           
        
    






