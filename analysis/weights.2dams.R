weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
weights.dam2 = read.csv('../model-control-chain/stats/weights2.txt', header=FALSE)

plot.weights = function(weights.dam){
  par(mfrow=c(5,1))
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  elevation.high = as.numeric(weights.dam.end[(1:12)])
  plot(elevation.high)
  elevation.high = as.numeric(weights.dam.end[(1:12 + 24)])
  plot(elevation.high)
  elevation.ok = as.numeric(weights.dam.end[(1:12 + 48)])
  plot(elevation.ok)
  elevation.low = as.numeric(weights.dam.end[(1:12 + 36)])
  plot(elevation.low)
  elevation.low = as.numeric(weights.dam.end[(1:12 + 12)])
  plot(elevation.low)
}
plot.weights(weights.dam1)
plot.weights(weights.dam2)

plot.weights.all = function(weights.dam){
  par(mfrow=c(1,1))
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  plot(as.numeric(weights.dam.end), col='orange', lwd=2, xaxt='n')
  axis(1, at=12*(0:(ceiling(ncol(weights.dam.end) / 12))))
}

plot.weights.combined = function(weights.dam){
  par(mfrow=c(1,1))
  colors = rainbow(5)
  weights.dam.end = weights.dam[nrow(weights.dam1),]
  plot(as.numeric(weights.dam.end[(1:12)]), col=colors[1], lwd=2,
       ylim = c(min(weights.dam.end, na.rm=T),max(weights.dam.end, na.rm=T)))
  points(as.numeric(weights.dam.end[(1:12 + 24)]), col=colors[2],lwd=2)
  points(as.numeric(weights.dam.end[(1:12 + 48)]), col=colors[3],lwd=2)
  points(as.numeric(weights.dam.end[(1:12 + 36)]), col=colors[4],lwd=2)
  points(as.numeric(weights.dam.end[(1:12 + 12)]), col=colors[5],lwd=2)
  legend('topleft', c('max high', 'target high', 'ok', 'target low', 'low'), col=colors, pch=1,lwd=2 )
}
plot.weight.evolution = function (weights){
  par(mfrow=c(1,1))
  plot(weights$V1, typ='l', xaxt='n', 
       ylim=c(min(weights[,1:12], na.rm=T),max(weights[,1:12], na.rm=T)))
  axis(1, at=365*(0:(ceiling(nrow(rewards) / 365))))
  lines(weights$V2)
  lines(weights$V3)
  lines(weights$V4)
  lines(weights$V5)
  lines(weights$V6)
  lines(weights$V7)
  lines(weights$V8)
  lines(weights$V9)
  lines(weights$V10)
  lines(weights$V11)
  lines(weights$V12)
}


weights.dam1 = read.csv('../model-control-chain/stats/weights1.txt', header=FALSE)
weights.dam2 = read.csv('../model-control-chain/stats/weights2.txt', header=FALSE)
plot.weights.combined(weights.dam1)
plot.weights.combined(weights.dam2)

plot.weight.evolution(weights.dam1)
weights.dam2 = read.csv('../model-control-chain/stats/weights2.txt', header=FALSE)
plot.weight.evolution(weights.dam2)

plot.weights.all(weights.dam1)
plot.weights.all(weights.dam2)


rewards = read.csv('../model-control-chain/stats/rewards.txt', header=FALSE)
names(rewards) = c('reward1', 'reward2',
                   'elevation1', 'elevation2' )
par(mfrow=c(2,1))
plot(rewards$elevation1, typ='l', xaxt='n', ylim=c(215,230))
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
abline(h=225,col='red')
abline(h=220,col='blue')
plot(rewards$elevation2, typ='l', xaxt='n', ylim=c(215,230))
axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
abline(h=225,col='red')
abline(h=220,col='blue')



par(mfrow=c(2,1))
plot(rewards$reward1, typ='l', xaxt='n')
plot(rewards$reward2, typ='l', xaxt='n')

