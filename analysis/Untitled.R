library(ggplot2)
qin = read.csv('../model-control-chain/models/5year-test/QINs.txt', header=F)
actions = read.csv('../model-control-chain/models/5year-test/actions.txt', header=F)
plot(qin$V1, actions$V1)

#229.5 pt
png(filename='../../229-project/midreport/qout-qin.png', width=459, height=459, units='px')
ggplot(data=data.frame(qin = qin$V1, action=actions$V1), aes(qin, action)) + 
  geom_jitter(color=c('blue'), size=2) +
  xlab('Inflow') + 
  ylab('Chosen Action (Outflow)')+
  theme(axis.text.x = element_text(size=13)) +
  theme(axis.text.y = element_text(size=13)) +
  theme(axis.title.x = element_text(size=13)) +
  theme(axis.title.y = element_text(size=13))
dev.off()


rewards = read.csv('../model-control-chain/models/5year-test/rewards.txt', header=F)
rewards$V2
mean(abs(rewards$V2 - 223))
# 1.183 - generalization error

rewards = read.csv('../model-control-chain/stats/rewards.txt', header=F)
rewards$V2
mean(abs(rewards$V2 - 223))
# 4.471658 - error with no policy


delta = c(4.53227907,  2.61630698,  1.33862326,  1.34072558,  1.46636279,  1.46863256)
df = data.frame(delta, 0:5)
png(filename='../../229-project/midreport/training-error.png', width=459, height=459, units='px')
ggplot(data = df, aes(X0.5, delta)) +
 geom_line(color=c('blue')) +
  xlab('Iteration') + 
  theme(axis.text.x = element_text(size=13)) +
  theme(axis.text.y = element_text(size=13)) +
  theme(axis.title.x = element_text(size=13)) +
  theme(axis.title.y = element_text(size=13)) +
  ylab('Elevation Mean Abolute Error (m)')
dev.off()


