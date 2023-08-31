import datetime

# Database setup
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  database="ANPR"
)

cursor = db.cursor()





# function to retrive start and end of journey
def get_journey_start_end(vehicle_id, journey_date):

    cursor.execute('''SELECT camera_id, timestamp 
                FROM journeys 
                WHERE vehicle_id=? AND day_of_month=?
                ORDER BY timestamp''', 
                (vehicle_id, journey_date.day))
                
    points = cursor.fetchall()
    
    start_camera_id = points[0][0]
    start_time = points[0][1]
    
    end_camera_id = points[-1][0]
    end_time = points[-1][1]
    
    cursor.execute('SELECT lat, lon FROM cameras WHERE id=?', (start_camera_id,))
    start_lat, start_lon = cursor.fetchone()
    
    cursor.execute('SELECT lat, lon FROM cameras WHERE id=?', (end_camera_id,)) 
    end_lat, end_lon = cursor.fetchone()
    
    return start_lat, start_lon, end_lat, end_lon
    
 
    
    
# function for common jounrey of a vehicle
def find_common_journeys(vehicle_id):
    
    cursor.execute('''SELECT day_of_week, start_lat, start_lon, end_lat, end_lon 
               FROM journeys j
               JOIN cameras c1 ON j.start_camera = c1.id
               JOIN cameras c2 ON j.end_camera = c2.id 
               WHERE vehicle_id=?
               GROUP BY day_of_week, start_lat, start_lon, end_lat, end_lon
               HAVING COUNT(*) > 1''', (vehicle_id,))
               
    common_journeys = cursor.fetchall()
    
    return common_journeys



# function to count avg_appearances of a vehicle
def get_avg_appearances(vehicle_id, start, end, day_of_week):

    cursor.execute('''SELECT AVG(*) AS num_appearances
               FROM journeys j
               JOIN cameras c1 ON j.start_camera = c1.id 
               JOIN cameras c2 ON j.end_camera = c2.id
               WHERE vehicle_id=? 
                AND start_lat=? AND start_lon=?
                AND end_lat=? AND end_lon=?
                AND day_of_week=?''',
               (vehicle_id, start[0], start[1], end[0], end[1], day_of_week))
               
    avg = cursor.fetchone()[0]
    
    return avg



# find usual route and insert into table
def populate_usual_routes(vehicle_id):
    
    common_journeys = find_common_journeys(vehicle_id)
    for journey in common_journeys:
    
       day_of_week, start_lat, start_long, end_lat, end_long = journey
       
       avg_appearances = get_avg_appearances(vehicle_id, (start_lat, start_long), (end_lat, end_long), day_of_week)
       
       cursor.execute('''INSERT INTO usual_routes
                   (vehicle_id, start_lat, start_lon, end_lat, end_lon, 
                   day_of_week, num_appearances)
                   VALUES (?,?,?,?,?,?,?)''', 
                   (vehicle_id, start_lat, start_long, end_lat, end_long,
                    day_of_week, avg_appearances))
    
    cursor.commit()

# get existing usual route
def get_usual_route(vehicle_id, vehicle_loc,day_of_week):

  # Get common routes for vehicle
  cursor.execute("SELECT start_lat, start_lon, end_lat, end_lon FROM usual_routes WHERE vehicle_id=? AND day_of_week=?", (vehicle_id, day_of_week))
  start_lat, start_lon, end_lat, end_lon = cursor.fetchone()
  
  # explore google maps api to get directions
  distance, time, journey = call_direction_API (start_lat, start_lon, end_lat, end_lon)
  
  if vehicle_loc in journey:
      return 1
  
  return 0




# main

import requests

#Get feed from camera
while camera.feed():
vehicle_loc = camera.id
#Extract a frame from feed
    frame = feed.frame()
    with open(frame, 'rb') as fp:
        # request ALPR system API
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token 5ea9aaf15a07f768e4959ece52955592138fb925'})
    
    result = response.json()
    
    if response['results']:
        # LP from the response
        lp =  response['results'][0]['plate'] 
        # check LP if exsits in database
        cursor.execute('''SELECT vehicle_id
                    FROM vehicles WHERE LP_num=?
                    ''', (lp))
                    
        vehicle = cursor.fetch_one()
        if not vehicle is None:
            res = get_usual_route(vehicle_id)
            
            if res ==1:
                continue
            else:
                print(f"{lp} is not on usual track, alert!")
                call_authorities()
                
        else: 
            print('''vehicle with {lp} hasn't opted for usual route tracking''')
            continue
    else:
        print('no detection from ALPR!')


