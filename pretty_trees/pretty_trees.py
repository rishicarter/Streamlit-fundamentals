import streamlit as st
import pandas as pd
st.set_page_config(layout='wide')
st.title('SF Trees')
st.write('This app analyses trees in San Francisco using a dataset kindly provided by SF DPW')
trees_df = pd.read_csv('trees.csv')

# first_width,second_width,third_width=st.number_input('First Width', min_value=1, value=1),st.select_slider('Second Width', options=range(1,101,1)),st.select_slider('Third_width',options=range(1,101,1))

col_1,col_2,col_3=st.columns((1,1,1))
first_width,second_width,third_width=col_1.number_input('First Width', min_value=1, value=1),col_2.select_slider('Second Width', options=range(1,11,1)),col_3.select_slider('Third_width',options=range(1,11,1))

col1,col2,col3=st.columns((first_width,second_width,third_width))

df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['tree_count']


with col1:
    st.line_chart(df_dbh_grouped)

with col2:
    st.bar_chart(df_dbh_grouped)
    
with col3:
    st.area_chart(df_dbh_grouped)
    