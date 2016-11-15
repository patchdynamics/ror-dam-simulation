weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
weights.dam2 = read.csv('../model-control-chain/stats/weights2.txt', header=FALSE)
weights.dam3 = read.csv('../model-control-chain/stats/weights3.txt', header=FALSE)
weights.dam4 = read.csv('../model-control-chain/stats/weights4.txt', header=FALSE)

rewards = read.csv('../model-control-chain/stats/rewards.txt', header=FALSE)
names(rewards) = c('reward1', 'reward2', 'reward3', 'reward4', 
                   'elevation1','elevation2','elevation3','elevation4' )

par(mfrow=c(2,1))
plot(rewards$reward1, typ='l')
plot(rewards$elevation1, typ='l')
abline(h=225,col='red')
abline(h=220,col='blue')


numActions = 12
numStates = 2
#elevation weights
# indices = 0:(numActions-1) * numStates  + 1
indices = 1:12

#starting weights
weights.dam1.start = weights.dam1[1,]
elevation.high = as.numeric(weights.dam1.start[indices])
plot(elevation.high)

# get last timestep and evalute weights
weights.dam1.end = weights.dam1[nrow(weights.dam1),]
elevation.high = as.numeric(weights.dam1.end[1:12])
plot(elevation.high)

par(mfrow=c(2,1))
plot(weights.dam1[,1])


plot(weights.dam1[,2])