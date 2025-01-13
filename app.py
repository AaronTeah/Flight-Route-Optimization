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
################## Show the airport location in a simple plot#####################
# # Scatter plot for airport locations
# fig = plt.figure(figsize=(12, 8))
# plt.scatter(airport_data['Longitude'], airport_data['Latitude'], color='red', s=10, label='Airports')
# # Add labels for each airport
# for i, row in airport_data.iterrows():
#     plt.text(
#         row['Longitude'],
#         row['Latitude'],
#         row['Airport'],  # Display the airport name
#         fontsize=8,
#         ha='right',      # Horizontal alignment
#         va='bottom'      # Vertical alignment
#     )
# # Add title, labels, legend, and grid
# plt.title('Airports Map with Names', fontsize=16)
# plt.xlabel('Longitude', fontsize=12)
# plt.ylabel('Latitude', fontsize=12)
# plt.legend()
# plt.grid(True)
# st.pyplot(fig)
#################################### Data arrangement ############################################
import numpy as np
from geopy.distance import geodesic
import random
# Prepare the dataset for route optimization
# Keep only the required columns and add a unique ID for each airport
airport_data = airport_data[['Airport', 'Latitude', 'Longitude']]
airport_data['ID'] = range(len(airport_data))
# Filter data to include only relevant airports (e.g., max 20 for simplicity in this demo)
selected_airports = airport_data.iloc[:20]  # Limiting to 20 airports for computation
selected_airports.reset_index(drop=True, inplace=True)
# Get the coordinates for LAX (start and end point)
lax = selected_airports[selected_airports['Airport'].str.contains('Los Angeles International Airport')]
# Check if LAX is included
if lax.empty:
    raise ValueError("LAX is not included in the selected airports.")

lax_coords = (lax.iloc[0]['Latitude'], lax.iloc[0]['Longitude'])
# Generate the distance matrix
def create_distance_matrix(airports):
    n = len(airports)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            coord1 = (airports.iloc[i]['Latitude'], airports.iloc[i]['Longitude'])
            coord2 = (airports.iloc[j]['Latitude'], airports.iloc[j]['Longitude'])
            matrix[i, j] = geodesic(coord1, coord2).km
    return matrix
distance_matrix = create_distance_matrix(selected_airports)
##################################### Model development #################################################
import time
start_time = time.time()

# Genetic Algorithm components
def initialize_population(pop_size, num_airports):
    population = []
    for _ in range(pop_size):
        route = list(range(1, num_airports))  # Exclude LAX (index 0)
        random.shuffle(route)
        population.append([0] + route + [0])  # Start and end at LAX
    return population

def fitness(route, distance_matrix):
    return sum(distance_matrix[route[i], route[i+1]] for i in range(len(route)-1))

def select_parents(population, fitnesses, num_parents):
    fitness_prob = [1/f for f in fitnesses]
    fitness_prob /= np.sum(fitness_prob)
    return random.choices(population, weights=fitness_prob, k=num_parents)

def crossover(parent1, parent2):
    size = len(parent1) - 2
    start, end = sorted(random.sample(range(1, size+1), 2))
    child = [-1] * len(parent1)
    child[start:end+1] = parent1[start:end+1]
    pointer = 1
    for gene in parent2[1:-1]:
        if gene not in child:
            while child[pointer] != -1:
                pointer += 1
            child[pointer] = gene
    child[0] = child[-1] = 0
    return child

def mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = sorted(random.sample(range(1, len(route)-1), 2))
        route[idx1], route[idx2] = route[idx2], route[idx1]

def genetic_algorithm(distance_matrix, pop_size, num_generations, mutation_rate):
    num_airports = len(distance_matrix)
    population = initialize_population(pop_size, num_airports)
    best_route = None
    best_distance = float('inf')
    history = []

    for generation in range(num_generations):
        fitnesses = [fitness(route, distance_matrix) for route in population]
        min_distance = min(fitnesses)
        history.append(min_distance)
        if min_distance < best_distance:
            best_distance = min_distance
            best_route = population[fitnesses.index(min_distance)]

        # Use tournament selection for more competitive parent selection
        parents = [
            min(random.sample(population, k=5), key=lambda x: fitness(x, distance_matrix))
            for _ in range(pop_size // 2)
        ]

        # Generate offspring
        offspring = []
        for i in range(0, len(parents), 2):
            offspring.append(crossover(parents[i], parents[i+1]))
            offspring.append(crossover(parents[i+1], parents[i]))

        # Apply mutation
        for child in offspring:
            mutate(child, mutation_rate)

        # Replace population with offspring
        population = offspring

    return best_route, best_distance, history
############################################### Run the Genetic Algorithm ######################################################
best_route, best_distance, history = genetic_algorithm(distance_matrix, pop_size=300, num_generations=700, mutation_rate=0.01)
# Display the best route and its distance
best_route_details = selected_airports.iloc[best_route]
best_route_details = best_route_details.drop(columns=['ID']).reset_index(drop=True)

# Streamlit app to display the results
st.title("Best Route Details")
st.table(best_route_details)

########################################## visualize the route ###################################
# Extract coordinates from the route
latitudes = [selected_airports.iloc[i]['Latitude'] for i in best_route]
longitudes = [selected_airports.iloc[i]['Longitude'] for i in best_route]
airport_names = [selected_airports.iloc[i]['Airport'] for i in best_route]

# Create the plot
fig = plt.figure(figsize=(10, 6))
plt.scatter(longitudes, latitudes, color='blue', label='Airports')
plt.plot(longitudes, latitudes, color='red', linestyle='-', linewidth=1, label='Route')

# Annotate each airport
for i, name in enumerate(airport_names):
    plt.text(longitudes[i], latitudes[i], f'{i + 1}. {name.split(" ")[0]}', fontsize=8)

# Add labels and legend
plt.title('Optimized Flight Route')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.write("Total distance: {best_distance} km")
# End time
end_time = time.time()
total_runtime = end_time - start_time
st.write(f"Total Runtime: {total_runtime} seconds")


# Visualization of performance
fig = plt.figure(figsize=(10, 6))
plt.plot(history, label='Total Distance')
plt.title('Genetic Algorithm Performance')
plt.xlabel('Generation')
plt.ylabel('Total Distance (km)')
plt.legend()
st.pyplot(fig)

################################# Baseline comparison using a random route ##################################
st.title("Baseline comparison using a random route")
def random_route_baseline(distance_matrix):
    num_airports = len(distance_matrix)
    random_route = [0] + random.sample(range(1, num_airports), num_airports - 1) + [0]
    random_distance = fitness(random_route, distance_matrix)
    return random_route, random_distance

# Generate a random route and calculate its distance
random_route, random_distance = random_route_baseline(distance_matrix)

# Calculate improvement percentage
improvement_percentage = ((random_distance - best_distance) / random_distance) * 100

# Display results
random_route_details = selected_airports.iloc[random_route]
random_route_details = selected_airports.drop(columns=['ID']).reset_index(drop=True)
st.write("Random Route")
st.table(random_route_details)
st.write("Total distance of random route: ", random_distance)
st.write("Improved Percentage: ", improvement_percentage)
