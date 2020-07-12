from argparse import ArgumentParser
import folium
import json
import time
    
def make_map(larger_coordinates_list,larger_text_list,larger_name_list,geo_list):
    
    geo_counter = 0
    
    for i in range(len(larger_coordinates_list)):
        
        coordinates_right_order = []
        
        if len(larger_coordinates_list[i]) != 0:
            for j in range(len(larger_coordinates_list[i])): #Coordinates need to be flipped for true latitude and longitude.
                local_list = []
                local_list.append(larger_coordinates_list[i][j][1])
                local_list.append(larger_coordinates_list[i][j][0])
                
                coordinates_right_order.append(local_list)
                
            sample_map = folium.Map(location=[50,5], zoom_start=5) #Initiates the map object
            
            for j in range(len(larger_coordinates_list[i])):
            
                name_list = larger_name_list[i][j]
                text_list = larger_text_list[i][j]
                
                marker = folium.Marker(coordinates_right_order[j], popup=(name_list + ':     ' + text_list))
                marker.add_to(sample_map)
                
                print(marker)
                print(type(marker))
                time.sleep(1000)
            
            sample_map.save(geo_list[geo_counter][14:-6] + '.html')
        
        elif len(larger_coordinates_list[i]) == 0:
            print('It was empty!') #It is possible some twitter users return no geo-enabled tweets
   
        geo_counter += 1
    
if __name__ == '__main__':
    
    make_map()