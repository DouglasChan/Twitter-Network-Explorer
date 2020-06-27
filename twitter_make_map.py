from argparse import ArgumentParser
import folium
import json
import time
    
def make_map(larger_coordinates_list,larger_text_list,larger_name_list,geo_list):
    
    geo_counter = 0
    
    for i in range(len(larger_coordinates_list)):
        
        coordinates_right_order = []
        #print(len(larger_coordinates_list[0]))
        #time.sleep(1000)
        #print(i)
        #print(larger_coordinates_list[i])
        
        if len(larger_coordinates_list[i]) != 0:
            for j in range(len(larger_coordinates_list[i])):
                local_list = []
                local_list.append(larger_coordinates_list[i][j][1])
                local_list.append(larger_coordinates_list[i][j][0])
                
                coordinates_right_order.append(local_list)
                
            sample_map = folium.Map(location=[50,5], zoom_start=5)
            
            for j in range(len(larger_coordinates_list[i])):
            
                name_list = larger_name_list[i][j]
                text_list = larger_text_list[i][j]
                
                print(name_list)
                print(text_list)
                print(coordinates_right_order[j])
                #time.sleep(3)
                #print(name_list)
                #print(text_list)
                #print(coordinates_right_order)
                #time.sleep(1000)
            #time.sleep(1)
            
            
                marker = folium.Marker(coordinates_right_order[j], popup=(name_list + ':     ' + text_list))
                marker.add_to(sample_map)
            
            sample_map.save(geo_list[geo_counter][14:-6] + '.html')
        
        elif len(larger_coordinates_list[i]) == 0:
            print('It was empty!')
            print(larger_coordinates_list[i])
            time.sleep(1)
            
            #geo_counter += 1
        
        #for j in range(len(larger_coordinates_list[i])):

            
        geo_counter += 1
                

            
            
        print('geo counter is ' + str(geo_counter))
        #print(
        
        
        '''
        for j in range(len(larger_coordinates_list[i])):
            print(counter)
            print('that was counter')
            counter += 1
            print(len(larger_coordinates_list[i]))
            print('that was length')
            print(larger_coordinates_list[i])
            local_list = []
            local_list.append(larger_coordinates_list[i][j][1])
            local_list.append(larger_coordinates_list[i][j][0])
            
            coordinates_right_order.append(local_list)

        sample_map = folium.Map(location=[50, 5], zoom_start=5)

        for j in range(len(larger_coordinates_list)[i]):
            marker = folium.Marker(coordinates_right_order[i], popup=(name_list[j] + ':     ' + text_list[i]))
            marker.add_to(sample_map)
    
        sample_map.save(map_file)
        '''


    '''
    for i in range(len(larger_coordinates_list)):
        if len(larger_coordinates_list[i]) == 0:
            continue
        else:
            coordinates_right_order = []
            for j in range(len(larger_coordinates_list[i][j])):
                local_list = []
                local_list.append(larger_coordinates_list[i][j][1])
                local_list.append(larger_coordinates_list[i][j][0])
                
                coordinates_right_order.append(local_list)
 
            sample_map = folium.Map(location=[50, 5], zoom_start=5)
    
            for j in range(len(coordinates_list)):
                marker = folium.Marker(coordinates_right_order[i], popup=(name_list[j] + ':     ' + text_list[i]))
                marker.add_to(sample_map)
        
            sample_map.save(map_file)
    '''                

    #print(larger_coordinates_list)
    #print(larger_text_list)
    #print(larger_name_list)
    #time.sleep(1000)
    #print('wut')
    

    '''
    coordinates_list = [[-74.041878, 40.570842], [-118.668404, 33.704538], [-122.6395145, 45.309499], [-104.99164266562248, 39.739250675852105], [-74.088762, 41.50978], [-122.34266, 37.699279], [-78.912276, 42.826008], [-117.282538, 32.53962], [-122.34266, 37.699279], [-87.940033, 41.644102], [-74.026675, 40.683935], [-96.806031, 40.710053], [-96.806031, 40.710053], [-112.3239143, 33.29026], [-76.7115205, 39.197211], [-73.508143, 41.187054], [-87.940033, 41.644102], [-81.046876, 35.001706], [-118.668404, 33.704538], [-111.9869461, 40.6275567], [-122.514926, 37.708075], [-122.514926, 37.708075], [-122.34266, 37.699279], [-74.026675, 40.683935], [-90.4181075, 41.696088], [-122.436232, 47.4953154], [-43.795449, -23.08302], [-122.34266, 37.699279], [-96.806031, 40.710053], [-74.026675, 40.683935], [-74.327484, 40.633736], [-118.3910877, 33.97632], [-118.668404, 33.704538], [-122.436232, 47.4953154], [-119.321696, 34.23444], [-87.940033, 41.644102], [-81.593675, 41.4570674], [-92.889433, 42.491921], [-74.026675, 40.683935], [-74.026675, 40.683935], [-90.137908, 29.889574], [-83.353955, 32.04683], [-90.137908, 29.889574], [-74.045819, 40.750571], [-71.33156600000001, 42.894917], [-73.83095261362119, 40.75934966052931], [-77.40747, 39.021548]]
    
    coordinates_right_order = []
    for i in range(len(coordinates_list)):
        local_list = []
        
        local_list.append(coordinates_list[i][1])
        local_list.append(coordinates_list[i][0])
        
        coordinates_right_order.append(local_list)

    text_list = ['Can all businesses take @blueapron‘s lead here? Paid day off to #vote lets get that #trending https://t.co/Ks2vM94AOr', 'New Swag. Quarantine Haircut. Repping Gen-X, Filmmakers, Artists, Goths for the #YangGang &amp; @AndrewYang. ✊ https://t.co/z6GqahzuPy', 'Loved this insightful conversation with @AndrewYang and @mcuban. https://t.co/QjeKKcZC72', "I'm about to #SecureTheBag 💰 for @AndrewYang and the #YangGang https://t.co/Ga2Vdty6P3", 'Kept this above the door in my office forever so I could see it every time I walked out #BeWater #30For30 https://t.co/XmdnlixIVZ', 'Fighters are people too! #JiuJitsuForYang #UFC @LeslieSmith_GF #EmpowerMMAFighters https://t.co/w9RS6ypmWM', 'Silence in solidarity.\n\n#BlackLivesMatter #Buffalo https://t.co/RDrOEYZ9t5', '@AndrewYang latest yangspeaks podcast about mental health is 100% on point. He gets it. https://t.co/qYuzlSEboy', '"We love @AndrewYang and we love you too!"\nActual quote from somebody I helped obtain a $250 micro grant from… https://t.co/J2jARrMgbX', '💯🇺🇸💰👇 I am soooo in favor in bail  ing out actual citizens and NOT big companies and banks and other corporations tha… https://t.co/bQ4YbAY4vs', 'Let’s join the “Shake Up the Congress Car Protest &amp; Parade” organized by the Income Movement, 52 Chambers Street, N… https://t.co/K6gOqTskuD', '#YangGangDanceParty is tonight from 8PM to 10PM EST. If any #YangGang attending can successfully pull off a good mo… https://t.co/tUL1de5Q9n', "I'm thinking of hosting a #YangGang exclusive dance party over Zoom for an hour or two on Friday night, using a pla… https://t.co/RHLe2jFWto", 'This is another meaningful endorsement of another local candiate running for office here in #AZ. I am impressed wit… https://t.co/aSCJsWF7gN', 'This could have happened to any of us. Often, people don’t see our talents, achievements, joys, struggles, pain, lo… https://t.co/SyApXCxvzs', 'NEW episode of @JoeBiden’s podcast HERES THE DEAL featuring @AndrewYang is LIVE. \n\nBoth are asked by a listener wha… https://t.co/04uC0PP1gi', 'This makes sense to me. We bail out companies all the time. Wall Street. Airlines. That’s great. But what about the… https://t.co/vyOSsqHCgB', 'I did this today.  Did you?\n\n#UBI #YangGang https://t.co/KhAv3H20rS', 'Good morning! I am so excited to share that I had the HONOR of writing the theme song for @AndrewYang’s podcast wit… https://t.co/z2ucffKuko', 'Proud of the alliance of more than 20 Chinese American groups who have been donating medical PPE to hospitals, 1st… https://t.co/7LvVMNAf3l', 'Subscribed https://t.co/1abhuqSKOc', '❤️❤️❤️ https://t.co/YfDRZQyea7', 'If you’ve ever wondered how I came to support @AndrewYang, here is your answer. He fought for my friend and teammat… https://t.co/I1l5o4N0iy', 'World records broken for sure today @kulturec - we had a 3 year old (daughter) and a 98 year old (14 year old golde… https://t.co/YRsluaftja', 'Getting some masks sent out! #MasksForHumanity #YangGang https://t.co/zf3nem8gaV', 'Thank you @YGBookClub!! I had so much fun with this #TakeoverTuesday!\n\nThank you @AndrewYang, @EvelynYang,… https://t.co/lDmhhKLYlt', 'It\'s easy to say "stay home". Everyone understand that a life is the most important and they also don\'t want to tak… https://t.co/P5mapXwwOK', 'My #ScreamTeam heroes knock it out of the park in their new #YouTube podcast. Yang origin stories, racism, and bour… https://t.co/nk0KZxsvmU', '@AndrewYang, many people are hurting right now, so I have committed a #HumanityFirst micro grant towards… https://t.co/1i3cDHtFdF', 'For months I watched @AndrewYang warn voters that one day in the not too distant future, many of us would be stuck… https://t.co/LdowsNahxl', 'Hey @AndrewYang how about a shout out to the millions of Manufacturing workers who are showing up to make the food,… https://t.co/twrd53a89y', 'UBI is apparently also very contagious. Hat tip to @AndrewYang for being a superspreader, if not Patient Zero https://t.co/iWfrrP2ZXs', 'He didn’t need to become President. Unfortunately it took a national crises for @AndrewYang’s signature policy to b… https://t.co/YoikTgDRum', 'Had to our for one last drink at our local. As of tomorrow.... no more. Thinking of our friends in the service indu… https://t.co/3e1AyKI3l2', '57 million Americans live off the gig economy....actors, musicians, personal trainers, independent contractors... h… https://t.co/ADs52Jm9KU', 'This might be a good time to implement a short term #FreedomDividend. I think it would go a long way for most. @AndrewYang #yanggang', 'Why not combine the GOP/ @realDonaldTrump plan with the @AndrewYang @TulsiGabbard plan? \nPass #PayrollTaxRelief-the… https://t.co/9W84tVju2D', 'Die hard or lazy? #YangGang https://t.co/fXZie8ROyw', 'NEWS: @AndrewYang is launching a new nonprofit that will seek to advance the ideas of his camapign. \n\nThere will be… https://t.co/9k1pTJ6zLR', 'Excited for what we can accomplish together. https://t.co/DqvqwS3zdw', 'This beautiful piece by @imstilljulie just came in the mail. All it needs is a few pen strokes from @AndrewYang. (c… https://t.co/chd6OgLlqz', 'Tonight will be the last #DemDebate before Super Tuesday, so this debate really matters. \n\nLet me be clear: all Ame… https://t.co/O19bSRI9E9', '"Andrew will continue to be a fierce advocate for Universal Basic Income as we continue to see the impact of automa… https://t.co/VwpTF6jgl1', '$tories - Election Day (Freestyle) [Feat. Andrew Yang] https://t.co/6P5IqJTXuE @AndrewYang @evelynyang… https://t.co/cx6eaLqwdg', 'Is this @CollegeGameDay or an @AndrewYang press hit?\n\nLet’s go New Hampshire! Tomorrow is the day! https://t.co/6OKpNPIj1n', 'A “Vote for @AndrewYang” mural on Roosevelt Ave. in Flushing, Queens, NYC, in the heart of Chinatown. Whoever owns… https://t.co/JvmmIHn6BA', 'Just had our server at Outback tell us she still has the @AndrewYang business card we left last time and she plans… https://t.co/tMfhSBsd2w']

    name_list = ['Sepideh Moafi', 'chad rullman', 'Oliver Maroney', '🇺🇸Fred The Felon🇺🇸', 'Matt Dembinsky', 'Cas    hBill 🧢', 'lisamkhoury', 'AV_Seal', 'CashBill 🧢', 'Dave Ross', 'Ching Juhl 陈清🧢', 'Alan Wilkins🧢🌺🔮🌹🤠🇺🇲', 'Alan   Wilkins🧢🌺🔮🌹🤠🀼򌠧', 'Garrick A. McFadden, Esq.', 'Lawrence Brown, MD, MPH, MHS', 'TJ Ducklo', 'Dave Ross', 'Move F orward 🧢', 'suzy shinn', 'Karen Kwan', 'jack', 'jack', 'CashBill 🧢', 'Griffin R. Baum M.D.', 'Erin #ICantbreathe🧢💡🤠', 'Trevor Russell 🠧', 'KeisukeHonda(本田圭佑)', 'CashBill 🧢', 'Alan Wilkins🧢🌺🔮🌹🤠🇺🇲', 'Matt Stevens', 'Hugh Welsh',   'Jeff Yang', 'Marc Ambinder', 'Matt Case', 'lee arenberg', 'Tony Sheffler', 'Geraldo Rivera', 'Charity 🧢', 'Matt Stevens', 'Susan Danziger', 'Erick Sanchez', 'Martin Luther King III', 'Erick Sanchez', '$tories 🧢', 'Zach Graumann🧢', 'Ryan Songalia', 'Nate Daniels']
    '''

    '''
    sample_map = folium.Map(location=[50, 5],
                            zoom_start=5)
    
    for i in range(len(coordinates_list)):
        marker = folium.Marker(coordinates_right_order[i], popup=(name_list[i] + ':     ' + text_list[i]))
        marker.add_to(sample_map)
        
    sample_map.save(map_file)
    '''
    
    
if __name__ == '__main__':
    
    #parser = get_parser()
    #args = parser.parse_args()
    
    make_map()