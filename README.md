# Pi
run gen_data.py to generate test_data.json every 10 min
temperature in degrees F
pressure in Pa
Humidity in %
wind direction angle in degrees clockwise of N
windspeed mph
pic is jpg encoded in base64 string 
time stamp format = YYYY-MM-DD HR:MM     military time
data presented in following format
{ 'node 1' : [ <time stamped data dictionary> , latitude, longitude],
'node 2': .................
}
for subnodes
< time stamped data dictionary > = { <time1>: [temperature, humidity,UV]}

for supernodes 
< time stamped data dictionary > = { <time1>: [temperature, humidity, UV, pressure, windspeed, winddirection, windgust, pic]}
