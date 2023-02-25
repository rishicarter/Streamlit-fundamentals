import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Penguins Species Predictor')
st.subheader('Using penguin features to determine the species of the penguin')


penguin_file = st.file_uploader('Upload your own penguin data')
if penguin_file is None:
    with open('./random_forest_penguin.pickle','rb') as rf_pickle:
        rfc=pickle.load(rf_pickle)
    with open('./output_penguin.pickle', 'rb') as map_pickle:
        mapping=pickle.load(map_pickle)
else:
    penguin_df = pd.read_csv(penguin_file)
    penguin_df.dropna(inplace=True)
    output = penguin_df['species']
    features = penguin_df[['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g',
    'sex']]
    features = pd.get_dummies(features)
    output, uniques = pd.factorize(output)
    x_train, x_test, y_train, y_test = train_test_split(features, output, test_size=.8)
    rfc = RandomForestClassifier(random_state=42)
    rfc.fit(x_train, y_train)
    y_pred = rfc.predict(x_test)
    score = accuracy_score(y_pred, y_test)
    st.write('Accuracy score for this model is {}'.format(score))

# st.write(rfc)
# st.write(mapping)

penguin_df = pd.read_csv('penguins.csv')
penguin_df.dropna(inplace=True)
output = penguin_df['species']
features = penguin_df[['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g',
'sex']]

# st.write(penguin_df.tail())
# st.write(penguin_df.bill_length_mm.min(),penguin_df.bill_length_mm.max())

with st.form('user_inputs'):
    selected_island = st.selectbox('Which island was the penguin found on?', penguin_df['island'].unique())

    selected_gender = st.selectbox('Gender', penguin_df['sex'].unique())

    selected_bill_length = st.select_slider('Bill Length (mm)', options=range(10,101,1))

    selected_bill_depth=st.select_slider('Bill Depth (mm)', options=range(10,101,1))

    selected_flipper_length=st.select_slider('Flipper Length (mm)', options=range(100,201,1))

    selected_bodymass = st.select_slider('Body Mass (g)',
                                        options=range(3000, 4000,1))
    st.form_submit_button()

st.write('the user inputs are {}'.format([selected_island, selected_gender, selected_bill_length, selected_bill_depth, selected_flipper_length, selected_bodymass]))

island_biscoe, island_dream, island_torgerson = 0, 0, 0
if selected_island == 'Biscoe':
    island_biscoe = 1
elif selected_island == 'Dream':
    island_dream = 1
elif selected_island == 'Torgerson':
    island_torgerson = 1
sex_female, sex_male = 0, 0
if selected_gender == 'Female':
    sex_female = 1
elif selected_gender == 'Male':
    sex_male = 1


new_prediction = rfc.predict([[selected_bill_length,selected_bill_depth, selected_flipper_length, selected_bodymass, island_biscoe, island_dream,  island_torgerson, sex_female, sex_male]])

prediction_species = mapping[new_prediction][0]
st.write('We predict your penguin is of the `{}` species'.format(prediction_species))

st.write('We used a machine learning (Random Forest) model to predict the species, the features used in this prediction are ranked by relative importance below.')
st.image('feature_importance.png')

st.write('Below are the histograms for each continuous variable separated by penguin species. The vertical line represents your the inputted value.')

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['bill_length_mm'],hue=penguin_df['species'])
plt.axvline(selected_bill_length)
plt.title('Bill Length by Species')
st.pyplot(ax)
fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['bill_depth_mm'],hue=penguin_df['species'])
plt.axvline(selected_bill_depth)
plt.title('Bill Depth by Species')
st.pyplot(ax)
fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['flipper_length_mm'],
 hue=penguin_df['species'])
plt.axvline(selected_flipper_length)
plt.title('Flipper Length by Species')
st.pyplot(ax)
fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['body_mass_g'],
 hue=penguin_df['species'])
plt.axvline(selected_bodymass)
plt.title('BodyMass by Species')
st.pyplot(ax)