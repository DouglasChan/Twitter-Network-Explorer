import json
from argparse import ArgumentParser
import time

# f is the filename:
# line working as expected

#def get_parser():
#	parser = ArgumentParser()
#	parser.add_argument('--tweets')
#	parser.add_argument('--geojson')
#	return parser

def main_geo_creator(geo_list):
    #args = parser.parse_args()
    
    
    for i in range(len(geo_list)):
        print(geo_list[i])
        
    time.sleep(1000)
    print('wut')
    coordinates_list = []
    text_list = []
    name_list = []
	
    with open(args.tweets, 'r') as f:
        geo_data = {
            "type" : "FeatureCollection",
            "features": []
		}
        for line in f:
            tweet = json.loads(line)
            try:
                if tweet['retweeted_status']['place']:
                    print(tweet['retweeted_status']['user']['name'])
                    print(tweet['retweeted_status']['place']['bounding_box']['coordinates'][0][0])
                    print(tweet['retweeted_status']['text'])
                    
                    coordinates_list.append(tweet['retweeted_status']['place']['bounding_box']['coordinates'][0][0])
                    text_list.append(tweet['retweeted_status']['text'])
                    name_list.append(tweet['retweeted_status']['user']['name'])
                    
                else:
                    pass
            except KeyError:
                continue
    
    print(coordinates_list)
    print(text_list)
    print(name_list)


if __name__ == '__main__':
    main_geo_creator()

    #return coordinates_list, text_list, name_list
                    
#Links : 
#https://cheatography.com/davechild/cheat-sheets/regular-expressions/