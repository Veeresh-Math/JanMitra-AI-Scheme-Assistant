import inspect, streamlit as st
print(inspect.getsource(st.Page))
print('---')
print(inspect.getsource(st.navigation))