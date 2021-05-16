import requests
import json
import sqlite3

conn = sqlite3.connect('onecall-owm.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS weather 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity INTEGER,
            dew_point INTEGER,
            wind_speed INTEGER 
            )''')

city = "Tbilisi"
key = "a96d6412ce5a268dcbfba2e59b7f9cc5"
lat = 33.44
lon = -94.04
units = "metric"
part = "hourly, daily"
url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={key}&units={units}"

r = requests.get(url)
print(r.status_code)
print(r.headers)
print(r.text)
res = r.json()
#print(json.dumps(res, indent=4))


with open('data.json', 'w') as file:
    json.dump(res, file, indent=4)

print(res['minutely'])
print(res['current']['temp'])


for each in res['daily']:
    humidity = each['humidity']
    dew_point = each['dew_point']
    wind_speed = each['wind_speed']
    row = (humidity, dew_point, wind_speed)

    c.execute('INSERT INTO weather (humidity, dew_point, wind_speed) VALUES (?, ?, ?)', row)

conn.commit()
conn.close()