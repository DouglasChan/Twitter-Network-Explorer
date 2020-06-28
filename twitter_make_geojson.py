import json
from argparse import ArgumentParser
import time

def main_geo_creator(geo_list):
    larger_coordinates_list = []
    larger_text_list = []
    larger_name_list = []
    
    for i in range(len(geo_list)): #Keeping track with geo_list, a list of all users that may or may not have geottagged tweets.    
        coordinates_list = []
        text_list = []
        name_list = []
	
        with open(geo_list[i], 'r') as f: #Boilerplate code from Twitter Data Mining series in creating custom json files to be pased into Folium.
            geo_data = {
                "type" : "FeatureCollection",
                "features": []
            }
            for line in f:
                tweet = json.loads(line)
                try: #If geodata is found, passes coordinates, tweet text, and name of Tweeter as these are the data that will be important to the end visualization.
                    if tweet['retweeted_status']['place']:                        
                        coordinates_list.append(tweet['retweeted_status']['place']['bounding_box']['coordinates'][0][0]) #Taking the top left corner of bounding box, if it exists.
                        text_list.append(tweet['retweeted_status']['text'])
                        name_list.append(tweet['retweeted_status']['user']['name'])
                        
                    else:
                        pass
                except KeyError:
                    continue
        
        larger_coordinates_list.append(coordinates_list)
        larger_text_list.append(text_list)
        larger_name_list.append(name_list)

    return larger_coordinates_list, larger_text_list, larger_name_list, geo_list

if __name__ == '__main__':
    main_geo_creator()
                    