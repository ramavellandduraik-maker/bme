#!/usr/bin/env python3
import sys

def calculate_map(systolic: float, diastolic: float) -> float:
    pulse_pressure = systolic - diastolic
    return diastolic + (pulse_pressure / 3.0)

def calculate_pulse_pressure(systolic: float, diastolic: float) -> float:
    return systolic - diastolic

def classify_blood_pressure(systolic: float, diastolic: float) -> str:
    if systolic > 180 or diastolic > 120:
        return "Hypertensive Crisis (Emergency)"
    elif systolic >= 140 or diastolic >= 90:
        return "Hypertension Stage 2"
    elif (130 <= systolic < 140) or (80 <= diastolic < 90):
        return "Hypertension Stage 1"
    elif (120 <= systolic < 130) and diastolic < 80:
        return "Elevated"
    elif systolic < 120 and diastolic < 80:
        return "Normal"
    else:
        return "Stage 1 Hypertension (Borderline)"

def print_report(systolic: float, diastolic: float):
    classification = classify_blood_pressure(systolic, diastolic)
    map_val = calculate_map(systolic, diastolic)
    pulse_p = calculate_pulse_pressure(systolic, diastolic)
    
    print("-" * 50)
    print(f"BLOOD PRESSURE REPORT: {systolic:.0f}/{diastolic:.0f} mmHg")
    print("-" * 50)
    print(f"Classification:  {classification}")
    print(f"Pulse Pressure:  {pulse_p:.1f} mmHg (Normal range: 30 - 40 mmHg)")
    print(f"Mean Arterial:   {map_val:.1f} mmHg (Normal range: 70 - 100 mmHg)")
    
    if "Crisis" in classification:
        print("\n[WARNING] Critical reading. Seek medical attention immediately.")
    elif "Stage 2" in classification:
        print("\n[NOTE] Hypertension Stage 2 requires medical review and lifestyle/medication changes.")
    elif "Stage 1" in classification:
        print("\n[NOTE] Hypertension Stage 1 should be monitored and discussed with a physician.")
    elif "Elevated" in classification:
        print("\n[NOTE] Elevated blood pressure. Lifestyle modifications can help reduce it.")
    else:
        print("\n[INFO] Cardiovascular metrics are within normal ranges.")
    print("-" * 50)

def run_examples():
    cases = [
        (115, 75),
        (124, 78),
        (135, 82),
        (145, 95),
        (185, 125)
    ]
    for sys, dia in cases:
        print_report(sys, dia)
        print()

def interactive_mode():
    print("\n--- Cardiovascular Metrics Calculator ---")
    while True:
        try:
            sys_input = input("\nEnter Systolic pressure (mmHg) [or 'q' to quit]: ").strip()
            if sys_input.lower() == 'q':
                break
            dia_input = input("Enter Diastolic pressure (mmHg): ").strip()
            
            sys = float(sys_input)
            dia = float(dia_input)
            
            if sys <= dia or sys <= 0 or dia <= 0:
                print("Error: Systolic must be greater than Diastolic, and both must be positive.")
                continue
                
            print_report(sys, dia)
        except ValueError:
            print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            sys_val = float(sys.argv[1])
            dia_val = float(sys.argv[2])
            print_report(sys_val, dia_val)
        except ValueError:
            print("Error: Please supply numeric values. Usage: python blood_pressure_classifier.py [systolic] [diastolic]")
    else:
        run_examples()
        interactive_mode()
