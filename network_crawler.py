import main
import time
import twitter_mention_frequency

#total_combinations = []
#handle_list = []
combined_file_list = []

def network_crawler(seed_handle, levels):
    
    first_handle = seed_handle #Uses the input from the command line.
    
    #handle_list.append(first_handle) #Appending seed?
    
    for i in range(levels+1):
        #total_combinations.append(i) # To do with differences in indexes, Python quirks etc...
        
        '''
        The code runs differently depending on the number of levels specified to the crawler.
        
        If the level argument is 0, only the seed person is returned.
        
        If the level argument is 1, the top neighbors to the seed account are returned.
        
        If the level argument is 2 or more, neighbors for subsequent degrees of separation are returned.
        
        '''
        
        if i == 0:
            first_file_name = main.downloading_json(first_handle)
            
            first_list = []
            first_list.append(first_file_name)

            combined_file_list.append(first_list) #The usernames at each level are appended to combined_file_list to keep track of who is in the network at each degree of separation.
    
        elif (i == 1): 
            
            for j in range(len(combined_file_list[i-1])): #In this case, this list of length 1 only has the seed profile to start with.
                
                most_common_list = twitter_mention_frequency.twitter_mentioning(combined_file_list[i-1][j]) #Uses the previously built function of getting top N twitter users in network by mention
                
                local_file_list = main.getting_file_names(most_common_list)[0] #Gets the returned file list, we won't need the handle list so only taking the output at index 0.
                
                #print(local_file_list)
                #print(local_handle_list)
                #print('hot potato')
                #time.sleep(1000)
                
                combined_file_list.append(local_file_list) 
                #handle_list.append(local_handle_list)
        
        else:
            larger_file_list = []
            larger_handle_list = []
            
            for j in range(len(combined_file_list[i-1])):
                #What is the length?
                
                most_common_list = twitter_mention_frequency.twitter_mentioning(combined_file_list[i-1][j])
                
                local_file_list, local_handle_list = main.getting_file_names(most_common_list)
                
                larger_file_list.append(local_file_list)
                larger_handle_list.append(local_handle_list)
                
            combined_file_list.append(larger_file_list)
            #handle_list.append(larger_handle_list)
            
            print('OOGABOOGA')
            time.sleep(3)
            #print(combined_file_list[i])
            
            #Flattening list?
            
            print('CACAW')
            temp_flat_list = [item for sublist in combined_file_list[i] for item in sublist]
            temp_flat_list = list(set(temp_flat_list))
            
            
            #print(temp_flat_list)
            time.sleep(3)
            
            combined_file_list[i] = temp_flat_list
            
    print(combined_file_list)
    
    json_filenames = combined_file_list
    return json_filenames
            
if __name__ == '__main__':
    network_crawler()