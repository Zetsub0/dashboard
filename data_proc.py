import xml.etree.ElementTree as xml
from os import walk
import pandas as pd
import datetime
import csv
import dload
import numpy as np


#excel_data = pd.read_excel('graph3.xls', index_col=None, header=None)
#for name in excel_data.iterrows():
#	print(name[1].tolist())

#median_cost = excel_data[2].median()


regions = dict()
nums_regions = median_excel_data = pd.read_excel('reg.xlsx', index_col=None, header=None)

for row in nums_regions.iterrows():
	regions[row[1].tolist()[1].replace('\xa0', ' ')] = [row[1].tolist()[0], 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0]

regions_routes = regions.copy()
#print(regions)

median_excel_data = pd.read_excel('M1_b.xls', index_col=None, header=None)
median_excel_data = median_excel_data.fillna(0)
median_excel_data = median_excel_data[1:]
for row in median_excel_data.iterrows():
	regions[row[1].tolist()[0].replace('  ', ' ')][1] += row[1].tolist()[4]
	regions[row[1].tolist()[0].replace('  ', ' ')][2] += row[1].tolist()[5]

	regions[row[1].tolist()[0].replace('  ', ' ')][5] += row[1].tolist()[6]
	regions[row[1].tolist()[0].replace('  ', ' ')][4] += row[1].tolist()[2]
	regions[row[1].tolist()[0].replace('  ', ' ')][4] += row[1].tolist()[3]

	if not(regions[row[1].tolist()[0].replace('  ', ' ')][6]):
		regions[row[1].tolist()[0].replace('  ', ' ')][6] = row[1].tolist()[1]

budget_excel_data = pd.read_excel('budget.xlsx', index_col=None, header=None)
for row in budget_excel_data.iterrows():
	regions[row[1].tolist()[0].replace('  ', ' ')][3] += int(row[1].tolist()[1][:-2].replace(' ', ''))


school_excel_data = pd.read_excel('M1_school.xls', index_col=None, header=None)
school_excel_data = school_excel_data.fillna(0)
school_excel_data = school_excel_data[1:]
for row in school_excel_data.iterrows():
	regions[row[1].tolist()[0].replace('  ', ' ')][12] += row[1].tolist()[5]
	regions[row[1].tolist()[0].replace('  ', ' ')][13] += row[1].tolist()[6]
	regions[row[1].tolist()[0].replace('  ', ' ')][14] += row[1].tolist()[7]


volontier_excel_data = pd.read_excel('M1_vol.xls', index_col=None, header=None).fillna(0)
volontier_excel_data = volontier_excel_data[1:]
vol1 = volontier_excel_data[10::31]
vol2 = volontier_excel_data[15::12]

for i in range(len(vol1[0].tolist())):
	regions[vol1[0].tolist()[i].replace('  ', ' ')][11] += vol1[4].tolist()[i]
	regions[vol2[0].tolist()[i].replace('  ', ' ')][11] += vol2[4].tolist()[i]


grant_median_dict = dict()
grant_median_excel_data = pd.read_excel('median.xls', index_col=None, header=None).fillna(0)
grant_median_excel_data = grant_median_excel_data[1:]
for row in budget_excel_data.iterrows():
	if row[1].tolist()[0].replace('  ', ' ') in grant_median_dict:
		grant_median_dict[row[1].tolist()[0].replace('  ', ' ')].append(row[1].tolist()[3])
	else:
		grant_median_dict[row[1].tolist()[0].replace('  ', ' ')] = []

#print(grant_median_dict)
median_data = []

# сохраняем обобщенную таблицу
#with open('grant_median_reg.csv', 'w', newline='') as file:
#	writer = csv.writer(file)
#
#	writer.writerow(["name", "median"])
#	for key, value in grant_median_dict.items():
#
#		writer.writerow([key, np.median(value)])


news_excel_data = pd.read_excel('M1_news.xls', index_col=None, header=None)
news_excel_data = news_excel_data[1:]
new_users = news_excel_data[::12]
budget_news_region = news_excel_data[2::12]
amount_news_region = news_excel_data[4::12]
title_amount_news_region = news_excel_data[3::12]
title2_amount_news_region = news_excel_data[8::12]
amount2_news_region = news_excel_data[9::12]
publication_amount_news_region = news_excel_data[11::12]

for i in range(len(new_users[0].tolist())):
	regions[new_users[0].tolist()[i].replace('  ', ' ')][7] += new_users[2].tolist()[i]
	regions[budget_news_region[0].tolist()[i].replace('  ', ' ')][8] += budget_news_region[2].tolist()[i]
	
	regions[amount_news_region[0].tolist()[i].replace('  ', ' ')][9] += amount_news_region[2].tolist()[i]
	regions[title_amount_news_region[0].tolist()[i].replace('  ', ' ')][9] += title_amount_news_region[2].tolist()[i]
	regions[title2_amount_news_region[0].tolist()[i].replace('  ', ' ')][9] += title2_amount_news_region[2].tolist()[i]
	regions[amount2_news_region[0].tolist()[i].replace('  ', ' ')][9] += amount2_news_region[2].tolist()[i]
	regions[publication_amount_news_region[0].tolist()[i].replace('  ', ' ')][9] += publication_amount_news_region[2].tolist()[i]


chisl_excel_data = pd.read_excel('chisl.xls', index_col=None, header=None).fillna(0)
for row in chisl_excel_data.iterrows():
	name = row[1].tolist()[0].replace('  ', ' ').strip()
	regions[name][10] += row[1].tolist()[1]


# сохраняем обобщенную таблицу
with open('region_vectors.csv', 'w', newline='') as file:
	writer = csv.writer(file)

	writer.writerow(["name", "code", "amount_grant", "budget_grant_reg", "budget_reg", "budget2youth_reg", "volontiers_amount_reg", "area", "uniq_users", "budget_marketing", "marketing_units", "population", "volontiers_amount", "volontiers_amount_school", "volontiers_amount_college", "volontiers_amount_university"]) #"volontiers_amount", "family_road", "volontiers_road", "sport_road"])
	for key, value in regions.items():
		writer.writerow([key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13], value[14]])


regions_routes = dict()

for row in nums_regions.iterrows():
	regions_routes[row[1].tolist()[1].replace('\xa0', ' ')] = [row[1].tolist()[0], None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


roads_excel_data = pd.read_excel('М1_routes.xls', index_col=None, header=None)
roads_excel_data = roads_excel_data[1:]
biomed_users = roads_excel_data[1::27]
nanotech = roads_excel_data[2::27]
aerospace = roads_excel_data[3::27]
national_economy = roads_excel_data[4::27]
infor_tech = roads_excel_data[5::27]
others = roads_excel_data[6::27]
news_road = roads_excel_data[8::27]
bad_road = roads_excel_data[11::27]
art_road = roads_excel_data[12::27]
family_road = roads_excel_data[15::27]
volontiers_road = roads_excel_data[24::27]
sport_road = roads_excel_data[25::27]


for i in range(len(biomed_users[0].tolist())):
	if not(regions_routes[biomed_users[0].tolist()[i].replace('  ', ' ')][1]):
		regions_routes[biomed_users[0].tolist()[i].replace('  ', ' ')][1] = biomed_users[1].tolist()[i]


	regions_routes[biomed_users[0].tolist()[i].replace('  ', ' ')][2] += biomed_users[4].tolist()[i]
	regions_routes[nanotech[0].tolist()[i].replace('  ', ' ')][3] += nanotech[4].tolist()[i]
	
	regions_routes[aerospace[0].tolist()[i].replace('  ', ' ')][4] += aerospace[4].tolist()[i]
	regions_routes[national_economy[0].tolist()[i].replace('  ', ' ')][5] += national_economy[4].tolist()[i]
	regions_routes[infor_tech[0].tolist()[i].replace('  ', ' ')][6] += infor_tech[4].tolist()[i]
	regions_routes[others[0].tolist()[i].replace('  ', ' ')][7] += others[4].tolist()[i]

	regions_routes[news_road[0].tolist()[i].replace('  ', ' ')][8] += news_road[4].tolist()[i]
	regions_routes[bad_road[0].tolist()[i].replace('  ', ' ')][9] += bad_road[4].tolist()[i]
	regions_routes[art_road[0].tolist()[i].replace('  ', ' ')][10] += art_road[4].tolist()[i]
	regions_routes[family_road[0].tolist()[i].replace('  ', ' ')][11] += family_road[4].tolist()[i]
	regions_routes[volontiers_road[0].tolist()[i].replace('  ', ' ')][12] += volontiers_road[4].tolist()[i]
	regions_routes[sport_road[0].tolist()[i].replace('  ', ' ')][13] += sport_road[4].tolist()[i]



# сохраняем обобщенную таблицу
#with open('region_roads.csv', 'w', newline='') as file:
#	writer = csv.writer(file)
#
#	writer.writerow(["name", "code", "area", "biomed_users", "nanotech", "aerospace", "national_economy", "infor_tech", "others", "news_road", "bad_road", "art_road", "family_road", "volontiers_road", "sport_road"])
#	for key, value in regions_routes.items():
#			writer.writerow([key,value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13]])



print(regions_routes['Алтайский край'])
