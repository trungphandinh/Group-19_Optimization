from ortools.linear_solver import pywraplp

def create_data_model():
    """Lưu trữ dữ liệu cho bài toán"""
    data = {}
    
    # Đọc số lượng đơn hàng và xe
    num_orders, num_vehicles = tuple(map(int, input().split()))
    data['num_orders'] = num_orders
    data['num_vehicles'] = num_vehicles
    
    # Đọc thông tin đơn hàng
    orders_quantity = []
    orders_cost = []
    for _ in range(num_orders):
        quantity, cost = tuple(map(int, input().split()))
        orders_quantity.append(quantity)
        orders_cost.append(cost)
    data['orders_quantity'] = orders_quantity
    data['orders_cost'] = orders_cost
    
    # Đọc thông tin xe
    vehicles_lower_cap = []
    vehicles_upper_cap = []
    for _ in range(num_vehicles):
        lower_cap, upper_cap = tuple(map(int, input().split()))
        vehicles_lower_cap.append(lower_cap)
        vehicles_upper_cap.append(upper_cap)
    data['vehicles_lower_cap'] = vehicles_lower_cap
    data['vehicles_upper_cap'] = vehicles_upper_cap
    
    return data

def main():
    # Tạo data model
    data = create_data_model()
    
    # Tạo solver
    solver = pywraplp.Solver.CreateSolver("SCIP")
    
    # Tạo biến x[i,j]
    x = {}
    for i in range(data['num_orders']):
        for j in range(data['num_vehicles']):
            x[(i, j)] = solver.IntVar(0, 1, f'x_{i}_{j}')
    
    # Ràng buộc 1: Mỗi đơn hàng được phục vụ bởi tối đa 1 xe
    for i in range(data['num_orders']):
        solver.Add(sum(x[(i, j)] for j in range(data['num_vehicles'])) <= 1)
    
    # Ràng buộc 2: Tổng số lượng đơn hàng trên mỗi xe phải nằm trong khoảng cho phép
    for j in range(data['num_vehicles']):
        # Ràng buộc lower capacity
        solver.Add(sum(x[(i, j)] * data['orders_quantity'][i] \
            for i in range(data['num_orders'])) >= data['vehicles_lower_cap'][j])
        
        # Ràng buộc upper capacity
        solver.Add(sum(x[(i, j)] * data['orders_quantity'][i] \
            for i in range(data['num_orders'])) <= data['vehicles_upper_cap'][j])
    
    # Hàm mục tiêu: Tối đa hóa tổng cost
    objective = solver.Sum(x[(i, j)] * data['orders_cost'][i] \
        for i in range(data['num_orders']) for j in range(data['num_vehicles']))
    solver.Maximize(objective)
    
    # Giải bài toán
    status = solver.Solve()
    
    # In kết quả
    if status == pywraplp.Solver.OPTIMAL:
        # Đếm số đơn hàng được phục vụ
        served_orders = 0
        for i in range(data['num_orders']):
            for j in range(data['num_vehicles']):
                if x[(i, j)].solution_value() > 0:
                    served_orders += 1
        
        # In số đơn hàng được phục vụ
        print(served_orders)
        
        # In chi tiết phân bổ
        for i in range(data['num_orders']):
            for j in range(data['num_vehicles']):
                if x[(i, j)].solution_value() > 0:
                    print(f"{i + 1} {j + 1}")
    else:
        print("The problem does not have an optimal solution")

if __name__ == "__main__":
    main()