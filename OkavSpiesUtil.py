import numpy as np
from math import floor


#######################################################################################################################
###################################################### CONSTANTS ######################################################
#######################################################################################################################

dayStart = 15 # jour début du jeu (0h00)
dayEnd = 28 # jour fin du jeu (23h59)
dt = 480 # [min]
t = np.arange(dayStart, dayEnd+1.01, dt/1440)
iterations = int((dayEnd - dayStart + 1) * 24 * (60/dt))

DOMAINS = ['HighTech', 'Spatial', 'Alimentaire', 'Militaire', 'Contre-espionnage', 'Business'] # domaines technique dans lesquels les espions se spécialisent
FACTIONS = ['Staff', 'Pumas', 'Grizzlis', 'Cobras', 'Jaguars']

STATE_NOT_INIT = 0
STATE_STAND_BY = 1
STATE_DEPLOYED = 2

lastComputedIteration = 0
def setLastComputedIteration(iterationNb):
    global lastComputedIteration
    lastComputedIteration = iterationNb
def getLastComputedIteration():
    return lastComputedIteration
def getLCI(): # short
    return getLastComputedIteration()
def setLCI(iterationNb): # short
    setLastComputedIteration(iterationNb)

#######################################################################################################################
####################################################### CLASSES #######################################################
#######################################################################################################################

class Agent:
    name = '' # nom de l'agent
    domain = '' # domaine d'activité
    state = STATE_NOT_INIT # état de l'agent
    skill = 0 # compétense
    insight = 0 # perspicacité
    targetFaction = '' # faction infiltrée

    def __init__(self, name):
        self.name = name

    def __str__(self):
        string = self.name
        if self.state == STATE_NOT_INIT: 
            string += '\n    non_init'
        elif self.state == STATE_STAND_BY:
            string += '\n    stands by'
            string += '\n    skill_level    : ' + str(self.skill)
        elif self.state == STATE_DEPLOYED:
            string += '\n    deployed'
            string += '\n    skill_level    : ' + str(self.skill)
            string += '\n    insight_points : ' + str(self.insight)
            string += '\n    target_faction : ' + self.targetFaction
        else:
            string += '\n    unknown_state'

        return string

    def recruit(self, domain):
        if domain not in DOMAINS:
            cprint('Failed to recruit ' + self.name + ' : ' + domain + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif self.state == STATE_NOT_INIT:
            self.domain = domain
            self.state = STATE_STAND_BY
        elif self.state == STATE_STAND_BY:
            self.domain = domain
            self.skill /= 2
            cprint(self.name + ' has reconverted into new domain', 'red', attrs=['bold', 'reverse'])
        else:
            cprint('Failed to recruit ' + self.name + ' : agent already deployed', 'red', attrs=['bold', 'reverse'])

    def train(self, budget):
        print('train TODO') # TODO

    def deploy(self, targetFaction):
        if targetFaction not in FACTIONS:
            cprint('Failed to deploy ' + self.name + ' : ' + self.targetFaction + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif self.state == STATE_NOT_INIT:
            cprint('Failed to deploy ' + self.name + ' : agent not initiated', 'red', attrs=['bold', 'reverse'])
        else:
            self.targetFaction = targetFaction
            self.state = STATE_DEPLOYED
            self.insight = 0
            
    def extract(self):
        if self.state != STATE_DEPLOYED:
            cprint('Failed to extract ' + self.name + ' : agent not deployed', 'red', attrs=['bold', 'reverse'])
        else:
            self.targetFaction = ''
            self.state = STATE_STAND_BY
            self.insight = 0

    # effectue espionnage industriel (technologique et/ou économique)
    # mission réussie :
    #    - rapporte des points pour Faction dans le domaine espionné
    #    - targetFaction n'est pas averti
    # mission échoue : (en fonction de la gravité)
    #    - espion s'enfuit sans données, rentre en stad-by mais l'alerte est donnée
    #    - espion est capturé, perd des points de skill et est mis en stand-by
    #    - espion est tué, perd tous ses points et est mit en non-initié
    def spy(self, buget):
        print('spy TODO') # TODO
    
    # effectue sabotage
    # mission réussie :
    #    - fait perdre des points à targetFaction dans le domaine saboté
    #    - targetFaction n'est pas averti de qui a commi le sabotage
    # mission échoue : (en fonction de la gravité)
    #    - espion s'enfuit sans saboter, rentre en stand-by mais l'alerte est donnée
    #    - espion est capturé, perd des points de skill et est mis en stand-by
    #    - espion est tué, perd tous ses points et est mit en non-initié
    def sabotage(self, budget):
        print('sabotage TODO') # TODO
        
class Faction:
    name = ''
    agents = None
    money = None
    counterIntel = None

    tech = None
    techBudget = 0
    spatial = None
    spatialBudget = 0
    food = None
    foodBudget = 0
    military = None
    militaryBudget = 0


    def __init__(self, name, members):
        self.name = name
        self.agents = np.empty(len(members), dtype=Agent)
        i = 0
        for m in members:
            self.agents[i] = Agent(m)
            i += 1

        global iterations
        self.money = np.zeros(iterations+1)
        self.money[0] = 10000000
        self.tech = np.zeros(iterations+1)
        self.tech[0] = 100
        self.spatial = np.zeros(iterations+1)
        self.spatial[0] = 10
        self.food = np.zeros(iterations+1)
        self.food[0] = 100
        self.military = np.zeros(iterations+1)
        self.military[0] = 100
        self.counterIntel = np.zeros(iterations+1)
            
    def __str__(self):
        string = self.name  + ' : ' + str(self.agents.size)
        for a in self.agents:
            string += '\n  ' + str(a)

        return string
    
    # investi dans un des domaines
    # allouer du budget au contre-espionnage diminue fortement la précision des données si spyGroup se fait espionner
    def invest(self, domain, budget):
        if domain not in DOMAINS:
            cprint('Failed to invest : ' + domain + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif budget > self.money[lastComputedIteration]:
            cprint('Failed to invest : not enough funds', 'red', attrs=['bold', 'reverse'])
        elif domain == DOMAINS[0]:
            self.techBudget += budget
            self.money[lastComputedIteration] -= budget
        elif domain == DOMAINS[1]:
            self.spatialBudget += budget
            self.money[lastComputedIteration] -= budget
        elif domain == DOMAINS[2]:
            self.foodBudget += budget
            self.money[lastComputedIteration] -= budget
        elif domain == DOMAINS[3]:
            self.militaryBudget += budget
            self.money[lastComputedIteration] -= budget
        elif domain == DOMAINS[4]:
            self.counterIntel += budget
            self.money[lastComputedIteration] -= budget
        else:
            cprint('Failed to invest : ' + domain + ' not recognised', 'red', attrs=['bold', 'reverse'])



#######################################################################################################################
###################################################### FUNCTIONS ######################################################
#######################################################################################################################


def advanceUntil(day, hour, minute):
    assert day < 32 and hour < 24 and minute < 60, 'Wrong arguments'
    global lastComputedIteration
    global iterations
    global factions

    computeUpToIteration = int(min(iterations, (day - dayStart) * 24 * (60/dt) + floor(60*hour/dt) + floor(minute/dt)))
    iterationsPerDay = (1440/dt)
    for i in range(lastComputedIteration+1, computeUpToIteration+1, 1): # for every turn
        print('---------------------- TURN', i, '----------------------')

        # compute next values for all domains
        # increment insight for all deployed spies


        # % relative contribution of each domain for new cash
        x = 4 * 8000 / iterationsPerDay # tech
        y = 12 * 8000 / iterationsPerDay # spatial
        z = 2 * 8000 / iterationsPerDay # military

        # % contribution of allocated budget to domain
        a = 2 # tech
        b = 2.4 # spatial
        c = 12 # food
        d = 1.6 # military

        # % allocated budget spending rate
        m = 5 # rest
        n = 4 # food

        totalMoney = 0
        for f in range(len(factions)): # compute totalMoney
            totalMoney += factions[f].money[i-1]

        for f in range(len(factions)): # for every faction
            factions[f].money[i] = factions[f].money[i-1] + (x*factions[f].tech[i-1] + y*factions[f].spatial[i-1] + z*factions[f].military[i-1]) * (factions[f].food[i-1]*0.013 + 0.2)
            factions[f].tech[i] = factions[f].tech[i-1] * (1 + factions[f].techBudget/(iterationsPerDay/a)/totalMoney) #+ factions[f].spatialBudget/(iterationsPerDay/2)*0.1/totalMoney)
            factions[f].spatial[i] = factions[f].spatial[i-1] * (1 + factions[f].spatialBudget/(iterationsPerDay/b)/totalMoney) #+ factions[f].techBudget/(iterationsPerDay/2)*0.05/totalMoney)
            factions[f].food[i] = factions[f].food[i-1] * (1 + factions[f].foodBudget/(iterationsPerDay/c)/totalMoney - factions[f].money[i-1]*0.0000000001)
            factions[f].military[i] = factions[f].military[i-1] * (1 + factions[f].militaryBudget/(iterationsPerDay/d)/totalMoney) #+ factions[f].techBudget/(iterationsPerDay/2)*0.05/totalMoney)

            if factions[f].techBudget >= factions[f].money[i] *0.001: # if budget is higher than 0.1% of faction's budget
                factions[f].techBudget -= factions[f].techBudget*m/iterationsPerDay
            else:
                factions[f].techBudget = 0
            if factions[f].spatialBudget >= factions[f].money[i] *0.001: # if budget is higher than 0.1% of faction's budget
                factions[f].spatialBudget -= factions[f].spatialBudget*m/iterationsPerDay
            else:
                factions[f].spatialBudget = 0
            if factions[f].foodBudget >= factions[f].money[i] *0.001: # if budget is higher than 0.1% of faction's budget
                factions[f].foodBudget -= factions[f].foodBudget*n/iterationsPerDay
            else:
                factions[f].foodBudget = 0
            if factions[f].militaryBudget >= factions[f].money[i] *0.001: # if budget is higher than 0.1% of faction's budget
                factions[f].militaryBudget -= factions[f].militaryBudget*m/iterationsPerDay
            else:
                factions[f].militaryBudget = 0
    
    setLastComputedIteration(max(lastComputedIteration, computeUpToIteration))
    if lastComputedIteration == iterations:
        cprint('END OF GAME : max number of iterations reached', 'red', attrs=['bold', 'reverse'])


#######################################################################################################################
###################################################### FACTIONS #######################################################
#######################################################################################################################


staff = Faction(FACTIONS[0], ['Hokkaido', 'Otocyon', 'Ocelot', 'Brocard', 'Douc', 'Alpaga', 'Gerfaut', 'Bourbour'])
pumas = Faction(FACTIONS[1], ['Muscardin', 'Gulawani', 'Ouandji', 'Castor', 'Nanuk', 'Racoon', 'Dhole', 'Balkanski', 'Pierric', 'Emeric'])
grizzlis = Faction(FACTIONS[2], [])
cobras = Faction(FACTIONS[3], [])
jaguars = Faction(FACTIONS[4], [])
factions = [staff, pumas, grizzlis, cobras, jaguars]