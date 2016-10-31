load('qclcd.2005.2015.Rdata')
load('dswr.2005.2015.Rdata')
load('clouds.2005.2015.Rdata')

station.index = 1; # one is Lewiston
station.data = qclcd.2005.2015[qclcd.2005.2015$WBAN==24149,]

df = as.data.frame(1:nrow(station.data))

air.temperature = as.numeric(levels(station.data$Tavg))[station.data$Tavg]
air.temperature = na.interp(air.temperature)
air.temperature.C = (air.temperature-32)*(5/9)
df$AirTemperature = air.temperature.C

dewpoint = as.numeric(levels(station.data$DewPoint))[station.data$DewPoint]
dewpoint = na.interp(dewpoint)
df$Dewpoint = (dewpoint-32) *(5/9)

wind = as.numeric(levels(station.data$AvgSpeed))[station.data$AvgSpeed]  
wind = na.interp(wind)
df$Wind = wind

direction = as.numeric(levels(station.data$WindDirection))[station.data$WindDirection] 
direction = na.interp(direction)
df$WindDirection = direction * 2 * pi / 36 # convert from 10s of degress to radians

df$Clouds = clouds[station.index,]/10

df$Swr = dswr.2005.2015[station.index,]

filename = 'met.npt'
write(paste0('****************** Meteorology ****************'),
      file = filename, append=FALSE)
write(paste0(''), file = filename, append=TRUE)
write('JDAY,TAIR,TDEW,WIND,PHI,CLOUD,Solar,',  file = filename, append=TRUE)
write.table(formatted.df, file = filename, append = TRUE, sep=',', col.name=FALSE, quote=FALSE, row.names=FALSE)
