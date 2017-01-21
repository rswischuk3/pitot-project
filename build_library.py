import numpy as np
import matplotlib.pyplot as plt
import h5py as hf
from numpy import math 
import pickle
import operator
with open('tas', 'r') as fp:
	tas = pickle.load(fp)
with open('yaw', 'r') as f2:
	trident = pickle.load(f2)
with open('roll', 'r') as f3:
	roll = pickle.load(f3)
with open('pitch', 'r') as f4:
	pitch = pickle.load(f4)
with open('gs', 'r') as f4:
	gs = pickle.load(f4)
plt.plot(tas[5])
	
psi = []
theta = []
for r in range(10):
	psi.append(roll[r][::2])
	theta.append(pitch[r][::2])
total = 458016
DCM = np.zeros((3,total))
i = 0
for j in range(10):
	for k in range(psi[j].shape[0]):
		DCM[0,i] = math.sin(psi[j][k])*math.sin(theta[j][k])*math.cos(trident[j][k]*math.pi/180)-math.sin(trident[j][k]*math.pi/180)*math.cos(psi[j][k])
		DCM[1,i] = math.sin(psi[j][k])*math.sin(theta[j][k])*math.sin(trident[j][k]*math.pi/180)+math.cos(psi[j][k])*math.cos(trident[j][k]*math.pi/180)
		DCM[2,i] = math.sin(psi[j][k])*math.cos(theta[j][k])
		i=i+1
shape = psi[0].shape[0]+psi[1].shape[0]+psi[2].shape[0]

train = np.zeros((shape,5))
train[:,0] = np.append(trident[0],np.append(trident[1], trident[2]))
train[:,1] = np.append(theta[0], np.append(theta[1], theta[2]))
train[:,2] = np.append(psi[0], np.append(psi[1],psi[2]))
train[:,3] = np.append(gs[0], np.append(gs[1], gs[2]))
train[:,4] = np.append(tas[0], np.append(tas[1], tas[2]))

#test = [trident[5][5000], theta[5][5000], psi[5][5000], gs[5][5000], tas[5][5000]]




def euclidean(x1,x2,length = 4):
	distance = 0
	for i in range(length):
		if i==3:
			distance += 10*(x1[i]-x2[i])**2
		else:
			distance += (x1[i]-x2[i])**2
	return math.sqrt(distance)
def kNeighbors(trainSet, test, k):
	distances = []
	length = len(test)-1 # attributes: yaw, pitch, roll, ground speed, label: true airspeed
	for x in range(len(trainSet)):
		dist = euclidean(test, trainSet[x], length)
		distances.append((trainSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors #this will return the index of the closest point

test = [trident[5][5000], theta[5][5000], psi[5][5000], gs[5][5000], tas[5][5000]]
neighbors = kNeighbors(train, test, 4)

# est = np.zeros(psi[5].shape[0])
# for y in range(psi[5].shape[0]):
	# test = [trident[5][y], theta[5][y], psi[5][y], gs[5][y], tas[5][y]]
	# neighbors = kNeighbors(train,test,4)
	# avg = (neighbors[0][4]+neighbors[1][4]+neighbors[2][4]+neighbors[3][4])/4
	# est[y] = avg
# plt.plot(est)
# plt.plot(tas[5], label = 'true')
# plt.show()



	