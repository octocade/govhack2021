import csv

# TODO: consider handling desriptions?

# Name: code, desc mappings
JOBS = {}

"""
skill_task: {
	jobs: [{
		name:,
		code:,
	}, ],
	cluster: str,
	family: str,

}
"""
SKILLS = {}

"""
comptency: {
	# jobs_that_need_it: [ {
		name:,
		code:,
	}, ...
	]
	intermediate: [],
	high: [],
	basic: []
}
"""
COMPETENCIES = {}

def job_parser():
	with open('Occupation Descriptions-Table 1.csv', 'r') as fh:
		reader = csv.reader(fh, delimiter=',')
		skip_count = 0
		for row in reader:
			if not skip_count >= 1:
				skip_count += 1
				continue
			JOBS[row[1]] = {"code": row[0], "desc:": row[2]}
	with open('dumps/job_dump', 'w') as fh:
		fh.write(str(JOBS))

job_parser()


"""
ANZSCO_Code	ANZSCO_Title	Specialist_Task	% of time spent on task	Specialist_Cluster	% of time spent on cluster	Cluster_Family	% of time spent on family
1111	Chief Executives and Managing Directors	Direct financial operations	16%	Manage, monitor and undertake financial activities	16%	Business operations and financial activities	52%
"""
def skills_parser():
	with open('Specialist tasks-Table 1.csv', 'r') as fh:
		reader = csv.reader(fh, delimiter=',')
		skip_count = 0
		for row in reader:
			if not skip_count >= 1:
				skip_count += 1
				continue
			if row[2] not in SKILLS:
				SKILLS[row[2]] = {
					"jobs": [{"name": row[1], "code":row[0]}],
					"cluster": row[4],
					"family": row[6],
				}
			else:
				SKILLS[row[2]]["jobs"].append({"name": row[1], "code":row[0]})

	with open('dumps/skills_dump', 'w') as fh:
		fh.write(str(SKILLS))
skills_parser()


"""
ANZSCO_Code	ANZSCO_Title	Core_Competencies	Score	Proficiency_level	Anchor_value
1111	Chief Executives and Managing Directors	Numeracy	6	Intermediate	Calculate the square footage of a new home under construction based on plans using scales and ratios
"""
def competencies_parser():
	with open('Core_competencies-Table 1.csv', 'r') as fh:
		reader = csv.reader(fh, delimiter=',')
		skip_count = 0
		for row in reader:
			if not skip_count >= 1:
				skip_count += 1
				continue
			if row[2] not in COMPETENCIES:
				COMPETENCIES[row[2]] = {
					"High": [],
					"Intermediate": [],
					"Basic": [],
				}
			COMPETENCIES[row[2]][row[4]].append({"name": row[1], "code": row[0]})
	with open('dumps/competencies_dump', 'w') as fh:
		fh.write(str(COMPETENCIES))
competencies_parser()