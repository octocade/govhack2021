import os

personaility_types_to_career = {
"ISTJ": set(),
"ISTP": set(),
"ISFJ": set(),
"ISFP": set(),
"INFJ": set(),
"INFP": set(),
"INTJ": set(),
"INTP": set(),
"ESTP": set(),
"ESTJ": set(),
"ESFP": set(),
"ESFJ": set(),
"ENFP": set(),
"ENFJ": set(),
"ENTP": set(),
"ENTJ": set()
}

IGNORE = set(["..", ".", ".DS_Store"])

def parse_novoresume(lines):
	p_type = ''
	capturing = []

	for i in range(len(lines)):
		line = lines[i]
		words_in_line = line.split()
		if not words_in_line: 
			# print(capturing)
			if p_type and len(capturing) > 0:
			
				for job in capturing:
					personaility_types_to_career[p_type].add(job)
				p_type = ''
				# print(capturing)
				capturing = []
			continue

		if words_in_line[0] in personaility_types_to_career:
			p_type = words_in_line[0]
		else:
			if p_type:
				capturing.append(line.strip())
			# Capture grouped together stuff.
	# print(personaility_types_to_career)

def parse_indeed(lines):
	p_type = ''
	capturing = []
	
	for i in range(len(lines)):
		line = lines[i]
		words_in_line = line.split()
		if not words_in_line: 
			# print(capturing)
			if p_type and len(capturing) > 0:
			
				for job in capturing:
					personaility_types_to_career[p_type].add(job)
				p_type = ''
				# print(capturing)
				capturing = []
			continue

		if words_in_line[0] in personaility_types_to_career:
			p_type = words_in_line[0]
		else:
			if p_type:
				capturing.append(line.strip())
	# print(personaility_types_to_career)


def parse_workopolis(lines):
	p_type = ''
	capturing = []
	
	for i in range(len(lines)):
		line = lines[i]
		words_in_line = line.split()
		if not words_in_line: 
			# print(capturing)
			if p_type and len(capturing) > 0:
			
				for job in capturing:
					personaility_types_to_career[p_type].add(job)
				p_type = ''
				# print(capturing)
				capturing = []
			continue

		if words_in_line[0] in personaility_types_to_career:
			p_type = words_in_line[0]
		else:
			if p_type:
				capturing.append(line.strip())
	# print(personaility_types_to_career)

def main():
	for file in os.listdir(os.path.join(os.getcwd(), "personality_dumps")):
		if file in IGNORE: continue
		with open(os.path.join(os.getcwd(), "personality_dumps", file), 'r') as fh:
			data = fh.readlines()
			if file == "1_novoresume.txt": 
				parse_novoresume(data)
			if file == "2_indeed.txt": 
				parse_indeed(data)
			if file == "3_workopolis.txt":
				parse_workopolis(data)
	# Yay this works!
	print(personaility_types_to_career)
	with open("personality_type_to_career", "w") as fh:
		fh.write(str(personaility_types_to_career))

main()