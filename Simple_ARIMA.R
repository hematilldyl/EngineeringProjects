library('tseries')
library('forecast')
library('ggplot2')

#input data
daily_data=read.csv("C:/Users/Tomoko/Downloads/day.csv",header=T,stringsAsFactors=F)

daily_data$Date = as.Date(daily_data$dteday)
#visualize data
ggplot(daily_data,aes(Date,cnt)) +geom_line() +scale_x_date('month')+ylab("Daily Bike Checkouts")+xlab("")

#convert to ts object and clean outliers
time_series = ts(daily_data[,c('cnt')])
daily_data$clean_cnt=tsclean(time_series)
ggplot(daily_data,aes(Date,cnt)) +geom_line() +scale_x_date('month')+ylab("Cleaned Daily Bike Checkouts")+xlab("")


#create weekly MA
daily_data$cnt_ma = ma(daily_data$clean_cnt, order=7) # using the clean count with no outliers
#create monthly MA
daily_data$cnt_ma30 = ma(daily_data$clean_cnt, order=30)

#plot them
ggplot() +
  geom_line(data = daily_data, aes(x = Date, y = clean_cnt, colour = "Counts")) +
  geom_line(data = daily_data, aes(x = Date, y = cnt_ma,   colour = "Weekly Moving Average"))  +
  geom_line(data = daily_data, aes(x = Date, y = cnt_ma30, colour = "Monthly Moving Average"))  +
  ylab('Bicycle Count')

#decomp Y=S*T*E, seasonal, trend, remaining error: mult model
count_ma = ts(na.omit(daily_data$cnt_ma), frequency=30)
decomp = stl(count_ma, s.window="periodic")
deseasonal_cnt <- seasadj(decomp)
plot(decomp)

#Dickey Fuller. H0 series is non stationary.
adf.test(count_ma, alternative = "stationary")

#autocorrelation plots
Acf(count_ma, main='')
Pacf(count_ma, main='')

#1st order difference and adf
count_d1 = diff(deseasonal_cnt, differences = 1)
plot(count_d1)
adf.test(count_d1, alternative = "stationary")

#spikes at lag 1 and 2 in signficance region, use AR or MA with order 1,2 and 7
#since at 7, possible seasonality
Acf(count_d1, main='ACF for Differenced Series')
Pacf(count_d1, main='PACF for Differenced Series')

#ARIMA ignoring seasonality
auto.arima(deseasonal_cnt, seasonal=FALSE)
fit<-auto.arima(deseasonal_cnt, seasonal=FALSE)
tsdisplay(residuals(fit), lag.max=45, main='(1,1,1) Model Residuals')

#from before, spike at 7 makes clear the seasonality
fit2 = arima(deseasonal_cnt, order=c(1,1,7))
tsdisplay(residuals(fit2), lag.max=15, main='Seasonal Model Residuals')
arima(x = deseasonal_cnt, order = c(1, 1, 7))

#forecast the model with holdout
hold <- window(ts(deseasonal_cnt), start=700)
fit_no_holdout = arima(ts(deseasonal_cnt[-c(700:725)]), order=c(1,1,7))
fcast_no_holdout <- forecast(fit_no_holdout,h=25)
plot(fcast_no_holdout, main=" ")
lines(ts(deseasonal_cnt))

#model is very naive since model assumes series with no seasonaility
#add back seasonality
fit_w_seasonality = auto.arima(deseasonal_cnt, seasonal=TRUE)
seas_fcast <- forecast(fit_w_seasonality, h=30)
plot(seas_fcast)
