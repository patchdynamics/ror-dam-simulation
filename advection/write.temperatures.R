temperatures = read.table('SnakeRM137.txt')
names(temperatures) = c('Date', 'Mile', 'Temp', 'StdDev')
temperatures$Year = floor(temperatures$Date)
for( year in 2005:2015){
  data = filter(temperatures, Year==year)
  filename = paste0('TIN',year,'.npt')
  write(paste0('****************** Temperature File ****************'),
        file = filename, append=FALSE)
  write('', file=filename, append=TRUE)
  write('    JDAY     TIN', file=filename, append=TRUE)
  formatted.df = sprintf("%8.0f%8.2f", index(data), data$Temp)
  write(formatted.df, file=filename, append=TRUE)
}



# justcheatinghere
crs.narr = '+proj=lcc +x_0=5632642.22547 +y_0=4612545.65137 +lat_0=50 +lon_0=-107 +lat_1=50 +lat_2=50 +ellps=WGS84'
station.locations = shapefile('../../Columbia/GIS/WeatherStationsUsed.shp')
station.locations = spTransform(station.locations, crs.narr)
crs(station.locations)
values = NULL
first.year=2005
last.year=2015
for(year in first.year:last.year){
  download.file(str_replace(url.dswrf, 'YYYY', year), 'dswrf.nc')
  uswrf.sfc = brick('uswrf.nc')
  extracted.values = raster::extract(uswrf.sfc, station.locations)  
  if(is.null(values)){
    values = extracted.values
  } else {
    values = cbind(values, extracted.values)
  }
}
# NARR: W/m^2  (per day)
# CE-QUAL-W2: W/m^2

swr.2005.2015 = values
save(swr.2005.2015, file='swr.2005.2015.Rdata')
