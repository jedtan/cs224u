from format_imsdb import format_script
import math
from extract_features import extract_features

file_base = "imsdb_scripts/"

file_name = '{}{}'.format(file_base,"American Hustle.txt")


scenes = format_script(file_name)


# parameter to be tuned - segment length in number of minutes/pages


# divide film into 30 minute chunks

# Divide film by page numbers
def script_to_n_chunks(scenes, num_segments = 4):
	def get_script_by_page(scenes):
		disaggregated_script = [event for events in scenes for event in events]
		script_by_page = []
		curr_events = []
		for event in disaggregated_script:
			if event[1] == 'page number':
				script_by_page.append(curr_events)
				curr_events = [] # don't include page number as event
			else:
				curr_events.append(event)
		return script_by_page
	# divide film into four chunks
	# Returns generator
	def get_n_chunks(l, n):
		return [l[i:i+n] for i in xrange(0, len(l), n)]
	def get_num_chunks(l, num_segments):
		return math.ceil(len(l)/float(num_segments))
	script_by_page = get_script_by_page(scenes)
	num_chunks = get_num_chunks(script_by_page, num_segments)
	temp = get_n_chunks(script_by_page, int(num_chunks))
	chunks = []
	# temp has four elements each with 38 elements
	for chunk in temp:
		chunks.append([event for page in chunk for event in page])
	return chunks

# Process data and build features. Scale features is next step

# scaling data
def build_features():
	with open('imsdb_ratings.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if get_status(row) == "Good" or get_status(row) == "Bad":
				file_name = file_base + row[0] + ".txt"
				scenes = format_script(file_name)
				chunks = script_to_n_chunks(scenes)
				features = []
				for chunk in chunks:
				# change input parameter to scenes for extract features
					chunk_features = extract_features(file_name, row[0])
					features = features + chunk_features

#chunks = script_to_n_chunks(scenes)
#features = []
#for chunk in chunks:
# change input parameter to scenes for extract features
#	chunk_features = extract_features(file_name, "American Hustle")
#	features = features + chunk_features

