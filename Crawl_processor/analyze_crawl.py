import crawl_processor as cp
import utils as u
import operator
from collections import Counter
import os

def main():

	list=cp.get_tokenLists()
	
	while(1):
		os.system('clear')
		print("=========== Menu ===========")
		ip=input("\n1.Number of pages crawled \n2.Longest page \n3.500 most frequent words \n4.20 most common three grams \n5.20 most common two grams \n6.Subdomains \n7.Exit\nEnter your choice: ")
		print ''

		if ip==1:
			string = "Number of pages crawled : " + str(len(list[0]))
			print string
			#url_freq = u.computeWordFrequencies(list[0])
			#print url_freq
			file = open('pages_crawled.txt','w')
			file.write(string+'\n\n')
			file.close()
	
		elif ip==2:
			max_url=list[0][0]
			max=len(list[1][0])
			url_list=list[0]
			token_list=list[1]
			i=0
			index=0
			for page in token_list:	
				if len(page)>max:
					max_url=url_list[i]
					index=i
				i+=1

			string = "The URL of largest page is " + max_url + "\nLength of page is : "+str(len(token_list[index]))
			print string

			file = open('longest_page.txt', 'w')
			file.write(string+'\n\n')
			file.close()

			
		elif ip==3:
			allwords = []
			for page in list[1]:
				allwords += page

			words=u.computeWordFrequencies(allwords)
			sortedwords=words.most_common()

			stop_file = open('stop_words.txt', 'r')
			stop_words = stop_file.read().split('\n')
			stop_file.close()

			file = open('Frequent.txt', 'w')
			file.write('Here are the 500 most frequent words:\n')

			print "Here are the 500 most frequent words:"
			count = 0
			i = 0
			while True:
				if count == 500:
					break

				if sortedwords[i][0].isalpha() and sortedwords[i][0] not in stop_words:
					string = sortedwords[i][0] + ' : ' + str(sortedwords[i][1])
					print string
					file.write(string+'\n')
					count += 1

				i += 1

			file.write('\n')
			file.close()


		elif ip==4:
			#three_grams={}
			pages=list[1]
			
			all_3_grams = []
			for page in pages:
				gram_3_list = u.getThreeGrams(page)
				all_3_grams += gram_3_list

			all_3_grams_freq = Counter(all_3_grams)
			sorted_3_grams = all_3_grams_freq.most_common()

			stop_file = open('stop_words.txt', 'r')
			stop_words = stop_file.read().split('\n')
			stop_file.close()

			file = open('three_grams.txt','w')
			file.write('The 20 most common 3-grams:\n')

			print "Welcome to 3-grams! Here are the 20 most common 3-grams:"

			count = 0
			i = 0
			while True:
				if count == 20:
					break

				tup = sorted_3_grams[i][0]

				if tup[0].isalpha() and tup[1].isalpha() and tup[2].isalpha():
					if tup[0] not in stop_words and tup[1] not in stop_words and tup[2] not in stop_words:
						string = sorted_3_grams[i][0][0]+' '+sorted_3_grams[i][0][1]+' '+sorted_3_grams[i][0][2]+' : '+str(sorted_3_grams[i][1])
						print string
						file.write(string+'\n')
						count += 1

				i += 1

			file.write('\n')
			file.close()
				
			
		elif ip==5:
			pages=list[1]
			all_2_grams=[]
			for page in pages:
				gram_2_list = u.getTwoGrams(page)
				all_2_grams += gram_2_list

			all_2_grams_freq = Counter(all_2_grams)
			sorted_2_grams = all_2_grams_freq.most_common()

			stop_file = open('stop_words.txt', 'r')
			stop_words = stop_file.read().split('\n')
			stop_file.close()

			file = open('two_grams.txt','w')
			file.write('The 20 most common 2-grams:\n')
			
			print "Welcome to two grams! Here are the 20 most common two grams:"
			count=0
			i=0
			while True:
				if count==20:
					break

				tup=sorted_2_grams[i][0]

				if tup[0].isalpha() and tup[1].isalpha():
					if tup[0] not in stop_words and tup[1] not in stop_words:
						string = sorted_2_grams[i][0][0]+' '+sorted_2_grams[i][0][1]+' : '+str(sorted_2_grams[i][1])
						print string
						file.write(string+'\n')
						count+=1

				i+=1

			file.write('\n')
			file.close()

			
		elif ip==6:
			sub = cp.get_subCount(list[0])

			file = open('Subdomains.txt', 'w')
			file.write('Subdomains of ics.uci.edu and number of pages crawled within each subdomain:\n')

			print "Welcome to subdomains! Here are the subdomains alphabetically arranged with their size displayed:"
			for name in sub:
				string = "http://" + name[0] + ".ics.uci.edu : " + str(name[1])
				print string
				file.write(string+'\n')

			file.write('\n')
			file.close()
				
		elif ip==7:
			break

		else:
			continue

		raw_input()
			

if __name__ == "__main__":
	main()
