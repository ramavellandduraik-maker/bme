import math

# R-peak times in milliseconds
peaks = [0, 800, 1610, 2400, 3220, 4010, 4820]

# Calculate RR intervals
rr_intervals = []
for i in range(len(peaks) - 1):
    rr_intervals.append(peaks[i+1] - peaks[i])

# Calculate Heart Rate (BPM)
avg_rr = sum(rr_intervals) / len(rr_intervals)
bpm = 60000 / avg_rr

# Calculate SDNN (Standard Deviation)
sdnn_sum = sum((x - avg_rr) ** 2 for x in rr_intervals)
sdnn = math.sqrt(sdnn_sum / (len(rr_intervals) - 1))

# Calculate RMSSD
diffs = []
for i in range(len(rr_intervals) - 1):
    diffs.append(rr_intervals[i+1] - rr_intervals[i])
rmssd_sum = sum(d ** 2 for d in diffs)
rmssd = math.sqrt(rmssd_sum / len(diffs))

# Print Results
print("RR Intervals (ms):", rr_intervals)
print("Heart Rate (BPM):", round(bpm, 1))
print("SDNN (ms):", round(sdnn, 1))
print("RMSSD (ms):", round(rmssd, 1))
