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
else:
    with open('pickels/factions_upToIterX.pkl', 'rb') as infile: # DEFINE X !
        factions = pickle.load(infile)
    staff = factions[0]
    pumas = factions[1]
    grizzlis = factions[2]
    cobras = factions[3]
    jaguars = factions[4]
    with open('pickels/util_upToIterX.pkl', 'rb') as infile: # DEFINE X !
        util = pickle.load(infile)
    setLCI(util[0])


#######################################################################################################################

advanceUntil(15, 18, 46)
staff.invest('HighTech', 10000000)
advanceUntil(16, 10, 45)

#######################################################################################################################

if saveState:
    print('Are you sure you want to save the new state up to iteration ' + str(getLCI()) + ' ? (yes/no)')
    userInput = input()
    if userInput == 'yes':
        factionsFileName = 'pickels/factions_upToIter' + str(getLCI()) + '.pkl'
        with open(factionsFileName, 'wb') as outfile:
            pickle.dump(factions, outfile, pickle.HIGHEST_PROTOCOL)
        utilFileName = 'pickels/util_upToIter' + str(getLCI()) + '.pkl'
        with open(utilFileName, 'wb') as outfile:
            pickle.dump([getLCI()], outfile, pickle.HIGHEST_PROTOCOL)
        print('Stated saved up to iteration ' + str(getLCI()) )
    else:
        print('Stated not saved')


#######################################################################################################################
######################################################## TESTS ########################################################
#######################################################################################################################


advanceUntil(15, 1, 1)

staff.agents[5].recruit('Spatial')
staff.agents[5].train(5)
staff.agents[5].deploy('Pumas')
# print(staff.agents[5])
staff.agents[5].extract()
# staff.agents[2].deploy('Jaguars') # UserWarning: Failed to deploy Ocelot : agent not initiated
staff.agents[3].recruit('HighTech')
staff.agents[3].deploy('Jaguars')

# print(staff)
# print(pumas)
# print(jaguars)

advanceUntil(15, 12, 1)

staff.invest('Alimentaire', 10000000)
pumas.invest('HighTech',    10000000)

'''

advanceUntil(16, 0, 1)

staff.invest('Alimentaire', 6000000)
pumas.invest('HighTech',    6000000)

advanceUntil(17, 0, 1)

staff.invest('Spatial',  17000000)
pumas.invest('HighTech', 6000000)

advanceUntil(18, 0, 1)

staff.invest('Spatial', 15000000)
pumas.invest('HighTech', 6000000)

advanceUntil(20, 0, 1)

print('money staff :', factions[0].money[getLCI()])
print('money pumas :', factions[1].money[getLCI()])

'''
plt.figure(1)
plt.suptitle('Staff')
plotMoney = plt.subplot(511)
plt.plot(t[1:getLCI()], staff.money[1:getLCI()])
plt.setp(plotMoney.get_xticklabels(), visible=False)
plt.ylabel('Money')
plotTech = plt.subplot(512, sharex=plotMoney)
plt.plot(t[1:getLCI()], staff.tech[1:getLCI()])
plt.setp(plotTech.get_xticklabels(), visible=False)
plt.ylabel('Tech')
plotSpatial = plt.subplot(513, sharex=plotMoney)
plt.plot(t[1:getLCI()], staff.spatial[1:getLCI()])
plt.setp(plotSpatial.get_xticklabels(), visible=False)
plt.ylabel('Spatial')
plotFood = plt.subplot(514, sharex=plotMoney)
plt.plot(t[1:getLCI()], staff.food[1:getLCI()])
plt.setp(plotFood.get_xticklabels(), visible=False)
plt.ylabel('Food')
plotMilitary = plt.subplot(515, sharex=plotMoney)
plt.plot(t[1:getLCI()], staff.military[1:getLCI()])
plt.ylabel('Military')

plt.figure(2)
plt.suptitle('Pumas')
plotMoney = plt.subplot(511)
plt.plot(t[1:getLCI()], pumas.money[1:getLCI()])
plt.setp(plotMoney.get_xticklabels(), visible=False)
plt.ylabel('Money')
plotTech = plt.subplot(512, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.tech[1:getLCI()])
plt.setp(plotTech.get_xticklabels(), visible=False)
plt.ylabel('Tech')
plotSpatial = plt.subplot(513, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.spatial[1:getLCI()])
plt.setp(plotSpatial.get_xticklabels(), visible=False)
plt.ylabel('Spatial')
plotFood = plt.subplot(514, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.food[1:getLCI()])
plt.setp(plotFood.get_xticklabels(), visible=False)
plt.ylabel('Food')
plotMilitary = plt.subplot(515, sharex=plotMoney)
plt.plot(t[1:getLCI()], pumas.military[1:getLCI()])
plt.ylabel('Military')

plt.show()

# '''