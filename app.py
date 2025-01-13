import streamlit as st
#streamlit page title and header setting
st.set_page_config(
  page_title="Flight Route Optimization"
)
st.header("Flight Route Optimization", divider="gray") 

# Create a form
with st.form("input_form"):
    pop_size = st.number_input("Enter your Population Size", min_value=100, max_value=1000)
    num_generations = st.number_input("Enter your Number of Generation", min_value=100, max_value=1000)
    mutation_rate = st.number_input("Enter your Mutation Rate", min_value=0.01, max_value=0.05)
    
    # Submit button inside the form
    submitted = st.form_submit_button("Confirm")

# Code after form submission
if submitted:
    st.write("You have confirmed the parameters!")
    st.write("Population Size: ", pop_size)
    st.write("Number of Generation: ", num_generations)
    st.write("Mutation Rate: ", mutation_rate) 

