# Imports
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Functions ---------------
# @st.cache_data
def get_value_from_choice(df,choice):
    return df[df['stock']==choice]['quantity'].values[0]

def refresh_df():
    # st.experimental_rerun()
    pass

#--------------------------

# App Config
st.set_page_config(
    page_title="IMS App",
    page_icon="🍗",
    layout="centered",
    initial_sidebar_state='collapsed',
    menu_items={
        'About': "# App to organise, manage and plan stock requirements!"
    }
)

# App Brief
st.title('Inventory Management with Friends!')
st.subheader('App to organise, manage and plan stock requirements.')

# TODO: File handling using data_upload.py
filepath='./stock_info.csv'
main_df=pd.read_csv(filepath)

# Sidebar Filtering
df_categories=main_df['category'].unique()
selected_categories=st.sidebar.multiselect("Filter the Categories", df_categories)
df=main_df.copy()
if selected_categories:
    df=df[df['category'].isin(selected_categories)].reset_index(drop=True)
# df_table=st.dataframe(df)
# Data Viz
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
    df_table=st.dataframe(df)

# Data Add/Update
tab_update,tab_add=st.tabs(["Update Stock","Add Stock"])
with tab_update:
    update_container=st.container()
    with update_container:
        col_update_form, col_data_editor=st.columns(2)
        with col_update_form:
            # All items list
            all_items=list(df['stock'].unique())
            choice=st.selectbox('Enter Stock Item',all_items,key='choice')
            st.write(df.loc[df['stock']==choice,'quantity'])
            new_value=0
            old_value=get_value_from_choice(df,choice)
            # st.write(old_value)
            new_value=st.number_input(f"New Value of Stock Item? (Old Value={old_value})",
                                        min_value=0, value=old_value, key='new_value')
            df['quantity'] = np.where(df['stock']==choice, new_value, df['quantity'])
            st.write(df)
                    # # df.loc[df['stock']==choice,'quantity']=new_value
                    # st.success('Stock Info updated Successfully!')
        
        with col_data_editor:
            df = st.experimental_data_editor(df, key='update_editor')
            # st.experimental_rerun()
            # update_container.experimental_rerun()

with tab_add:
    add_container=st.container()
    with add_container:
        quant_flg,cat_flg=True,True
        col_add_stock,col_add_quantity=st.columns(2)
        add_stock=col_add_stock.text_input('Stock Item name', placeholder='add `(individual)` for single stock. Eg: Eggs (individual)')
        quant_flg=False if add_stock else True
        add_quantity=col_add_quantity.number_input('Stock Quantity', min_value=0, disabled=quant_flg)
        cat_flg=False if add_quantity else True
        col_add_cat_radio,col_add_cat_value=st.columns(2)
        add_cat_option=col_add_cat_radio.radio('Select Category option',
                                         ('Pre-existing Category','New Category'),
                                         disabled=cat_flg)
        if add_cat_option=='Pre-existing Category':
            add_cat_value=col_add_cat_value.selectbox('Select Category', options=df_categories,
                                                      disabled=cat_flg)
        elif add_cat_option=='New Category':
            add_cat_value=col_add_cat_value.text_input('Input Category', disabled=cat_flg)
        if cat_flg:
            add_cat_value=""
        if add_cat_value:
            temp_df=pd.DataFrame({'stock':add_stock,
                                       'quantity':add_quantity,
                                       'category':add_cat_value}, index=[0])
            # temp_df=pd.DataFrame([[add_stock,add_quantity,add_cat_value]],
            #                      columns=['stock','quantity','category'])
            # temp_df={'stock':add_stock,
            #          'quantity':[add_quantity],
            #          'category':[add_cat_value]}
            if st.button('Add Item'):
                # st.dataframe(pd.DataFrame(df_table))
                # st.write(temp_df)
                main_df=pd.concat([main_df,temp_df]).reset_index(drop=True)
                # st.write(main_df)
                main_df.to_csv(filepath,index=False)
                col1,col2=st.columns(2)
                col1.success('Data Added Successfully!!')
                with col2:
                    with st.spinner('Refreshing data...'):
                        time.sleep(2)
                        st.experimental_rerun()
                
                
        


    