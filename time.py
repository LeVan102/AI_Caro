import time

# Lấy thời gian bắt đầu
start_time = time.time()

# Đoạn mã bạn muốn đếm thời gian
# Ví dụ: tính tổng các số từ 1 đến 1000000
total = 0
for i in range(1, 1000001):
    total += i

# Lấy thời gian kết thúc
end_time = time.time()

# Tính thời gian đã trôi qua
elapsed_time = end_time - start_time
print(elapsed_time)
