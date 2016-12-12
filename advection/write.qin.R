library(chron)
advection = read.csv('Advection.2005.2015.csv')
julian = advection$X + julian(as.Date('2005-01-01')) - 1
out = month.day.year(julian)
qin = advection$Clearwater + advection$Snake + advection$NFClearwater
qin = qin * 0.0283168
for (i in 1:11) {
  year = (2005:2015)[i]
  qin.year.q = qin[out$year == year]
  qin.julian = julian[out$year == year] - julian(as.Date(paste0(year,'-01-01'))) + 1
  data = data.frame(Julian=qin.julian, Q = qin.year.q)
  filename = paste0('QIN',year,'.npt')
  write(paste0('****************** Q In File ****************'),
        file = filename, append=FALSE)
  write('', file=filename, append=TRUE)
  write('    JDAY    QIN', file=filename, append=TRUE)
  formatted.df = sprintf("%8.0f%8.2f", data$Julian, data$Q)
  write(formatted.df, file=filename, append=TRUE)
}

df = data.frame(Julian=c(), Q=c())
for (i in 1:11) {
  year = (2005:2015)[i]
  qin.year.q = qin[out$year == year]
  qin.julian = julian[out$year == year] - julian(as.Date(paste0(year,'-01-01'))) + 1
  data = data.frame(Julian=qin.julian, Q = qin.year.q)
  df = rbind(df, data)
}
stats = dplyr::summarize(group_by(df, Julian), mean = mean(Q) , sd = sd(Q))

rnorm(1, stats[1,]$mean, stats[1,]$sd)

simulatedQ = function(stats){
  simQ = numeric(nrow(stats))
  simQ[1] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  simQ[2] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  simQ[3] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  simQ[4] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  simQ[5] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  for(i in 1:nrow(stats)){
    simQ[5+i] = rnorm(1,stats[i,]$mean, stats[i,]$sd)
  }
  print(length(simQ))
  simQ = rollmean(simQ,5, align='right')
  print(length(simQ))
  return(simQ)
}
simQ = simulatedQ(stats)
plot(simQ, typ='l')


for(i in 1:1000){
  simQ = simulatedQ(stats)
  
  qin.year.q = simQ
  qin.julian = 1:365
  data = data.frame(Julian=qin.julian, Q = qin.year.q)
  filename = paste0('QIN.SIM',i,'.npt')
  write(paste0('****************** Q In File ****************'),
        file = filename, append=FALSE)
  write('', file=filename, append=TRUE)
  write('    JDAY    QIN', file=filename, append=TRUE)
  formatted.df = sprintf("%8.0f%8.2f", data$Julian, data$Q)
  write(formatted.df, file=filename, append=TRUE)
}

