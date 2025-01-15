num_of_orders, num_of_vehicles = tuple(map(int, input().split()))
orders = []
vehicles = []

for i in range(num_of_orders):
    weight, profit = tuple(map(int, input().split()))
    orders.append({"weight": weight, "profit": profit, "index": i + 1, "available": True})
for i in range(num_of_vehicles):
    lower, upper = tuple(map(int, input().split()))
    vehicles.append({"lower": lower, "upper": upper, "current": 0, "served": [], "v_profit": 0, "index": i + 1, "available": True})

# Sort the vehicles in increasing order based on upper capacity
vehicles.sort(key=lambda x: x['upper'])
# Sort the orders in non-increasing order based on profit
orders.sort(key=lambda x: x['profit'], reverse=True)

# Set up the necessary variables
num_of_served_order = 0
unsatistied_vehicle = []
satisfied_vehicle = []

# Kiểm tra xem có thêm order vào vehicle được không, và kiểm tra xem thêm liệu trước
# khi thêm order vào vehicle thì vehicle đã thỏa mãn chưa hay là không?
def feasible(order, vehicle, num_of_orders, num_of_served_order, orders):
    x = vehicle['current'] + order['weight']
    if x <= vehicle['upper']:
        if num_of_orders - num_of_served_order > 0:
            temp = 1e9
            for z in orders:
                if z != order and z['weight'] < temp and z['available']:
                    temp = z['weight']
            if x + temp > vehicle['upper']:
                if x < vehicle['lower']:
                    return False
                else:
                    vehicle['available'] = False
                    return True
            else:
                return True
        else:
            if x < vehicle['lower']:
                return False
            else:
                vehicle['available'] = False
                return True
    return False

# Main program
# Lần gán thứ nhất
for j in range(num_of_vehicles):
    for i in range(num_of_orders):
        if orders[i]['available']:
            if feasible(orders[i], vehicles[j], num_of_orders, num_of_served_order, orders):
                vehicles[j]['served'].append(orders[i])
                vehicles[j]['v_profit'] += orders[i]['profit']
                orders[i]['available'] = False
                num_of_served_order += 1
                vehicles[j]['current'] += orders[i]['weight']

# Sau khi xong lần gán thứ 1, chia thành 2 loại: vehicle đáp ứng capacity và không
for v in vehicles:
    if v['lower'] <= v['current'] <= v['upper']:
        satisfied_vehicle.append(v)
    else:
        unsatistied_vehicle.append(v)

# cố gắng gán nốt những order chưa có vehicle assign cho những vehicle chưa đủ điều kiện
for v in unsatistied_vehicle:
    for i in orders:
        if i['available']:
            v['served'].append(i)
            i['available'] = False
            v['current'] += i['weight']
            v['v_profit'] += i['profit']

# Lần chỉnh sửa thứ 2: Di chuyển đơn hàng từ một vehicle đang thỏa mãn sang vehicle đang không thỏa mãn
# và cố gắng làm cho cả 2 đơn hàng này thỏa mãn
def move(v1, v2):
    if v1['current'] < v1['lower'] or v2['current'] >= v2['upper']:
        return False
    for i in v1['served'][:]:
        m = i['weight']
        if v1['current'] - m >= v1['lower'] and v2['current'] + m <= v2['upper']:
            # Perform Moving Operation
            v1['served'].remove(i)
            v2['served'].append(i)
            # Update Information
            v1['current'] -= m
            v2['current'] += m
            v1['v_profit'] -= i['profit']
            v2['v_profit'] += i['profit']
            return True
    return False

# Lần chỉnh sửa thứ 3: lần này: đổi chỗ order i1 của vehicle j1 
# cho order j2 của vehicle j2 nếu như sau khi đổi mà hai vehicle vẫn
# thỏa mãn ràng buộc
def swap(v1, v2):
    m = min(v1['current'] - v1['lower'], v2['upper'] - v2['current'])
    if m == 0:
        return False
    for i in v2['served']:
        for j in v1['served']:
            if 0 < j['weight'] - i['weight'] <= m:
                v2['served'].append(j)
                v1['served'].append(i)
                v2['served'].remove(i)
                v1['served'].remove(j)
                v1['current'] = v1['current'] - j['weight'] + i['weight']
                v2['current'] = v2['current'] + j['weight'] - i['weight']
                v1['v_profit'] = v1['v_profit'] - j['profit'] + i['profit']
                v2['v_profit'] = v2['v_profit'] + j['profit'] - i['profit']
                return True
    return False

for v2 in unsatistied_vehicle[:]:
    for v1 in satisfied_vehicle:
        while move(v1, v2):
            continue
        if v2['lower'] <= v2['current']:
            break
    if v2['lower'] <= v2['current']:
        unsatistied_vehicle.remove(v2)
        satisfied_vehicle.append(v2)
        continue

for v2 in unsatistied_vehicle[:]:
    for v1 in satisfied_vehicle:
        while swap(v1, v2):
            continue
    if v2['lower'] <= v2['current']:
        unsatistied_vehicle.remove(v2)
        satisfied_vehicle.append(v2)
        continue

# Print the results
final_served = 0
total_cost = 0
for v in vehicles:
    if v['lower'] <= v['current'] <= v['upper']:
        final_served += len(v['served'])
        total_cost += v['v_profit']
print(final_served)
for v in vehicles:
    if v['lower'] <= v['current'] <= v['upper']:
        for o in v['served']:
            print(o['index'], end=' ')
            print(v['index'])
# print(f"Max cost: {total_cost}")
# # Tính tỷ lệ đơn hàng phục vụ
# service_rate = (final_served / num_of_orders) * 100

# # In kết quả tỷ lệ phục vụ
# print(f"Service rate: {service_rate:.2f}%")

