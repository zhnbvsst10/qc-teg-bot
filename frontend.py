import streamlit as st
import psycopg2
import pandas as pd


def update_db():
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute("""select * from pvc_params""")
    data = cursor.fetchall()
    cols =[]
    for i in cursor.description:
        cols.append(i[0])
    cursor.close()
    conn.close()
    return pd.DataFrame(data, columns = cols)

st.header('PVC data table')
df = update_db()
if st.button('update table') == True:
    df = update_db()

st.dataframe(df)
st.line_chart(df['diameter'], height=100)
st.line_chart(df['weight'], height=100)
st.line_chart(df['width'], height=100)
