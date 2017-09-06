
# Implementation of collaborative filtering recommendation engine

from dataset import dataset
from math import sqrt
#print "Sahil rating on C programming: {}n".format(book_dataset['Lisa Rose']['C programming'])
#print "Kangres rating on C programming: {}n".format(book_dataset['Michael Phillips']['C programming'])

#print 'All rating of users in following books are:'
#print dataset

def similarity_score(person1,person2):
	
	# Returns ratio Euclidean distance score of person1 and person2 

	both_viewed = {}		# To get both rated items by person1 and person2

	for item in dataset[person1]:
		if item in dataset[person2]:
			both_viewed[item] = 1

		# Conditions to check they both have an common rating items	
		if len(both_viewed) == 0:
			return 0

		# Finding Euclidean distance 
		sum_of_eclidean_distance = []	

		for item in dataset[person1]:
			if item in dataset[person2]:
				sum_of_eclidean_distance.append(pow(dataset[person1][item] - dataset[person2][item],2))
		sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

		return 1/(1+sqrt(sum_of_eclidean_distance))
	    
def pearson_correlation(person1,person2):

	# To get both rated items
	both_rated = {}
	for item in dataset[person1]:
		if item in dataset[person2]:
			both_rated[item] = 1

	number_of_ratings = len(both_rated)		
	
	# Checking for number of ratings in common
	if number_of_ratings == 0:
		return 0

	# Add up all the preferences of each user
	person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
	person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

	# Sum up the squares of preferences of each user
	person1_square_preferences_sum = sum([pow(dataset[person1][item],2) for item in both_rated])
	person2_square_preferences_sum = sum([pow(dataset[person2][item],2) for item in both_rated])

	# Sum up the product value of both preferences for each item
	product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

	# Calculate the pearson score
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
	if denominator_value == 0:
		return 0
	else:
		r = numerator_value/denominator_value
		return r

print'enter two person name to know similarity score'
print'user1:'
str1=input()
print'user2:'
str2=input()
print ('similarity score between user1 and user2 is=%f'%pearson_correlation(str1,str2))




def user_reommendations(person):

	# Gets recommendations for a person by using a weighted average of every other user's rankings
	totals = {}
	simSums = {}
	rankings_list =[]
	for other in dataset:
		# don't compare me to myself
		if other == person:
			continue
		sim = pearson_correlation(person,other)

		# ignore scores of zero or lower
		#if sim &lt;=0: 
		#	continue
		for item in dataset[other]:

			# only score book's which i haven't seen yet
			if item not in dataset[person] or dataset[person][item] == 0:

			# Similrity * score
				totals.setdefault(item,0)
				totals[item] += dataset[other][item]* sim
                                
				# sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+= sim

		# Create the normalized list

	rankings = [(total/1+simSums[item],item) for item,total in totals.items()]
	rankings.sort()
	rankings.reverse()
	# returns the recommended items
	recommendataions_list = [recommend_item for score,recommend_item in rankings]
	return recommendataions_list

s=str((input("enter user name to recommend book:")))
print('following are the book recommended for %s:'%s)
print user_reommendations(s)








