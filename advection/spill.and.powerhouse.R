library(stringr)
library(xts)

projects = c('LGNW')
syear = 2005; eyear=2015
spill = powerhouse = date = NULL
for(project in projects){
  data = download.dart.daily(project, syear, eyear)
  data$Outflow..kcfs = as.numeric(data$Outflow..kcfs) *1000
  data$Spill = as.numeric(data$Spill..kcfs.) * 1000
  data$Powerhouse = data$Outflow..kcfs - data$Spill
  if(is.null(spill)){
    spill = data$Spill
    powerhouse = data$Powerhouse
    date = index(data)
  } else {
    spill = cbind(spill, data$Spill)
    powerhouse = cbind(powerhouse, data$Powerhouse)
    date = cbind(date, index(data))
  }
}
powerhouse.and.spill = data.frame(Powerhouse = powerhouse, Spill=spill, Date=date)

plot(powerhouse.and.spill$Spill, typ='l')
lines(powerhouse.and.spill$Powerhouse, col='blue')



# lets just get 2015 for the moment
data.2015 = grep('2015', powerhouse.and.spill$Date)
data.2015 = powerhouse.and.spill[data.2015,]
data.2015$Julian = as.numeric(strftime(as.POSIXct(data.2015$Date), format='%j'))

filename = 'QOUT2015.npt'
write(paste0('****************** Q Out File ****************'),
      file = filename, append=FALSE)
write('', file=filename, append=TRUE)
write('    JDAY    QOUT    QOUT', file=filename, append=TRUE)
formatted.df = sprintf("%8.0f%8.2f%8.2f", data.2015$Julian, data.2015$Powerhouse, data.2015$Spill)
write(formatted.df, file=filename, append=TRUE)