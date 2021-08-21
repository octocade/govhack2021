from flask import request
from flask import Flask
import json
import gensim.models as gensimModels
import gensim
from gensim.models.doc2vec import Doc2Vec
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_NAME = "./models/doc2vec_model_final"
model = Doc2Vec.load(MODEL_NAME)
print(model)

with open('models/preserved_mappings', 'r') as fh:
	TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING = eval(fh.read())
print("number ofTOKANIZED_SENTANCE_TO_JOB_ID_MAPPING: " + str(len(TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING)))

JOB_ID_TO_DETAILS_MAPPING = {}

with open('aus_skills_data_dump/dumps/job_dump', 'r') as fh:
	data = eval(fh.read())
	for key, item in data.items():
		JOB_ID_TO_DETAILS_MAPPING[str(item["code"])] = {
			"name": key,
			"desc": item["desc:"]
		}

# Parse from wiki ontology + yt api.
youtube_interests = ["Rock music",
"Lifestyle",
"Film",
"Health",
"Food",
"Action game",
"Physical fitness",
"Pop music",
"Hobby",
"Strategy video game",
"Knowledge",
"Business",
"Video game culture",
"Independent music",
"Action adventure game",
"Entertainment",
"Sociology",
"Electronic music",
"Technology",
"Role playing video game",
"Music"]

# print(JOB_ID_TO_DETAILS_MAPPING)
def job_id_to_job_json(job_id):
	data = JOB_ID_TO_DETAILS_MAPPING[job_id] 
	data.update({"code": job_id})
	return data

def get_similar_jobs(query):
	raw_tokens = gensim.utils.simple_preprocess(query)
	print(raw_tokens)
	query_vector = model.infer_vector(raw_tokens)
	sims = model.dv.most_similar([query_vector], topn=len(model.dv))
	results = []
	# 677 job matching tokens.
	# Search in top 35 similar things top 2% of matches.
	for i in range(0, 10):
		document_id = sims[i][0]
		if str(document_id) in TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING:
			print("most similar match found at: %s with docId: %s" % (str(i), str(document_id)))
			print(TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING[str(document_id)])
			results.append(job_id_to_job_json(TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING[str(document_id)]["job_code"]))
		else:
			print("no match for sim index: " + str(i))
	return results

# /jobs?query=sentance here
# http://localhost:5000/get_jobs?query=food
@app.route("/get_jobs")
def get_jobs():
	query = request.args.get('query')
	print("get jobs query: " + query)
	results = get_similar_jobs(query)
	# print(results)
	return {"results": results}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# http://localhost:5000/get_youtube_interests?with_all_jobs=true
@app.route("/get_youtube_interests")
def get_youtube_interests():
	with_all_jobs = request.args.get('with_all_jobs')
	if not with_all_jobs:
		return { "youtube_interests": youtube_interests}
	else:
		data = []
		seen_job_codes = set()
		TRUNCATE_COUNT_PER_JOB = 3
		for interest in youtube_interests:
			similar_jobs = get_similar_jobs(interest)
			jobs_to_add = []
			jobs_seen = 0
			for job in similar_jobs:
				if job["code"] not in seen_job_codes:
					seen_job_codes.add(job["code"])
					job.update({"source": "Youtube: " + interest})
					jobs_to_add.append(job)
					jobs_seen += 1
				if jobs_seen >= TRUNCATE_COUNT_PER_JOB:
					break
			data.append({"interest": interest, "similar_jobs": jobs_to_add})
		# print(data)
		return {"youtube_interests_with_jobs": data};


with open("../personality_type_to_career", "r") as fh:
		PERSONAILITY_MAPPINGS_TO_CAREER = eval(fh.read())

IGNORE_CAREER_SET = {'Religion'}
# http://localhost:5000/personality_mappings?ptype=INTJ
@app.route("/personality_mappings")
def personality_mappings():
		ptype = request.args.get('ptype')
		# Web scrapped parsed personality type to career.
		potential_careers = PERSONAILITY_MAPPINGS_TO_CAREER[ptype]
		# For all potential careers, get similar ML learnt vector.
		seen_jobs = set()
		jobs = [] 

		for career in potential_careers:
			if career in IGNORE_CAREER_SET:
				continue
			TRUNCATE_COUNT_PER_JOB = 1
			similar_jobs = get_similar_jobs(career)
			jobs_to_add = []
			jobs_seen = 0

			for job in similar_jobs:
				if job["code"] not in seen_jobs:
					seen_jobs.add(job["code"])
					job.update({"source": "Person: " + career + ", " + ptype})
					jobs_to_add.append(job)
					jobs_seen += 1
					if jobs_seen >= TRUNCATE_COUNT_PER_JOB:
						break
			jobs.append({"career": career, "similar_jobs": jobs_to_add})
		return {"personality_mappings": jobs}
