
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sys, os
import pandas.io.sql as psql
import psycopg2 as pg
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
import json
import math

# Connect to database
conn = pg.connect(host='192.168.61.4', database='summer', user='postgres')

#Load the relationship between problem_id(id) and chanllenge_id(challenge_id)
df_problems = pd.read_sql_query('select * from problems_multiple_choice_problem', con=conn)

#Load the relationship between challenge_id(id) and quest_id(quest_id)
df_challenges = pd.read_sql_query('select * from content_challenge', con=conn)

#Load the relationship between quest_id(id) and order(order)
df_quests = pd.read_sql_query('select * from content_quest', con=conn)

quad_list = []
for row_index, row in df_problems.iterrows():
    quad = {}
    if not math.isnan(row['challenge_id']):
        quad['problem_id'] = row['id']
        quad['challenge_id'] = int(row['challenge_id'])
        quad_list.append(quad)
        
for item in quad_list:
    for row_index, row in df_challenges.iterrows():
        if (item['challenge_id'] == row['id']) & (not math.isnan(row['quest_id'])):
            item['quest_id'] = int(row['quest_id'])


# In[2]:


# print(quad_list)
quad_list1 = []
for item in quad_list:
    if len(item) == 3:
        quad_list1.append(item)

for item in quad_list1:
    for row_index, row in df_quests.iterrows():
        if item['quest_id'] == row['id']:
            item['order'] = int(row['order'])


# In[3]:


df_quad = pd.DataFrame(quad_list1)
df_quad = df_quad.sort_values(by = ['order', 'challenge_id'])
# print(df_quad)


# In[4]:


# Load submissions
df_submissions = pd.read_sql_query('select * from problems_multiple_choice_submission', con=conn)
df_submissions.head()
# Load choices of submissions
df_choice = pd.read_sql_query('select * from problems_multiple_choice_optionselection', con=conn)
df_choice.head()
# Encode the choices of each submission
grouped = df_choice.groupby('submission_id')
choice = []

for group_name, df_group in grouped:
    choice_encode = ''
    for row_index, row in df_group.iterrows():
        if row['was_selected']:
            choice_encode += '1'
        else:
            choice_encode += '0'
    choice.append(choice_encode)

df_submissions = df_submissions.sort_values(by=['id'])
df_submissions['choice_enc'] = choice
df_submissions.head()


# In[5]:


# Correct rate of the submission
# correct_rate = 1 means the student passed
df_submissions['correct_rate'] = df_submissions.groupby('problem_id', group_keys=False).apply(lambda g: g['score'] / g['score'].max())
df_submissions = df_submissions.sort_values(by = ['problem_id', 'user_id', 'timestamp'])
print(df_submissions.head())


# In[6]:


# The first submission is -1
df_submissions = df_submissions.reset_index(drop=True)
first = []
# df_submissions = df_submissions.groupby(['problem_id', 'user_id'], group_keys = False, as_index = False, sort = False)
current_id = ''
for row_index, row in df_submissions.iterrows():
    if row['user_id'] != current_id:
        first.append(1)
        current_id = row['user_id']
    else:
        first.append(0)
        current_id = row['user_id']
df_submissions['first'] = first  
df_submissions


# In[7]:


# Time spent between two submissions
diff = df_submissions['timestamp'].diff().astype('timedelta64[s]')
df_submissions['time_duration'] = diff
df_submissions


# In[8]:


# detecting gaming
pro_id = 327
test = 0
df_pcrsuser = pd.read_sql_query('select * from users_pcrsuser', con=conn)

def judge_null(_digits):
    digit_list = [int(d) for d in _digits]
    if sum(digit_list) == 0:
        return True
    else:
        return False
    
def judge_student(user_id):
    for row_index, row in df_pcrsuser.iterrows():
        if row['username'] == user_id:
            return row['is_student']
    
def gaming_detect(pro_id):
    df_one_problem = df_submissions[df_submissions['problem_id'] == pro_id]
    game_id = set()
    first_pass_id = set()
    all_id = set()
    count = 0
    for row_index, row in df_one_problem.iterrows():
#         if judge_student(row['user_id']):
        all_id.add(row['user_id'])
        if row['first'] == 1:
            count = 1
        if (row['first'] == 1) & (row['correct_rate'] >= 0.99):
            first_pass_id.add(row['user_id'])
        if (row['first'] == 1) & judge_null(row['choice_enc']):
            game_id.add(row['user_id'])
        if (count >= 3) & (abs(row['time_duration']) < 8):
            game_id.add(row['user_id'])
#         if abs(row['time_duration']) < 5:
#             game_id.add(row['user_id'])
        count += 1
    return (game_id, first_pass_id, all_id)

test = gaming_detect(pro_id)
print(len(test[0]))
    


# In[9]:


# detecting gaming1
def gaming_detect_after(pro_id):
    df_one_problem = df_submissions[df_submissions['problem_id'] == pro_id]
    game_id = set()
    first_pass_id = set()
    all_id = set()
    count = 0
    k = 0
    for row_index, row in df_one_problem.iterrows():
#         if judge_student(row['user_id']):
#         print(df_one_problem.iloc[0]['id'])
        all_id.add(row['user_id'])
        if row['first'] == 1:
            count = 1
        if (row['first'] == 1) & (row['correct_rate'] >= 0.99):
            first_pass_id.add(row['user_id'])
        if (row['first'] == 0) & judge_null(row['choice_enc']) & (count >= 2) & (df_one_problem.iloc[k-1]['time_duration'] < 20):
            game_id.add(row['user_id'])
        if (count >= 3) & (abs(row['time_duration']) < 8):
            game_id.add(row['user_id'])
#         if abs(row['time_duration']) < 5:
#             game_id.add(row['user_id'])
        count += 1
        k += 1
    return (game_id, first_pass_id, all_id)

test = gaming_detect_after(327)
print(len(test[0]))
    


# In[10]:


# detect the gaming students for every problem
gaming_list= []
first_list = []
all_list = []
game_ratio = []
first_ratio = []
similar_one = []
similar_one_game = []
similar_two = []
similar_two_game = []
recent = [539, 540, 327, 544, 102, 103, 104, 85, 11]
recent_pro = []
recent_pro_game = []
recent_difficulty = []
for item in quad_list:
    pro_id = item['problem_id']
    gaming, first, all_id = gaming_detect_after(pro_id)
    gaming_list.append(gaming)
    first_list.append(first)
    all_list.append(all_id)
    
    if pro_id in recent:
        recent_pro.append(pro_id)
        recent_pro_game.append(gaming)
        difficulty = len(first)*1.0/len(all_id)
        recent_difficulty.append(difficulty)
        
    if len(all_id) != 0:
        difficulty = len(first)*1.0/len(all_id)
#         if pro_id == 327:
#             print(difficulty)
#         if pro_id == 544:
#             print(difficulty) 
        if (difficulty >= 0.705) & (difficulty < 0.715):
            similar_one.append(pro_id)
            similar_one_game.append(gaming)
        if(difficulty >= 0.555) & (difficulty < 0.565):
            similar_two.append(pro_id)
            similar_two_game.append(gaming)
print(similar_one)
print(similar_two)
# 0.5602094240837696
# 0.7073170731707317
print(recent_pro)
# print(recent_pro_game)
print(recent_difficulty)
for i in range(0, len(quad_list)):   
    if len(all_list[i]) != 0:
        game_ratio.append(len(gaming_list[i])*1.0/len(all_list[i]))
        first_ratio.append(len(first_list[i])*1.0/len(all_list[i]))
#         print(str(len(gaming_list[i])*1.0/len(all_list[i])) + ', ' + str(len(first_pass[i])*1.0/len(all_list[i])))
# for item in gaming_all:
#     print(len(item))


# In[11]:


import matplotlib.pyplot as plt
x = []
count = 1
for i in range(0, len(game_ratio)):
    x.append(count)
    count += 1
plt.plot(x, game_ratio, color = 'blue')
plt.plot(x, first_ratio, color = 'red')
plt.axis([0, 50, 0, 1])
plt.ylabel('some numbers')
plt.show()


# In[12]:


df_hash = pd.read_sql_query('select * from experiments_userhash', con=conn)
print(df_hash.head())
df_pcrsuser = pd.read_sql_query('select * from users_pcrsuser', con=conn)
# print(df_pcrsuser.head())


# In[13]:


df_survey = pd.read_csv("D://HKUST//Projects//2019//CHI//data//depolyment data//one.csv")
df_survey.head()

df_survey2 = pd.read_csv("D://HKUST//Projects//2019//CHI//data//depolyment data//two.csv")
df_survey2.head()


# In[14]:


# problem 327 all submissions
problem1_submission = df_submissions[df_submissions['problem_id'] == 327]
problem1_submission = problem1_submission.sort_values(by = ['user_id', 'timestamp'])
problem1_submission.head()

set_submission = set()
for id in problem1_submission['user_id']:
    set_submission.add(id)
# print(len(set_submission))
# print(set_submission)
# pd.set_option('display.max_rows', 500)

# all students who submit to problem 327
set_all_id = set()
for id in set_submission:
    for row_index, row in df_pcrsuser.iterrows():
        if id == row['username']:
            set_all_id.add(row['id'])
            break

set_students_id = set()
for id in set_all_id:
    for row_index, row in df_pcrsuser.iterrows():
        if (id == row['id']) & (row['is_student']) & (not row['is_ta']) & (not row['is_instructor']) & (not row['is_admin']) & (not row['is_staff']):
            set_students_id.add(id)
# print(len(set_students_id))

set_all_id_hashed = set()
for id in set_students_id:
    for row_index, row in df_hash.iterrows():
        if id == row['user_id']:
            set_all_id_hashed.add(row['hashed_id'])
# print(len(set_all_id_hashed))
print("number of submissions to 327:" + str(len(set_all_id_hashed)))

# four groups
v1_people = set()
df_v1 = df_survey[df_survey['v1'] == 'yes']
for row_index, row in df_v1.iterrows():
    v1_people.add(row['user_id'])
print("number of v1 in 327: " + str(len(v1_people)))

v2_people = set()
df_v2 = df_survey[df_survey['v2'] == 'yes']
for row_index, row in df_v2.iterrows():
    v2_people.add(row['user_id'])
print("number of v2 in 327: " + str(len(v2_people)))

v3_people = set()
df_v3 = df_survey[df_survey['v3'] == 'yes']
for row_index, row in df_v3.iterrows():
    v3_people.add(row['user_id'])
print("number of v2 in 327: " + str(len(v3_people)))

# calculate the control group
# experiment_people_id = set()
# experiment_people_id_hashed = set()
# df_experiment = pd.read_sql_query('select * from experiments_experimentenrollment', con=conn)
# for row_index, row in df_experiment.iterrows():
#     if (row['experiment_id'] == 16) & row['in_experiment']:
#         experiment_people_id.add(row['enrolled_user_id'])
# print(len(experiment_people_id))
# for id in experiment_people_id:
#     for row_index, row in df_hash.iterrows():
#         if id == row['user_id']:
#             experiment_people_id_hashed.add(row['hashed_id'])
# print(len(experiment_people_id_hashed))

# v0_people = set_all_id_hashed - experiment_people_id_hashed

# print(len(v0_people))

v0_people = set_all_id_hashed - v1_people - v2_people - v3_people
print("number of v0 in 327: " + str(len(v0_people)))

df_survey['Finished'] = pd.to_numeric(df_survey['Finished'])
# four sub groups for one
v1_people_sub_one = set()
df_v1 = df_survey[(df_survey['v1'] == 'yes') & (df_survey['Finished'] == 1)]
for row_index, row in df_v1.iterrows():
    v1_people_sub_one.add(row['user_id'])
print("number of students who finshed v1 survey in 327: " + str(len(v1_people_sub_one)))

v2_people_sub_one = set()
df_v2 = df_survey[(df_survey['v2'] == 'yes') & (df_survey['Finished'] == 1)]
for row_index, row in df_v2.iterrows():
    v2_people_sub_one.add(row['user_id'])
print("number of students who finshed v2 survey in 327: " + str(len(v2_people_sub_one)))

v3_people_sub_one = set()
df_v3 = df_survey[(df_survey['v3'] == 'yes') & (df_survey['Finished'] == 1)]
for row_index, row in df_v3.iterrows():
    v3_people_sub_one.add(row['user_id'])
print("number of students who finshed v3 survey in 327: " +str(len(v3_people_sub_one)))


# In[15]:


# problem 544 all submissions
problem2_submission = df_submissions[df_submissions['problem_id'] == 544]
problem2_submission = problem2_submission.sort_values(by = ['user_id', 'timestamp'])
problem2_submission.head()

set_submission = set()
for id in problem2_submission['user_id']:
    set_submission.add(id)
# print(len(set_submission))
# print(set_submission)
# pd.set_option('display.max_rows', 500)

# all students who submit to problem 544
set_all_id = set()
for id in set_submission:
    for row_index, row in df_pcrsuser.iterrows():
        if id == row['username']:
            set_all_id.add(row['id'])
            break
# print(len(set_all_id))

set_students_id = set()
for id in set_all_id:
    for row_index, row in df_pcrsuser.iterrows():
        if (id == row['id']) & (row['is_student']) & (not row['is_ta']) & (not row['is_instructor']) & (not row['is_admin']) & (not row['is_staff']):
            set_students_id.add(id)
# print(len(set_students_id))

set_all_id_hashed = set()
for id in set_students_id:
    for row_index, row in df_hash.iterrows():
        if id == row['user_id']:
            set_all_id_hashed.add(row['hashed_id'])
print("number of submissions to 544: " + str(len(set_all_id_hashed)))


v1_people_2 = set()
df_v1_2 = df_survey2[df_survey2['v1'] == 'yes']
for row_index, row in df_v1_2.iterrows():
    v1_people_2.add(row['user_id'])
print("number of v1 in 544: " + str(len(v1_people_2)))

    
v2_people_2 = set()
df_v2_2 = df_survey2[df_survey2['v2'] == 'yes']
for row_index, row in df_v2_2.iterrows():
    v2_people_2.add(row['user_id'])
print("number of v2 in 544: " + str(len(v2_people_2)))

v3_people_2 = set()
df_v3_2 = df_survey2[df_survey2['v3'] == 'yes']
for row_index, row in df_v3_2.iterrows():
    v3_people_2.add(row['user_id'])
print("number of v3 in 544: " + str(len(v3_people_2)))

v0_people_2 = set_all_id_hashed - v1_people_2 - v2_people_2 - v3_people_2
print("number of v0 in 544: " + str(len(v0_people_2)))

df_survey2['Finished'] = pd.to_numeric(df_survey2['Finished'])
# four sub groups for two
v1_people_sub_two = set()
df2_v1 = df_survey2[(df_survey2['v1'] == 'yes') & (df_survey2['Finished'] == 1)]
for row_index, row in df2_v1.iterrows():
    v1_people_sub_two.add(row['user_id'])
print("number of students who finished v1 survey in 544: " + str(len(v1_people_sub_two)))

v2_people_sub_two = set()
df2_v2 = df_survey2[(df_survey2['v2'] == 'yes') & (df_survey2['Finished'] == 1)]
for row_index, row in df2_v2.iterrows():
    v2_people_sub_two.add(row['user_id'])
print("number of students who finished v2 survey in 544: " + str(len(v2_people_sub_two)))

v3_people_sub_two = set()
df2_v3 = df_survey2[(df_survey2['v3'] == 'yes') & (df_survey2['Finished'] == 1)]
for row_index, row in df2_v3.iterrows():
    v3_people_sub_two.add(row['user_id'])
print("number of students who finished v3 survey in 544: " + str(len(v3_people_sub_two)))

# check the order whether student submit 327 first and then 544
time_order = []
for student in set_submission:
    temp = [0, 0]
    for row_index, row in problem2_submission.iterrows():
        if (row['user_id'] == student) & (row['first'] == 1):
            temp[0] = row['timestamp']
            break
    for row_index, row in problem1_submission.iterrows():
        if(row['user_id'] == student) & (row['first'] == 1):
            temp[1] = row['timestamp']
            break
    time_order.append(temp)
print(len(time_order))
# print(time_order)
count_no_1 = 0
count_no_2 = 0
count_ok = 0
for item in time_order:
    if item[0] == 0:
        count_no_1 += 1
        continue
    if item[1] == 0:
        count_no_2 += 1
        continue
    if (item[0] - item[1]).seconds > 0:
        count_ok += 1
print("didn't submit to 327: " + str(count_no_2))
print("number of students who submit 327 first: " + str(count_ok))


# In[20]:


print(len(v0_people & v0_people_2), len(v1_people & v1_people_2), len(v2_people & v2_people_2), len(v3_people & v3_people_2))

final_0 = v0_people & v0_people_2
final_1 = v1_people & v1_people_2
final_2 = v2_people & v2_people_2
final_3 = v3_people & v3_people_2


# In[21]:


def username_to_hashed(name_group):
    hashed_group = set()
    id_group = set()
    for item in name_group:
        for row_index, row in df_pcrsuser.iterrows():
            if row['username'] == item:
                id_group.add(row['id'])
    for item in id_group:
        for row_index, row in df_hash.iterrows():
            if row['user_id'] == item:
                hashed_group.add(row['hashed_id'])
    return hashed_group

similar_one_game_hashed = []
for item in similar_one_game:
    hashed_group = username_to_hashed(item)
    similar_one_game_hashed.append(hashed_group)
# print(similar_one_game_hashed)

similar_two_game_hashed = []
for item in similar_two_game:
    hashed_group = username_to_hashed(item)
    similar_two_game_hashed.append(hashed_group)
# print(similar_two_game_hashed)

recent_pro_game_hashed = []
for item in recent_pro_game:
    hashed_group = username_to_hashed(item)
    recent_pro_game_hashed.append(hashed_group)


# In[19]:


# the similar problems with problem one and the game ratio of all the students
v0_game_ratio_set = []
v1_game_ratio_set = []
v2_game_ratio_set = []
v3_game_ratio_set = []

for item in similar_one_game_hashed:
    v0_game = item & v0_people
    v0_ratio = len(v0_game)*1.0/len(v0_people)
    v0_game_ratio_set.append(v0_ratio)
    
    v1_game = item & v1_people
    v1_ratio = len(v1_game)*1.0/len(v1_people)
    v1_game_ratio_set.append(v1_ratio)
    
    v2_game = item & v2_people
    v2_ratio = len(v2_game)*1.0/len(v2_people)
    v2_game_ratio_set.append(v2_ratio)
    
    v3_game = item & v3_people
    v3_ratio = len(v3_game)*1.0/len(v3_people)
    v3_game_ratio_set.append(v3_ratio)
    
print(v0_game_ratio_set)
print(v1_game_ratio_set)
print(v2_game_ratio_set)
print(v3_game_ratio_set)


# In[22]:


# the similar problems with problem one and the game ratio of students who answered the questions
v0_game_ratio_set = []
v1_game_ratio_set = []
v2_game_ratio_set = []
v3_game_ratio_set = []

for item in similar_one_game_hashed:
    v0_game = item & v0_people
    v0_ratio = len(v0_game)*1.0/len(v0_people)
    v0_game_ratio_set.append(v0_ratio)
    
    v1_game = item & v1_people_sub_one
    v1_ratio = len(v1_game)*1.0/len(v1_people_sub_one)
    v1_game_ratio_set.append(v1_ratio)
    
    v2_game = item & v2_people_sub_one
    v2_ratio = len(v2_game)*1.0/len(v2_people_sub_one)
    v2_game_ratio_set.append(v2_ratio)
    
    v3_game = item & v3_people_sub_one
    v3_ratio = len(v3_game)*1.0/len(v3_people_sub_one)
    v3_game_ratio_set.append(v3_ratio)
print(v0_game_ratio_set)
print(v1_game_ratio_set)
print(v2_game_ratio_set)
print(v3_game_ratio_set)


# In[21]:


# the similar problems with problem two and the game ratio of all the students
v0_game_ratio_set = []
v1_game_ratio_set = []
v2_game_ratio_set = []
v3_game_ratio_set = []

for item in similar_two_game_hashed:
    v0_game = item & v0_people
    v0_ratio = len(v0_game)*1.0/len(v0_people)
    v0_game_ratio_set.append(v0_ratio)
    
    v1_game = item & v1_people
    v1_ratio = len(v1_game)*1.0/len(v1_people)
    v1_game_ratio_set.append(v1_ratio)
    
    v2_game = item & v2_people
    v2_ratio = len(v2_game)*1.0/len(v2_people)
    v2_game_ratio_set.append(v2_ratio)
    
    v3_game = item & v3_people
    v3_ratio = len(v3_game)*1.0/len(v3_people)
    v3_game_ratio_set.append(v3_ratio)
print(v0_game_ratio_set)
print(v1_game_ratio_set)
print(v2_game_ratio_set)
print(v3_game_ratio_set)


# In[23]:


# the similar problems with problem two and the game ratio of students who answered the questions
v0_game_ratio_set = []
v1_game_ratio_set = []
v2_game_ratio_set = []
v3_game_ratio_set = []

for item in similar_two_game_hashed:
    v0_game = item & v0_people
    v0_ratio = len(v0_game)*1.0/len(v0_people)
    v0_game_ratio_set.append(v0_ratio)
    
    v1_game = item & v1_people_sub_two
    v1_ratio = len(v1_game)*1.0/len(v1_people_sub_two)
    v1_game_ratio_set.append(v1_ratio)
    
    v2_game = item & v2_people_sub_two
    v2_ratio = len(v2_game)*1.0/len(v2_people_sub_two)
    v2_game_ratio_set.append(v2_ratio)
    
    v3_game = item & v3_people_sub_two
    v3_ratio = len(v3_game)*1.0/len(v3_people_sub_two)
    v3_game_ratio_set.append(v3_ratio)
print(v0_game_ratio_set)
print(v1_game_ratio_set)
print(v2_game_ratio_set)
print(v3_game_ratio_set)


# In[24]:


# recent problems

# calculate who are the "frequent" gaming students:define by gaming on all the recent problems
# for item in recent_pro_game_hashed:
#     print(len(item))

# frequent_game = recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[3]
# frequent_game = frequent_game | (recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[5])
# frequent_game = frequent_game | (recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[6])
# frequent_game = frequent_game | (recent_pro_game_hashed[2] & recent_pro_game_hashed[3] & recent_pro_game_hashed[5])
# frequent_game = frequent_game | (recent_pro_game_hashed[2] & recent_pro_game_hashed[3] & recent_pro_game_hashed[6])
# frequent_game = frequent_game | (recent_pro_game_hashed[3] & recent_pro_game_hashed[5] & recent_pro_game_hashed[6])
# frequent_game = recent_pro_game_hashed[5] & recent_pro_game_hashed[6]
frequent_game = recent_pro_game_hashed[1]



# print(len(frequent_game))


# calculate the people the tansition from gaming to non-gaming in each group
# first calculate gaming people in each group on problem 544


# since v0 has more people, we sample 45 people from
# import random
# v0_frequent_list = []
# v0_still_544_list = []
# v0_still_327_list = []
# # print(len(v0_people))
# for i in range(0, 100):
#     v0_people_sample = random.sample(v0_people, 49)
#     v0_people_sample =set(v0_people_sample)
#     v0_frequent = v0_people_sample & frequent_game
#     v0_frequent_list.append(len(v0_frequent))
# #     v0_still_544 = v0_people_sample & recent_pro_game_hashed[0]
#     v0_still_544 = v0_frequent & recent_pro_game_hashed[0]
#     v0_still_544_list.append(len(v0_still_544))
# #     v0_still_327 = v0_people_sample & recent_pro_game_hashed[4]
#     v0_still_327 = v0_frequent & recent_pro_game_hashed[4]
#     v0_still_327_list.append(len(v0_still_327))
    
# v0_0 = np.average(v0_frequent_list)
# v0_1 = np.average(v0_still_327_list)
# v0_2 = np.average(v0_still_544_list)
# print(math.ceil(v0_0), math.ceil(v0_1), math.ceil(v0_1)/math.ceil(v0_0), math.ceil(v0_2), math.ceil(v0_2)/math.ceil(v0_0))



v0_still_544 = v0_people_2 & recent_pro_game_hashed[5]
v1_still_544 = v1_people_2 & recent_pro_game_hashed[5]
v2_still_544 = v2_people_2 & recent_pro_game_hashed[5]
v3_still_544 = v3_people_2 & recent_pro_game_hashed[5]


print(len(v0_still_544))
print(len(v1_still_544))
print(len(v2_still_544))
print(len(v3_still_544))
# print(frequent_game)

# print(len(frequent_game&v0_people),len(frequent_game&v1_people_sub_one), len(frequent_game&v2_people_sub_one), len(frequent_game&v3_people_sub_one))
# print(len(frequent_game&v1_people_sub_one&recent_pro_game_hashed[4]), len(frequent_game&v2_people_sub_one&recent_pro_game_hashed[4]), len(frequent_game&v3_people_sub_one&recent_pro_game_hashed[4]))
# print(len(frequent_game&v0_people),len(frequent_game&v1_people_sub_two), len(frequent_game&v1_people_sub_two), len(frequent_game&v1_people_sub_two))


# In[ ]:


# recent problems

# calculate who are the "frequent" gaming students:define by gaming on all the recent problems
# for item in recent_pro_game_hashed:
#     print(len(item))

# frequent_game = recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[3]
# frequent_game = frequent_game | (recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[5])
# frequent_game = frequent_game | (recent_pro_game_hashed[1] & recent_pro_game_hashed[2] & recent_pro_game_hashed[6])
# frequent_game = frequent_game | (recent_pro_game_hashed[2] & recent_pro_game_hashed[3] & recent_pro_game_hashed[5])
# frequent_game = frequent_game | (recent_pro_game_hashed[2] & recent_pro_game_hashed[3] & recent_pro_game_hashed[6])
# frequent_game = frequent_game | (recent_pro_game_hashed[3] & recent_pro_game_hashed[5] & recent_pro_game_hashed[6])
frequent_game = recent_pro_game_hashed[5] & recent_pro_game_hashed[6]
# frequent_game = recent_pro_game_hashed[5]



# print(len(frequent_game))


# calculate the people the tansition from gaming to non-gaming in each group
# first calculate gaming people in each group on problem 544


# since v0 has more people, we sample 45 people from
# import random
# v0_frequent_list = []
# v0_still_544_list = []
# v0_still_327_list = []
# # print(len(v0_people))
# for i in range(0, 100):
#     v0_people_sample = random.sample(v0_people, 49)
#     v0_people_sample =set(v0_people_sample)
#     v0_frequent = v0_people_sample & frequent_game
#     v0_frequent_list.append(len(v0_frequent))
# #     v0_still_544 = v0_people_sample & recent_pro_game_hashed[0]
#     v0_still_544 = v0_frequent & recent_pro_game_hashed[0]
#     v0_still_544_list.append(len(v0_still_544))
# #     v0_still_327 = v0_people_sample & recent_pro_game_hashed[4]
#     v0_still_327 = v0_frequent & recent_pro_game_hashed[4]
#     v0_still_327_list.append(len(v0_still_327))
    
# v0_0 = np.average(v0_frequent_list)
# v0_1 = np.average(v0_still_327_list)
# v0_2 = np.average(v0_still_544_list)
# print(math.ceil(v0_0), math.ceil(v0_1), math.ceil(v0_1)/math.ceil(v0_0), math.ceil(v0_2), math.ceil(v0_2)/math.ceil(v0_0))

print(len(v0_people))
v0_frequent = v0_people & frequent_game
v1_frequent = v1_people & frequent_game
v2_frequent = v2_people & frequent_game
v3_frequent = v3_people & frequent_game

v0_frequent_2 = v0_people_2 & frequent_game
v1_frequent_2 = v1_people_2 & frequent_game
v2_frequent_2 = v2_people_2 & frequent_game
v3_frequent_2 = v3_people_2 & frequent_game


v0_still_544 = v0_people_2 & recent_pro_game_hashed[0]
v1_still_544 = v1_people_2 & recent_pro_game_hashed[0]
v2_still_544 = v2_people_2 & recent_pro_game_hashed[0]
v3_still_544 = v3_people_2 & recent_pro_game_hashed[0]

v0_still_327 = v0_people_2 & recent_pro_game_hashed[4]
v1_still_327 = v1_people_2 & recent_pro_game_hashed[4]
v2_still_327 = v2_people_2 & recent_pro_game_hashed[4]
v3_still_327 = v3_people & recent_pro_game_hashed[4] 

print(len(v0_people), len(v0_frequent),len(v0_still_327), len(v0_people_2),len(v0_frequent_2),len(v0_still_544))
print(len(v1_people), len(v1_frequent),len(v1_still_327), len(v1_people_2),len(v1_frequent_2),len(v1_still_544))
print(len(v2_people), len(v2_frequent),len(v2_still_327), len(v2_people_2), len(v2_frequent_2),len(v2_still_544))
print(len(v3_people), len(v3_frequent),len(v3_still_327), len(v3_people_2), len(v3_frequent_2),len(v3_still_544))
# print(frequent_game)

# print(len(frequent_game&v0_people),len(frequent_game&v1_people_sub_one), len(frequent_game&v2_people_sub_one), len(frequent_game&v3_people_sub_one))
# print(len(frequent_game&v1_people_sub_one&recent_pro_game_hashed[4]), len(frequent_game&v2_people_sub_one&recent_pro_game_hashed[4]), len(frequent_game&v3_people_sub_one&recent_pro_game_hashed[4]))
# print(len(frequent_game&v0_people),len(frequent_game&v1_people_sub_two), len(frequent_game&v1_people_sub_two), len(frequent_game&v1_people_sub_two))


# In[61]:


from statsmodels.stats.proportion import proportions_ztest
a1 = [9, 17]
a2 = [41, 48]
print(proportions_ztest(a1, a2))


# In[33]:


ground_truth_raw = set(["aziztal1", "batistan", "bilalaal", "caiyuemi", "chenke35", "chenq112", "chenz161", "choshar1", "choyuika", 
"colang54","fanfrank", "gaojie7", "gnanaoli", "hassalsa", "huan1066", "huayutia", "jindals1", "jinshen2", "liaoyant", "liuzeyu6",
"liyixue", "liweixu1", "lizehao1", "longtri2", "makryan", "mandalas", "marresek", "masoodme", "monizeal", "morga102", "namasi18",
"nohjaeho", "oriakuso", "sarkerp1", "shuvalov", "tahahib1", "totonchy", "wangj684", "wangw233", "yanghye4", "yaoshun2", "yaoyuqi1",
"zhaoqiuw"])

ground_truth_id = set()
ground_truth_hashed = set()

for id in ground_truth_raw:
    for row_index, row in df_pcrsuser.iterrows():
        if id == row['username']:
            ground_truth_id.add(row['id'])
            break

for id in ground_truth_id:
    for row_index, row in df_hash.iterrows():
        if id == row['user_id']:
            ground_truth_hashed.add(row['hashed_id'])
print(len(ground_truth_hashed))

v1_people = set()
df_v1 = df_survey[df_survey['v1'] == 'yes']
for row_index, row in df_v1.iterrows():
    v1_people.add(row['user_id'])
print(len(v1_people))

v2_people = set()
df_v2 = df_survey[df_survey['v2'] == 'yes']
for row_index, row in df_v2.iterrows():
    v2_people.add(row['user_id'])
print(len(v2_people))

v3_people = set()
df_v3 = df_survey[df_survey['v3'] == 'yes']
for row_index, row in df_v3.iterrows():
    v3_people.add(row['user_id'])
print(len(v3_people))


v0_people = set_all_id_hashed - v1_people - v2_people - v3_people
print(len(v0_people))

v0_gaming_ratio = len(ground_truth_hashed & v0_people)*1.0/len(v0_people)
v1_gaming_ratio = len(ground_truth_hashed & v1_people)*1.0/len(v1_people)
v2_gaming_ratio = len(ground_truth_hashed & v2_people)*1.0/len(v2_people)
v3_gaming_ratio = len(ground_truth_hashed & v3_people)*1.0/len(v3_people)

print(v0_gaming_ratio, v1_gaming_ratio, v2_gaming_ratio, v3_gaming_ratio)


# In[137]:


def select_D(_digits):
    digit_list = [int(d) for d in _digits]
    if len(digit_list) < 4:
        return False
    elif sum(digit_list) != 1:
        return False
    elif digit_list[3] == 1:
            return True
    else:
        return False
    
weather_D = []

for row_index, row in df_1.iterrows():
    weather_D.append(select_D(row['choice_enc']))
    
df_1['weather_D'] = weather_D
df_1.head()


# In[25]:


problem_D = []

for row_index, row in df_1.iterrows():
    if row['has_best_score'] & row['weather_D']:
        problem_D.append(row['problem_id'])
        
problem_D = set(problem_D)
print(problem_D)


# In[51]:


problem_similar = []
for problem in problem_D:
    num_attempts = []
    one_problem = df_1[df_1['problem_id'] == problem]
    grouped = one_problem.sort_values("timestamp").groupby("user_id")
    
    for group_name, df_group in grouped:
        num = 1
        for row_index, row in df_group.iterrows():
            if row['correct_rate'] < 1:
                num += 1
            else:
                break
        num_attempts.append(num)
    if len(num_attempts) != 0:
        first_rate = num_attempts.count(1)/len(num_attempts)
    else:
        first_rate = 0
    if (first_rate > 0.5) & (first_rate < 0.6):
        problem_similar.append(problem)
print(problem_similar) 


# In[79]:


plt.hist(df_1['correct_rate'])
plt.title("Histogram of correct_rate")
plt.show()


# In[80]:


plt.hist(df_1['improve_from_last_sub'])
plt.title("Histogram of improve_from_last_sub")
plt.show()


# In[23]:


plt.hist(df_1['time_from_last_sub'], range=(50, 300))
plt.title("Histogram of time_from_last_sub")
plt.show()


# In[21]:


# Choose the problem to look at
# prob_id = 544
prob_id = 544


# In[22]:


# The number of attempts of each student
filtered = df_1[df_1['problem_id'] == prob_id]
grouped = filtered.sort_values("timestamp").groupby("user_id")
num_attemps = []

for group_name, df_group in grouped:
    num = 1
    for row_index, row in df_group.iterrows():
        if row['correct_rate'] < 1:
            num += 1
        else:
            break
    num_attemps.append(num)


# In[23]:


np.median(num_attemps)


# In[24]:


# The avarage correct rate of n-th attempt
filtered = df_1[df_1['problem_id'] == prob_id]
for i in range(max(num_attemps)):
    nth = filtered.sort_values("timestamp").groupby("user_id", as_index=False).nth(i)
    print(nth['correct_rate'].mean())


# In[25]:


# Cumulative pass rate
num_attemps = np.array(num_attemps)
passed = 0
for i in range(1, max(num_attemps) + 1):
    passed += len(num_attemps[num_attemps == i])
    print(passed / len(num_attemps))


# In[123]:


np.mean(num_attemps)


# In[124]:


plt.hist(num_attemps)
plt.title("Number of attempts")
plt.show()

