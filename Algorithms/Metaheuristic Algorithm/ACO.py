import random
import math

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
    return data

def ant_colony_optimization(data, num_ants=20, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.1, Q=100):
    # Extract data
    order_num = data["order_num"]
    vehicle_num = data["vehicle_num"]
    quantities = data["quantity"]
    costs = data["cost"]
    lower_bounds = data["lower_bounds"]
    upper_bounds = data["upper_bounds"]
    
    # Initialize pheromone matrix
    pheromone = [[1.0 for _ in range(vehicle_num)] for _ in range(order_num)]
    
    # Heuristic information: based on cost-to-quantity ratio
    heuristic = [[costs[i] / quantities[i] if quantities[i] <= upper_bounds[j] else 0 \
        for j in range(vehicle_num)] \
            for i in range(order_num)]
    
    # Best solution
    best_solution = None
    best_cost = -float("inf")
    
    # Main loop
    for iteration in range(num_iterations):
        solutions = []
        costs_of_solutions = []

        # Step 1: Each ant constructs a solution
        for ant in range(num_ants):
            # Assign orders to vehicles
            solution = [[] for _ in range(vehicle_num)]
            vehicle_loads = [0] * vehicle_num
            total_cost = 0
            
            for order in range(order_num):
                # Calculate probabilities for each vehicle
                probabilities = []
                for vehicle in range(vehicle_num):
                    if vehicle_loads[vehicle] + quantities[order] <= upper_bounds[vehicle]:
                        tau = pheromone[order][vehicle] ** alpha
                        eta = heuristic[order][vehicle] ** beta
                        probabilities.append(tau * eta)
                    else:
                        probabilities.append(0)  # Infeasible assignment
                
                # Normalize probabilities
                total_prob = sum(probabilities)
                if total_prob == 0:
                    probabilities = [1 / vehicle_num] * vehicle_num  # Randomize if no valid options
                else:
                    probabilities = [p / total_prob for p in probabilities]
                
                # Choose vehicle based on probabilities
                selected_vehicle = random.choices(range(vehicle_num), weights=probabilities)[0]
                
                # Assign order to the selected vehicle
                solution[selected_vehicle].append(order)
                vehicle_loads[selected_vehicle] += quantities[order]
                total_cost += costs[order]
            
            # Check feasibility of the solution
            is_feasible = all(lower_bounds[vehicle] <= vehicle_loads[vehicle] <= upper_bounds[vehicle] \
                for vehicle in range(vehicle_num))
            if is_feasible:
                solutions.append(solution)
                costs_of_solutions.append(total_cost)
        
        # Step 2: Update pheromones
        for i in range(order_num):
            for j in range(vehicle_num):
                pheromone[i][j] *= (1 - evaporation_rate)  # Evaporation
        
        for solution, solution_cost in zip(solutions, costs_of_solutions):
            for vehicle, orders in enumerate(solution):
                for order in orders:
                    pheromone[order][vehicle] += Q / solution_cost  # Deposit pheromone
        
        # Update best solution
        for solution, solution_cost in zip(solutions, costs_of_solutions):
            if solution_cost > best_cost:
                best_cost = solution_cost
                best_solution = solution
        
        # Print iteration status
        print(f"Iteration {iteration + 1}: Best Cost = {best_cost}")
    
    return best_solution, best_cost

# Input data
data = create_data_model()
order_num = data["order_num"]
vehicle_num = data["vehicle_num"]

# Run ACO
solution, cost = ant_colony_optimization(data)
orders_served = 0
for vehicle in solution:
    orders_served += len(vehicle)

# Output solution
print("Best Cost:", cost)
print("Orders served:", orders_served)
for vehicle_id, orders in enumerate(solution):
    for order in orders:
        print(order + 1, vehicle_id + 1)


