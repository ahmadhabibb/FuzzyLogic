import csv
import sys
import math
import pandas as pd
from pandas import DataFrame

# Ahmad Habib Fitriansyah
# Bandung, Indonesia
# 28 November 2019, 11:40 PM

def read_data():
    followers = []
    engagement = []
    with open('E:\Learning Coding\AI\Tugas 3\FuzzyLogic-1\influencers.csv', mode='r') as csv_input:
        influencers_data = csv.reader(csv_input)
        next(influencers_data)
        for row in influencers_data:
            followers.append(float(row[1]))
            engagement.append(float(row[2]))
    return followers, engagement

#  Linguistic
#
#  Follower Count    |      Small       Medium          Large          Huge
#  Engagement Rate   |      Low         Medium          High          
#  ------------------------------------------------------------------------
#  Acceptance        |      No          Low           Medium           High 

# FOLLOWER -------------------------------------------------------------------------------------
def follower_small(followers, index):
    data_followers = followers[index]
    if (data_followers <= 20000):
        return 1
    elif (data_followers <= 40000 and data_followers > 20000):
        count = (data_followers - 20000) / (40000 - 20000)
        return count
    elif (data_followers > 40000):
        return 0

def follower_medium(followers, index):
    data_followers = followers[index]
    if (data_followers < 40000 and data_followers > 20000):
        count = (40000 - data_followers) / (40000 - 20000)
        return count
    elif (data_followers >= 40000 and data_followers <= 45000):
        return 1
    elif (data_followers < 50000 and data_followers > 45000):
        count = (data_followers - 45000) / (50000 - 45000)
        return count
    else:
        return 0

def follower_large(followers, index):
    data_followers = followers[index]
    if (data_followers < 50000 and data_followers > 45000):
        count = (50000 - data_followers) / (50000 - 45000)
        return count
    elif (data_followers >= 50000 and data_followers <= 60000):
        return 1
    elif (data_followers < 70000 and data_followers > 60000):
        count = (data_followers - 60000) / (70000 - 60000)
        return count
    else:
        return 0

def follower_huge(followers, index):
    data_followers = followers[index]
    if (data_followers < 70000 and data_followers > 60000):
        count = (70000 - data_followers) / (70000 - 60000)
        return count
    elif (data_followers >= 70000):
        return 1
    else:
        return 0         

# ENGAGEMENT -------------------------------------------------------------------------------------
def engagement_low(engagement, index):
    data_engagament = engagement[index]
    if (data_engagament <= float(2)):
        return 1
    elif (data_engagament <= float(4) and data_engagament > float(2)):
        count = (data_engagament - 2) / (4 - 2)
        return count
    elif (data_engagament > 4):
        return 0

def engagement_medium(engagement, index):
    data_engagament = engagement[index]
    if (data_engagament < float(4) and data_engagament > float(2)):
        count = (4 - data_engagament) / (4 - 2)
        return count
    elif (data_engagament <= float(5.5) and data_engagament >= float(4)):
        return 1
    elif (data_engagament < float(7) and data_engagament > float(5.5)):
        count = (data_engagament - 5.5) / (7 - 5.5)
        return count
    else:
        return 0

def engagement_high(engagement, index):
    data_engagament = engagement[index]
    if (data_engagament < float(7) and data_engagament > float(5.5)):
        count = (7 - data_engagament) / (7 - 5.5)
        return count
    elif (data_engagament >= 7):
        return 1
    else:
        return 0

# RULE
#  eng\fol          small	 medium	   large	 huge
#  low				 N		   L		 M		  M
#  medium			 L	       M		 H		  H
#  high				 L		   M		 H		  H

def inference(small_fol, medium_fol, large_fol, huge_fol, low_eng, medium_eng, high_eng):
    rule = [[min(small_fol, low_eng), 'N'], [min(medium_fol, low_eng), 'L'], [min(large_fol, low_eng), 'M'], [min(huge_fol, low_eng), 'M'],
    	 	[min(small_fol, medium_eng), 'L'], [min(medium_fol, medium_eng), 'M'], [min(large_fol, medium_eng), 'H'], [min(huge_fol, medium_eng), 'H'],
    		[min(small_fol, high_eng), 'L'], [min(medium_fol, high_eng), 'M'], [min(large_fol, high_eng), 'H'], [min(huge_fol, high_eng), 'H']]

    no = []
    low = []
    medium = []
    high = []
    
    for i in range(len(rule)):
        if (rule[i][1] == "N"):
            no.append(rule[i][0])
        elif (rule[i][1] == "L"):
            low.append(rule[i][0])
        elif (rule[i][1] == "M"):
            medium.append(rule[i][0])
        elif (rule[i][1] == "H"):
            high.append(rule[i][0])

    return max(no), max(low), max(medium), max(high)

def defuzzyfication(a, b, c ,d):
    count = (a*20) + (b*35) + (c*70) + (d*100) / (a+b+c+d)
    return count

def main():
    brand_ambassadors = []
    best_ambassadors = []
    followers = []
    engagement = []
    jumAmbassadors = 20
    followers, engagement = read_data()

    # Count Linguistic
    for i in range(len(followers)):
        small_fol = follower_small(followers, i)
        medium_fol = follower_medium(followers, i)
        large_fol = follower_large(followers, i)
        huge_fol = follower_huge(followers, i)
        low_eng = engagement_low(engagement, i)
        medium_eng = engagement_medium(engagement, i)
        high_eng = engagement_high(engagement, i)

        no_value, low_value, med_value, high_value = inference(small_fol, medium_fol, large_fol, huge_fol, low_eng, medium_eng, high_eng)
        result = defuzzyfication(no_value, low_value, med_value, high_value)
        brand_ambassadors.append([result, (i + 1)])

    #OUTPUT
    print("Nilai Kelayakan dari Influencers :")
    print()
    for k in range(len(followers)):
        print(k+1,". -----------------")
        print("Jumlah Followers :",math.ceil(followers[k]))
        print("Nilai Kelayakan :",brand_ambassadors[k][0])
        print()

    print()
    print("Untuk melihat 20 Influencer terbaik, buka file chosen.csv !")
    
    brand_ambassadors.sort()
    for j in range(jumAmbassadors):
        best_ambassadors.append(brand_ambassadors[99-j][1])
        

    df = DataFrame(best_ambassadors)
    export_csv = df.to_csv("E:/Learning Coding/AI/Tugas 3/chosen.csv", header=False, index=None)

if __name__ == "__main__":
    main()    