from math import radians, sin, cos, asin, sqrt, degrees
# from shapely.geometry import Point, LineString
import pandas as pd
import plotly.graph_objects as go

"""Python script to output the shortest distance between two user specified airports and output coordinates for the flight path. Script can also plot the flight path
"""

# Use pandas to read and convert csv file
airports_list = pd.read_csv("airports.csv", delimiter=',',skiprows=1,names=['Code','Latitude','Longitude','Country'])


# Ensure the user inputted data corresponds to a specific airport
counter = 0
while counter == 0:
    airport1 = input("What airport are you flying from?\n Input the 3 letter code \n").upper()
    for i in range(len(airports_list)):
        if airport1 == airports_list["Code"][i]:
            counter+=1
            index1 = i
            break
    if counter == 0:
        print("Please enter a valid airport code.")
        
counter2 = 0
while counter2 == 0:
    airport2 = input("What is your destination?\n Input the 3 letter code \n").upper()
    for i in range(len(airports_list)):
        if airport2 == airports_list["Code"][i]:
            counter2+=1
            index2 = i
            break
    if counter2 == 0:
        print("Please enter a valid airport code.")


# # # Using Haversine formula 
# Convert all coordinates to radians
lat1 = radians(airports_list["Latitude"][index1])
lat2 = radians(airports_list["Latitude"][index2])
lon1 = radians(airports_list["Longitude"][index1])
lon2 = radians(airports_list["Longitude"][index2])
radius_E = 6371     # Assumed radius of the earth

# Find value in radians
# Difference in longitude and latitude
dlon = lon2 - lon1
dlat = lat2 - lat1

# Great Circle calculations
a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * asin(sqrt(a))
shortest_distance = radius_E * c

"""Use of a library to interpolate between the two points"""
# def generate_points_on_line(number,line):
#     points = []
#     for i in range(number):
#         point = line.interpolate(i/10,normalized = True).wkt
#         points.append(point)
#     return points

# start_point = Point(degrees(lon1), degrees(lat1))
# end_point = Point(degrees(lon2), degrees(lat2))
# straight_line = LineString([start_point, end_point])

# points = generate_points_on_line(11,straight_line)


def gen_points(lat1,lon1,lat2,lon2,dlon,dlat,separation):
    """Use of for loop to interpolate regularly spaced coordinates between two end points"""
    lat = []
    lon = []
    for i in range(0,separation+1):
        pointLat = round(degrees(lat1) + (i/separation) * degrees(dlat),2)
        pointLon = round(degrees(lon1) + (i/separation) * degrees(dlon),2)
        lat.append(pointLat)
        lon.append(pointLon)
    return lat,lon

lat,lon = gen_points(lat1,lon1,lat2,lon2,dlon,dlat,10)

## Print answers
print("Shortest distance between "+ str(airports_list["Code"][index1]) + ", " + str(airports_list["Country"][index1]) + " and " + str(airports_list["Code"][index2]) + ", " + str(airports_list["Country"][index2]) + ": " + str(round(shortest_distance,2)) + " Km")
print("Coordinates for flight path: [Latitude, Longitude]")

for i in range(len(lat)):
    print("["+str(lat[i]) + ", " + str(lon[i])+ "]")


## Plot flight path using plotly.go.Scattergeo library
fig = go.Figure()

# If would like all airports present
# fig.add_trace(go.Scattergeo(lon = airports_list["Longitude"], lat = airports_list["Latitude"], mode = 'markers',name = str(airports_list["Code"])+"Airport", marker = dict(size=3,color="black")))

# If would like only source and destination airports present
fig.add_trace(go.Scattergeo(lon = [degrees(lon1),degrees(lon2)], lat = [degrees(lat1),degrees(lat2)], mode = 'markers', marker = dict(size=3,color="black")))
fig.add_trace(go.Scattergeo(lon = [degrees(lon1), degrees(lon2)], lat = [degrees(lat1),degrees(lat2)], mode = 'lines',name = "Flight Path"))
fig.update_layout(showlegend =False)

fig.show()

