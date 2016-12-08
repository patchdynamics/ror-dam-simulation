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

