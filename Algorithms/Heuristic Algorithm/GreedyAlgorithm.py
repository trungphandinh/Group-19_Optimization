import time

# Đo thời gian bắt đầu
start_time = time.time()

# Đọc dữ liệu đầu vào
n, k = map(int, input().split())
bins = []
orders = []

for order_id in range(1, n + 1):
    d, c = map(int, input().split())
    orders.append({
        "order_id": order_id,
        "bin": 0,
        "open": True,
        "weight": d,
        "cost": c,
    })

for bin_id in range(1, k + 1):
    c1, c2 = map(int, input().split())
    bins.append({
        "bin_id": bin_id,
        "lower_bound": c1,
        "upper_bound": c2,
        "weight": 0,
        "cost": 0,
        "items": []
    })

# Sắp xếp phương tiện theo khoảng tải trọng tăng dần
bins.sort(key=lambda x: x["upper_bound"] - x["lower_bound"], reverse=False)

# Sắp xếp đơn hàng theo chi phí giảm dần
orders.sort(key=lambda x: x['cost'], reverse=True)
served = 0

# Hàm kiểm tra tính khả thi khi gán đơn hàng vào phương tiện
def feasible(order, bin) -> bool:
    bin_total = bin['weight'] + order['weight']
    in_bounds = bin_total <= bin['upper_bound']
    if in_bounds:
        if n - served > 0:
            min_weight = 0
            for other_order in orders:
                if other_order != order and other_order['weight'] < min_weight and other_order['open']:
                    min_weight = other_order['weight']
            if bin_total + min_weight > bin['upper_bound']:
                if bin_total < bin['lower_bound']:
                    return False
                else:
                    bin['open'] = False
                    return True
            else:
                return True
        else:
            if bin_total < bin['lower_bound']:
                return False
            else:
                bin['open'] = False
                return True
    return False

# Gán đơn hàng cho phương tiện
for bin in bins:
    for order in orders:
        if order['open']:
            if feasible(order, bin):
                bin['items'].append(order['order_id'])
                order['open'] = False
                bin['weight'] += order['weight']
                bin['cost'] += order['cost']
                served += 1

# Tính số đơn hàng được phục vụ
final_served_count = 0
total_cost = 0  # Tổng chi phí tối ưu (best cost)
valid_bin = 0
total_fill_rate = 0  # Tỷ lệ lấp đầy trung bình
for bin in bins:
    if bin['lower_bound'] <= bin['weight'] <= bin['upper_bound']:
        valid_bin += 1
        final_served_count += len(bin['items'])
        total_cost += bin['cost']  # Cộng chi phí của các phương tiện hợp lệ
        fill_rate = (bin['weight'] / bin['upper_bound']) * 100
        total_fill_rate += fill_rate  # Cộng tỷ lệ lấp đầy của từng xe

# Tính tỷ lệ lấp đầy trung bình
average_fill_rate = total_fill_rate / valid_bin if valid_bin > 0 else 0

# Đo thời gian kết thúc
end_time = time.time()
execution_time = end_time - start_time

# In kết quả
print(f"Total Orders Served: {final_served_count}")
print(f"Best Cost (Optimal Value): {total_cost}")
print(f"Average Fill Rate: {average_fill_rate:.2f}%")
print(f"Execution Time: {execution_time:.4f} seconds")

# In thông tin chi tiết từng phương tiện
for bin in bins:
    if bin['lower_bound'] <= bin['weight'] <= bin['upper_bound']:
        fill_rate = (bin['weight'] / bin['upper_bound']) * 100  # Tỷ lệ lấp đầy (dạng phần trăm)
        print(f"Bin {bin['bin_id']}:")
        print(f"  Total Weight: {bin['weight']}/{bin['upper_bound']} ({fill_rate:.2f}% filled)")
        # print(f"  Cost: {bin['cost']}")
        # print(f"  Items: {bin['items']}")
