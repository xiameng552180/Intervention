import os
import json
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

if __name__ == "__main__":
   connection = pg.connect(host='192.168.61.4', database = 'postgres', user = 'postgres')
   df_submission_time = pd.read_sql_query('select * from problems_multiple_choice_submission', con=connection)
   df_submission_raw = pd.read_sql_query('select * from problems_multiple_choice_optionselection', con=connection)

   submission_id = []
   submission_result = []
   previous = {}
   previous['submission_id'] = df_submission_raw.iloc[0]['submission_id']
   previous['string'] = '0'
   
   for i in range(1, len(df_submission_time)):
       if df_submission_raw.iloc[i]['submission_id'] == previous['submission_id']:
        #    print('ok')
           if df_submission_raw.iloc[i]['was_selected'] == df_submission_raw.iloc[0]['was_selected']:
               previous['string'] += '0'
           else: previous['string'] += '1'
       else:
        #    print(previous)
           temp = {}
           temp['submission_id'] = previous['submission_id']
           temp['string'] = previous['string']
           submission_id.append(temp['submission_id'])
           submission_result.append(temp['string'])
           previous['submission_id'] = df_submission_raw.iloc[i]['submission_id']
           previous['string'] = ''
           if df_submission_raw.iloc[i]['was_selected'] == df_submission_raw.iloc[0]['was_selected']:
               previous['string'] += '0'
           else: previous['string'] += '1'
            
   submission = {'id': submission_id,
                 'submission_result': submission_result}
   df_submission = DataFrame(submission)
   df_new = df_submission_time.merge(df_submission, on = 'id', how = 'left')
   print(df_new)

   
#    a = [1, 2, 3]
#    b = ['i', 'love', 'you']
#    c = ['i', 'hate', 'you']
   
#    df1 = pd.DataFrame({'a': a, 'b': b})
#    df2 = pd.DataFrame({'a': a, 'c': c})

# #    df1.set_index('a')
# #    df2.set_index('a')

#    print(df1.merge(df2, on = 'a', how = 'left'))

#    print(df1)
#    print(df2)
