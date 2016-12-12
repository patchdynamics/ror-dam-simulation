library(xts)

knn.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/KNN-lastday.txt', header=FALSE)  
linear.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/Linear-lastday.txt', header=FALSE)   
lookup.lastday = read.csv('/Users/matthewxi/machine-learning-project/229-project/poster/data/Lookup-lastday.txt', header=FALSE)  

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