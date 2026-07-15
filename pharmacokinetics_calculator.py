import math

dose = 500  # mg
vd = 50     # Liters
ke = 0.15   # elimination rate per hour
c0 = dose / vd

print("Time (h) | Drug Concentration (mg/L)")
print("-" * 35)

# Simulate IV bolus decay over 12 hours
for hour in range(13):
    concentration = c0 * math.exp(-ke * hour)
    print(f"{hour:8d} | {concentration:.2f}")

half_life = 0.693 / ke
print("-" * 35)
print("Half-life:", round(half_life, 2), "hours")
