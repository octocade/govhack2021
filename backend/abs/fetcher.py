import requests
import os


headers = {'accept': 'application/vnd.sdmx.data+json'}

os.mkdir('industry_dumps')

industries = [
              {
"id": "Q",
"order": 17,
"name": "Health Care and Social Assistance",
"names": {
"en": "Health Care and Social Assistance"
},
"parent": "TOT",
"annotations": [
10
]
},
{
"id": "O",
"order": 15,
"name": "Public Administration and Safety",
"names": {
"en": "Public Administration and Safety"
},
"parent": "TOT",
"annotations": [
11
]
},
{
"id": "C",
"order": 3,
"name": "Manufacturing",
"names": {
"en": "Manufacturing"
},
"parent": "TOT",
"annotations": [
12
]
},
{
"id": "D",
"order": 4,
"name": "Electricity, Gas, Water and Waste Services",
"names": {
"en": "Electricity, Gas, Water and Waste Services"
},
"parent": "TOT",
"annotations": [
13
]
},
{
"id": "B",
"order": 2,
"name": "Mining",
"names": {
"en": "Mining"
},
"parent": "TOT",
"annotations": [
14
]
},
{
"id": "TOT",
"order": 0,
"name": "All Industries",
"names": {
"en": "All Industries"
},
"annotations": [
9
]
},
{
"id": "F",
"order": 6,
"name": "Wholesale Trade",
"names": {
"en": "Wholesale Trade"
},
"parent": "TOT",
"annotations": [
15
]
},
{
"id": "H",
"order": 8,
"name": "Accommodation and Food Services",
"names": {
"en": "Accommodation and Food Services"
},
"parent": "TOT",
"annotations": [
16
]
},
{
"id": "P",
"order": 16,
"name": "Education and Training",
"names": {
"en": "Education and Training"
},
"parent": "TOT",
"annotations": [
17
]
},
{
"id": "R",
"order": 18,
"name": "Arts and Recreation Services",
"names": {
"en": "Arts and Recreation Services"
},
"parent": "TOT",
"annotations": [
18
]
},
{
"id": "N",
"order": 14,
"name": "Administrative and Support Services",
"names": {
"en": "Administrative and Support Services"
},
"parent": "TOT",
"annotations": [
19
]
},
{
"id": "J",
"order": 10,
"name": "Information Media and Telecommunications",
"names": {
"en": "Information Media and Telecommunications"
},
"parent": "TOT",
"annotations": [
20
]
},
{
"id": "L",
"order": 12,
"name": "Rental, Hiring and Real Estate Services",
"names": {
"en": "Rental, Hiring and Real Estate Services"
},
"parent": "TOT",
"annotations": [
21
]
},
{
"id": "G",
"order": 7,
"name": "Retail Trade",
"names": {
"en": "Retail Trade"
},
"parent": "TOT",
"annotations": [
22
]
},
{
"id": "E",
"order": 5,
"name": "Construction",
"names": {
"en": "Construction"
},
"parent": "TOT",
"annotations": [
23
]
},
{
"id": "S",
"order": 19,
"name": "Other Services",
"names": {
"en": "Other Services"
},
"parent": "TOT",
"annotations": [
24
]
},
{
"id": "I",
"order": 9,
"name": "Transport, Postal and Warehousing",
"names": {
"en": "Transport, Postal and Warehousing"
},
"parent": "TOT",
"annotations": [
25
]
},
{
"id": "M",
"order": 13,
"name": "Professional, Scientific and Technical Services",
"names": {
"en": "Professional, Scientific and Technical Services"
},
"parent": "TOT",
"annotations": [
26
]
},
{
"id": "K",
"order": 11,
"name": "Financial and Insurance Services",
"names": {
"en": "Financial and Insurance Services"
},
"parent": "TOT",
"annotations": [
27
]
}
]

for i in industries:
	industry_key = i["id"]
	industry_name = i["name"]
	print("GET:  " + industry_name)
	r = requests.get("https://api.data.abs.gov.au/data/JV/M1.7.H..AUS..?startPeriod=2020&detail=full", headers=headers)
	j = "_".join(industry_name.split())
	print(j)
	with open(os.path.join("industry_dumps", j + ".dump"), 'w') as fh:
		fh.write(r.text)

	print(r.text)
