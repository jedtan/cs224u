from bs4 import BeautifulSoup
import urllib2
import re

transitions = ["FADE IN:", "FADE OUT:", "CUT TO:", "MATCH CUT:", "MONTAGE:", "INSERT:", "INTERCUT:", "SERIES OF SHOTS:", "DISSOLVE TO:", "BACK TO SCENE:"]
scene_headings = ["INT.", "EXT.", "INT/EXT."]
#character_name_parentheticals = ["(CONT'D)", "(V.O.)", "(O.S.)"]
# There are cases with no period after scene heading. 
#url = "http://www.imsdb.com/scripts/Revenant,-The.html"
# url = "http://www.imsdb.com/scripts/Silver-Linings-Playbook.html"

# different characters separated by multiple empty strings
# starts with first fade in
# http://www.writingroom.com/viewwriting/wr_how_to/How-To-Format-A-Screenplay


#text_types = ["scene heading", "action", "character name", "dialogue", "parenthetical", "transition", 'page number']

# Processed screenplay will be list of (text, type)
# merge lines that have no new line in between

def is_scene_heading(line):
	for heading in scene_headings:
		if heading in line:
			return True
	return False

def is_dialogue(curr_line, next_line):
	curr_line_split = curr_line.split()
	next_line_split = next_line.split()
	if len(curr_line_split) == 0 or len(next_line_split) == 0:
		return False
	if len(curr_line_split) > 2:
		return False
	# includes character cue
	if len(curr_line_split) == 2 and not (curr_line_split[1].startswith('(') and curr_line_split[1].endswith(')')):#curr_line_split[1] != "(CONT'D)":
		return False
	if not curr_line_split[0].isalpha():
		return False
	return True


# Returns list of list of tups: scenes --> lines --> (text, type)
# Each line in a scene is annotated with a type, 
# e.g. scene heading, dialogue, character name, action, transitiondef format_script(url = "http://www.imsdb.com/scripts/Revenant,-The.html"):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")
	scr = soup.find_all('td', attrs = {"class": "scrtext"})[0].get_text()
	scr_lines = [s.strip() for s in scr.splitlines()]
	idx = 0
	start = False # skips title, writer, etc.
	first_scene = True # for case that screenplay opens with transition
	scenes = []
	formatted_lines = []
	curr_lines = []
	page_number_regex = re.compile(r'\d\.')
	dialogue = False # flag for dialogue, triggered by character name
	while idx < len(scr_lines):
		curr_line = scr_lines[idx]
		if curr_line == u'':
			if len(curr_lines) > 0:
				if dialogue:
					formatted_lines.append((' '.join(curr_lines), "dialogue"))
					dialogue = False
				else:
					if start:
						formatted_lines.append((' '.join(curr_lines), "action"))
				curr_lines = []
		elif curr_line in transitions:
			formatted_lines.append((curr_line, "transition"))
			start = True
		elif page_number_regex.search(curr_line) is not None:
			formatted_lines.append((curr_line, "page number"))
		elif is_scene_heading(curr_line):
			if not first_scene:
				scenes.append(formatted_lines)
				formatted_lines = []
				formatted_lines.append((curr_line, "scene heading"))
			else: 
				first_scene = False
			start = True
		elif idx + 1 < len(scr_lines) and is_dialogue(curr_line, scr_lines[idx+1]):
			formatted_lines.append((curr_line, "character name"))
			dialogue = True
		else:
			curr_lines.append(curr_line)
		idx += 1
		if idx == len(scr_lines):
			formatted_lines = formatted_lines[:len(formatted_lines)-2]
			scenes.append(formatted_lines)
	return scenes






