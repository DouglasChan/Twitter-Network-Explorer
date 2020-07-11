import main
import time
import twitter_mention_frequency

combined_file_list = []

def network_crawler(seed_handle, levels):

    first_handle = seed_handle #Uses the input that was entered into the command line.
    
    for i in range(levels+1):        
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
                
                local_file_list = main.getting_file_names(most_common_list)
                
                combined_file_list.append(local_file_list)

        else:
            larger_file_list = []
            larger_handle_list = []
            
            for j in range(len(combined_file_list[i-1])): # The program will refer back to the most recent list of users. 
                                                        #So if we were looking at the 6th degree of separation, we would be looking at network neighbors from the 5th degree of separation from the seed profile.
                               
                most_common_list = twitter_mention_frequency.twitter_mentioning(combined_file_list[i-1][j])

                local_file_list = main.getting_file_names(most_common_list)
                
                larger_file_list.append(local_file_list) #This list of lists has to be used since at 2 or + degrees of separation, each exploration of new neighbors is its own list.
                
            combined_file_list.append(larger_file_list)

            flat_list = [item for sublist in combined_file_list[i] for item in sublist]
            flat_list = list(set(flat_list)) #Since the order of which we've identified the neighbors at a given level doesn't matter, 
                                            #we set all of the users within that search degree as a flat list so that our function can work recursively.
            
            combined_file_list[i] = flat_list #With this code at say level 2, we have 3 lists within the larger list. 
                                            #The first is the seed profile, the second is their neighbors, and the third is the flat list of 2nd degree neighbors.
    
    json_filenames = combined_file_list
    
    return json_filenames
            
if __name__ == '__main__':
    network_crawler()