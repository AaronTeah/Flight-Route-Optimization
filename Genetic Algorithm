import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import random

# Import your genetic algorithm functions and other necessary functions
from flight_route_genetic_algorithm_v2 import (
    create_distance_matrix,
    initialize_population,
    fitness,
    crossover,
    mutate,
    genetic_algorithm,
    visualize_route,
)

# Load the airport dataset
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = 'Airport_Coordinates_Dataset__Real-World_Airports_.csv'
airport_data = load_data(file_path)

# Streamlit App
st.title("Flight Route Optimization")

# Sidebar Inputs
st.sidebar.header("User Input Parameters")
pop_size = st.sidebar.slider("Population Size", min_value=100, max_value=500, step=50, value=300)
num_generations = st.sidebar.slider("Number of Generations", min_value=100, max_value=1000, step=100, value=700)
mutation_rate = st.sidebar.slider("Mutation Rate", min_value=0.01, max_value=0.1, step=0.01, value=0.01)

# Preprocess the data
airport_data = airport_data[['Airport', 'Latitude', 'Longitude']]
airport_data['ID'] = range(len(airport_data))

selected_airports = airport_data.iloc[:20]  # Limit to 20 airports for simplicity
distance_matrix = create_distance_matrix(selected_airports)

# Run Genetic Algorithm
if st.button("Optimize Route"):
    with st.spinner("Running optimization..."):
        best_route, best_distance, history = genetic_algorithm(
            distance_matrix, pop_size, num_generations, mutation_rate
        )
        st.success("Optimization complete!")
        st.write(f"Best Distance: {best_distance:.2f} km")
        
        # Display the best route
        best_route_details = selected_airports.iloc[best_route]
        st.write("Optimized Route:")
        st.dataframe(best_route_details)

        # Visualize the history
        st.subheader("Algorithm Performance")
        plt.figure(figsize=(10, 6))
        plt.plot(history, label="Total Distance")
        plt.xlabel("Generation")
        plt.ylabel("Total Distance (km)")
        plt.title("Genetic Algorithm Performance")
        plt.legend()
        st.pyplot(plt)

        # Route visualization
        st.subheader("Optimized Route Visualization")
        visualize_route(best_route, selected_airports)

# Upload and explore the dataset
st.sidebar.subheader("Explore Dataset")
if st.sidebar.checkbox("Show Dataset"):
    st.write(airport_data)
