
import pandas as pd
import requests
import csv
import re
import string
from bs4 import BeautifulSoup

alphabetical_base = "http://www.imsdb.com/all%20scripts/"
imsdb_base = "http://www.imsdb.com"
imsdb_films_file = "imsdb_ratings.csv"
locations_directory = "imsdb_scripts/"

pull_scripts = False

soup = requests.get(alphabetical_base)
full_list = BeautifulSoup(soup.text)
mod_contents = full_list.find_all('td', valign="top")
movie_list = mod_contents[2].find_all('p')



all_movie_names = []

def fix_movie_name(movie_name):
	
	movie_name.replace("\"", " ")
	if "The" in movie_name:
		match_object = re.match(r'(.*?), The', movie_name)
		if match_object is not None:
			movie_name = "The " + match_object.group(0)[:-5]
	
	movie_name.replace(" ", "+")
	return movie_name

with open('imsdb_ratings.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile)

	for elem in movie_list:
		link = elem.find_all('a')

		all_movie_names.append(link[0].get_text())
		movie_name = link[0].get_text()

		api_movie_name = fix_movie_name(movie_name)
		
		api_link = "http://www.omdbapi.com/?t=%s&y=&plot=short&r=json&tomatoes=true" %(api_movie_name)


		r = requests.get(api_link)
		print api_movie_name
		movie_info = r.json()

		if 'imdbRating' not in movie_info:
			movie_info['imdbRating'] = "N/A"
		if 'Metascore' not in movie_info:
			movie_info['Metascore'] = "N/A"

		def get_elem(key):
			if key in movie_info:
				return movie_info[key]
			else:
				return "N/A"

		spamwriter.writerow((movie_name, get_elem("Genre"), get_elem('imdbRating'), get_elem('Metascore'), get_elem('tomatoRating'), get_elem('tomatoReviews'), get_elem('tomatoFresh'), get_elem('tomatoRotten'), get_elem('tomatoUserMeter'), get_elem('tomatoUserRating')))

		if pull_scripts:
			current_link = link[0]['href']

			new_request = imsdb_base + current_link
			current_path = requests.get(new_request)
			get_path = BeautifulSoup(current_path.text)

			details = get_path.find_all('table', {"class":"script-details"})
			all_links = details[0].find_all('a')
			script_link = all_links[len(all_links)-1]
			#print script_link

			movie_script_link = script_link['href']
			movie_script = requests.get(imsdb_base + movie_script_link)
			parsed_movie_script_page = BeautifulSoup(movie_script.text)


			print movie_name
			script_files = parsed_movie_script_page.find_all('pre')

			if len(script_files) > 0:
				script_text = script_files[0].get_text()

			
				file_name = locations_directory + movie_name + ".txt"

				f = open(file_name, 'w')
				f.write(script_text.encode('utf-8'))
				f.close()

















