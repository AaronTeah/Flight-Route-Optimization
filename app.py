import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#streamlit page title and header setting
st.set_page_config(
  page_title="Flight Route Optimization"
)
st.header("Flight Route Optimization", divider="gray") 

# Load the dataset
file_path_select = 'Airport_Coordinates_Dataset__Real-World_Airports_.csv'
airport_data_select = pd.read_csv(file_path_select)

# Create a form widget
with st.form("airport_form"):
    
    # Create checkboxes for each airport
    st.write("Select airports from the list below:")
    selected_airports = []
    for airport in airport_data_select['Airport'][1:]:
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
        first_airport = airport_data_select.iloc[0]
        selected_airports_data = airport_data_select[airport_data_select['Airport'].isin(selected_airports)]
        # Combine the first airport and selected airports
        result_df = pd.concat([first_airport.to_frame().T, selected_airports_data], ignore_index=True)

        # Save to a new CSV file
        result_csv_path = "selected_airports.csv"
        result_df.to_csv(result_csv_path, index=False)
        st.write("You selected the following airports:")
        st.write(result_df)
        st.success(f"CSV file created successfully: {result_csv_path}")
        # Print the parameters
        st.write("You have confirmed the parameters!")
        st.write("Population Size: ", pop_size)
        st.write("Number of Generation: ", num_generations)
        st.write("Mutation Rate: ", mutation_rate) 


######################## Data Preparation for GA ############################
# Load the uploaded CSV file to examine its content
file_path = 'selected_airports.csv'
airport_data = pd.read_csv(file_path)
# Scatter plot for airport locations
fig = plt.figure(figsize=(12, 8))
plt.scatter(airport_data['Longitude'], airport_data['Latitude'], color='red', s=10, label='Airports')
# Add labels for each airport
for i, row in airport_data.iterrows():
    plt.text(
        row['Longitude'],
        row['Latitude'],
        row['Airport'],  # Display the airport name
        fontsize=8,
        ha='right',      # Horizontal alignment
        va='bottom'      # Vertical alignment
    )
# Add title, labels, legend, and grid
plt.title('Airports Map with Names', fontsize=16)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.legend()

st.pyplot(fig)
plt.grid(True)
plt.show()
