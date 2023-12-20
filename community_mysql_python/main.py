#Install packages
# pip install numpy
# pip install pandas
# pip install sklearn
# pip install igraph
# pip install networkx
# pip install leidenalg
#pip install mysql
#pip install sqlalchemy

#Import packages

import sys

import mysql.connector
import sqlalchemy


#Import otherfiles from this project
from leiden_communities import *
from cluster_coeffs_pca_abs import *


if __name__ == "__main__":

    # Defining method to create dictionaries with key-multiple values for all communities from list of lists
    def community_dict(comm_list):

        dict_name = {}
        for i, name in enumerate(comm_list):
            dict_name[i] = comm_list[i]
        return dict_name

    # Defining method to convert multiple values dictionaries to single values dictionary
    def community_singlevaldict(dict_mul):

        list_tuples = [(key, i) for key, val in dict_mul.items() for i in val]

        finall = dict((j, i) for i, j in list_tuples)

        return finall

    #Defining method to convert dictionary to dataframe
    def dict_to_df(dict,columns=['student_id','cluster_id']):

        df = pd.DataFrame(dict.items(), columns=columns)

        return df


    # Calling method to create dictionaries for all communities from list of lists
    ext_final = community_dict(partition_extro_final)
    opt_final = community_dict(partition_optim_final)
    tough_final = community_dict(partition_tough_final)
    manage_final = community_dict(partition_manage_final)
    comm_final = community_dict(partition_comm_final)
    success_final = community_dict(partition_success_final)
    members_final = community_dict(members_final_ll)

    # Calling method to convert multiple values dictionaries to single values dictionary
    ext_final_dict = community_singlevaldict(ext_final)
    opt_final_dict = community_singlevaldict(opt_final)
    tough_final_dict = community_singlevaldict(tough_final)
    manage_final_dict = community_singlevaldict(manage_final)
    comm_final_dict = community_singlevaldict(comm_final)
    success_final_dict = community_singlevaldict(success_final)
    members_final_dict = community_singlevaldict(members_final)

    # Calling method to convert dictionary to dataframe
    ext_final_df = dict_to_df(ext_final_dict,columns=['student_id','cluster_id'])
    opt_final_df = dict_to_df(opt_final_dict,columns=['student_id','cluster_id'])
    tough_final_df = dict_to_df(tough_final_dict,columns=['student_id','cluster_id'])
    manage_final_df = dict_to_df(manage_final_dict,columns=['student_id','cluster_id'])
    comm_final_df = dict_to_df(comm_final_dict,columns=['student_id','cluster_id'])
    success_final_df = dict_to_df(success_final_dict,columns=['student_id','cluster_id'])
    members_final_df = dict_to_df(members_final_dict,columns=['student_id','member_id'])

    # Output dataframes
    print(ext_final_df)
    print(opt_final_df)
    print(tough_final_df)
    print(manage_final_df)
    print(comm_final_df)
    print(success_final_df)
    print(members_final_df)

    # Create a communities database and add a connection to db
    outdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    db_cursor = outdb.cursor()

    db_cursor.execute("CREATE DATABASE IF NOT EXISTS stpartner_communities")

    # Create tables for storing partitions, membership and clustering coefficients
    connectdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stpartner_communities"
    )
    connect_cursor = connectdb.cursor()

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS extro_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS optim_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS tough_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS manage_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS comm_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS success_partition (student_id INT PRIMARY KEY UNIQUE KEY, cluster_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS mem_communities (student_id INT PRIMARY KEY UNIQUE KEY, member_id INT, ts TIMESTAMP)")

    connect_cursor.execute("CREATE TABLE IF NOT EXISTS clustering_coeffs (student_id INT PRIMARY KEY UNIQUE KEY, clustering_coefficient FLOAT, ts TIMESTAMP)")


    #Connect to db through sql alchemy
    my_conn = sqlalchemy.create_engine("mysql+mysqldb://root:@localhost/stpartner_communities")

    dtype = {
        "TS": sqlalchemy.TIMESTAMP
    }
    #Insert communities dataframes into respective tables
    #1
    extro_temptable = "temp"
    extro_table = "extro_partition"
    key = ["student_id"]
    ext_final_df.to_sql(name=extro_temptable, con=my_conn, index=False, if_exists='append',dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {extro_table} ({",".join(ext_final_df.columns)}) 
                     select * from {extro_temptable} t 
                     where not exists 
                       (select 1 from {extro_table} m 
                       where {"and".join([f" t.{col} = m.{col} " for col in key])}
                       )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {extro_temptable}")
    conn.close()
    #2
    opt_temptable = "temp"
    opt_table = "optim_partition"
    key = ["student_id"]
    opt_final_df.to_sql(name=opt_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {opt_table} ({",".join(opt_final_df.columns)}) 
                         select * from {opt_temptable} t 
                         where not exists 
                           (select 1 from {opt_table} m 
                           where {"and".join([f" t.{col} = m.{col} " for col in key])}
                           )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {opt_temptable}")
    conn.close()
    #3
    tough_temptable = "temp"
    tough_table = "tough_partition"
    key = ["student_id"]
    tough_final_df.to_sql(name=tough_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {tough_table} ({",".join(tough_final_df.columns)}) 
                             select * from {tough_temptable} t 
                             where not exists 
                               (select 1 from {tough_table} m 
                               where {"and".join([f" t.{col} = m.{col} " for col in key])}
                               )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {tough_temptable}")
    conn.close()
    #4
    manage_temptable = "temp"
    manage_table = "manage_partition"
    key = ["student_id"]
    manage_final_df.to_sql(name=manage_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {manage_table} ({",".join(manage_final_df.columns)}) 
                                 select * from {manage_temptable} t 
                                 where not exists 
                                   (select 1 from {manage_table} m 
                                   where {"and".join([f" t.{col} = m.{col} " for col in key])}
                                   )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {manage_temptable}")
    conn.close()
    #5
    comm_temptable = "temp"
    comm_table = "comm_partition"
    key = ["student_id"]
    comm_final_df.to_sql(name=comm_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {comm_table} ({",".join(comm_final_df.columns)}) 
                                     select * from {comm_temptable} t 
                                     where not exists 
                                       (select 1 from {comm_table} m 
                                       where {"and".join([f" t.{col} = m.{col} " for col in key])}
                                       )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {comm_temptable}")
    conn.close()
    #6
    success_temptable = "temp"
    success_table = "success_partition"
    key = ["student_id"]
    success_final_df.to_sql(name=success_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {success_table} ({",".join(success_final_df.columns)}) 
                                         select * from {success_temptable} t 
                                         where not exists 
                                           (select 1 from {success_table} m 
                                           where {"and".join([f" t.{col} = m.{col} " for col in key])}
                                           )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {success_temptable}")
    conn.close()
    #7
    mem_temptable = "temp"
    mem_table = "mem_communities"
    key = ["student_id"]
    members_final_df.to_sql(name=mem_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {mem_table} ({",".join(members_final_df.columns)}) 
                                             select * from {mem_temptable} t 
                                             where not exists 
                                               (select 1 from {mem_table} m 
                                               where {"and".join([f" t.{col} = m.{col} " for col in key])}
                                               )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {mem_temptable}")
    conn.close()
    #8
    clustering_temptable = "temp"
    clustering_table = "clustering_coeffs"
    key = ["student_id"]
    final_clusters_df.to_sql(name=clustering_temptable, con=my_conn, index=False, if_exists='append', dtype=dtype)
    conn = my_conn.connect()
    querymsql = f"""insert into {clustering_table} ({",".join(final_clusters_df.columns)}) 
                                                 select * from {clustering_temptable} t 
                                                 where not exists 
                                                   (select 1 from {clustering_table} m 
                                                   where {"and".join([f" t.{col} = m.{col} " for col in key])}
                                                   )"""

    conn.execute(querymsql)
    conn.execute(f"drop table {clustering_temptable}")
    conn.close()