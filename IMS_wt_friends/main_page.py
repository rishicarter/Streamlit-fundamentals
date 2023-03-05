# Imports
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Functions ---------------
@st.cache_data
def get_value_from_choice(df,choice):
    return df[df['stock']==choice]['quantity'].values[0]


#--------------------------

# App Config
st.set_page_config(
    page_title="IMS App",
    page_icon="🍗",
    layout="centered",
    menu_items={
        'About': "# App to organise, manage and plan stock requirements!"
    }
)

# App Brief
st.title('Inventory Management with Friends!')
st.subheader('App to organise, manage and plan stock requirements.')

# TODO: File handling using data_upload.py

# Data Viz
df=pd.read_csv('./stock_info.csv')
# _,col_viz,_=st.columns([1,10,1])
# with col_viz:
viz_container=st.container()
plt.style.use('dark_background')
fig_viz,ax_viz=plt.subplots()
ax_viz=sns.barplot(data=df,x='stock',y='quantity',hue='category',dodge=False)
for i in ax_viz.containers:
    ax_viz.bar_label(i,)
plt.title("Items present in Stock")
plt.xticks(rotation=-80)
plt.xlabel('')
plt.ylabel("Quantity")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
viz_container.pyplot(fig_viz)
with viz_container.expander('Show Table'):
    st.dataframe(df)

# Data Add/Update
tab_update,tab_add=st.tabs(["Update Stock","Add Stock"])
with tab_update:
    col_update_form, col_data_editor=st.columns(2)
    with col_update_form:
        # All items list
        all_items=list(df['stock'].unique())
        
        choice=st.selectbox('Enter Stock Item',all_items,key=-1)
        st.write(df.loc[df['stock']==choice,'quantity'])
        with col_update_form.form(key='Update_form'):
            new_value=0
            old_value=get_value_from_choice(df,choice)
            # st.write(old_value)
            new_value=st.number_input(f"New Value of Stock Item? (Old Value={old_value})",
                                      min_value=0, value=old_value)
            
            submit_flg=st.form_submit_button('Submit')
            if submit_flg:
                df['quantity'] = np.where(df['stock']==choice, new_value, df['quantity'])
                st.write(df)
                st.write(df.loc[df['stock']==choice,'quantity'])
                # # df.loc[df['stock']==choice,'quantity']=new_value
                # st.success('Stock Info updated Successfully!')
