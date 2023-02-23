import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.plotting import figure
import altair as alt
import pydeck as pdk

st.title('SF Trees')
st.subheader('App to analyse trees in San Fransico!')

treesdf=pd.read_csv('./trees.csv')
treesdf.dropna(how='any', inplace=True)

sf_initial_view = pdk.ViewState(
    latitude=37.77,
    longitude=-122.4,
    zoom=15,
    pitch=30
)
st.write(treesdf[['latitude','longitude']].head())
sp_layer=pdk.Layer(
    'HexagonLayer',
    data=treesdf[['latitude','longitude']],
    get_postition=['longitude','latitude'],
    radius=100,
    extruded=True
)
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=sf_initial_view,
    layers=[sp_layer]
))









#fig=alt.Chart(treesdf).mark_bar().encode(x='caretaker',y='count(*):Q')
# st.altair_chart(fig)
# st.write(treesdf.head())

# treesdf['age']=(pd.to_datetime('today')-pd.to_datetime(treesdf['date'])).dt.days

# fig,ax=plt.subplots()
# ax=sns.histplot(treesdf['age'])
# plt.xlabel('Age (Days) - Seaborn')
# st.pyplot(fig)
# ax=plt.hist(treesdf['age'])
# plt.xlabel('Age (Days) - Matplotlib')
# st.pyplot(fig)

# scatterplot=figure(title='Bokeh Scatterplot')
# scatterplot.scatter(treesdf['dbh'],treesdf['site_order'])
# scatterplot.yaxis.axis_label='Site-order'
# scatterplot.xaxis.axis_label='DBH'
# st.bokeh_chart(scatterplot)





# dbh_df=pd.DataFrame(treesdf.groupby('dbh')['tree_id'].count().reset_index(drop=True))
# dbh_df.columns=['tree_count']

# st.line_chart(dbh_df)
# dbh_df['new_col']=np.random.randn(len(dbh_df))*500
# st.line_chart(dbh_df)
# # st.bar_chart(dbh_df)
# # st.area_chart(dbh_df)
# trees_df = pd.read_csv('trees.csv')
# trees_df = trees_df.dropna(subset=['longitude', 'latitude'])
# trees_df = trees_df.sample(n = 1000)
# st.map(trees_df)
# fig=px.histogram(treesdf['dbh'])
# st.plotly_chart(fig)