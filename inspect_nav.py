import inspect, streamlit as st
print('Page signature:', inspect.signature(st.Page))
print()
print('switch_page source:')
print(inspect.getsource(st.switch_page))
print()
print('navigation source (first 200 chars):')
print(inspect.getsource(st.navigation)[:200])