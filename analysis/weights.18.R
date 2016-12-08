weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)

numActions = 18
numStates = 2


#starting weights
#weights.dam1.start = weights.dam1[1,]
#elevation.high = as.numeric(weights.dam1.start[indices])
#plot(elevation.high, ylim=c(-1,1))

# get last timestep and evalute weights
weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
par(mfrow=c(5,1))
weights.dam1.end = weights.dam1[nrow(weights.dam1),]
elevation.high = as.numeric(weights.dam1.end[(1:numActions)])
plot(elevation.high)
elevation.high = as.numeric(weights.dam1.end[(1:numActions + 2*numActions)])
plot(elevation.high)
elevation.ok = as.numeric(weights.dam1.end[(1:numActions + 4*numActions)])
plot(elevation.ok)
elevation.low = as.numeric(weights.dam1.end[(1:numActions + 3*numActions)])
plot(elevation.low)
elevation.low = as.numeric(weights.dam1.end[(1:numActions + numActions)])
plot(elevation.low)

plot.weights(weights.dam1,18)

weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
par(mfrow=c(1,1))
plot(weights.dam1$V1, typ='l', xaxt='n', 
     ylim=c(min(weights.dam1[,1:numActions], na.rm=T),max(weights.dam1[,1:numActions], na.rm=T)))
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




#rewards = read.csv('~/memex/stats/rewards.txt', header=FALSE)

plot.rewards = function(rewards, top=230, bottom=210, temperatures=NA) {
  
names(rewards) = c('reward1', 'elevation1' )
par(mfrow=c(2,1))
#plot(tail(rollapply(rewards$reward,215,mean),10000), typ='l', xaxt='n')
plot(rewards$reward, typ='p', xaxt='n')
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
#plot(tail(rewards$elevation1,10000), typ='l', xaxt='n', ylim=c(205,240))

if(!is.na(temperatures)) {
  plot(temperatures$V1, typ='l', col='pink',  yaxt='n', xaxt='n')  
  axis(side=4)
  par(new=T)
}
plot(rewards$elevation, typ='l', xaxt='n', ylim=c(205,240))
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
abline(h=top,col='red')
abline(h=bottom,col='blue')

}

rewards = read.csv('../model-control-chain/stats/rewards.txt', header=FALSE)
rewards = tail(rewards,400)
temperatures = read.csv('../model-control-chain/stats/temperatures1.txt', header=FALSE)
temperatures = tail(temperatures,400)
plot.rewards(rewards, top=225, bottom=215, temperatures)
weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
plot(as.numeric(tail(weights.dam1,1)))
lastday = read.csv('../model-control-chain/stats/lastday.txt', header=FALSE)
plot(lastday$V1)

temperatures = read.csv('../model-control-chain/stats/temperatures1.txt', header=FALSE)
#plot(temperatures$V1, typ='l')  


qin = tail(read.csv('../model-control-chain/stats/QINs.txt'),200)
qin[qin==0] = NA
qout = tail(read.csv('../model-control-chain/stats/actions.txt'),200)
par(mfrow=c(1,1))
plot(qin[,1], col='orange', typ='l',ylim=c(0,3000))
lines(qout[,1], col='blue')


#lookup (annealling)
rewards = read.csv('~/memex/ror-dam-simulation2/model-control-chain/stats/rewards.txt', header=FALSE)
plot.rewards(rewards, top=225, bottom=215)
lastday = read.csv('~/memex/ror-dam-simulation2/model-control-chain/stats/lastday.txt', header=FALSE)
plot(lastday$V1)

qin = read.csv('~/memex/ror-dam-simulation-lookup/model-control-chain/stats/QINs.txt')
qin[qin==0] = NA
qout = read.csv('~/memex/ror-dam-simulation-lookup/model-control-chain/stats/actions.txt')
par(mfrow=c(1,1))
plot(qin[,1], col='orange', typ='l',ylim=c(0,3000))
lines(qout[,1], col='blue')

#default (not annealing)
rewards = read.csv('~/memex/ror-dam-simulation/model-control-chain/stats/rewards.txt', header=FALSE)
temperatures = read.csv('~/memex/ror-dam-simulation/model-control-chain/stats/temperatures1.txt', header=FALSE)
plot.rewards(rewards, top=225, bottom=215, temperatures)
lastday = read.csv('~/memex/ror-dam-simulation/model-control-chain/stats/lastday.txt', header=FALSE)
plot(lastday$V1)


plot.weights = function(weights.dam, numActions){
  par(mfrow=c(5,1))
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  elevation.high = as.numeric(weights.dam.end[(1:numActions)])
  plot(elevation.high)
  elevation.high = as.numeric(weights.dam.end[(1:numActions + numActions*2)])
  plot(elevation.high)
  elevation.ok = as.numeric(weights.dam.end[(1:numActions + numActions*4)])
  plot(elevation.ok)
  elevation.low = as.numeric(weights.dam.end[(1:numActions + numActions*3)])
  plot(elevation.low)
  elevation.low = as.numeric(weights.dam.end[(1:numActions + numActions)])
  plot(elevation.low)
}


