#Install packages
# pip install numpy
# pip install pandas
# pip install sklearn
# pip install igraph
# pip install networkx
# pip install leidenalg
#pip install mysql
#pip install sqlalchemy

# #Import packages
import os
import sys

import mysql.connector
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', 40)
pd.set_option('display.max_rows', 500)


semesID = '20'

#Connection to db
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sqlvali_eval"
)

mydb2 = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sqlvali_data"
)

#Retrieve data from the db as dataframes using sqlalchemy
my_conn = create_engine("mysql+mysqldb://root:@localhost/sqlvali_eval")

my_conn2 = create_engine("mysql+mysqldb://root:@localhost/sqlvali_data")


extint_data01 = pd.read_sql("SELECT Q_ID, UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='22'",my_conn)
extint_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
extint_data = pd.merge(extint_data01, extint_data02, left_on='UserID', right_on='usr_id')
extint_data = extint_data.drop('usr_id', axis=1)
extint_data = extint_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
extint_data = extint_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
extint_data.columns = extint_data.columns.tolist()

toughtend_data01 = pd.read_sql("SELECT Q_ID, UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='29'",my_conn)
toughtend_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
toughtend_data = pd.merge(toughtend_data01, toughtend_data02, left_on='UserID', right_on='usr_id')
toughtend_data = toughtend_data.drop('usr_id', axis=1)
toughtend_data = toughtend_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
toughtend_data = toughtend_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
toughtend_data.columns = toughtend_data.columns.tolist()

successrsk_data01 = pd.read_sql("SELECT Q_ID, UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='30'",my_conn)
successrsk_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
successrsk_data = pd.merge(successrsk_data01, successrsk_data02, left_on='UserID', right_on='usr_id')
successrsk_data = successrsk_data.drop('usr_id', axis=1)
successrsk_data = successrsk_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
successrsk_data = successrsk_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
successrsk_data.columns = successrsk_data.columns.tolist()

optimpessim_data01 = pd.read_sql("SELECT Q_ID, UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='31'",my_conn)
optimpessim_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
optimpessim_data = pd.merge(optimpessim_data01, optimpessim_data02, left_on='UserID', right_on='usr_id')
optimpessim_data = optimpessim_data.drop('usr_id', axis=1)
optimpessim_data = optimpessim_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
optimpessim_data = optimpessim_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
optimpessim_data.columns = optimpessim_data.columns.tolist()

commrole_data01 = pd.read_sql("SELECT UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='33'",my_conn)
commrole_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
commrole_data = pd.merge(commrole_data01, commrole_data02, left_on='UserID', right_on='usr_id')
commrole_data = commrole_data.drop('usr_id', axis=1)
commrole_data = commrole_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
commrole_data = commrole_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
commrole_data.columns = commrole_data.columns.tolist()

manageppl_data01 = pd.read_sql("SELECT UserID, trial, TaskNum, result FROM qanswers WHERE Q_ID='34'",my_conn)
manageppl_data02 = pd.read_sql("SELECT usr_id FROM user WHERE usr_sem_id = " + semesID,my_conn2)
manageppl_data = pd.merge(manageppl_data01, manageppl_data02, left_on='UserID', right_on='usr_id')
manageppl_data = manageppl_data.drop('usr_id', axis=1)
manageppl_data = manageppl_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
manageppl_data = manageppl_data.set_index(['UserID', 'trial', 'TaskNum'])['result'].unstack().reset_index()
manageppl_data.columns = manageppl_data.columns.tolist()
