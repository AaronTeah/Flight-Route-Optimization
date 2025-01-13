import streamlit as st
import pandas as pd
#streamlit page title and header setting
st.set_page_config(
  page_title="Flight Route Optimization"
)
st.header("Flight Route Optimization", divider="gray") 

# Load the dataset
file_path = 'Airport_Coordinates_Dataset__Real-World_Airports_.csv'
airport_data = pd.read_csv(file_path)
# Extract the airport names
airport_names = airport_data['Airport'].tolist()

# Create a form
with st.form("input_form"):
    pop_size = st.number_input("Enter your Population Size", min_value=100, max_value=1000)
    num_generations = st.number_input("Enter your Number of Generation", min_value=100, max_value=1000)
    mutation_rate = st.number_input("Enter your Mutation Rate", min_value=0.01, max_value=0.05)
    # Create a listbox in Streamlit
    selected_airport = st.selectbox("Select an Airport:", airport_names)
    
    # Submit button inside the form
    submitted = st.form_submit_button("Confirm")

# Code after form submission
if submitted:
    st.write("You have confirmed the parameters!")
    st.write("Population Size: ", pop_size)
    st.write("Number of Generation: ", num_generations)
    st.write("Mutation Rate: ", mutation_rate) 
    st.write(f"You selected: {selected_airport}")
