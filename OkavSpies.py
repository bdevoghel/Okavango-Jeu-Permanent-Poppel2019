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
    setLCI(0)
    setLCI(0) # LastComputedIteration = 0
else:
    with open('pickles/factions_upToIterX.pkl', 'rb') as infile: # DEFINE X !
        factions = pickle.load(infile)
    staff = factions[0]
    pumas = factions[1]
    grizzlis = factions[2]
    cobras = factions[3]
    jaguars = factions[4]
    with open('pickles/util_upToIterX.pkl', 'rb') as infile: # DEFINE X !
        util = pickle.load(infile)
    setLCI(util[0])


#######################################################################################################################

advanceUntil(15, 10, 0)
staff.invest(Tech, 100)
staff.invest(Art, 100)
pumas.invest(Militaire,100)
advanceUntil(16, 10, 0)
# staff.money[getLCI()] += 100
# advanceUntil(17, 10, 0)



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


#######################################################################################################################
######################################################## TESTS ########################################################
#######################################################################################################################

'''
advanceUntil(15, 1, 1)

staff.agents[5].recruit('Military')
staff.agents[5].train(5)
staff.agents[5].deploy('Pumas')
# print(staff.agents[5])
staff.agents[5].extract()
# staff.agents[2].deploy('Jaguars') # UserWarning: Failed to deploy Ocelot : agent not initiated
staff.agents[3].recruit('Tech')
staff.agents[3].deploy('Jaguars')

# print(staff)
# print(pumas)
# print(jaguars)

advanceUntil(15, 12, 1)

staff.invest('Art', 10000000)
pumas.invest('Tech',    10000000)


advanceUntil(16, 0, 1)

staff.invest('Art', 6000000)
pumas.invest('Tech',    6000000)

advanceUntil(17, 0, 1)

staff.invest('Military',  17000000)
pumas.invest('Tech', 6000000)

advanceUntil(18, 0, 1)

staff.invest('Military', 15000000)
pumas.invest('Tech', 6000000)

advanceUntil(20, 0, 1)

print('money staff :', factions[0].money[getLCI()])
print('money pumas :', factions[1].money[getLCI()])

'''
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

'''
plt.figure(2)
plt.suptitle('Pumas')
plotMoney = plt.subplot(511)
plt.plot(t[1:getLCI()], pumas.money[1:getLCI()])
plt.setp(plotMoney.get_xticklabels(), visible=False)
plt.ylabel('Fonds')
plotTech = plt.subplot(512, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.tech[1:getLCI()])
plt.setp(plotTech.get_xticklabels(), visible=False)
plt.ylabel('Technologie')
plotMilitary = plt.subplot(513, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.military[1:getLCI()])
plt.setp(plotMilitary.get_xticklabels(), visible=False)
plt.ylabel('Militaire')
plotRessources = plt.subplot(514, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.ressources[1:getLCI()])
plt.setp(plotRessources.get_xticklabels(), visible=False)
plt.ylabel('Ressources')
plotArt = plt.subplot(514, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.art[1:getLCI()])
plt.setp(plotRessources.get_xticklabels(), visible=False)
plt.ylabel('Art')
plotCounterIntel = plt.subplot(515, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.counterIntel[1:getLCI()])
plt.ylabel('Countre-espionnage')
'''

plt.show()

# '''