def classify_bp(sys, dia):
    if sys > 180 or dia > 120:
        return "Hypertensive Crisis"
    elif sys >= 140 or dia >= 90:
        return "Hypertension Stage 2"
    elif sys >= 130 or dia >= 80:
        return "Hypertension Stage 1"
    elif sys >= 120 and dia < 80:
        return "Elevated"
    else:
        return "Normal"

# Inputs
sys_val = 135
dia_val = 85

# Calculations
pulse_pressure = sys_val - dia_val
map_val = dia_val + (pulse_pressure / 3)

# Outputs
print("Systolic/Diastolic:", sys_val, "/", dia_val)
print("Classification:", classify_bp(sys_val, dia_val))
print("Pulse Pressure (mmHg):", pulse_pressure)
print("Mean Arterial Pressure (mmHg):", round(map_val, 2))
