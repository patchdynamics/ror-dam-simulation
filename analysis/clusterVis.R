# old but good
# nolose3.elevation.knn0
# nolose.elevation.knn0


plot.rewards = function(rewards, top=230, bottom=210, temperatures=numeric(), tins=numeric()) {
  names(rewards) = c('reward1', 'elevation1' )
  par(mfrow=c(2,1))
  plot(rewards$reward, typ='p', xaxt='n')
  axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
  if(length(temperatures) > 0) {
    #metric = tins - temperatures
    #metric = rollmean(metric, 244 - 90)
    #par(new=T)
    #plot(metric)
    
    plot(temperatures$V1, typ='l', col='pink',  yaxt='n', xaxt='n')  
    axis(side=4)
    par(new=T)
  }
  if(length(tins) > 0) {
    lines(tins$V1, col='red')  
    axis(side=4)
    par(new=T)
  }
  plot(rewards$elevation, typ='l', xaxt='n', ylim=c(180,250))
  axis(1, at=215*(0:(ceiling(nrow(rewards) / 215))))
  abline(h=top,col='red')
  abline(h=bottom,col='blue')
}


showRewardStatus = function(tag, tail.num=NA){
  rewards = read.csv(paste0('~/memex/learning/',tag,'/stats/rewards.txt'), header=FALSE)
  temperatures = read.csv(paste0('~/memex/learning/',tag,'/stats/temperatures1.txt'), header=FALSE)
  tins = read.csv(paste0('~/memex/learning/',tag,'/stats/TINs.txt'), header=FALSE)
  if(!is.na(tail.num)){
    rewards = tail(rewards, tail.num)
    temperatures = tail(temperatures, tail.num)
    tins = tail(tins, tail.num)
  }
  names(rewards)
  plot.rewards(rewards, top=235, bottom=220, temperatures, tins)
  return(data.frame(temperatures=temperatures$V1, tins=tins$V1, rewards=rewards$V1, elevations=rewards$V2))
}

showRewardStatusOld = function(tag, tail.num=NA){
  rewards = read.csv(paste0('~/memex/learning/',tag,'/stats/rewards.txt'), header=FALSE)
  temperatures = read.csv(paste0('~/memex/learning/',tag,'/stats/temperatures1.txt'), header=FALSE)
  #tins = read.csv(paste0('~/memex/learning/',tag,'/stats/TINs.txt'), header=FALSE)
  if(!is.na(tail.num)){
    rewards = tail(rewards, tail.num)
    temperatures = tail(temperatures, tail.num)
    tins = tail(tins, tail.num)
  }
  names(rewards)
  plot.rewards(rewards, top=235, bottom=220, temperatures, tins)
  return(data.frame(temperatures=temperatures$V1, tins=tins$V1))
}

showRewardStatusOld('lookup.anneal.one',600)

showLastDay = function(tag){
  lastday = read.csv(paste0('~/memex/learning/',tag,'/stats/lastday.txt'), header=FALSE)
  plot(lastday$V1)
}

getTemperatureMetrics = function(df, start=0, end){
  if(start != 0){
    df = tail(df,start)
  }
  df$ind = 1:nrow(df)
  df$epoch = floor(df$ind / (end-90))
  df$metric = df$temperatures - df$tins
  df$level2 = df$metric > 2 
  df$level1 = df$metric > 1
  return(df)
}

showTemperatureMetric = function(df, start=0){
  par(mfrow=c(2,1))
  df = getTemperatureMetrics(df, start)
  plot(df$metric)
  metric = summarise(group_by(df, epoch), mean= mean(metric), sd = sd(metric), level1=sum(level1), level2=sum(level2))
  print(metric)
  plot(metric$mean)
  par(new=T)
  plot(metric$sd, yaxt='n', col='orange')
  axis(side=4)
  plot(metric$level1, main='Level 1', ylab='# days')  
  plot(metric$level2, main='Level 2', ylab='# days')  
}

qin = read.csv('~/memex/ror-dam-simulation-lookup/model-control-chain/stats/QINs.txt')
qin[qin==0] = NA
qout = read.csv('~/memex/ror-dam-simulation-lookup/model-control-chain/stats/actions.txt')
par(mfrow=c(1,1))
plot(qin[,1], col='orange', typ='l',ylim=c(0,3000))
lines(qout[,1], col='blue')



df = showRewardStatus('multicore/elevation.linear0')
showRewardStatus('multicore/elevation.linear1')
showLastDay('multicore/elevation.linear0')

df = showRewardStatus('multicore/elevation.lookup0')
showRewardStatus('multicore/elevation.lookup1')
showLastDay('multicore/elevation.lookup0')

df = showRewardStatus('multicore/elevation.knn0')
showLastDay('multicore/elevation.knn0')
#showRewardStatus('multicore/elevation.knn1')

df = showRewardStatus('multicore/nolose.elevation.knn0',1000)
# plot departure from elevation, 227.5  MAE
showLastDay('multicore/elevation.nolose.knn0')
showRewardStatus('multicore/nolose.elevation.knn1')
showRewardStatus('multicore/nolose.elevation.knn2')
showRewardStatus('multicore/nolose.elevation.knn3')
showRewardStatus('multicore/nolose.elevation.knn4')
showRewardStatus('multicore/nolose.elevation.knn5')
showRewardStatus('multicore/nolose.elevation.knn6')


df = showRewardStatus('multicore/nolose2.elevation.knn0')
df = showRewardStatus('multicore/nolose2.elevation.knn1')

df = showRewardStatus('multicore/nolose3.elevation.knn0')
df = showRewardStatus('multicore/nolose3.elevation.linear0')
df = showRewardStatus('multicore/nolose3.elevation.lookup0')

df = showRewardStatus('multicore/time.elevation.linear0')
df = showRewardStatus('multicore/time.elevation.lookup0')


df.knn = showRewardStatus('multicore/anneal.elevation.knn0')
showElevationMetric(df.knn, 220 - 90, 227.5)
df.linear = showRewardStatus('multicore/anneal.elevation.linear0')
showElevationMetric(df.linear, 220 - 90, 227.5)
df.lookup = showRewardStatus('multicore/anneal.elevation.lookup0')
showElevationMetric(df.lookup, 220 - 90, 227.5)


df.knn = showRewardStatus('multicore/epsilon.elevation.knn0')
showElevationMetric(df.knn, 220 - 90, 227.5)
df.linear = showRewardStatus('multicore/epsilon.elevation.linear0')
showElevationMetric(df.linear, 220 - 90, 227.5)
df.lookup = showRewardStatus('multicore/epsilon.elevation.lookup0')
showElevationMetric(df.lookup, 220 - 90, 227.5)


df.randow = showRewardStatus('multicore/random.linear0')

df.knn = showRewardStatus('multicore/nolose3.elevation.knn0')
showElevationMetric(df.knn, 220 - 90, 227.5)
df.linear = showRewardStatus('multicore/nolose3.elevation.linear0')
showElevationMetric(df.linear, 220 - 90, 227.5)
df.lookup = showRewardStatus('multicore/nolose3.elevation.lookup0')
showElevationMetric(df.lookup, 220 - 90, 227.5)

metric.linear = getElevationMetric(df.linear, 220 - 90, 227.5)
metric.lookup = getElevationMetric(df.lookup, 220 - 90, 227.5)
metric.knn = getElevationMetric(df.knn, 220 - 90, 227.5)

metric.linear = head(metric.linear,-1)
metric.lookup = head(metric.lookup,-1)
metric.knn = head(metric.knn,-1)
metric.first = (metric.linear$mean[1] + metric.lookup$mean[2] + metric.knn$mean[2])/3

metric.linear$mean[1] = metric.first
metric.lookup$mean[1] = metric.first
metric.knn$mean[1] = metric.first

plot.new()
par(mfrow=c(1,1))
par(mar=c(4,4,4,4))
par(bg=NA) 
cex = 2
plot(metric.linear$epoch, metric.linear$mean, 
     typ='l', col='blue', lwd=4, ylim=c(0,40),
     #xlab='Training Epoch', ylab='Mean Absolute Distance from Target',
     xlab='', ylab='',
     cex.axis=cex, cex.lab=cex)
lines(metric.lookup$epoch, metric.lookup$mean, typ='l', col='red', lwd=4)
lines(metric.knn$epoch, metric.knn$mean, typ='l', col='orange', lwd=4)
legend('topright', legend=c('Linear', 'Lookup', 'KNN'),
       lwd=4, col=c('blue', 'red', 'orange'), cex=cex)


getElevationMetric = function(df, epoch.len, target, start=0){
  if(start != 0){
    df = tail(df,start)
  }
  df$ind = 1:nrow(df)
  df$epoch = floor(df$ind / (epoch.len))
  df$ae = abs(df$elevations - target)
  metric = summarise(group_by(df, epoch), mean= mean(ae), sd = sd(ae))
  return(metric)
}

showElevationMetric = function(df, epoch.len, target, start=0){
  par(mfrow=c(1,2)) 
  metric = getElevationMetric(df, epoch.len, target, start)
  print(metric)
  plot(metric$mean)
  plot(metric$sd, yaxt='n', col='orange')
  axis(side=4)
}

#
# We should be plotting actions vs. elevation as well.
#

df = showRewardStatus('wb1-learning')


df = showRewardStatus('multicore/experimental.lineartemp0')
showTemperatureMetric(df, -409)
showRewardStatus('multicore/experimental.lineartemp1')

df = showRewardStatus('multicore/experimental.lookuptemp0')
showTemperatureMetric(df, -94)
showRewardStatus('multicore/experimental.lookuptemp1')

df = showRewardStatus('multicore/experimental.knntemp0')
showTemperatureMetric(df)
showRewardStatus('multicore/experimental.knntemp1')


df = showRewardStatus('multicore/negtemp.knntemp0')
showTemperatureMetric(df)


# plots
df = showRewardStatus('multicore/experimental.lineartemp0')
df.linear = getTemperatureMetrics(df, -409)
metric.linear = summarise(group_by(df.linear, epoch), mean= mean(metric), sd = sd(metric), level1=sum(level1), level2=sum(level2))
df = showRewardStatus('multicore/experimental.lookuptemp0')
df.lookup = getTemperatureMetrics(df, -94)
metric.lookup = summarise(group_by(df.lookup, epoch), mean= mean(metric), sd = sd(metric), level1=sum(level1), level2=sum(level2))
df = showRewardStatus('multicore/experimental.knntemp0')
df.knn = getTemperatureMetrics(df)
metric.knn = summarise(group_by(df.knn, epoch), mean= mean(metric), sd = sd(metric), level1=sum(level1), level2=sum(level2))

level2.first = (metric.linear$level1[1] + metric.lookup$level1[2] + metric.knn$level1[2])/3

metric.linear = head(metric.linear,-1)
metric.lookup = head(metric.lookup,-1)
metric.knn = head(metric.knn,-1)

metric.linear$level2[1] = level2.first
metric.lookup$level2[1] = level2.first
metric.knn$level2[1] = level2.first

#1100x1100
png(filename='temp.learning.curve2.png', width=1100, height=1100, units='px')
par(mfrow=c(1,1))
par(mar=c(4,4,4,4))
par(bg=NA) 
cex = 2
plot(metric.linear$epoch*5, metric.linear$level2, 
     typ='l', col='blue', lwd=4, ylim=c(0,40),
     #xlab='Training Epoch', ylab='Days Outflow Temperature Excedes Inflow By Two Degrees',
     xlab='', ylab='',
     cex.axis=cex, cex.lab=cex)
lines(metric.lookup$epoch*5, metric.lookup$level2, typ='l', col='red', lwd=4)
lines(metric.knn$epoch*5, metric.knn$level2, typ='l', col='orange', lwd=4)
legend('topright', legend=c('Linear', 'Lookup', 'KNN'),
       lwd=4, col=c('blue', 'red', 'orange'), cex=cex)
dev.off()

ggplot() +
  geom_line(data=metric.linear, aes(x=epoch, y=level2, col='blue')) +
  geom_line(data=metric.lookup, aes(x=epoch, y=level2, color='red')) +
  geom_line(data=metric.linear, aes(x=epoch, y=level2, color='orange')) +
  theme_classic()


ggplot(data = df.metrics, aes(X0.5, delta)) +
  geom_line(color=c('blue')) +
  xlab('Iteration') + 
  theme(axis.text.x = element_text(size=13)) +
  theme(axis.text.y = element_text(size=13)) +
  theme(axis.title.x = element_text(size=13)) +
  theme(axis.title.y = element_text(size=13)) +
  ylab('Elevation Mean Abolute Error (m)')


knn.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/KNN-lastday.txt', header=FALSE)  
linear.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/Linear-lastday.txt', header=FALSE)   
lookup.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/Lookup-lastday.txt', header=FALSE)  
plot(knn.lastday$V1)

metric.knn = data.frame(epoch=1:(nrow(knn.lastday)-24), rollmean=rollmean(knn.lastday$V1,25))
metric.linear = data.frame(epoch=1:(nrow(linear.lastday)-24), rollmean=rollmean(linear.lastday$V1,25))
metric.lookup = data.frame(epoch=1:(nrow(lookup.lastday)-24), rollmean=rollmean(lookup.lastday$V1,25))

metric.first = (metric.linear$rollmean[1] + metric.lookup$rollmean[2] + metric.knn$rollmean[2])/3

metric.linear$rollmean[1] = metric.first
metric.lookup$rollmean[1] = metric.first
metric.knn$rollmean[1] = metric.first


#png(filename='elev.learning.curve2.png', width=1100, height=1100, units='px')
# just export using Rstudio
par(mfrow=c(1,1))
par(mar=c(4,4,4,4))
par(bg=NA) 
cex = 2
plot(metric.linear$epoch, metric.linear$rollmean-90, 
     typ='l', col='blue', lwd=4, ylim=c(20,130), xlim=c(0,800),
     #xlab='Training Epoch', ylab='Days Outflow Temperature Excedes Inflow By Two Degrees',
     xlab='', ylab='',
     cex.axis=cex, cex.lab=cex)
lines(metric.lookup$epoch, metric.lookup$rollmean-90, typ='l', col='red', lwd=4)
lines(metric.knn$epoch, metric.knn$rollmean-90, typ='l', col='orange', lwd=4)
abline(h=126, lwd=3, col='cyan3')
text(75,128, 'Success', cex=1.8)
#legend('topright', legend=c('Linear', 'Lookup', 'KNN'),
#       lwd=4, col=c('blue', 'red', 'orange'), cex=cex)
#dev.off()



plot(linear.lastday$V1)
plot(lookup.lastday$V1)

