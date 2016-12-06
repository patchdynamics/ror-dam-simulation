library(stringr)
library(xts)
library(stringr)

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
powerhouse.and.spill = data.frame(Powerhouse = powerhouse * 0.0283168, Spill=spill * 0.0283168, Date=date)

plot(powerhouse.and.spill$Powerhouse + powerhouse.and.spill$Spill, col='red', typ='l')
lines(powerhouse.and.spill$Spill)
lines(powerhouse.and.spill$Powerhouse, col='blue')

plot(powerhouse.and.spill$Spill, typ='l')
plot(powerhouse.and.spill$Powerhouse, typ='l')



# write out the files
for(i in 2005:2015) {

  data = grep(as.character(i), powerhouse.and.spill$Date)
  data = powerhouse.and.spill[data,]
  data$Julian = as.numeric(strftime(as.POSIXct(data$Date), format='%j'))

  filename = paste0('QOUT',i,'.npt')
  write(paste0('****************** Q Out File ****************'),
      file = filename, append=FALSE)
  write('', file=filename, append=TRUE)
  write('    JDAY    QOUT    QOUT', file=filename, append=TRUE)
  formatted.df = sprintf("%8.0f%8.2f%8.2f", data$Julian, data$Powerhouse, data$Spill)
  write(formatted.df, file=filename, append=TRUE)
}