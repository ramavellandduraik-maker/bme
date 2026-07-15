#!/usr/bin/env python3
import math
import csv

def simulate_iv_bolus(dose: float, vd: float, ke: float, times: list[float]) -> list[float]:
    c0 = dose / vd
    concentrations = []
    for t in times:
        c = c0 * math.exp(-ke * t)
        concentrations.append(c)
    return concentrations

def simulate_oral_dose(dose: float, vd: float, ke: float, ka: float, f: float, times: list[float]) -> list[float]:
    factor = (f * dose * ka) / (vd * (ka - ke))
    concentrations = []
    for t in times:
        c = factor * (math.exp(-ke * t) - math.exp(-ka * t))
        concentrations.append(max(0.0, c))
    return concentrations

def calculate_pk_parameters(dose: float, vd: float, ke: float, ka: float = None, f: float = 1.0) -> dict:
    half_life = math.log(2) / ke
    auc = (f * dose) / (vd * ke)
    clearance = vd * ke
    
    params = {
        "half_life_hr": half_life,
        "auc_mg_l_hr": auc,
        "clearance_l_hr": clearance
    }
    
    if ka is not None:
        if ka != ke:
            tmax = math.log(ka / ke) / (ka - ke)
        else:
            tmax = 1.0 / ke
            
        factor = (f * dose * ka) / (vd * (ka - ke))
        cmax = factor * (math.exp(-ke * tmax) - math.exp(-ka * tmax))
        
        params["tmax_hr"] = tmax
        params["cmax_mg_l"] = cmax
    else:
        params["tmax_hr"] = 0.0
        params["cmax_mg_l"] = dose / vd
        
    return params

def draw_pk_ascii_plot(times: list[float], concentrations: list[float], mec: float, mtc: float):
    print("\n" + "=" * 75)
    print("      DRUG CONCENTRATION PROFILE & THERAPEUTIC WINDOW OVER TIME")
    print("=" * 75)
    print("  Time (h)  Conc (mg/L)   |------------------[THERAPEUTIC WINDOW]-------------------|")
    print("-" * 75)
    
    max_c = max(concentrations)
    width = 45
    
    for t, c in zip(times, concentrations):
        c_pos = int((c / max_c) * (width - 1)) if max_c > 0 else 0
        c_pos = max(0, min(width - 1, c_pos))
        
        status = "    "
        if c < mec:
            status = " SUB"
        elif c > mtc:
            status = "TOXIC"
        else:
            status = " OK "
            
        canvas = [" "] * width
        
        mec_pos = int((mec / max_c) * (width - 1)) if max_c > 0 else 0
        mtc_pos = int((mtc / max_c) * (width - 1)) if max_c > 0 else 0
        
        if 0 <= mec_pos < width:
            canvas[mec_pos] = ":"
        if 0 <= mtc_pos < width:
            canvas[mtc_pos] = "!"
            
        canvas[c_pos] = "*"
        
        line_str = "".join(canvas)
        print(f"t={t:04.1f} hr   C={c:05.2f} mg/L    [{line_str}]   [{status}]")
        
    print("-" * 75)
    print("Legend:  * = Concentration   : = Min Effective Conc (MEC)   ! = Min Toxic Conc (MTC)")
    print("         [SUB] = Sub-therapeutic   [OK] = Therapeutic   [TOXIC] = Toxic")
    print("=" * 75)

def export_to_csv(filename: str, times: list, concentrations: list):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (hours)", "Concentration (mg/L)"])
        for t, c in zip(times, concentrations):
            writer.writerow([f"{t:.2f}", f"{c:.4f}"])
    print(f"\n[INFO] Successfully exported PK time-concentration profile to: {filename}")

def run_pk_simulation():
    dose = 500.0
    vd = 50.0
    ke = 0.15
    ka = 0.8
    f = 0.85
    mec = 3.0
    mtc = 9.0
    times = [float(x) for x in range(25)]
    
    print("--- Pharmacokinetics Single-Dose Simulation ---")
    print(f"Dose: {dose} mg | Vd: {vd} L | Bioavailability F: {f}")
    print(f"Elimination Ke: {ke}/hr | Absorption Ka: {ka}/hr")
    
    oral_params = calculate_pk_parameters(dose, vd, ke, ka, f)
    
    print("\nPharmacokinetic Parameters calculated:")
    print(f"  Drug Half-Life:         {oral_params['half_life_hr']:.2f} hours")
    print(f"  Systemic Clearance:     {oral_params['clearance_l_hr']:.2f} L/hour")
    print(f"  Oral Peak Time (Tmax):  {oral_params['tmax_hr']:.2f} hours")
    print(f"  Oral Peak Conc (Cmax):  {oral_params['cmax_mg_l']:.2f} mg/L")
    print(f"  Oral Total AUC:         {oral_params['auc_mg_l_hr']:.2f} mg*hr/L")
    
    oral_concentrations = simulate_oral_dose(dose, vd, ke, ka, f, times)
    draw_pk_ascii_plot(times, oral_concentrations, mec, mtc)
    
    export_to_csv("pk_simulation.csv", times, oral_concentrations)

if __name__ == "__main__":
    run_pk_simulation()
