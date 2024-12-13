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
total_cost = 0

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
                total_cost += order["cost"]
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

print(total_cost)
