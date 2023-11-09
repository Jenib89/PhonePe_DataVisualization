import streamlit as st
from PIL import Image
import mysql.connector as sql
import pulse_dataextraction
import pandas as pd
import plotly.express as px



# dataframe to csv
#pulse_dataextraction.convert_to_csvfile()

# # Creating connection with mysql workbench
connection = sql.connect(host="localhost",   
                   user = "root",               
                   password="Jeni27589$",
                   database  = "phonepe_pulse",
                   auth_plugin ="mysql_native_password")
mycursor = connection.cursor()

# Inserting values into Aggregated Transaction Table:
#df_agg_trans = pulse_dataextraction.extract_aggregated_transactions()
#pulse_dataextraction.insert_values(df_agg_trans,"agg_trans",mycursor,connection)

# Inserting values into Aggregated User Table:
#df_agg_user = pulse_dataextraction.extract_aggregated_user()
#pulse_dataextraction.insert_values(df_agg_user,"agg_user",mycursor,connection)

# Inserting values into Map Transaction Table
#df_map_trans = pulse_dataextraction.extract_map_transactions()
#pulse_dataextraction.insert_values(df_map_trans,"map_trans",mycursor,connection)

# Inserting values into Map User Table
#df_map_user = pulse_dataextraction.extract_map_user()
#pulse_dataextraction.insert_values(df_map_user,"map_user",mycursor,connection)

# Inserting values into Top Transaction Table
#df_top_trans = pulse_dataextraction.extract_top_transactions()
#pulse_dataextraction.insert_values(df_top_trans,"top_trans",mycursor,connection)

# Inserting values into Top User Table
#df_top_user = pulse_dataextraction.extract_top_user()
#for i,row in df_top_user.iterrows():
# sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
# mycursor.execute(sql, tuple(row))
 #connection.commit()


# Setting up page configuration
st.set_page_config(page_title= "Phonepe Pulse Data Visualization & Exploration",
                   layout= "wide")

st.header(" :violet[Phonepe dashboard]")


#tab1 = st.tabs(["Charts"])    
column1, column2 = st.columns(2, gap="medium")
with column1:
    Type = st.selectbox(":blue[Type]", ("Transactions", "Users"))       
    Quarter = st.selectbox(":blue[Quarter]", ("1", "2", "3", "4"))
with column2:
    Year = st.selectbox(":blue[Year]", ("2018", "2019", "2020", "2021", "2022", "2023"))
    # Top Charts - Visualization of Transaction Data
if Type  == "Transactions":
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    
    with col1:
        st.markdown("### :blue[State]")
        mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transactions_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :blue[District]")
        mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :blue[Pincode]")
        mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


    
        #Scatter chart
    mycursor.execute(f"select State, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
    chart_data = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
    st.scatter_chart(
    		chart_data,
    		x='State',
    		y='Total_amount',
    		color='Total_Transactions'    
    		)

    # barchart
    mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
    df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])
    fig = px.bar(df,  title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)
    
    
    mycursor.execute(f"select distinct state from agg_trans")
    dfstate = pd.DataFrame(mycursor.fetchall(), columns=['State'])
    state_list = dfstate['State'].tolist()
    selected_state = st.selectbox('## :blue[Select a State]', state_list)
    mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                          'Total_Transactions', 'Total_amount'])
    fig = px.bar(df1,
                     title='District wise Transactions ',
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)


    # Visualization of Users Data
if Type == "Users":
    col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
    with col1:
        st.markdown("### :blue[Brand]")
        mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
        fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown("### :blue[State]")
        mycursor.execute(f"select state, sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                     names='State',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Total_Appopens'],
                     labels={'Total_Appopens': 'Total_Appopens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :blue[District]")
        mycursor.execute(f"select district, sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)


    with col4:
        st.markdown("### :blue[Pincode]")
        mycursor.execute(
                f"select Pincode, sum(registeredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
        fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Total Users Statewise")
    mycursor.execute(f"select distinct state from agg_trans")
    dfstate = pd.DataFrame(mycursor.fetchall(), columns=['State'])
    state_list = dfstate['State'].tolist()
    selected_state = st.selectbox('## :blue[Select a State]', state_list)
    mycursor.execute(f"select State,District,sum(registeredUsers) as Total_Users from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

    df = pd.DataFrame(mycursor.fetchall(),columns=['State', 'District', 'Total_Users'])
    df.Total_Users = df.Total_Users.astype(int)
    df.set_index('District', inplace=True)
    st.line_chart(df)    

#  fig = px.scatter(
       #        df,
        #       x="District",
         #      y="Total_Users",
          #     color='Total_Users',
           #    color_continuous_scale="reds",
            #   )

        
       # st.plotly_chart(fig, use_container_width=True)