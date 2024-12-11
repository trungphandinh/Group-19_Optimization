# # Create Vehicle class and Order class
# class Order:
#     tag = 1

#     def __init__(self, quantity, cost):
#         self.quantity = quantity
#         self.cost = cost
#         self.index = Order.tag
#         Order.tag += 1
#         self.available = True

#     def __str__(self):
#         return f"Order {self.index} has quantity {self.quantity} and cost {self.cost}"


# class Vehicle:
#     tag = 1

#     def __init__(self, lower_capacity, upper_capacity):
#         self.lower_capacity = lower_capacity
#         self.upper_capacity = upper_capacity
#         self.current_capacity = 0
#         self.served_order = []
#         self.order_cost = 0
#         self.index = Vehicle.tag
#         Vehicle.tag += 1
#         self.available = True
        
#     def __str__(self):
#         return f"The truck has lower capacity: {self.lower_capacity} and upper capacity: {self.upper_capacity}"


# # Get the data
# num_of_orders, num_of_vehicles = tuple(map(int, input().split()))
# orders = []
# vehicles = []

# for i in range(num_of_orders):
#     quantity, cost = tuple(map(int, input().split()))
#     orders.append(Order(quantity, cost))
# for i in range(num_of_vehicles):
#     lower_capacity, upper_capacity = tuple(map(int, input().split()))
#     vehicles.append(Vehicle(lower_capacity, upper_capacity))

# # Sort the vehicles in non-increasing order based on upper capacity
# vehicles.sort(key=lambda x: 0.8*x.upper_capacity - x.lower_capacity, reverse=False)
# # Sort the orders in non-increasing order based on quantity
# orders.sort(key=lambda x: float(x.cost / x.quantity + x.quantity / 10), reverse=True)

# # Set up the necessary variables
# num_of_served_order = 0
# final_served = 0
# total_cost = 0

# # Feasible function
# def feasible(order, vehicle):
#     x = vehicle.current_capacity + order.quantity
#     first_condition = x <= vehicle.upper_capacity
#     if first_condition:
#         if num_of_orders - num_of_served_order > 0:
#             temp = 1e9
#             for z in orders:
#                 if z!=order and z.quantity < temp and z.available == True:
#                     temp = z.quantity
#             if x + temp > vehicle.upper_capacity:
#                 if x < vehicle.lower_capacity:
#                     return False
#                 else:
#                     vehicle.available = False
#                     return True
#             else:
#                 return True
#         else:
#             if x < vehicle.lower_capacity:
#                 return False
#             else:
#                 vehicle.available = False
#                 return True
#     return False

# for j in range(num_of_vehicles):
#     for i in range(num_of_orders):
#         if orders[i].available == True:
#             if feasible(orders[i], vehicles[j]):
#                 vehicles[j].served_order.append(orders[i])
#                 vehicles[j].order_cost += orders[i].cost
#                 orders[i].available = False
#                 num_of_served_order += 1
#                 vehicles[j].current_capacity += orders[i].quantity

# for v in vehicles: 
#     if v.lower_capacity <= v.current_capacity <= v.upper_capacity:
#         final_served += len(v.served_order)
# print(final_served)
# for v in vehicles:
#     if v.lower_capacity <= v.current_capacity <= v.upper_capacity:
#         for o in v.served_order:
#             print(o.index, end = ' ')
#             print(v.index)

# Nhập và khởi tạo dữ liệu
num_orders, num_vehicles = tuple(map(int, input().split()))
orders = []
vehicles = []

for order_id in range(1, num_orders + 1):
    quantity, cost = tuple(map(int, input().split()))
    orders.append({
        "order_id": order_id,
        "quantity": quantity,
        "cost": cost,
        "is_available": True
    })

for vehicle_id in range(1, num_vehicles + 1):
    min_capacity, max_capacity = tuple(map(int, input().split()))
    vehicles.append({
        "vehicle_id": vehicle_id,
        "min_capacity": min_capacity,
        "max_capacity": max_capacity,
        "current_capacity": 0,
        "assigned_orders": [],
        "total_cost": 0,
        "is_active": True
    })

vehicles.sort(key=lambda x: x["max_capacity"] - x["min_capacity"], reverse=False)
orders.sort(key=lambda x: 0.9 * x["cost"] / x["quantity"] + x["quantity"] / 10, reverse=True)

total_served_orders = 0
final_served_count = 0

def is_feasible(order, vehicle):
    updated_capacity = vehicle["current_capacity"] + order["quantity"]
    within_capacity = updated_capacity <= vehicle["max_capacity"]
    if within_capacity:
        if num_orders - total_served_orders > 0:
            smallest_quantity = float("inf")
            for other_order in orders:
                if other_order != order and other_order["quantity"] < smallest_quantity and other_order["is_available"]:
                    smallest_quantity = other_order["quantity"]
            if updated_capacity + smallest_quantity > vehicle["max_capacity"]:
                if updated_capacity < vehicle["min_capacity"]:
                    return False
                else:
                    vehicle["is_active"] = False
                    return True
            else:
                return True
        else:
            if updated_capacity < vehicle["min_capacity"]:
                return False
            else:
                vehicle["is_active"] = False
                return True
    return False

for vehicle in vehicles:
    for order in orders:
        if order["is_available"]:
            if is_feasible(order, vehicle):
                vehicle["assigned_orders"].append(order["order_id"])
                vehicle["total_cost"] += order["cost"]
                order["is_available"] = False
                total_served_orders += 1
                vehicle["current_capacity"] += order["quantity"]

final_served_count = 0
for vehicle in vehicles:
    if vehicle["min_capacity"] <= vehicle["current_capacity"] <= vehicle["max_capacity"]:
        final_served_count += len(vehicle["assigned_orders"])

print(final_served_count)
for vehicle in vehicles:
    if vehicle["min_capacity"] <= vehicle["current_capacity"] <= vehicle["max_capacity"]:
        for order_id in vehicle["assigned_orders"]:
            print(order_id, vehicle["vehicle_id"])
