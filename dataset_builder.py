import pickle

f = open('final_dataset.txt')
o = open('model.pk1', 'wb')
model = {}
for line in f:
	line = line.strip()
	userID,itemID,rating = line.split(',')
	rating = float(rating)
	model.setdefault(userID,{})
	model[userID][itemID] = rating

pickle.dump(model,o)
o.close()
