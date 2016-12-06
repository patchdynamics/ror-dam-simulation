import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ACTIONS_FILE = "../model-control-chain/stats/actions.txt"
REWARDS_FILE = "../model-control-chain/stats/rewards.txt"#"../model-control-chain/models/rewards_2014train.txt"
QIN_FILE = "../model-control-chain/stats/QINs.txt"

NUM_DAYS_PER_YEAR = 215
NUM_TRAIN_REPEATS = 0
NUM_TRAIN_ITS = NUM_DAYS_PER_YEAR * NUM_TRAIN_REPEATS
TARGET_HIGH_ELEVATION = 223.5
TARGET_LOW_ELEVATION = 221.5

def calcAvgDeviations(elevations):
    elevationsHigh = elevations > TARGET_HIGH_ELEVATION
    elevationsLow = elevations < TARGET_LOW_ELEVATION
    deviations = np.zeros_like(elevations)
    deviations[elevationsHigh] = elevations[elevationsHigh] - TARGET_HIGH_ELEVATION
    deviations[elevationsLow] = TARGET_LOW_ELEVATION - elevations[elevationsLow]
    numYears = len(elevations)/NUM_DAYS_PER_YEAR
    avgDev = np.zeros(numYears)
    for i in range(numYears):
        avgDev[i] = np.mean(deviations[i*NUM_DAYS_PER_YEAR:(i+1)*NUM_DAYS_PER_YEAR])
    return avgDev

with open(ACTIONS_FILE) as f:
    actions = np.genfromtxt(f, delimiter=",", usecols=0)
with open(REWARDS_FILE) as f:
    rewardsElevs = np.genfromtxt(f, delimiter=",")
    print rewardsElevs.shape
    rewards = rewardsElevs[:,0]
    elevations = rewardsElevs[:,1]
with open(QIN_FILE) as f:
    qins = np.genfromtxt(f, delimiter=",", usecols=0)

# Plot best action vs. elevation
fig = plt.figure()
ax3d = fig.add_subplot(111, projection='3d')
ax3d.scatter(elevations[NUM_TRAIN_ITS:], qins[NUM_TRAIN_ITS:], actions[NUM_TRAIN_ITS:] )
ax3d.set_xlabel('Elevation')
ax3d.set_ylabel('Qin')
ax3d.set_zlabel('Qout')
plt.show()

exit()

plt.scatter(elevations[NUM_TRAIN_ITS:], actions[NUM_TRAIN_ITS:])
plt.show()

# Plot best action vs. QIN_FILE
plt.scatter(qins[NUM_TRAIN_ITS:], actions[NUM_TRAIN_ITS:])
plt.show()

# Plot deviation from target elevation over training
avgDev = calcAvgDeviations(elevations[:NUM_TRAIN_ITS])
plt.plot(avgDev)
plt.show()

# Plot rewards over training
numYears = len(rewards)/NUM_DAYS_PER_YEAR
avgReward = np.zeros(numYears)
for i in range(numYears):
    avgReward[i] = np.mean(rewards[i*NUM_DAYS_PER_YEAR:(i+1)*NUM_DAYS_PER_YEAR])
plt.plot(avgReward)
plt.show

# Plot deviations from target elevation over testing
avgDev = calcAvgDeviations(elevations[NUM_TRAIN_ITS:])
print avgDev
plt.plot(avgDev)
plt.show() #TODO: This doesn't make sense to plot as such since no meaning to the various times. Maybe just report avgDev for different test years (as compared to random policy)
