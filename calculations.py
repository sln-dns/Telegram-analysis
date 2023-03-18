import sqlite3
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Total messages
def total_messages():
    
    query = '''
        SELECT COUNT(*) 
        FROM messages
        '''
    cursor.execute(query)
    results = cursor.fetchall()
    return  results[0][0]