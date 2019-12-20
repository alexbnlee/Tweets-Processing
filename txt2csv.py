from math import radians, sin
import json, os, codecs

# area of bounding box
def area(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    r = 6372
    return abs(r**2 * (lon2 - lon1) * (sin(lat2) - sin(lat1)))

# tweets of txt to csv
def txt2csv(foldername, filename):
    files = os.listdir(foldername)
    os.chdir(foldername)

    fo = open(filename, "w")
    fo.write("\ufeff")
    fo.write("id,created_at,coordinates,co_lon,co_lat,geo,geo_lat,geo_lon," + 
             "user_location,place_type,place_name," + 
             "place_full_name,place_country,place_bounding_box,pb_avg_lon,pb_avg_lat," + 
             "min_lon,min_lat,max_lon,max_lat,bb_area,lang,source,text")
    count = 0

    for file in files:
        # determine is file or directory
        if os.path.isdir(file):
            continue

        count += 1
        print(count, ":", file)

        tweets_file = open(file, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                csv_text = "\n"
                # id
                csv_text += tweet["id_str"]
                csv_text += ","
                # created_at
                csv_text += str(tweet["created_at"])
                csv_text += ","
                # coordinates
                if (tweet["coordinates"]):
                    csv_text += "Yes,"
                    csv_text += str(tweet["coordinates"]["coordinates"][0])
                    csv_text += ","
                    csv_text += str(tweet["coordinates"]["coordinates"][1])
                else:
                    csv_text += "None,None,None"
                csv_text += ","
                # geo
                if (tweet["geo"]):
                    csv_text += "Yes,"
                    csv_text += str(tweet["geo"]["coordinates"][0])
                    csv_text += ","
                    csv_text += str(tweet["geo"]["coordinates"][1])
                else:
                    csv_text += "None,None,None"
                csv_text += ","
                # user->location
                ul = str(tweet["user"]["location"])
                ul = ul.replace("\n", " ")
                ul = ul.replace("\"", "")
                ul = ul.replace("\'", "")
                csv_text += "\"" + ul + "\""
                csv_text += ","
                # place->type
                csv_text += str(tweet["place"]["place_type"])
                csv_text += ","
                # place->name
                csv_text += "\"" + str(tweet["place"]["name"]) + "\""
                csv_text += ","
                # place->full_name
                csv_text += "\"" + str(tweet["place"]["full_name"]) + "\""
                csv_text += ","
                # place->country
                csv_text += "\"" + str(tweet["place"]["country"]) + "\""
                csv_text += ","
                # place->bounding_box
                if (tweet["place"]["bounding_box"]["coordinates"]):
                    # min_lon
                    min_lon = tweet["place"]["bounding_box"]["coordinates"][0][0][0]
                    # min_lat
                    min_lat = tweet["place"]["bounding_box"]["coordinates"][0][0][1]
                    # max_lon
                    max_lon = tweet["place"]["bounding_box"]["coordinates"][0][2][0]
                    # max_lat
                    max_lat = tweet["place"]["bounding_box"]["coordinates"][0][2][1]
                    # avg of lon and lat
                    lon = (min_lon + max_lon)/2
                    lat = (min_lat + max_lat)/2
                    # area of bounding box
                    area_bb = area(min_lon, min_lat, max_lon, max_lat)
                    csv_text += "Yes,"
                    csv_text += str(lon)
                    csv_text += ","
                    csv_text += str(lat)
                    csv_text += ","
                    csv_text += str(min_lon)
                    csv_text += ","
                    csv_text += str(min_lat)
                    csv_text += ","
                    csv_text += str(max_lon)
                    csv_text += ","
                    csv_text += str(max_lat)
                    csv_text += ","
                    csv_text += str(area_bb)
                else:
                    csv_text += "None, None, None"
                csv_text += ","
                # lang
                csv_text += str(tweet["lang"])
                csv_text += ","
                # source
                csv_text += "\"" + str(tweet["source"]) + "\""
                csv_text += ","
                # text
                # replace carriage return, double quotation marks, single quotation marks with space or nothing
                text = str(tweet["text"])
                text = text.replace("\r", " ")
                text = text.replace("\n", " ")
                text = text.replace("\"", "")
                text = text.replace("\'", "")
                csv_text += "\"" + text + "\""
                fo.write(csv_text)

            except:
                continue

    fo.close()    
    
txt2csv(r"D:\UNSW\data", r"D:\UNSW\tweets.csv")

import pandas as pd
df = pd.read_csv(r"D:\UNSW\tweets.csv")
df.head()
