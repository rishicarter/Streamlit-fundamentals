import numpy as np
import streamlit as st
import time

progress_bar=st.sidebar.progress(0)
status_text=st.sidebar.empty()
last_rows=np.random.randn(1,1)
chart = st.line_chart(last_rows)

for i in range(1,101):
    new_rows = last_rows[-1, :] + np.random.randn(10,1).cumsum(axis=0)
    status_text.text(f"{i}% Complete")
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows=new_rows
    time.sleep(0.05)
    
progress_bar.empty()
st.button("Re-run")