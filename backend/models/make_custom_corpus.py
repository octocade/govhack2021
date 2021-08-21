import csv

def construct_corpus():
	# Job descriptions.
	job_desc = {}
	with open('../aus_skills_data_dump/dumps/job_dump', 'r') as fh:
		data = eval(fh.read())
		for key, value in data.items():
			# Strin map to a job code.
			job_desc[value['desc:']] = value['code']

	# Skillsets.
	compmetencies = {}

	with open('../aus_skills_data_dump/Core_competencies-Table 1.csv', 'r') as fh:
		reader = csv.reader(fh, delimiter=',')
		skip_count = 0
		for row in reader:
			if not skip_count >= 1:
				skip_count += 1
				continue
			data = row[-1].strip()
			if data in compmetencies: continue
			# Map to a code.
			compmetencies[data] = row[0]

	# Personality types.
	# Just used glassdoor since it is unused.
	with open('../../personality_dumps/4_glassdoor.txt', 'r') as fh:
		lines = fh.readlines()
		lines = [l.strip() for l in lines if len(l.split()) > 4]
	
		peronality = lines

	# Youtube channel descriptions.
	
	youtube_channel_desc = []
	with open('../../channel_data_corpus', 'r') as fh:
		lines = fh.readlines()
		for l in lines:
			if l:
				youtube_channel_desc.append(l.strip())

	return list(job_desc.items()) + list(compmetencies.items()) + peronality + youtube_channel_desc

# preserve dec -> job mappings
# ~700 sentances.
corpus = construct_corpus()
with open('corpus_dump', 'w') as fh:
	for line in corpus:
		if "tuple" in str(line.__class__): 
			# Specia case for mapping preservation.
			line = "%s~%s" % (line[0], line[1])
		fh.write("%s\n" % str(line))
