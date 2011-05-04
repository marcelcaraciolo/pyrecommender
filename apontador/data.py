import matplotlib.pyplot as plt
import numpy as np
import random

a = open('dataset.txt')

users = []
ratings = {}
places = []
ratingsUser = {}
ratingsPlace = {}

for linha in a:
    linha = linha.strip()
    try:
        user,place,rating = linha.split(',')
    except:
        print 'FAIL'
        continue
    
    if user not in users:
        users.append(user)
    if place not in places:
        places.append(place)
    if (user,place) not in ratings:
        ratings[(user,place)] = rating
        ratingsUser.setdefault(user,0)
        ratingsUser[user]+=1
        ratingsPlace.setdefault(place,0)
        ratingsPlace[place]+=1


'''
print '==== TOTAL ===='
print 'USERS: %d'  % len(users)
print 'RATINGS: %d' % len(ratings)
print 'PLACES: %d' % len(places)

print '===PLACES==='
p =  [  (user,place,ratings[(user,place)])  for user,place in ratings if ratingsPlace[place] > 1]
print 'RATINGS %d' % len(p)
print 'PLACES  %d'  % len([place  for place in ratingsPlace  if ratingsPlace[place] > 1])
users = []
for user,place,rating in p:
    if user not in users:
        users.append(user)
print 'USERS %d' % len(users)

'''


print '===USERS==='

f = open('final_dataset.txt', 'w')

pDict = {}

p =  [  pDict.update({(user,place): ratings[(user,place)]}) for user,place in ratings if ratingsUser[user] > 1]
print 'RATINGS %d' % len(pDict)
print 'USERS  %d'  % len([user  for user in ratingsUser  if ratingsUser[user] > 1])
places = {}
for user,place in pDict:
    places.setdefault(place,0)
    places[place]+=1
    f.write('%s,%s,%s\n' % (user,place,ratings[(user,place)]))
print 'PLACES  %d' %  len(places)


def plot_distribution():
    matrix = []
    pusers = [user  for user in ratingsUser  if ratingsUser[user] > 1]
    for user in pusers:
        matrix.append([ int(pDict[(user,place)])  if (user,place) in pDict else 0  for place in places])
    
    fig = plt.figure()
    plt.pcolormesh(np.array(matrix), cmap = plt.get_cmap('hot'))
    plt.colorbar() 
    plt.savefig('final_distribution.png')
    
