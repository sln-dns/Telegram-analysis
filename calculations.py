import sqlite3
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = 'data.sqlite'

#Total messages
def total_messages():

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    query = '''
        SELECT COUNT(*) 
        FROM messages
        '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    return  str(results[0][0])


# Total users
def total_users():

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    query = '''
        SELECT COUNT(*) 
        FROM users
        '''

# Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

# Print the results
    return str(results[0][0])

def active_users(number_of_days):

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

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

    conn.close()
    return str(num_users)


def last_activity(days):

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

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

    conn.close()
    return str(num_messages)


def heat_map():

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
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

    
    conn.close()
    # Show the plot
    plt.title('Most Active Day/Time of Day for Sending Messages')
    return fig