import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time

def create_data_model():
    data = {}
    data["order_num"], data["vehicle_num"] = map(int, input().split())
    data["quantity"] = []
    data["cost"] = []
    data["lower_bounds"] = []
    data["upper_bounds"] = []
    for i in range(data["order_num"]):
        quantity, cost = map(int, input().split())
        data["quantity"].append(quantity)
        data["cost"].append(cost)
    for i in range(data["vehicle_num"]):
        lower_capacity, upper_capacity = map(int, input().split())
        data["lower_bounds"].append(lower_capacity)
        data["upper_bounds"].append(upper_capacity)

    # Check data validity
    assert sum(data["upper_bounds"]) >= sum(data["quantity"]), "Total vehicle capacity is insufficient!"
    assert all(any(data["quantity"][i] <= ub for ub in data["upper_bounds"]) for i in range(data["order_num"])), "Some orders cannot fit in any vehicle!"
    return data

def ant_colony_optimization(data, num_ants=100, num_iterations=50, alpha=1, beta=2, evaporation_rate=0.4, Q=200, p_greedy=0.5):
    # Extract data
    order_num = data["order_num"]
    vehicle_num = data["vehicle_num"]
    quantities = data["quantity"]
    costs = data["cost"]
    lower_bounds = data["lower_bounds"]
    upper_bounds = data["upper_bounds"]

    # Initialize pheromone matrix
    pheromone = [[1.0 for _ in range(vehicle_num)] for _ in range(order_num)]

    # Best solution
    best_solution = None
    best_cost = -float("inf")

    # Main loop
    for iteration in range(num_iterations):
        solutions = []
        costs_of_solutions = []

        # Step 1: Each ant constructs a solution
        for ant in range(num_ants):
            solution = [[] for _ in range(vehicle_num)]
            vehicle_loads = [0] * vehicle_num
            total_cost = 0

            for order in range(order_num):
                # Calculate heuristic
                heuristic = []
                for vehicle in range(vehicle_num):
                    remaining_capacity = upper_bounds[vehicle] - vehicle_loads[vehicle]
                    if quantities[order] <= remaining_capacity:
                        heuristic_value = (costs[order] / quantities[order]) * remaining_capacity
                    else:
                        heuristic_value = 0
                    heuristic.append(heuristic_value)
                    
                # Calculate probabilities for each vehicle
                probabilities = []
                for vehicle in range(vehicle_num):
                    if vehicle_loads[vehicle] + quantities[order] <= upper_bounds[vehicle]:
                        tau = pheromone[order][vehicle] ** alpha
                        eta = heuristic[vehicle] ** beta
                        probabilities.append(tau * eta)
                    else:
                        probabilities.append(0)

                # Normalize probabilities
                total_prob = sum(probabilities)
                if total_prob == 0:
                    continue
                probabilities = [p / total_prob for p in probabilities]

                # Choose vehicle
                if random.random() < p_greedy:
                    selected_vehicle = probabilities.index(max(probabilities))
                else:
                    selected_vehicle = random.choices(range(vehicle_num), weights=probabilities)[0]

                # Assign order to the selected vehicle
                solution[selected_vehicle].append(order)
                vehicle_loads[selected_vehicle] += quantities[order]
                total_cost += costs[order]

            # Check feasibility
            is_feasible = all(lower_bounds[vehicle] <= vehicle_loads[vehicle] <= upper_bounds[vehicle] \
                for vehicle in range(vehicle_num))
            if is_feasible:
                solutions.append(solution)
                costs_of_solutions.append(total_cost)

        # Handle no feasible solution
        if not solutions:
            continue

        # Step 2: Update pheromones
        for i in range(order_num):
            for j in range(vehicle_num):
                pheromone[i][j] *= (1 - evaporation_rate)

        for solution, solution_cost in zip(solutions, costs_of_solutions):
            for vehicle, orders in enumerate(solution):
                for order in orders:
                    pheromone[order][vehicle] += Q / solution_cost

        # Update best solution
        for solution, solution_cost in zip(solutions, costs_of_solutions):
            if solution_cost > best_cost:
                best_cost = solution_cost
                best_solution = solution

    return best_solution, best_cost


# Input data
data = create_data_model()

# Run ACO
# start_time = time.time()
solution, best_cost = ant_colony_optimization(data)
# end_time = time.time()

# Count served orders
served_orders = sum(len(vehicle) for vehicle in solution)

# Output results
print(served_orders)
for vehicle_id, orders in enumerate(solution):
    for order in orders:
        print(order + 1, vehicle_id + 1)
# print(best_cost)
