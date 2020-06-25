import json
from argparse import ArgumentParser
import time

# f is the filename:
# line working as expected


def main_geo_creator(geo_list):
    larger_coordinates_list = []
    larger_text_list = []
    larger_name_list = []
    
    for i in range(len(geo_list)):    
        coordinates_list = []
        text_list = []
        name_list = []
	
        with open(geo_list[i], 'r') as f:
            geo_data = {
                "type" : "FeatureCollection",
                "features": []
            }
            for line in f:
                tweet = json.loads(line)
                try:
                    if tweet['retweeted_status']['place']:                        
                        coordinates_list.append(tweet['retweeted_status']['place']['bounding_box']['coordinates'][0][0])
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
                    
#Links : 
#https://cheatography.com/davechild/cheat-sheets/regular-expressions/