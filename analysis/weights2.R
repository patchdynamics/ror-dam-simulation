weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)

numActions = 12
numStates = 2
#elevation weights
# indices = 0:(numActions-1) * numStates  + 1
indices = 1:12

#starting weights
#weights.dam1.start = weights.dam1[1,]
#elevation.high = as.numeric(weights.dam1.start[indices])
#plot(elevation.high, ylim=c(-1,1))

# get last timestep and evalute weights
weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
par(mfrow=c(5,1))
weights.dam1.end = weights.dam1[nrow(weights.dam1),]
elevation.high = as.numeric(weights.dam1.end[(1:12)])
plot(elevation.high)
elevation.high = as.numeric(weights.dam1.end[(1:12 + 24)])
plot(elevation.high)
elevation.ok = as.numeric(weights.dam1.end[(1:12 + 48)])
plot(elevation.ok)
elevation.low = as.numeric(weights.dam1.end[(1:12 + 36)])
plot(elevation.low)
elevation.low = as.numeric(weights.dam1.end[(1:12 + 12)])
plot(elevation.low)


weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
par(mfrow=c(1,1))
plot(weights.dam1$V1, typ='l', xaxt='n', 
     ylim=c(min(weights.dam1[,1:12], na.rm=T),max(weights.dam1[,1:12], na.rm=T)))
axis(1, at=365*(0:(ceiling(nrow(rewards) / 365))))
lines(weights.dam1$V2)
lines(weights.dam1$V3)
lines(weights.dam1$V4)
lines(weights.dam1$V5)
lines(weights.dam1$V6)
lines(weights.dam1$V7)
lines(weights.dam1$V8)
lines(weights.dam1$V9)
lines(weights.dam1$V10)
lines(weights.dam1$V11)
lines(weights.dam1$V12)



rewards = read.csv('../model-control-chain/stats/rewards.txt', header=FALSE)
names(rewards) = c('reward1', 
                   'elevation1' )

par(mfrow=c(2,1))
plot(rewards$reward1, typ='l', xaxt='n')
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
plot(rewards$elevation1, typ='l', xaxt='n', ylim=c(215,230))
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
abline(h=225,col='red')
abline(h=220,col='blue')

