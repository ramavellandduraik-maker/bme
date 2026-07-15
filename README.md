# BME Basics: Pure Python Biomedical Engineering Tools

A collection of lightweight, educational, and interactive Python scripts demonstrating core concepts in **Biomedical Engineering (BME)**, cardiovascular physiology, digital signal processing, and pharmacokinetics. 

All scripts are written in **100% pure Python** (using only the standard library). They require **zero external dependencies** (no `numpy`, `scipy`, `matplotlib`, or `pip` packages required) and run instantly in any terminal environment.

---

## 📂 Project Structure

This repository contains the following modules:

1. **`blood_pressure_classifier.py`**: Cardiovascular Metrics
2. **`ecg_hrv_calculator.py`**: Electrocardiogram & Autonomic Heart Rate Variability
3. **`moving_average_filter.py`**: Causal Digital Signal Filtering & Smoothing
4. **`pharmacokinetics_calculator.py`**: Drug Compartment Dynamics & Toxicology

---

## 🛠️ Module Details & Formulas

### 1. Blood Pressure Classifier (`blood_pressure_classifier.py`)
Analyzes systolic and diastolic blood pressure readings to evaluate arterial parameters and clinical categories.
- **Mean Arterial Pressure (MAP)**: Estimates organ perfusion pressure.
  $$\text{MAP} \approx \text{Diastolic} + \frac{\text{Systolic} - \text{Diastolic}}{3}$$
- **Pulse Pressure (PP)**: Evaluates pulse-contour force and arterial stiffness.
  $$\text{PP} = \text{Systolic} - \text{Diastolic}$$
- **Classification**: Groups blood pressure (Normal, Elevated, Stage 1/2 Hypertension, Crisis) according to standard American Heart Association (AHA) guidelines.

### 2. ECG HRV Calculator (`ecg_hrv_calculator.py`)
Analyzes inter-beat intervals (RR/NN intervals) from ECG peak timestamps to quantify autonomic nervous system (ANS) tone.
- **Heart Rate**: Calculates average Beats Per Minute (BPM) from interval statistics.
- **SDNN**: Standard deviation of all normal-to-normal intervals (overall variability).
  $$\text{SDNN} = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N} (RR_i - \overline{RR})^2}$$
- **RMSSD**: Root mean square of successive differences (parasympathetic/vagal tone).
  $$\text{RMSSD} = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N-1} (RR_{i+1} - RR_i)^2}$$

### 3. Moving Average Filter (`moving_average_filter.py`)
Demonstrates digital signal processing (DSP) smoothing on a noisy skin-temperature sensor stream.
- **Moving Average Filter**: Reduces high-frequency sensor noise using a sliding window.
  $$y[n] = \frac{1}{M} \sum_{k=0}^{M-1} x[n-k]$$
- **ASCII Plot**: Overlays raw noisy signal (`r`) vs. filtered smooth signal (`█`) directly in the console output.

### 4. Pharmacokinetics Calculator (`pharmacokinetics_calculator.py`)
Models absorption, distribution, and elimination of therapeutics using a classic one-compartment open system.
- **Oral Dosing Equation**:
  $$C(t) = \frac{F \cdot \text{Dose} \cdot k_a}{V_d \cdot (k_a - k_e)} \left( e^{-k_e \cdot t} - e^{-k_a \cdot t} \right)$$
- **IV Bolus Equation**:
  $$C(t) = C_0 \cdot e^{-k_e \cdot t}$$
- **Calculated Parameters**: Peak time ($T_{max}$), Peak concentration ($C_{max}$), Clearance ($Cl = V_d \cdot k_e$), Half-life ($T_{1/2} = \ln(2)/k_e$), and total Area Under the Curve (AUC).
- **Visualization**: Generates a text-based ASCII plot representing concentration levels relative to the therapeutic window (Minimum Effective vs. Toxic levels) and exports results to `pk_simulation.csv`.

---

## 🚀 Getting Started

No installation setup or packages are needed. Simply clone this repository and run any script directly using your Python interpreter:

```bash
# Run Blood Pressure Classifier
python blood_pressure_classifier.py

# Run ECG HRV Calculator
python ecg_hrv_calculator.py

# Run Moving Average Filter
python moving_average_filter.py

# Run Pharmacokinetics Calculator
python pharmacokinetics_calculator.py
```

### System Requirements
- Python 3.8 or higher.
- Standard shell/terminal window.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
