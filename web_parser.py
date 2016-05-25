
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

soup = requests.get(alphabetical_base)
full_list = BeautifulSoup(soup.text)
mod_contents = full_list.find_all('td', valign="top")
movie_list = mod_contents[2].find_all('p')



all_movie_names = []

def fix_movie_name(movie_name):
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



		#http://www.omdbapi.com/?t=Interstellar&y=&plot=short&r=json

		"""current_link = link[0]['href']

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
			f.close()"""





"""with open('names.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	for player in player_urls:
		player_url = player.split('player/')
		player_url.insert(1, 'player/stats/')

		player_url = ''.join(player_url)

		
		
		player_page = BeautifulSoup(soup.text)
		mod_contents = player_page.find_all('div', {'class' : 'mod-content'})


		name_id = player.split('/')
		insert_row = name_id[len(name_id)-1]
		

		position = mod_contents[0].find_all('li', {'class': 'first'})[0].string.split(' ')[1]
		birthday = mod_contents[0].find_all('ul', {'class' : 'player-metadata'})[0].find_all('li')[0].text

		#position = mod_contents[0].find_all('ul', {'class' : 'player-metadata'})
		m = re.search('Age: ([0-9]+)', birthday)

		spamwriter.writerow((insert_row, m.group(1), position))

		years = mod_contents[2].find_all('tr')
		percentage_years = mod_contents[1].find_all('tr')[2:]
		try:
			with open(insert_row + '-totals.csv', 'w') as playerfile:
				playerwriter = csv.writer(playerfile, delimiter=',')
				for i, elem in enumerate(years[2:]):

					p_td = [e.string for e in percentage_years[i].find_all('td', text=True)]
					fg = p_td[4].split('-')
					p_td.pop(4)
					p_td.insert(4, fg[0])
					p_td.insert(5, fg[1])
					fg = p_td[7].split('-')
					p_td.pop(7)
					p_td.insert(7, fg[0])
					p_td.insert(8, fg[1])
					fg = p_td[10].split('-')
					p_td.pop(10)
					p_td.insert(10, fg[0])
					p_td.insert(11, fg[1])

					td = [e.string for e in elem.find_all('td', text=True)]
					fg = td[1].split('-')
					td.pop(1)
					td.insert(1, fg[0])
					td.insert(2, fg[1])
					fg = td[4].split('-')
					td.pop(4)
					td.insert(4, fg[0])
					td.insert(5, fg[1])
					fg = td[7].split('-')
					td.pop(7)
					td.insert(7, fg[0])
					td.insert(8, fg[1])
					td.insert(0, insert_row)
					if td[1] != "Career":
						end_val = int(td[1].split("-'")[1])
						if end_val > 16:
							year = 2016 - 1900 - end_val
						else:
							year = 2016 - 2000 - end_val
						td.insert(2, int(m.group(1)) - year)
						playerwriter.writerow(td + p_td)
						rows.append(td + p_td)
		except:
			print "ERROR: %s" %(insert_row)

	with open('all-data.csv', 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',')
		for line in rows:
			spamwriter.writerow(line)


		
			#print "ERROR: %s" %(insert_row)"""












