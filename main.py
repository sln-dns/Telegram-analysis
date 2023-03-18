import sqlite3
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from calculations import total_messages, total_users, active_users, last_activity, heat_map

conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()




    
def week_growth():
   # Query to group users by week and count the number of users for each group
    query = '''
    SELECT strftime('%Y-%W', date) as week, count(distinct user_id) as count
    FROM messages
    GROUP BY week
    '''

    cursor.execute(query)
    results = cursor.fetchall()
    # Convert the results to a pandas dataframe
    df = pd.DataFrame(results, columns=['week', 'count'])

    # Plot the graph
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['week'], df['count'], marker='o', markersize=8, color='orange')
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_xlabel('Week')
    ax.set_ylabel('Number of Users')
    ax.set_title('Weekly Growth of Users')
    ax.grid(True)      

    # Rotate the x-axis tick labels for better visibility
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    return fig


def weekly_messages():
    # Query to group messages by week and count the number of messages for each group
    query = '''
    SELECT strftime('%Y-%W', date) as week, count(*) as count
    FROM messages
    GROUP BY week
    '''

    # Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the results to a pandas dataframe
    df = pd.DataFrame(results, columns=['week', 'count'])

    # Set the figure size and font size
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams.update({'font.size': 12})

    # Create a bar chart with a colormap
    fig, ax = plt.subplots()
    im = ax.bar(df['week'], df['count'], color=plt.cm.YlOrRd(df['count']/max(df['count'])))

    # Set the axis labels and title
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_xlabel('Week')
    ax.set_ylabel('Number of Messages')
    ax.set_title('Weekly Messages')

    # Set the x-axis tick labels rotation and alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    

    # Add data labels to the bars
    for i in im:
        height = i.get_height()
        ax.annotate('{}'.format(height),
                    xy=(i.get_x() + i.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom', color='black', rotation = 90)

    # Show the plot

    return fig

def weekly_metrics():
    # Query to group users by week and count the number of users for each group
    query_users = '''
    SELECT strftime('%Y-%W', date) as week, count(distinct user_id) as users
    FROM messages
    GROUP BY week
    '''

    # Query to group messages by week and count the number of messages for each group
    query_messages = '''
    SELECT strftime('%Y-%W', date) as week, count(*) as messages
    FROM messages
    GROUP BY week
    '''
    # Execute the queries and fetch the results
    cursor.execute(query_users)
    results_users = cursor.fetchall()
    cursor.execute(query_messages)
    results_messages = cursor.fetchall()

    # Convert the results to pandas dataframes
    df_users = pd.DataFrame(results_users, columns=['week', 'users'])
    df_messages = pd.DataFrame(results_messages, columns=['week', 'messages'])

    # Merge the dataframes on week
    df_combined = pd.merge(df_users, df_messages, on='week')

    # Set the week column as the index
    df_combined.set_index('week', inplace=True)

    # Plot the graph
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(df_combined.index, df_combined['users'], df_combined['messages'], labels=['Users', 'Messages'], colors=['#FFE07F', '#FFBB4A'])
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_xlabel('Week')
    ax.set_ylabel('Count')
    ax.set_title('Weekly Metrics')
    ax.legend(loc='upper left')

    # Rotate the x-axis tick labels for better visibility
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    
    return fig


# Define the Streamlit app
def main():
      
    st.set_page_config(
        page_title='Telegram Channel Analysis', 
        page_icon=':bar_chart', 
        layout='wide', 
        initial_sidebar_state='collapsed')

    st.header('Telegram channel analysis')    

    # TODO make section with upload *.sqlite file and then use it to analysis
    ## create a function to read the data from the uploaded file
#def read_uploaded_data(uploaded_file):
    #conn = sqlite3.connect('file:{}?mode=ro'.format(uploaded_file.name), uri=True)
    #cursor = conn.cursor()
    #cursor.execute('SELECT * FROM my_table')
    #data = cursor.fetchall()
    #conn.close()
    #return data
#
## use the st.file_uploader function to upload the file
#uploaded_file = st.file_uploader("Upload a SQLite file", type=".sqlite")
#
## check if a file has been uploaded
#if uploaded_file is not None:
    ## use the read_uploaded_data function to read the data from the uploaded file
    #data = read_uploaded_data(uploaded_file)
    ## display the data in a table
#    st.table(data)    

    with st.container():

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            wch_colour_box = (249,205,59)
            wch_colour_font = (115,15,15)
            fontsize = 36
            valign = "left"
            iconname = ""
            sline = "Total messages"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = total_messages()

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        text-align: center;
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

            st.markdown(lnk + htmlstr, unsafe_allow_html=True)            
            #st.metric(label="Total messages", value=total_messages)
        with col2:
            wch_colour_box = (249,205,59)
            wch_colour_font = (115,15,15)
            fontsize = 36
            valign = "left"
            iconname = ""
            sline = "Total users"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = total_users()

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        text-align: center;
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

            st.markdown(lnk + htmlstr, unsafe_allow_html=True)             
            #st.metric(label='Total users', value = total_users)
        with col3:
            wch_colour_box = (249,205,59)
            wch_colour_font = (115,15,15)
            fontsize = 36
            valign = "left"
            iconname = ""
            sline = "Active users last 7 days"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = active_users(7)

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        text-align: center;
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

            st.markdown(lnk + htmlstr, unsafe_allow_html=True)
        #    st.metric(label='Active users last 7 days', value = number_of_active_users)
        with col4:
            wch_colour_box = (249,205,59)
            wch_colour_font = (115,15,15)
            fontsize = 36
            valign = "left"
            iconname = ""
            sline = "Messages for the last 10 days"
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
            i = last_activity(10)

            htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        text-align: center;
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

            st.markdown(lnk + htmlstr, unsafe_allow_html=True)
        #    st.metric(label = 'Messages for the last 10 days', value = number_of_messages)

    
    # Create two columns in Streamlit
    col1, col2 = st.columns(2)

    # Insert the heatmap plot in the first column
    with col1:
        fig = weekly_messages()
        st.pyplot(fig)
        
        fig = heat_map()
        st.pyplot(fig)

    # Insert some text in the second column
    with col2:
        fig = week_growth()
        st.pyplot(fig)

        fig = weekly_metrics()
        st.pyplot(fig)
        

# Run the Streamlit app
if __name__ == '__main__':
    main()

