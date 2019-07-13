import os
import json
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
import numpy as np

if __name__ == "__main__":
   connection = pg.connect(host='192.168.61.3', database = 'postgres', user = 'postgres')
   df = pd.read_sql_query('select * from problems_multiple_choice_submission', con=connection)
   

   