# Raw noisy heart rate data
raw_data = [72, 75, 90, 71, 73, 72, 85, 74, 73, 75]
window = 3

filtered_data = []
for i in range(len(raw_data)):
    # Slice the last 'window' items up to current index
    start = max(0, i - window + 1)
    sub_list = raw_data[start:i+1]
    average = sum(sub_list) / len(sub_list)
    filtered_data.append(round(average, 1))

print("Raw Signal:", raw_data)
print("Filtered Signal:", filtered_data)
