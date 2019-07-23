import numpy as np
from math import floor
from termcolor import cprint # for warnings

#######################################################################################################################
###################################################### CONSTANTS ######################################################
#######################################################################################################################

dayStart = 15 # jour début du jeu (0h00)
dayEnd = 28 # jour fin du jeu (23h59)
dt = 15 # [min] (fine tuned for value:60 ; but stable)
t = np.arange(dayStart, dayEnd+1.01, dt/1440)
iterations = int((dayEnd - dayStart + 1) * 24 * (60/dt))

DOMAINS = ['Tech', 'Militaire', 'Ressources', 'Art', 'Contre-espionnage'] # domaines technique dans lesquels les espions se spécialisent
Tech = 0
Militaire = 1
Ressources = 2
Art = 3
CountreEspionnage = 4
FACTIONS = ['Staff', 'Pumas', 'Grizzlis', 'Cobras', 'Jaguars']
factions = None
startMoney = 1000
startValueDomain = 1000
budgetDeplationRate = 80 # percent per day (fine tuned for value:80)

STATE_NOT_INIT = 0
STATE_STAND_BY = 1
STATE_DEPLOYED = 2

lastComputedIteration = 0

#######################################################################################################################
####################################################### CLASSES #######################################################
#######################################################################################################################

class Agent:
    name = '' # nom de l'agent
    parentFaction = None
    domain = 0 # domaine d'activité
    state = STATE_NOT_INIT # état de l'agent
    skill = 0 # compétense
    insight = 0 # perspicacité
    targetFaction = None # faction infiltrée

    def __init__(self, name, parentFaction):
        self.name = name
        self.parentFaction = parentFaction

    def __str__(self):
        string = self.name
        if self.state == STATE_NOT_INIT: 
            string += '\n    non_init'
        elif self.state == STATE_STAND_BY:
            string += '\n    stands by      : ' + DOMAINS[self.domain]
        elif self.state == STATE_DEPLOYED:
            string += '\n    deployed       : ' + DOMAINS[self.domain]
            string += '\n    target_faction : ' + self.targetFaction.name
        else:
            string += '\n    unknown_state'
        
        string += '\n    skill_level    : ' + str(self.skill)
        string += '\n    insight_points : ' + str(self.insight)

        return string

    def recruit(self, domain):

        if domain > len(DOMAINS):
            cprint('Failed to recruit ' + self.name + ' : ' + str(domain) + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif self.state == STATE_NOT_INIT:
            self.domain = domain
            self.state = STATE_STAND_BY
            print(self.name + ' has been recruited in domain : ' + DOMAINS[domain])
        elif self.state == STATE_STAND_BY:
            self.domain = domain
            self.skill /= 2
            print(self.name + ' has reconverted into new domain : ' + DOMAINS[domain])
        else:
            cprint('Failed to recruit ' + self.name + ' : agent already deployed', 'red', attrs=['bold', 'reverse'])

    def train(self, budget):
        if budget > self.parentFaction.money[lastComputedIteration] or self.state != STATE_STAND_BY:
            cprint('Failed to train ' + self.name + ' : not enough funds or agent does not stands by', 'red', attrs=['bold', 'reverse'])
        else : 
            self.skill += budget
            self.parentFaction.money[lastComputedIteration] -= budget
            print(self.name + ' trained for ' + str(budget) + ' in ' + DOMAINS[self.domain])

    def deploy(self, targetFaction):
        if targetFaction.name not in FACTIONS:
            cprint('Failed to deploy ' + self.name + ' : ' + self.targetFaction.name + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif self.state == STATE_NOT_INIT:
            cprint('Failed to deploy ' + self.name + ' : agent not initiated', 'red', attrs=['bold', 'reverse'])
        else:
            self.targetFaction = targetFaction
            self.state = STATE_DEPLOYED
            self.insight = 0
            print(self.name + ' has been deployed in : ' + self.targetFaction.name)
            
    def extract(self):
        if self.state != STATE_DEPLOYED:
            cprint('Failed to extract ' + self.name + ' : agent not deployed', 'red', attrs=['bold', 'reverse'])
        else:
            self.targetFaction = None
            self.state = STATE_STAND_BY
            self.insight = 0
            print(self.name + ' has been extracted')

    # effectue espionnage industriel (technologique et/ou économique)
    # mission réussie :
    #    - rapporte des points pour Faction dans le domaine espionné
    #    - targetFaction n'est averti de rien
    # mission échoue : (en fonction de la gravité)
    #    - espion se cache sans avoir espionné, perd des points de skill mais l'alerte n'est pas donnée
    #    - espion s'enfuit sans avoir espionné, perd des points de skill et est mis en stand-by après avoir fait sonner l'alerte
    
    def spy(self, budget):
        if not assertMissionFeasability(self, budget):
            cprint(self.name + ' failed to spy due to assertFeasability', 'red', attrs=['bold', 'reverse'])
        else:
            self.parentFaction.money[lastComputedIteration] -= budget
            success = computeMissionSuccess(self, budget)
            if success < 50.0: # failure
                amount = success*2 / 100
                self.skill *= amount
                if success < 40:
                    print(self.name + ' failed to spy ' + self.targetFaction.name + ' - he has been extracted and lost ' + str(100 - (amount*100)) + '% of his skill points (still got ' + str(self.skill) + ' points left)')
                    print('NOTIFY ' + self.targetFaction.name + ' THEY HAVE BEEN SUBJECT OF A FAILED SPYING BY ' + self.parentFaction.name)
                    self.extract()
                else:
                    print(self.name + ' failed to spy ' + self.targetFaction.name + ' - he found a shelter but lost ' + str(100 - (amount*100)) + '% of his skill points (still got ' + str(self.skill) + ' points left)')
                    
            else: # success
                amount = 0 
                if self.domain == Tech:
                    amount = max(0, self.targetFaction.tech[lastComputedIteration] - self.parentFaction.tech[lastComputedIteration]) * (success/100.0) * 0.5
                    self.parentFaction.tech[lastComputedIteration] += amount
                elif self.domain == Militaire:
                    amount = max(0, self.targetFaction.military[lastComputedIteration] - self.parentFaction.military[lastComputedIteration]) * (success/100.0) * 0.5
                    self.parentFaction.military[lastComputedIteration] += amount
                elif self.domain == Ressources:
                    amount = max(0, self.targetFaction.ressources[lastComputedIteration] - self.parentFaction.ressources[lastComputedIteration]) * (success/100.0) * 0.5
                    self.parentFaction.ressources[lastComputedIteration] += amount
                elif self.domain == Art:
                    amount = max(0, self.targetFaction.art[lastComputedIteration] - self.parentFaction.art[lastComputedIteration]) * (success/100.0) * 0.5
                    self.parentFaction.art[lastComputedIteration] += amount
                else:
                    print(self.domain)
                    cprint(self.name + ' failed to spy : unknown domain', 'red', attrs=['bold', 'reverse'])
                    return
                print(self.name + ' has spied ' + self.targetFaction.name + ' ; ' + DOMAINS[self.domain] + ' and got himself ' + str(amount) + ' points')
                print('NOTIFY ' + self.parentFaction.name + ' THEY HAVE SPIED ON ' + self.targetFaction.name + ' AND NOW KNOW THIER POINTS IN ' + DOMAINS[self.domain])

    
    # effectue sabotage
    # mission réussie :
    #    - fait perdre des points à targetFaction dans le domaine saboté
    #    - targetFaction n'est pas averti de QUI a commit le sabotage
    # mission échoue : (en fonction de la gravité)
    #    - espion se cache sans avoir saboté, perd des points de skill mais l'alerte n'est pas donnée
    #    - espion s'enfuit sans avoir saboté, perd des points de skill et est mis en stand-by après avoir fait sonner l'alerte
    def sabotage(self, budget):
        if not assertMissionFeasability(self, budget):
            cprint(self.name + ' failed to sabotage due to assertFeasability', 'red', attrs=['bold', 'reverse'])
        else:
            self.parentFaction.money[lastComputedIteration] -= budget
            success = computeMissionSuccess(self, budget)
            if success < 50.0: # failure
                amount = success*2 / 100
                self.skill *= amount
                if success < 40:
                    print(self.name + ' failed to sabotage ' + self.targetFaction.name + ' - he has been extracted and lost ' + str(100 - (amount*100)) + '% of his skill points (still got ' + str(self.skill) + ' points left)')
                    print('NOTIFY ' + self.targetFaction.name + ' THEY HAVE BEEN SUBJECT OF A FAILED SABOTAGE BY ' + self.parentFaction.name)
                    self.extract()
                else:
                    print(self.name + ' failed to sabotage ' + self.targetFaction.name + ' - he found a shelter but lost ' + str(100 - (amount*100)) + '% of his skill points (still got ' + str(self.skill) + ' points left)')
                    
            else: # success
                amount = 0
                if self.domain == Tech:
                    if self.targetFaction.tech[lastComputedIteration] < self.parentFaction.tech[lastComputedIteration]:
                        amount = (self.parentFaction.tech[lastComputedIteration] - self.targetFaction.tech[lastComputedIteration]) * (success/100.0) * 0.5
                    else:
                        amount = (self.targetFaction.tech[lastComputedIteration] - self.parentFaction.tech[lastComputedIteration]) * (success/100.0) * 0.2
                    self.targetFaction.tech[lastComputedIteration] -= amount
                elif self.domain == Militaire:
                    if self.targetFaction.military[lastComputedIteration] < self.parentFaction.military[lastComputedIteration]:
                        amount = (self.parentFaction.military[lastComputedIteration] - self.targetFaction.military[lastComputedIteration]) * (success/100.0) * 0.5
                    else:
                        amount = (self.targetFaction.military[lastComputedIteration] - self.parentFaction.military[lastComputedIteration]) * (success/100.0) * 0.2
                    self.targetFaction.military[lastComputedIteration] -= amount
                elif self.domain == Ressources:
                    if self.targetFaction.ressources[lastComputedIteration] < self.parentFaction.ressources[lastComputedIteration]:
                        amount = (self.parentFaction.ressources[lastComputedIteration] - self.targetFaction.ressources[lastComputedIteration]) * (success/100.0) * 0.5
                    else:
                        amount = (self.targetFaction.ressources[lastComputedIteration] - self.parentFaction.ressources[lastComputedIteration]) * (success/100.0) * 0.2
                    self.targetFaction.ressources[lastComputedIteration] -= amount
                elif self.domain == Art:
                    if self.targetFaction.art[lastComputedIteration] < self.parentFaction.art[lastComputedIteration]:
                        amount = (self.parentFaction.art[lastComputedIteration] - self.targetFaction.art[lastComputedIteration]) * (success/100.0) * 0.5
                    else:
                        amount = (self.targetFaction.art[lastComputedIteration] - self.parentFaction.art[lastComputedIteration]) * (success/100.0) * 0.2
                    self.targetFaction.art[lastComputedIteration] -= amount
                else:
                    print(self.domain)
                    cprint(self.name + ' failed to sabotage : unknown domain', 'red', attrs=['bold', 'reverse'])
                    return
                print(self.name + ' has sabotaged ' + self.targetFaction.name + ' ; ' + DOMAINS[self.domain] + ' by ' + str(amount))
                print('NOTIFY ' + self.targetFaction.name + ' THEY HAVE BEEN SUBJECT OF A SABOTAGE AND LOST ' + str(amount) + ' ' + DOMAINS[self.domain] + ' POINTS')

class Faction:
    name = ''
    agents = None
    money = None

    tech = None
    techBudget = 0
    military = None
    militaryBudget = 0
    ressources = None
    ressourcesBudget = 0
    art = None
    artBudget = 0
    counterIntel = None
    counterIntelBudget = 0

    points = None
    classement = 1 # the higher the better
    def setClassement(self, x):
        self.classement = x


    def __init__(self, name, members):
        self.name = name
        self.agents = np.empty(len(members), dtype=Agent)

        # init agents
        i = 0
        for m in members:
            self.agents[i] = Agent(m, self)
            i += 1

        global iterations
        self.money = np.zeros(iterations+1)
        self.money[0] = startMoney
        self.tech = np.zeros(iterations+1)
        self.tech[0] = startValueDomain
        self.military = np.zeros(iterations+1)
        self.military[0] = startValueDomain
        self.ressources = np.zeros(iterations+1)
        self.ressources[0] = startValueDomain
        self.art = np.zeros(iterations+1)
        self.art[0] = startValueDomain
        self.counterIntel = np.zeros(iterations+1)
        self.counterIntel[0] = 0

        self.points = np.zeros(iterations+1)
        self.points[0] = 0
            
    def __str__(self):
        string = self.name  + ' : ' + str(self.agents.size)
        string += '\n  $    : ' + str(self.money[lastComputedIteration])
        string += '\n  Tech : ' + str(self.tech[lastComputedIteration])
        string += '\n  Mil  : ' + str(self.military[lastComputedIteration])
        string += '\n  Ress : ' + str(self.ressources[lastComputedIteration])
        string += '\n  Art  : ' + str(self.art[lastComputedIteration])
        string += '\n  CE   : ' + str(self.counterIntel[lastComputedIteration])
        string += '\n  #    : ' + str(self.points[lastComputedIteration])
        for a in self.agents:
            string += '\n  ' + str(a)

        return string
    
    # investi dans un des domaines
    # allouer du budget au contre-espionnage diminue fortement la précision des données si spyGroup se fait espionner
    def invest(self, domain, budget):
        if domain > len(DOMAINS):
            cprint('Failed to invest : ' + str(domain) + ' not recognised', 'red', attrs=['bold', 'reverse'])
        elif budget > self.money[lastComputedIteration]:
            cprint(self.name + ' failed to invest in ' + DOMAINS[domain] + ' : not enough funds', 'red', attrs=['bold', 'reverse'])
        elif domain == 0:
            self.techBudget += budget
            self.money[lastComputedIteration] -= budget
            print(self.name + ' invested ' + str(budget) + ' in Tech')
        elif domain == 1:
            self.militaryBudget += budget
            self.money[lastComputedIteration] -= budget
            print(self.name + ' invested ' + str(budget) + ' in Military')
        elif domain == 2:
            self.ressourcesBudget += budget
            self.money[lastComputedIteration] -= budget
            print(self.name + ' invested ' + str(budget) + ' in Ressources')
        elif domain == 3:
            self.artBudget += budget
            self.money[lastComputedIteration] -= budget
            print(self.name + ' invested ' + str(budget) + ' in Art')
        elif domain == 4:
            self.counterIntelBudget += budget
            self.money[lastComputedIteration] -= budget
            print(self.name + ' invested ' + str(budget) + ' in CounterIntel')
        else:
            cprint('Failed to invest : ' + str(domain) + ' not recognised', 'red', attrs=['bold', 'reverse'])



#######################################################################################################################
###################################################### FUNCTIONS ######################################################
#######################################################################################################################

def getLastComputedIteration():
    return lastComputedIteration
def getLCI(): # short
    return getLastComputedIteration()
def setLastComputedIteration(iterationNb):
    global lastComputedIteration
    lastComputedIteration = iterationNb
def setLCI(iterationNb): # short
    setLastComputedIteration(iterationNb)
def setFactions(s, p, g, c, j):
    global factions
    factions = [s, p, g, c, j]

def assertMissionFeasability(agent, budget):
    return agent.state == STATE_DEPLOYED and agent.targetFaction.name != agent.parentFaction.name and budget <= agent.parentFaction.money[lastComputedIteration]

# returns percentage of mission success (0% : total failure ; 50% nothing happened ; 100% : total success)
def computeMissionSuccess(agent, budget):
    value = max(0.0,min(100.0, ((100/1.5) * ((agent.skill * 1.4 + budget * 2) / (agent.targetFaction.counterIntel[lastComputedIteration]+0.001)) - (50.0/1.5)) * (agent.insight/100.0 + 0.5) ))
    print('Computing mission success - agent.skill = ' + str(agent.skill))
    print('                            agent.insight = ' + str(agent.insight))
    print('                            mission.budget = ' + str(budget))
    print('                            target.counterIntel = ' + str(agent.targetFaction.counterIntel[lastComputedIteration]+0.001))
    print('                  success = ' + str(value))
    return value

def advanceUntil(day, hour, minute):
    assert day < 32 and hour < 24 and minute < 60, 'Wrong arguments'
    global lastComputedIteration
    global iterations
    global factions

    computeUpToIteration = int(min(iterations, (day - dayStart) * 24 * (60/dt) + floor(60*hour/dt) + floor(minute/dt)))
    iterationsPerDay = (1440/dt)
    for i in range(lastComputedIteration+1, computeUpToIteration+1, 1): # for every turn
        print('---------------------- TURN', dayStart + i/iterationsPerDay, '----------------------')

        ''' INCREMENT INSIGHT FOR ALL DEPLOYED SPIES '''

        for f in range(len(factions)): # for every faction
            for a in range(len(factions[f].agents)): # for every agent
                if factions[f].agents[a].state == STATE_DEPLOYED:
                    factions[f].agents[a].insight += 100 / (5 * iterationsPerDay) # gets to 100% in 5 days
                    factions[f].agents[a].insight = min(100, factions[f].agents[a].insight)
                    
            
        ''' COMPUTE NEXT VALUES FOR ALL DOMAINS '''

        # relative contribution of each domain for new cash
        w = 0.05 # tech
        x = 0.02 # military
        y = 0.06 # ressources
        z = 0.26 # art

        # relative contribution of allocated budget to domain
        a = 0.00012 # tech
        b = 0.00015 # military
        c = 0.00010 # ressources
        d = 0.00003 # art
        e = 0.075 # counter-intel

        # relative contribution of each domain for points
        l = 1.0 # tech
        m = 1.5 # military
        n = 0.7 # ressources
        o = 0.1 # art
        p = 0 # money


        totalPoints = 0.1
        for f in range(len(factions)): # compute totalPoints
            totalPoints += factions[f].points[i-1]

        for f in range(len(factions)): # for every faction
            # if i <= 630: # TODO delete this shit
            #     factions[f].money[i] = factions[f].money[i-1] + (((w*(factions[f].tech[i-1]-startValueDomain) + x*(factions[f].military[i-1]-startValueDomain) + y*(factions[f].ressources[i-1]-startValueDomain) + z*(factions[f].art[i-1]-startValueDomain)) / iterationsPerDay * 20))
            # else:
            factions[f].money[i] = factions[f].money[i-1] + (((w*(factions[f].tech[i-1]-startValueDomain) + x*(factions[f].military[i-1]-startValueDomain) + y*(factions[f].ressources[i-1]-startValueDomain) + z*(factions[f].art[i-1]-startValueDomain)) / iterationsPerDay * 20)) * (4/factions[f].classement)

            factions[f].tech[i] = factions[f].tech[i-1] * (1 + a * factions[f].techBudget / iterationsPerDay * 24)
            factions[f].techBudget -= (factions[f].techBudget / (100/budgetDeplationRate)) / iterationsPerDay * 1.95
            factions[f].military[i] = factions[f].military[i-1] * (1 + b * factions[f].militaryBudget / iterationsPerDay * 24)
            factions[f].militaryBudget -= (factions[f].militaryBudget / (100/budgetDeplationRate)) / iterationsPerDay * 1.95
            factions[f].ressources[i] = factions[f].ressources[i-1] * (1 + c * factions[f].ressourcesBudget / iterationsPerDay * 24)
            factions[f].ressourcesBudget -= (factions[f].ressourcesBudget / (100/budgetDeplationRate)) / iterationsPerDay * 1.95
            factions[f].art[i] = factions[f].art[i-1] * (1 + d * factions[f].artBudget / iterationsPerDay * 24)
            factions[f].artBudget -= (factions[f].artBudget / (100/budgetDeplationRate)) / iterationsPerDay * 1.95
            factions[f].counterIntel[i] = factions[f].counterIntel[i-1] + (e * factions[f].counterIntelBudget / iterationsPerDay * 24)
            factions[f].counterIntelBudget -= (factions[f].counterIntelBudget / (100/budgetDeplationRate)) / iterationsPerDay * 1.95

            factions[f].points[i] = l*factions[f].tech[i-1] + m*factions[f].military[i-1] + n*factions[f].ressources[i-1] + o*factions[f].art[i-1] + p*factions[f].money[i-1]
            factions[f].setClassement( (factions[f].points[i] ** 2) / (10 * totalPoints) )

    setLastComputedIteration(max(lastComputedIteration, computeUpToIteration))
    if lastComputedIteration == iterations:
        cprint('END OF GAME : max number of iterations reached', 'red', attrs=['bold', 'reverse'])


#######################################################################################################################
###################################################### FACTIONS #######################################################
#######################################################################################################################


staff = Faction(FACTIONS[0], ['Hokkaido', 'Otocyon', 'Ocelot', 'Brocard', 'Douc', 'Alpaga', 'Gerfaut', 'Bourbour'])
pumas = Faction(FACTIONS[1], ['Muscardin', 'Gulawani', 'Ouandji', 'Castor', 'Nanuk', 'Racoon', 'Dhole', 'Balkanski', 'Pierric', 'Emeric'])
grizzlis = Faction(FACTIONS[2], ['Oncilla', 'Ligoni', 'Cheetah', 'Akita', 'Isard', 'Panthère', 'Busard', 'Jacques', 'Stephan'])
cobras = Faction(FACTIONS[3], ['Okapi', 'Lionceau', 'Suricate', 'Hobereau', 'Margay', 'Capybara', 'Kodiak', 'Lancelot', 'Grégoire'])
jaguars = Faction(FACTIONS[4], ['Aratinga', 'Baribal', 'Cheveche', 'Madoqua', 'Crecerelle', 'Bengal', 'Lynx', 'Milan', 'Matteo', 'Adrien'])

setFactions(staff, pumas, grizzlis, cobras, jaguars)

    