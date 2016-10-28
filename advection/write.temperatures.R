temperatures = read.table('SnakeRM137.txt')
names(temperatures) = c('Date', 'Mile', 'Temp', 'StdDev')
temperatures$Year = floor(temperatures$Date)
for( year in 2005:2015){
  data = filter(temperatures, Year==year)
  filename = paste('TIN',year,'.npt')
  write(paste0('****************** Temperature File ****************'),
        file = filename, append=FALSE)
  write('', file=filename, append=TRUE)
  formatted.df = sprintf("%8.0f%8.0f", index(data), data$Temp)
  write(formatted.df, file=filename, append=TRUE)
}