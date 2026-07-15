#!/usr/bin/env python3
"""
Pharmacokinetics (PK) One-Compartment Modeler
---------------------------------------------
This is a pure Python script demonstrating pharmacokinetic compartment modeling:
1. Simulating drug concentration over time for both IV Bolus and Oral Dosing.
2. Calculating key PK parameters: Half-life, Clearance, AUC, Cmax, and Tmax.
3. Exporting the simulated data to a standard CSV file.
4. Rendering a vertical ASCII concentration curve directly in the console.

Pharmacokinetics (PK) Background:
- PK describes what the body does to a drug (Absorption, Distribution, Metabolism, Excretion).
- 1-Compartment Model: Assumes the body acts as a single homogeneous chamber of volume (Vd).
- IV Bolus: The drug is injected instantly into the plasma. Concentration decays exponentially.
- Oral Dosing: The drug is absorbed from the gut at rate Ka, enters plasma, and is eliminated
  at rate Ke. Concentration rises to a peak (Cmax) at time (Tmax), then decays.
- Therapeutic Window: The concentration range between the Minimum Effective Concentration (MEC)
  and the Minimum Toxic Concentration (MTC).

No external dependencies are required. Run directly with:
    python pharmacokinetics_calculator.py
"""
import math
import csv

def simulate_iv_bolus(dose: float, vd: float, ke: float, times: list[float]) -> list[float]:
    """
    Simulates IV Bolus Concentration: C(t) = (Dose / Vd) * exp(-ke * t)
    """
    c0 = dose / vd
    concentrations = []
    for t in times:
        c = c0 * math.exp(-ke * t)
        concentrations.append(c)
    return concentrations


def simulate_oral_dose(dose: float, vd: float, ke: float, ka: float, f: float, times: list[float]) -> list[float]:
    """
    Simulates Oral Dosing (1st order absorption/elimination):
    C(t) = (F * Dose * Ka) / (Vd * (Ka - Ke)) * (exp(-ke * t) - exp(-ka * t))
    """
    # Bioavailable dose = F * Dose
    factor = (f * dose * ka) / (vd * (ka - ke))
    concentrations = []
    for t in times:
        # Avoid math domain errors at t=0 if ka == ke (handled by limiting ka/ke inputs)
        c = factor * (math.exp(-ke * t) - math.exp(-ka * t))
        concentrations.append(max(0.0, c))
    return concentrations


def calculate_pk_parameters(dose: float, vd: float, ke: float, ka: float = None, f: float = 1.0) -> dict:
    """
    Calculates primary pharmacokinetic metrics.
    """
    half_life = math.log(2) / ke
    auc = (f * dose) / (vd * ke)  # Area under the curve from 0 to infinity
    clearance = vd * ke           # Cl = Vd * Ke
    
    params = {
        "half_life_hr": half_life,
        "auc_mg_l_hr": auc,
        "clearance_l_hr": clearance
    }
    
    if ka is not None:
        # Calculate Tmax and Cmax for oral absorption
        # Tmax = ln(Ka/Ke) / (Ka - Ke)
        if ka != ke:
            tmax = math.log(ka / ke) / (ka - ke)
        else:
            tmax = 1.0 / ke # limit approximation
            
        factor = (f * dose * ka) / (vd * (ka - ke))
        cmax = factor * (math.exp(-ke * tmax) - math.exp(-ka * tmax))
        
        params["tmax_hr"] = tmax
        params["cmax_mg_l"] = cmax
    else:
        params["tmax_hr"] = 0.0
        params["cmax_mg_l"] = dose / vd
        
    return params


def draw_pk_ascii_plot(times: list[float], concentrations: list[float], mec: float, mtc: float):
    """
    Draws a vertical ASCII graph of drug concentration over time.
    Also flags the therapeutic window.
    """
    print("\n" + "=" * 75)
    print("      DRUG CONCENTRATION PROFILE & THERAPEUTIC WINDOW OVER TIME")
    print("=" * 75)
    print("  Time (h)  Conc (mg/L)   |------------------[THERAPEUTIC WINDOW]-------------------|")
    print("-" * 75)
    
    max_c = max(concentrations)
    width = 45
    
    for t, c in zip(times, concentrations):
        # Scale concentration to characters
        c_pos = int((c / max_c) * (width - 1)) if max_c > 0 else 0
        c_pos = max(0, min(width - 1, c_pos))
        
        # Determine status relative to therapeutic window
        status = "    "
        if c < mec:
            status = " SUB"  # Sub-therapeutic
        elif c > mtc:
            status = "TOXIC" # Toxic level
        else:
            status = " OK "  # Safe therapeutic range
            
        # Draw canvas line
        canvas = [" "] * width
        
        # Add visual boundaries for MEC and MTC on the plot
        mec_pos = int((mec / max_c) * (width - 1)) if max_c > 0 else 0
        mtc_pos = int((mtc / max_c) * (width - 1)) if max_c > 0 else 0
        
        if 0 <= mec_pos < width:
            canvas[mec_pos] = ":"
        if 0 <= mtc_pos < width:
            canvas[mtc_pos] = "!"
            
        # Plot the drug concentration dot
        canvas[c_pos] = "*"
        
        line_str = "".join(canvas)
        print(f"t={t:04.1f} hr   C={c:05.2f} mg/L    [{line_str}]   [{status}]")
        
    print("-" * 75)
    print("Legend:  * = Concentration   : = Min Effective Conc (MEC)   ! = Min Toxic Conc (MTC)")
    print("         [SUB] = Sub-therapeutic   [OK] = Therapeutic   [TOXIC] = Toxic")
    print("=" * 75)



def export_to_csv(filename: list, times: list, concentrations: list):
    """
    Writes simulated PK data to a CSV file.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (hours)", "Concentration (mg/L)"])
        for t, c in zip(times, concentrations):
            writer.writerow([f"{t:.2f}", f"{c:.4f}"])
    print(f"\n[INFO] Successfully exported PK time-concentration profile to: {filename}")


def run_pk_simulation():
    # 1. Input parameters
    dose = 500.0   # mg (e.g. Paracetamol)
    vd = 50.0      # Liters (Volume of distribution)
    ke = 0.15      # 1/hr (Elimination rate constant, corresponds to ~4.6h half-life)
    ka = 0.8       # 1/hr (Oral absorption rate constant, rapid absorption)
    f = 0.85       # Bioavailability (85% absorbed)
    
    # Therapeutic parameters
    mec = 3.0      # mg/L (Minimum Effective Concentration)
    mtc = 9.0      # mg/L (Minimum Toxic Concentration)
    
    # 2. Time points (0 to 24 hours in steps of 1 hour)
    times = [float(x) for x in range(25)]
    
    # 3. Simulate both IV Bolus and Oral routes
    print("--- Pharmacokinetics Single-Dose Simulation ---")
    print(f"Dose: {dose} mg | Vd: {vd} L | Bioavailability F: {f}")
    print(f"Elimination Ke: {ke}/hr | Absorption Ka: {ka}/hr")
    
    # Calculate PK parameters
    oral_params = calculate_pk_parameters(dose, vd, ke, ka, f)
    iv_params = calculate_pk_parameters(dose, vd, ke)
    
    print("\nPharmacokinetic Parameters calculated:")
    print(f"  Drug Half-Life:         {oral_params['half_life_hr']:.2f} hours")
    print(f"  Systemic Clearance:     {oral_params['clearance_l_hr']:.2f} L/hour")
    print(f"  Oral Peak Time (Tmax):  {oral_params['tmax_hr']:.2f} hours")
    print(f"  Oral Peak Conc (Cmax):  {oral_params['cmax_mg_l']:.2f} mg/L")
    print(f"  Oral Total AUC:         {oral_params['auc_mg_l_hr']:.2f} mg*hr/L")
    
    # 4. Simulate Oral profile and render ASCII plot
    oral_concentrations = simulate_oral_dose(dose, vd, ke, ka, f, times)
    draw_pk_ascii_plot(times, oral_concentrations, mec, mtc)
    
    # 5. Export results
    export_to_csv("pk_simulation.csv", times, oral_concentrations)


if __name__ == "__main__":
    run_pk_simulation()
