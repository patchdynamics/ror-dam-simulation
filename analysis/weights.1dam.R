weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)

numActions = 18
#elevation weights
# indices = 0:(numActions-1) * numStates  + 1
indices = 1:numActions

#starting weights
#weights.dam1.start = weights.dam1[1,]
#elevation.high = as.numeric(weights.dam1.start[indices])
#plot(elevation.high, ylim=c(-1,1))

plot.weights.combined = function(weights.dam){
  par(mfrow=c(1,1))
  colors = rainbow(5)
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  plot(as.numeric(weights.dam.end[(1:numActions)]), col=colors[1], lwd=2,
       ylim = c(min(weights.dam.end, na.rm=T),max(weights.dam.end, na.rm=T)))
  points(as.numeric(weights.dam.end[(1:numActions + 2*numActions)]), col=colors[2],lwd=2)
  points(as.numeric(weights.dam.end[(1:numActions + 4*numActions)]), col=colors[3],lwd=2)
  points(as.numeric(weights.dam.end[(1:numActions + 3*numActions)]), col=colors[4],lwd=2)
  points(as.numeric(weights.dam.end[(1:numActions + numActions)]), col=colors[5],lwd=2)
  legend('topleft', c('max high', 'target high', 'ok', 'target low', 'low'), col=colors, pch=1,lwd=2 )
}


weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
plot.weights.combined(weights.dam1)


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


weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
plot.weights.all = function(weights.dam){
  par(mfrow=c(1,1))
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  plot(as.numeric(weights.dam.end), col='orange', lwd=2, xaxt='n')
  axis(1, at=numActions*(0:(ceiling(ncol(weights.dam.end) / numActions))))
}
plot.weights.all(weights.dam1)


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

