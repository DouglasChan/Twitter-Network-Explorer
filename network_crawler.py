import main
import time
import twitter_mention_frequency

total_combinations = []
handle_list = []
mega_file_list = []

def network_crawler(seed_handle, levels):
    
    first_handle = seed_handle
    
    handle_list.append(first_handle) #Appending seed?
    
    for i in range(levels+1):
        total_combinations.append(i) # To do with differences in indexes, Python quirks etc...
        
        if i == 0:
            print(first_handle)
            time.sleep(10)
            print('We want to skip this as a loop')
            first_file_name = main.downloading_json(first_handle)
            
            first_list = []
            first_list.append(first_file_name)

            mega_file_list.append(first_list) #Might need to append as a list*
    
        elif (i == 1): #i == 2 is when we get the other stuff...
            print(mega_file_list)
            print(i)
            time.sleep(3)
            
            
            for j in range(len(mega_file_list[i-1])):
                #What is the length?
                
                most_common_list = twitter_mention_frequency.twitter_mentioning(mega_file_list[i-1][j])
                
                local_file_list, local_handle_list = main.getting_file_names(most_common_list)
                
                mega_file_list.append(local_file_list)
                handle_list.append(local_handle_list)
        
        else:
            larger_file_list = []
            larger_handle_list = []
            
            for j in range(len(mega_file_list[i-1])):
                #What is the length?
                
                most_common_list = twitter_mention_frequency.twitter_mentioning(mega_file_list[i-1][j])
                
                local_file_list, local_handle_list = getting_file_names(most_common_list)
                
                larger_file_list.append(local_file_list)
                larger_handle_list.append(local_handle_list)
                
            mega_file_list.append(larger_file_list)
            handle_list.append(larger_handle_list)
            
            print('OOGABOOGA')
            time.sleep(3)
            #print(mega_file_list[i])
            
            #Flattening list?
            
            print('CACAW')
            temp_flat_list = [item for sublist in mega_file_list[i] for item in sublist]
            temp_flat_list = list(set(temp_flat_list))
            
            
            #print(temp_flat_list)
            time.sleep(3)
            
            mega_file_list[i] = temp_flat_list
            
            print('Huzzah!')
    print('dun dun dun')
    print(mega_file_list)
            
if __name__ == '__main__':
    network_crawler()