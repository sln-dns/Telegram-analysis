import sqlite3
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

#Total messages
def total_messages():
    
    query = '''
        SELECT COUNT(*) 
        FROM messages
        '''
    cursor.execute(query)
    results = cursor.fetchall()
    return  results[0][0]

total_messages = str(total_messages())

def total_users():
    
    query = '''
        SELECT COUNT(*) 
        FROM users
        '''

# Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

# Print the results
    return results[0][0]

total_users = str(total_users())

def active_users(number_of_days):

    # calculate the date range for the last week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=number_of_days)

    # convert the date objects to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # query to get the number of users who sent messages in the last week
    query = """
    SELECT COUNT(DISTINCT user_id)
    FROM messages
    WHERE date BETWEEN ? AND ?
    """

    # execute the query with the date range parameters
    cursor.execute(query, (start_date_str, end_date_str))

    # fetch the result and print the number of users
    num_users = cursor.fetchone()[0]
    return num_users

number_of_active_users = str(active_users(10))

def last_activity(days):
    # calculate the date range for the last 'days'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # query to get the number of messages sent in the last 'days'
    query = """
    SELECT COUNT(*)
    FROM messages
    WHERE date BETWEEN ? AND ?
    """

    cursor.execute(query, (start_date, end_date))

    # fetch the result and return the number of messages
    num_messages = cursor.fetchone()[0]
    return num_messages

number_of_messages = str(last_activity(10))

def heat_map():
    # Query to group messages by day and hour and count the number of messages for each group
    query = '''
    SELECT strftime('%w', date) as day, strftime('%H', date) as hour, count(*) as count
    FROM messages
    GROUP BY day, hour
    '''

    # Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the results to a pandas dataframe
    df = pd.DataFrame(results, columns=['day', 'hour', 'count'])

    # Pivot the dataframe to create a heatmap
    df_pivot = df.pivot(index='day', columns='hour', values='count')

    # Plot the heatmap
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    im = ax.imshow(df_pivot, cmap='YlOrRd')

    # Add a colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    # Set the tick labels
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
             '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    
    ax.set_xticks(range(len(hours)))
    ax.set_yticks(range(len(days)))
    ax.set_xticklabels(hours)
    ax.set_yticklabels(days)
    ax.set_xticks(ax.get_xticks()[::2]
                  )
    # Rotate the tick labels and set the axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Day of Week')
    cbar.ax.set_ylabel('Number of Messages')

    # Add the count values as text annotations in each cell
    for i in range(len(days)):
        for j in range(len(hours)):
            text = ax.text(j, i, df_pivot.iloc[i, j],
                           ha="center", va="center", color="w", fontsize = 8)

    # Show the plot
    plt.title('Most Active Day/Time of Day for Sending Messages')
    return fig
    
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
            i = total_messages

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
            i = total_users

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
            i = number_of_active_users

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
            i = number_of_messages

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

