library(raster)

# get the qclcd data
source('meteorology-util/download.qclcd.daily.R')
qclcd.2005.2015 = downloadload.qclcd.daily('2005', '2015', wbans=c(24149, 24243))
save(qclcd.2005.2015, file='qclcd.2005.2015.Rdata')

# extract incident solar radiation and cloud cover from rasters

url.dswrf = 'ftp://ftp.cdc.noaa.gov/Datasets/NARR/Dailies/monolevel/dswrf.YYYY.nc'
url.clouds = 'ftp://ftp.cdc.noaa.gov/Datasets/NARR/Dailies/monolevel/tcdc.YYYY.nc'

crs.narr = '+proj=lcc +x_0=5632642.22547 +y_0=4612545.65137 +lat_0=50 +lon_0=-107 +lat_1=50 +lat_2=50 +ellps=WGS84'
station.locations = shapefile('GIS/WeatherStationsUsed.shp')
station.locations = spTransform(station.locations, crs.narr)
crs(station.locations)

first.year = 2005
last.year = 2015
values = NULL
for(year in first.year:last.year){
  download.file(str_replace(url.dswrf, 'YYYY', year), 'dswrf.sfc.nc')
  dswrf.sfc = brick('dswrf.sfc.nc')
  extracted.values = raster::extract(dswrf.sfc, station.locations)  
  if(is.null(values)){
    values = extracted.values
  } else {
    values = cbind(values, extracted.values)
  }
}
# NARR: W/m^2  (per day)
# CE-QUAL-W2: W/m^2

save(values, file='dswr.2005.2015.Rdata')
dswr.2005.2015 = values;


#clouds = NULL
#for(year in first.year:last.year){
#  download.file(str_replace(url.clouds, 'YYYY', year), 'clouds.nc')
#  clouds.narr = brick('clouds.nc')
#  extracted.values = raster::extract(clouds.narr, station.locations)  
#  if(is.null(clouds)){
#    clouds = extracted.values
#  } else {
#    clouds = cbind(clouds, extracted.values)
#  }
#}
#save(clouds, file='clouds.2005.2015.Rdata')
