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

# Create a form widget
with st.form("airport_form"):
    
    # Create checkboxes for each airport
    st.write("Select airports from the list below:")
    selected_airports = []
    for airport in airport_data['Airport'][1:]:
        if st.checkbox(airport, key=airport):
            selected_airports.append(airport)

    # Set the parameter
    pop_size = st.number_input("Enter your Population Size", min_value=100, max_value=1000)
    num_generations = st.number_input("Enter your Number of Generation", min_value=100, max_value=1000)
    mutation_rate = st.number_input("Enter your Mutation Rate", min_value=0.01, max_value=0.05)

    
    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Extract the first airport
        first_airport = airport_data.iloc[0]
        selected_airports_data = airport_data[airport_data['Airport'].isin(selected_airports)]
        # Combine the first airport and selected airports
        result_df = pd.concat([first_airport.to_frame().T, selected_airports_data], ignore_index=True)

        # Save to a new CSV file
        result_csv_path = "selected_airport/selected_airports.csv"
        result_df.to_csv(result_csv_path, index=False)
        st.write("You selected the following airports:")
        st.write(result_df)
        st.success(f"CSV file created successfully: {result_csv_path}")
        # Print the parameters
        st.write("You have confirmed the parameters!")
        st.write("Population Size: ", pop_size)
        st.write("Number of Generation: ", num_generations)
        st.write("Mutation Rate: ", mutation_rate) 
