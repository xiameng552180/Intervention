
# coding: utf-8

# In[16]:


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
conn = pg.connect(host='192.168.61.4', database='postgres', user='postgres')

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


# In[17]:


# print(quad_list)
quad_list1 = []
for item in quad_list:
    if len(item) == 3:
        quad_list1.append(item)

for item in quad_list1:
    for row_index, row in df_quests.iterrows():
        if item['quest_id'] == row['id']:
            item['order'] = int(row['order'])


# In[18]:


df_quad = pd.DataFrame(quad_list1)
df_quad = df_quad.sort_values(by = ['order', 'challenge_id'])
# print(df_quad)


# In[19]:


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


# In[20]:


# Correct rate of the submission
# correct_rate = 1 means the student passed
df_submissions['correct_rate'] = df_submissions.groupby('problem_id', group_keys=False).apply(lambda g: g['score'] / g['score'].max())
df_submissions = df_submissions.sort_values(by = ['problem_id', 'user_id', 'timestamp'])
print(df_submissions.head())


# In[21]:


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


# In[39]:


# Time spent between two submissions
diff = df_submissions['timestamp'].diff().astype('timedelta64[s]')
df_submissions['time_duration'] = diff
df_submissions


# In[41]:


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
    


# In[61]:


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

        if (count >= 3) & (abs(row['time_duration']) < 6):
            game_id.add(row['user_id'])
#         if abs(row['time_duration']) < 5:
#             game_id.add(row['user_id'])
        count += 1
        k += 1

    return (game_id, first_pass_id, all_id)

test = gaming_detect_after(327)
print(len(test[0]))
    


# In[62]:


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
recent = [539, 540, 327, 544, 102, 103, 104]
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
# print(similar_one)
# print(similar_two)
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


# In[55]:


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


# In[63]:


# problem 327 all submissions
problem1_submission = df_submissions[df_submissions['problem_id'] == 327]
problem1_submission = problem1_submission.sort_values(by = ['user_id', 'timestamp'])
problem1_submission.head()

set_submission1 = set()
for id in problem1_submission['user_id']:
    set_submission1.add(id)
print(len(set_submission1))
# print(set_submission)
# pd.set_option('display.max_rows', 500)


# In[64]:


# problem 544 all submissions
problem2_submission = df_submissions[df_submissions['problem_id'] == 544]
problem2_submission = problem2_submission.sort_values(by = ['user_id', 'timestamp'])
problem2_submission.head()

set_submission2 = set()
for id in problem2_submission['user_id']:
    set_submission2.add(id)
print(len(set_submission2))
# print(set_submission)
# pd.set_option('display.max_rows', 500)


# In[65]:


# problem 539 all submissions
problem3_submission = df_submissions[df_submissions['problem_id'] == 539]
problem3_submission = problem3_submission.sort_values(by = ['user_id', 'timestamp'])
problem3_submission.head()

set_submission3 = set()
for id in problem3_submission['user_id']:
    set_submission3.add(id)
print(len(set_submission3))
# print(set_submission)
# pd.set_option('display.max_rows', 500)


# In[66]:


# problem 540 all submissions
problem4_submission = df_submissions[df_submissions['problem_id'] == 540]
problem4_submission = problem3_submission.sort_values(by = ['user_id', 'timestamp'])
problem4_submission.head()

set_submission4 = set()
for id in problem4_submission['user_id']:
    set_submission4.add(id)
print(len(set_submission4))
# print(set_submission)
# pd.set_option('display.max_rows', 500)


# In[67]:


# recent problems
frequent_game = recent_pro_game[1] & recent_pro_game[2] & recent_pro_game[3]
frequent_game = frequent_game | (recent_pro_game[1] & recent_pro_game[2] & recent_pro_game[5])
frequent_game = frequent_game | (recent_pro_game[1] & recent_pro_game[2] & recent_pro_game[6])
frequent_game = frequent_game | (recent_pro_game[2] & recent_pro_game[3] & recent_pro_game[5])
frequent_game = frequent_game | (recent_pro_game[2] & recent_pro_game[3] & recent_pro_game[6])
frequent_game = frequent_game | (recent_pro_game[3] & recent_pro_game[5] & recent_pro_game[6])
# frequent_game = recent_pro_game[5] & recent_pro_game[6]

print("number of frequent gamers: " + str(len(frequent_game)))

frequent_game_327 = frequent_game & set_submission1
frequent_game_544 = frequent_game & set_submission2

still_game_327 = frequent_game_327 & recent_pro_game[4]
still_game_544 = frequent_game_544 & recent_pro_game[0]

game539 = set_submission3 & recent_pro_game[5]
game540 = set_submission4 & recent_pro_game[6]
game327 = set_submission1 & recent_pro_game[4]
game544 = set_submission2 & recent_pro_game[0]

print("number of students who submit on: 539: " + str(len(set_submission3)))

print("number of students who submit on: 544: " + str(len(set_submission4)))
print("number of students who submit on 327: " + str(len(set_submission1)))
# print("number of frequent gamers on 327: " + str(len(frequent_game_327)))
# print("number of students game on 327: " + str(len(recent_pro_game[4])))
# print("number of still game on 327: " + str(len(still_game_327)))
print("number of students who submit on: 544: " + str(len(set_submission2)))
# print("number of frequent gamers on 544: " + str(len(frequent_game_544)))
# print("number of students game on 544: " + str(len(recent_pro_game[0])))
# print("number of still game on 544: " + str(len(still_game_544)))

print("game on 539: " + str(len(game539)))
print("game on 540: " + str(len(game540)))
print("game on 327: " + str(len(game327)))
print("game on 544: " + str(len(game544)))


        
# calculate who are the "frequent" gaming students:define by gaming on all the recent problems


# In[4]:


from statsmodels.stats.proportion import proportions_ztest
a1 = [3, 9]
a2 = [44, 39]
print(proportions_ztest(a1, a2))

