import json
import os
import pandas as pd
import streamlit as st
import mysql.connector as sql
from sqlalchemy import create_engine

connection = sql.connect(host="localhost",   
                   user = "root",               
                   password="******",
                   database  = "phonepe_pulse",
                   auth_plugin ="mysql_native_password")
cursor = connection.cursor()


# Extracting Aggregated Transaction details from Statewise,Yearwise and Quarterwise
def extract_aggregated_transactions():
    path1 = "C://Users//Jeni//Desktop//phonepe pulse data//data//aggregated//transaction//country//india//state//"
    agg_trans_list = os.listdir(path1)
    columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
                'Transaction_amount': []}
    for state in agg_trans_list:
        cur_state = path1 + state + "/"
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = cur_state + year + "/"
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                A = json.load(data)

                for i in A['data']['transactionData']:
                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']
                    columns1['Transaction_type'].append(name)
                    columns1['Transaction_count'].append(count)
                    columns1['Transaction_amount'].append(amount)
                    columns1['State'].append(state)
                    columns1['Year'].append(year)
                    columns1['Quarter'].append(int(file.strip('.json')))

    df_agg_trans = pd.DataFrame(columns1)
    return df_agg_trans


# Extracting Aggregated User details from Statewise,Yearwise and Quarterwise
def extract_aggregated_user():
    path2 = "C://Users//Jeni//Desktop//phonepe pulse data//data//aggregated//user//country//india//state//"
    agg_user_list = os.listdir(path2)
    columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
                'Percentage': []}
    for state in agg_user_list:
        cur_state = path2 + state + "/"
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = cur_state + year + "/"
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                B = json.load(data)
                try:
                    for i in B["data"]["usersByDevice"]:
                        brand_name = i["brand"]
                        counts = i["count"]
                        percents = i["percentage"]
                        columns2["Brands"].append(brand_name)
                        columns2["Count"].append(counts)
                        columns2["Percentage"].append(percents)
                        columns2["State"].append(state)
                        columns2["Year"].append(year)
                        columns2["Quarter"].append(int(file.strip('.json')))
                except:
                    pass
    df_agg_user = pd.DataFrame(columns2)
    return df_agg_user


# Extracting Map Transaction details from Statewise,Yearwise and Quarterwise
def extract_map_transactions():
    path3 = "C://Users//Jeni//Desktop//phonepe pulse data//data//map//transaction//hover//country//india//state//"
    map_trans_list = os.listdir(path3)
    columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
                'Amount': []}

    for state in map_trans_list:
        cur_state = path3 + state + "/"
        map_year_list = os.listdir(cur_state)

        for year in map_year_list:
            cur_year = cur_state + year + "/"
            map_file_list = os.listdir(cur_year)

            for file in map_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                C = json.load(data)

                for i in C["data"]["hoverDataList"]:
                    District = i["name"]
                    Count = i["metric"][0]["count"]
                    Amount = i["metric"][0]["amount"]
                    columns3["District"].append(District)
                    columns3["Count"].append(Count)
                    columns3["Amount"].append(Amount)
                    columns3["State"].append(state)
                    columns3["Year"].append(year)
                    columns3["Quarter"].append(int(file.strip(".json")))

    df_map_trans = pd.DataFrame(columns3)
    return df_map_trans


# Extracting Map user details from Statewise,Yearwise and Quarterwise
def extract_map_user():
    path_4 = "C://Users//Jeni//Desktop//phonepe pulse data//data//map//user//hover//country//india//state//"
    map_user_list = os.listdir(path_4)
    columns4 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'registeredUsers': [],'AppOpens': []}

    for state in map_user_list:
        curr_stat = path_4 + state + "/"
        map_year_list = os.listdir(curr_stat)

        for year in map_year_list:
            curr_year = curr_stat + year + "/"
            map_file_list = os.listdir(curr_year)

            for file in map_file_list:
                curr_file = curr_year + file
                data = open(curr_file, 'r')
                D = json.load(data)

                for i in D["data"]["hoverData"].items():
                    district = i[0]
                    registeredusers = i[1]['registeredUsers']
                    appopens = i[1]["appOpens"]
                    columns4["District"].append(district)
                    columns4["registeredUsers"].append(registeredusers)
                    columns4["AppOpens"].append(appopens)
                    columns4["State"].append(state)
                    columns4["Year"].append(year)
                    columns4["Quarter"].append(int(file.strip('.json')))

    df_map_users = pd.DataFrame(columns4)
    return df_map_users


# Extracting Top Transaction details from Statewise,Yearwise and Quarterwise
def extract_top_transactions():
    path5 = "C://Users//Jeni//Desktop//phonepe pulse data//data//top//transaction//country//india//state//"
    top_trans_list = os.listdir(path5)
    columns5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
                'Transaction_amount': []}

    for state in top_trans_list:
        curr_stat = path5 + state + '/'
        top_year_list = os.listdir(curr_stat)

        for year in top_year_list:
            curr_year = curr_stat + year + '/'
            top_file_list = os.listdir(curr_year)

            for file in top_file_list:
                curr_file = curr_year + file
                data = open(curr_file, 'r')
                E = json.load(data)

                for i in E["data"]["pincodes"]:
                    name = i["entityName"]
                    count = i["metric"]["count"]
                    amount = i["metric"]["count"]
                    columns5['Pincode'].append(name)
                    columns5['Transaction_count'].append(count)
                    columns5['Transaction_amount'].append(amount)
                    columns5['State'].append(state)
                    columns5['Year'].append(year)
                    columns5['Quarter'].append(int(file.strip('.json')))

    df_top_trans = pd.DataFrame(columns5)
    return df_top_trans


# Extracting Top User details from Statewise,Yearwise and Quarterwise
def extract_top_user():
    path6 = "C://Users//Jeni//Desktop//phonepe pulse data//data//top//user//country//india//state//"
    top_user_list = os.listdir(path6)
    columns6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Registeredusers': []}

    for state in top_user_list:
        curr_stat = path6 + state + '/'
        top_year_list = os.listdir(curr_stat)

        for year in top_year_list:
            curr_year = curr_stat + year + '/'
            top_file_list = os.listdir(curr_year)

            for file in top_file_list:
                curr_file = curr_year + file
                data = open(curr_file, 'r')
                F = json.load(data)

                for i in F['data']['pincodes']:
                    pincode = i['name']
                    registeredusers = i['registeredUsers']
                    columns6['Pincode'].append(pincode)
                    columns6['Registeredusers'].append(registeredusers)
                    columns6['State'].append(state)
                    columns6['Year'].append(year)
                    columns6['Quarter'].append(int(file.strip('.json')))
    df_top_user = pd.DataFrame(columns6)
    return df_top_user


# Convert all the details from Dataframe to CSV file
def convert_to_csvfile():
    agg_trans = extract_aggregated_transactions()
    agg_trans.to_csv('agg_trans.csv',index=False)
    agg_user = extract_aggregated_user()
    agg_user.to_csv('agg_user.csv',index=False)
    map_trans = extract_map_transactions()
    map_trans.to_csv('map_trans.csv',index=False)
    map_user = extract_map_user()
    map_user.to_csv('map_user.csv',index=False)
    top_trans = extract_top_transactions()
    top_trans.to_csv('top_trans.csv',index=False)
    top_user = extract_top_user()
    top_user.to_csv('top_user.csv',index=False)


# Inserting values into Tables
def insert_values(variable_name,table_name,cursor,connection):
    for i, row in variable_name.iterrows():
        sql = f"INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()


#username = "root"
#password = "Jeni27589$"
#host = "localhost"
#database_name = "phonepe_pulse"
#auth_plugin = "?auth_plugin=mysql_native_password"

#df_trans = extract_aggregated_transactions()
#st.write(df_trans.dtypes)
#table_name = "agg_trans"

#cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_name = 'agg_trans'")
#result = cursor.fetchone()

#if not result:
# create_table_query = f"CREATE TABLE {table_name} ("
# for column_name, data_type in zip(df_trans.columns, df_trans.dtypes):
 #   if str(data_type) == 'object':
 #       column_type = "VARCHAR(255)"  # Adjust the maximum length as needed
    #elif str(data_type) == 'int64':
     #   column_type = "INT8"
    #elif str(data_type) == 'float64':
     #   column_type = "FLOAT10"
 #   else:
 #       column_type = "VARCHAR(255)"  # Default to VARCHAR
#
#    create_table_query += f"{column_name} {column_type}, "

# create_table_query = create_table_query[:-2]
# create_table_query += ");"
# cursor.execute(create_table_query)
 
#engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database_name}{auth_plugin}")
#df_trans.to_sql('agg_trans', con=engine, if_exists='replace', index=False)

#connection.commit()
#cursor.close()
#connection.close()
