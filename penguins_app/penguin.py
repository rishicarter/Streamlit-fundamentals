import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Penguins Rule!")
st.markdown('Plots on Penguins..')
penguin_file = st.file_uploader('Select Local Penguins CSV')
if penguin_file is not None:
    # st.write(penguin_file.name)
    penguindf=pd.read_csv(penguin_file.name)
    df=pd.read_csv(penguin_file.name)
else:
    df=pd.read_csv("penguins.csv")
    penguindf=pd.read_csv("penguins.csv")
    # st.stop()

# df=pd.read_csv("penguins.csv")
# st.write(df.head())
species=list(df.species.unique())
xy_vars=list(df.columns)[2:6]
selected_species=st.selectbox('Visualise Penguin Species', 
             species)
selected_xvar,selected_yvar=st.selectbox('Variable for x axis',xy_vars),st.selectbox('Variable for y axis', xy_vars)
selected_gender=st.selectbox('Penguin Gender Filter',('All','male','female'))
st.write(df.head())
# penguindf=pd.read_csv("penguins.csv")
penguindf=penguindf[penguindf['species']==selected_species]
if selected_gender!='All':
    penguindf=penguindf[penguindf['sex']==selected_gender]
fig,ax=plt.subplots()
ax=sns.scatterplot(data=penguindf,
                   x=penguindf[selected_xvar],
                   y=penguindf[selected_yvar])
plt.title(f'\'{selected_species}\' Penguins')
plt.xlabel(selected_xvar)
plt.ylabel(selected_yvar)
st.pyplot(fig)

st.header('Scatter Plot of all Penguin Species!')
sns.set_style('darkgrid')
markers={"Adelie": "X", "Gentoo": "s", "Chinstrap":'o'}
fig1,ax1=plt.subplots()
ax1=sns.scatterplot(data=df,
                    x=df[selected_xvar],
                    y=df[selected_yvar],
                    hue='species',
                    markers=markers,
                    style='species')
plt.title(f'All Penguins')
plt.xlabel(selected_xvar)
plt.ylabel(selected_yvar)
st.pyplot(fig1)