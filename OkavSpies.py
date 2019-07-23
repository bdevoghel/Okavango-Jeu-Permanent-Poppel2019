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

newGame = False
saveState = True

if newGame:
    setLCI(0) # LastComputedIteration = 0
else:
    lastPickleIteration = 630 # TODO define !!
    factionsFileName = 'pickles/factions_upToIter' + str(lastPickleIteration) + '.pkl'
    with open(factionsFileName, 'rb') as infile:
        factions = pickle.load(infile)
    staff = factions[0]
    pumas = factions[1]
    grizzlis = factions[2]
    cobras = factions[3]
    jaguars = factions[4]
    setFactions(staff, pumas, grizzlis, cobras, jaguars)

    utilFileName = 'pickles/util_upToIter' + str(lastPickleIteration) + '.pkl'
    with open(utilFileName, 'rb') as infile:
        util = pickle.load(infile)
    setLCI(util[0])


#######################################################################################################################

if newGame:
    advanceUntil(15, 16, 0)

    advanceUntil(15, 22, 20)
    jaguars.agents[9].recruit(Ressources)
    jaguars.agents[9].train(300)
    jaguars.invest(Ressources, 100)
    jaguars.invest(Tech, 150)
    jaguars.invest(Art, 200)
    jaguars.invest(CountreEspionnage, 250)
    jaguars.agents[9].deploy(grizzlis)

    advanceUntil(16, 12, 13) # PRINT

    advanceUntil(16, 13, 19)
    jaguars.invest(Art, 137)
    jaguars.invest(CountreEspionnage, 50)

    advanceUntil(16,18,19)
    pumas.invest(CountreEspionnage, 400)
    pumas.invest(Tech, 100)
    pumas.invest(Art, 300)
    pumas.agents[5].recruit(Ressources)
    pumas.agents[5].train(200)
    pumas.agents[5].deploy(jaguars)

    advanceUntil(16, 18, 41)
    cobras.invest(Art, 300)
    cobras.invest(Ressources, 300)
    cobras.invest(CountreEspionnage, 400)

    advanceUntil(16, 18, 52)
    grizzlis.invest(Art, 250)
    grizzlis.invest(CountreEspionnage, 300)
    grizzlis.agents[2].recruit(Tech)
    grizzlis.agents[2].train(50)
    grizzlis.agents[8].recruit(Tech)
    grizzlis.agents[8].train(50)
    grizzlis.agents[7].recruit(Tech)
    grizzlis.agents[7].train(50)
    grizzlis.agents[4].recruit(Militaire)
    grizzlis.agents[4].train(50)
    grizzlis.agents[5].recruit(Militaire)
    grizzlis.agents[5].train(50)
    grizzlis.agents[0].recruit(Militaire)
    grizzlis.agents[0].train(50)
    grizzlis.agents[1].recruit(Ressources)
    grizzlis.agents[1].train(50)
    grizzlis.agents[3].recruit(Ressources)
    grizzlis.agents[3].train(50)
    grizzlis.agents[6].recruit(Ressources)
    grizzlis.agents[6].train(50)

    advanceUntil(16, 20, 0)
    cobras.money[getLCI()] += 200 # WANTED : Crécerelle attrapé par Margay

    advanceUntil(17, 10, 20) # PRINT

    advanceUntil(17, 10, 50)
    pumas.money[getLCI()] += 200 # WANTED : Dhole échappe

    advanceUntil(17, 12, 35)
    jaguars.invest(Tech, 150)
    jaguars.invest(Militaire, 123)
    jaguars.invest(Art, 200)
    jaguars.invest(CountreEspionnage, 200)
    jaguars.agents[9].spy(200)

    advanceUntil(18, 14, 16)
    pumas.invest(Tech, 150)
    pumas.invest(Art, 200)
    pumas.invest(CountreEspionnage, 200)

    advanceUntil(18, 14, 30) # PRINT

    advanceUntil(18, 15, 28)
    pumas.invest(Art, 300)
    pumas.invest(CountreEspionnage, 135)
    pumas.agents[6].recruit(Militaire)
    pumas.agents[6].train(300)
    pumas.agents[6].deploy(cobras)

    advanceUntil(18, 15, 29)
    cobras.agents[4].recruit(Art)
    cobras.agents[4].train(800)
    cobras.agents[4].deploy(pumas)
    cobras.agents[1].recruit(Militaire)
    cobras.agents[1].train(400)
    cobras.agents[1].deploy(grizzlis)
    cobras.invest(Militaire, 300)
    cobras.invest(Art, 200)
    cobras.invest(CountreEspionnage, 200)
    cobras.invest(Tech, 33)

    advanceUntil(18, 15, 38)
    grizzlis.invest(CountreEspionnage, 250)
    grizzlis.agents[1].train(50)
    grizzlis.agents[2].train(50)
    grizzlis.agents[0].train(50)
    grizzlis.agents[1].deploy(jaguars)
    grizzlis.agents[2].deploy(pumas)
    grizzlis.agents[0].deploy(cobras)

    advanceUntil(18, 15, 42)
    jaguars.agents[6].recruit(Tech)
    jaguars.agents[6].train(400)
    jaguars.agents[6].deploy(cobras)
    jaguars.agents[4].recruit(Art)
    jaguars.agents[4].train(400)
    jaguars.agents[4].deploy(pumas)
    jaguars.invest(Militaire, 115)
    jaguars.invest(Tech, 300)
    jaguars.invest(Ressources, 250)
    jaguars.invest(Art, 250)
    jaguars.invest(CountreEspionnage, 400)

    advanceUntil(19, 14, 50)
    pumas.agents[5].spy(400)
    pumas.invest(Art, 300)
    pumas.invest(CountreEspionnage, 500)

    advanceUntil(19, 22, 0) # PRINT

    advanceUntil(20, 11, 0)
    jaguars.money[getLCI()] += 200 # WANTED Douroucouli

    advanceUntil(20, 11, 10)
    jaguars.agents[4].sabotage(400)
    jaguars.agents[6].spy(300)
    jaguars.agents[9].sabotage(200)

    advanceUntil(20, 11, 12)
    pumas.agents[5].spy(600)
    pumas.invest(CountreEspionnage, 500)
    # pumas.invest(Art, 500)

    grizzlis.invest(CountreEspionnage, grizzlis.money[getLCI()]) # STAFF IMPOSED

    advanceUntil(20, 11, 15)
    cobras.invest(CountreEspionnage, 1000)
    cobras.invest(Art, 1200)
    cobras.agents[3].recruit(Tech)
    cobras.agents[3].train(1000)
    cobras.agents[3].deploy(jaguars)

    advanceUntil(20, 12, 50)
    jaguars.agents[5].recruit(Militaire)
    jaguars.agents[5].train(636)
    jaguars.agents[5].deploy(pumas)
    jaguars.invest(Tech, 500)
    jaguars.invest(Militaire, 500)
    jaguars.invest(Art, 1200)
    jaguars.invest(Ressources, 1100)
    jaguars.invest(CountreEspionnage, 1600)

    cobras.invest(CountreEspionnage, cobras.money[getLCI()]) # STAFF IMPOSED
    advanceUntil(21, 12, 0) # NO PRINT (but they had a look)

    advanceUntil(21, 13, 9)
    pumas.invest(Ressources, 700)
    pumas.invest(Militaire, 350)
    pumas.invest(Art, 1000)
    pumas.invest(Tech, 1000)
    pumas.invest(CountreEspionnage, 2900)
    pumas.agents[5].extract()
    print(pumas.money[getLCI()])
    pumas.agents[5].train(800)
    pumas.agents[5].deploy(jaguars)

    grizzlis.invest(Ressources, grizzlis.money[getLCI()]) # STAFF IMPOSED

    advanceUntil(21, 13, 37)
    jaguars.invest(Tech, 2000)
    jaguars.invest(Militaire, 2000)
    jaguars.invest(Ressources, 2000)
    jaguars.invest(Art, 2000)
    jaguars.invest(CountreEspionnage, 3300)
    jaguars.agents[4].train(1000)
    jaguars.agents[4].deploy(pumas)
    jaguars.agents[9].sabotage(283)
    jaguars.agents[6].sabotage(700)
    jaguars.agents[2].recruit(Militaire)
    jaguars.agents[2].train(1000)
    jaguars.agents[2].deploy(cobras)
    jaguars.agents[0].recruit(Ressources)
    jaguars.agents[0].train(1000)
    jaguars.agents[0].deploy(pumas)

cprint('Game saved here at iteration ' + str(getLCI()), 'red', attrs=['bold', 'reverse']) 
# iter630 : added limited growth

advanceUntil(23, 21, 0) # PRINT


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
    # print(staff)
    print(pumas)
    print(grizzlis)
    print(cobras)
    print(jaguars)

    for f in range(len(factions)):
        plt.figure(f)
        plt.suptitle(factions[f].name)
        plotMoney = plt.subplot(711)
        plt.plot(t[1:getLCI()], factions[f].money[1:getLCI()])
        plt.setp(plotMoney.get_xticklabels(), visible=False)
        plt.ylabel('$')
        plotTech = plt.subplot(712, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].tech[1:getLCI()])
        plt.setp(plotTech.get_xticklabels(), visible=False)
        plt.ylabel('Tech')
        plotMilitary = plt.subplot(713, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].military[1:getLCI()])
        plt.setp(plotMilitary.get_xticklabels(), visible=False)
        plt.ylabel('Mil')
        plotRessources = plt.subplot(714, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].ressources[1:getLCI()])
        plt.setp(plotRessources.get_xticklabels(), visible=False)
        plt.ylabel('Res')
        plotArt = plt.subplot(715, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].art[1:getLCI()])
        plt.setp(plotArt.get_xticklabels(), visible=False)
        plt.ylabel('Art')
        plotCounterIntel = plt.subplot(716, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].counterIntel[1:getLCI()])
        plt.setp(plotCounterIntel.get_xticklabels(), visible=False)
        plt.ylabel('CE')
        plotPoints = plt.subplot(717, sharex=plotMoney)
        plt.plot(t[1:getLCI()], factions[f].points[1:getLCI()])
        plt.setp(plotPoints.get_xticklabels(), visible=True)
        plt.ylabel('#')
    plt.show()
else:
    print('')

# '''