import time

# # Đo thời gian bắt đầu
# start_time = time.time()

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
    return bin['lower_bound'] <= bin_total <= bin['upper_bound']

# Gán đơn hàng cho phương tiện
for bin in bins:
    for order in orders:
        if order['open'] and feasible(order, bin):
            bin['items'].append(order['order_id'])
            order['bin'] = bin['bin_id']  # Gán phương tiện cho đơn hàng
            order['open'] = False
            bin['weight'] += order['weight']
            bin['cost'] += order['cost']
            served += 1

# Đếm số lượng đơn hàng được phục vụ
m = 0
output = []
for order in orders:
    if not order['open']:  # Nếu đơn hàng đã được gán
        m += 1
        output.append((order['order_id'], order['bin']))

# # Đo thời gian kết thúc
# end_time = time.time()
# execution_time = end_time - start_time

# In kết quả đúng chuẩn đề bài
print(m)
for order_id, bin_id in output:
    print(order_id, bin_id)
