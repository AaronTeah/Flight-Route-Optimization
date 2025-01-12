# -*- coding: utf-8 -*-
"""Flight route genetic algorithm v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W7oXqOw9hPDMQ5T0BIiuUFw9UGQUGxM0

# Data Preparation
"""

import pandas as pd

# Load the uploaded CSV file to examine its content
file_path = 'Airport_Coordinates_Dataset__Real-World_Airports_.csv'
airport_data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
airport_data.head()

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))

# Scatter plot for airport locations
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
plt.grid(True)

# Save the plot as an image
image_path_with_names = 'Airport_Map_With_Names.png'
plt.savefig(image_path_with_names, dpi=300, bbox_inches='tight')
plt.show()

image_path_with_names

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

"""# Model development"""

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

# Run the Genetic Algorithm
best_route, best_distance, history = genetic_algorithm(distance_matrix, pop_size=300, num_generations=700, mutation_rate=0.01)

# Display the best route and its distance
best_route_details = selected_airports.iloc[best_route]
best_route_details, best_distance

# Run the GA or improved GA
end_time = time.time()
total_runtime = end_time - start_time
print(f"Total Runtime: {total_runtime} seconds")

"""# Result and Discussion"""

# Visualization of performance
plt.figure(figsize=(10, 6))
plt.plot(history, label='Total Distance')
plt.title('Genetic Algorithm Performance')
plt.xlabel('Generation')
plt.ylabel('Total Distance (km)')
plt.legend()
plt.show()

# Baseline comparison using a random route
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
random_route_details, random_distance, improvement_percentage

import folium

# Create a map centered around LAX
lax_map = folium.Map(location=lax_coords, zoom_start=4)

# Add markers for each airport in the best route
for index, row in best_route_details.iterrows():
    folium.Marker(
        location=(row['Latitude'], row['Longitude']),
        popup=row['Airport'],
    ).add_to(lax_map)

# Draw lines connecting the airports in the best route
route_coords = [(row['Latitude'], row['Longitude']) for _, row in best_route_details.iterrows()]
folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(lax_map)

# Save the map to an HTML file and display it
map_file_path = "best_flight_route_map.html"
lax_map.save(map_file_path)
map_file_path

def visualize_route(route, airport_data):
    # Extract coordinates from the route
    latitudes = [airport_data.iloc[i]['Latitude'] for i in route]
    longitudes = [airport_data.iloc[i]['Longitude'] for i in route]
    airport_names = [airport_data.iloc[i]['Airport'] for i in route]

    # Create the plot
    plt.figure(figsize=(10, 6))
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
    plt.show()

# Example usage:
visualize_route(best_route, selected_airports)