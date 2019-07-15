import numpy as np
import matplotlib.pyplot as plt
import pickle
from termcolor import cprint # for warnings

from OkavSpiesUtil import *


''' 
JEU PERMANENT POPPEL 2019

[INTRODUCTION]
[EXPLICATION FONCTIONNEMENT]

'''

newGame = True
saveState = False

if newGame:
    setLCI(0) # LastComputedIteration = 0
else:
    lastPickleIteration = 0 # TODO define !!
    factionsFileName = 'pickles/factions_upToIter' + str(lastPickleIteration) + '.pkl'
    with open(factionsFileName, 'rb') as infile:
        factions = pickle.load(infile)
    staff = factions[0]
    pumas = factions[1]
    grizzlis = factions[2]
    cobras = factions[3]
    jaguars = factions[4]

    utilFileName = 'pickles/util_upToIter' + str(lastPickleIteration) + '.pkl'
    with open(utilFileName, 'rb') as infile:
        util = pickle.load(infile)
    setLCI(util[0])


#######################################################################################################################

advanceUntil(16, 10, 0)
staff.invest(Tech, 200)
staff.invest(Militaire, 200)
staff.invest(Ressources, 200)
staff.invest(Art, 200)
staff.invest(CountreEspionnage, 100)
staff.agents[0].recruit(Tech)
staff.agents[0].train(100)
staff.agents[0].deploy(pumas)
# staff.agents[0].extract()
pumas.invest(Tech, 500)
pumas.invest(CountreEspionnage, 100)
# grizzlis.invest(Militaire, 200)
# jaguars.invest(Ressources, 200)
# cobras.invest(Art, 200)
advanceUntil(17, 10, 0)
staff.agents[0].sabotage(100)
advanceUntil(18, 10, 0)


# staff.money[getLCI()] += 100
# advanceUntil(19, 10, 0)



# advanceUntil(29, 0, 0)

#######################################################################################################################

if saveState:
    print('Are you sure you want to save the new state up to iteration ' + str(getLCI()) + ' ? (yes/no)')
    userInput = input()
    if userInput == 'yes':
        factionsFileName = 'pickles/factions_upToIter' + str(getLCI()) + '.pkl'
        with open(factionsFileName, 'wb') as outfile:
            pickle.dump(factions, outfile, pickle.HIGHEST_PROTOCOL)
        utilFileName = 'pickles/util_upToIter' + str(getLCI()) + '.pkl'
        with open(utilFileName, 'wb') as outfile:
            pickle.dump([getLCI()], outfile, pickle.HIGHEST_PROTOCOL)
        print('State saved up to iteration ' + str(getLCI()) )
    else:
        print('State not saved - Pickles unchanged')

print('Do you want to debug the factions ? (yes/no)')
userInput = input()
if userInput == 'yes':
    print(staff)
    print(pumas)
    print(grizzlis)
    print(cobras)
    print(jaguars)

    for f in range(len(factions)):
        plt.figure(f)
        plt.suptitle(factions[f].name)
        plotMoney = plt.subplot(611)
        plt.plot(t[1:getLCI()], factions[f].money[1:getLCI()])
        plt.setp(plotMoney.get_xticklabels(), visible=False)
        plt.ylabel('$')
        plotTech = plt.subplot(612, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].tech[1:getLCI()])
        plt.setp(plotTech.get_xticklabels(), visible=False)
        plt.ylabel('Tech')
        plotMilitary = plt.subplot(613, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].military[1:getLCI()])
        plt.setp(plotMilitary.get_xticklabels(), visible=False)
        plt.ylabel('Mil')
        plotRessources = plt.subplot(614, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].ressources[1:getLCI()])
        plt.setp(plotRessources.get_xticklabels(), visible=False)
        plt.ylabel('Res')
        plotArt = plt.subplot(615, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].art[1:getLCI()])
        plt.setp(plotArt.get_xticklabels(), visible=False)
        plt.ylabel('Art')
        plotCounterIntel = plt.subplot(616, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].counterIntel[1:getLCI()])
        plt.setp(plotCounterIntel.get_xticklabels(), visible=True)
        plt.ylabel('CE')
    plt.show()
else:
    print('')

# '''