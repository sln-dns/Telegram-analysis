import sqlite3
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from calculations import total_messages, total_users, active_users, last_activity, heat_map, week_growth, weekly_messages, weekly_metrics


#conn = sqlite3.connect('data.sqlite')
#cursor = conn.cursor()


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

