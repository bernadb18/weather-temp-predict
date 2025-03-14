import requests
import datetime
import pytz
import csv
import time
import pandas as pan
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import  mean_absolute_error
from sklearn.linear_model import LinearRegression

timepredhr = int(input("hour in (00): "))
timepredsec = int(input("sec in (00): "))
timepredmin = int(input("min in (00): "))

DULAT = 53.2814  
DULON =  -6.2842


#hour = input("in (00:00:00)24hour format: ")


apikey = "85f6ff7e57304e36c5de62551c8d9c60"
url = f"http://api.openweathermap.org/data/2.5/weather?lat={DULAT}&lon={DULON}&appid={apikey}"
response = requests.get(url)
weatherdata = response.json()
       
        
temp = weatherdata["main"]["temp"]
weatherdesc = weatherdata["weather"][0]["main"]
speed = weatherdata["wind"]["speed"]
pressure = weatherdata["main"]["pressure"]
humidity = weatherdata["main"]["humidity"]

dublintimezone = pytz.timezone("Europe/Dublin")
dublintime = datetime.datetime.now(dublintimezone)


date = dublintime.strftime("%Y-%m-%d")
time = dublintime.strftime("%H:%M:%S")

data1 = "weatherdata.csv"

def weathermodel():
    

    if response.status_code == 200:
        
        #print("youre temp is {}°C,description of the weather is {}, wind speed is {}m/s and the pressure is {}hPa".format(temp,weatherdesc,speed,pressure))

        
        with open(data1, mode="a", newline=" ") as file:
            writer = csv.writer(file)
            writer.writerow([date, time, temp, speed, pressure, humidity, weatherdesc])
    else:
        print("Error: {}".format(status_code))

#logic error somehwere
def bigtime():

    minute = dublintime.minute
    second = dublintime.second

    
    if minute == 0 and second == 0:
        
        return 0  
    elif minute == 30 and second == 0:
        
        return 0
         
    else:
       if minute < 30:
            waittime = (30 - minute) * 60 - second
            print(waittime)
       elif minute > 30:
            waittime = (60 - minute) * 60 - second + 30 * 60
            print(waittime)
            return waittime
    


#while True:
    
    #weathermodel()
    #time.sleep(300)

column_names = ["day", "timestamp", "temperature", "windspeed", "pressure", "humidity", "cloudiness"]
data = pan.read_csv(data1, names=column_names , header=None)
scaler =  StandardScaler()


def  weathercurrenthour():


    usedata = data[["windspeed", "pressure", "humidity"]]
    predictdata = data["temperature"]

    usedatascaled = scaler.fit_transform(usedata)

    usedatatrain, usedatatest, predictdatatrain, predictdataytest = train_test_split(usedatascaled, predictdata, test_size=0.15, random_state=67)


    model = LinearRegression()
    model.fit(usedatatrain, predictdatatrain)


    pred = model.predict(usedatatest)


    
    absolute = mean_absolute_error(predictdataytest, pred)

    newdata = [[speed, pressure, humidity]]
    newdatadf = pan.DataFrame(newdata, columns=["windspeed", "pressure", "humidity"])
    newdatascaled = scaler.transform(newdatadf)

    predictemperature = model.predict(newdatascaled)
    


    print("predicted temperature:{}".format(predictemperature[0]))

    
    print("mean absolute error: {}".format(absolute))

    #print(data.head())
    return weathercurrenthour

print(weathercurrenthour())
print("youre temp is {}°C,description of the weather is {}, wind speed is {}m/s and the pressure is {}hPa".format(temp,weatherdesc,speed,pressure))


### implementing   more features for more accurate predict in the future when the weather data big enough
def timepredtemp():
    data["timestamp"] = pan.to_datetime(data["timestamp"])
    data["hour"] = data["timestamp"].dt.hour
    data["second"] = data["timestamp"].dt.second
    data["minute"] = data["timestamp"].dt.minute


    usedata = data[["hour","second", "minute"]]
    predictdata = data["temperature"]

    usedatascaled = scaler.fit_transform(usedata)

    usedatatrain, usedatatest, predictdatatrain, predictdataytest = train_test_split(usedatascaled, predictdata, test_size=0.15, random_state=67)


    model = LinearRegression()
    model.fit(usedatatrain, predictdatatrain)


    pred = model.predict(usedatatest)


    
    absolute = mean_absolute_error(predictdataytest, pred)

    newdata = [[timepredhr, timepredsec, timepredmin]]
    newdatadf = pan.DataFrame(newdata, columns=["hour","second", "minute"])
    newdatascaled = scaler.transform(newdatadf)

    predictemperature = model.predict(newdatascaled)
    


    print("predicted temperature for pred time {}:{}:{} is {}".format(timepredhr,timepredmin,timepredsec,predictemperature[0]))

    
    print("mean absolute error: {}".format(absolute))

    #print(data['timestamp'].head())

    #print(predictdata.head())
    #print(usedata.head())
print(timepredtemp())
