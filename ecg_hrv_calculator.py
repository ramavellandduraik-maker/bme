#!/usr/bin/env python3
import math
import random
import statistics

def calculate_rr_intervals(r_peaks_ms: list[float]) -> list[float]:
    if len(r_peaks_ms) < 2:
        raise ValueError("Need at least 2 R-peaks to calculate intervals.")
    
    rr_intervals = []
    for i in range(len(r_peaks_ms) - 1):
        interval = r_peaks_ms[i+1] - r_peaks_ms[i]
        rr_intervals.append(interval)
    return rr_intervals

def calculate_hrv_metrics(rr_intervals: list[float]) -> dict:
    if len(rr_intervals) < 2:
        raise ValueError("Need at least 2 RR intervals to calculate HRV metrics.")
    
    mean_rr = statistics.mean(rr_intervals)
    bpm = 60000.0 / mean_rr
    
    sdnn = statistics.stdev(rr_intervals)
    
    successive_diffs = []
    for i in range(len(rr_intervals) - 1):
        diff = rr_intervals[i+1] - rr_intervals[i]
        successive_diffs.append(diff)
        
    squared_diffs = [d ** 2 for d in successive_diffs]
    mean_squared_diff = statistics.mean(squared_diffs)
    rmssd = math.sqrt(mean_squared_diff)
    
    return {
        "mean_rr_ms": mean_rr,
        "bpm": bpm,
        "sdnn_ms": sdnn,
        "rmssd_ms": rmssd
    }

def generate_synthetic_peaks(num_beats: int = 50, avg_hr_bpm: float = 75.0, variability_ms: float = 40.0) -> list[float]:
    base_interval = (60.0 / avg_hr_bpm) * 1000.0
    peaks = [0.0]
    current_time = 0.0
    
    for i in range(num_beats - 1):
        breathing_cycle = math.sin(i / 5.0)
        interval = base_interval + (variability_ms * breathing_cycle) + (random.normalvariate(0, 10))
        interval = max(300.0, interval)
        current_time += interval
        peaks.append(current_time)
        
    return peaks

def run_hrv_analysis():
    print("=" * 60)
    print("          BME ECG FEATURE & HRV ANALYZER")
    print("=" * 60)
    
    print("\nGenerating simulated R-peak timestamps (resting state)...")
    peaks = generate_synthetic_peaks(num_beats=60, avg_hr_bpm=72.0, variability_ms=50.0)
    print(f"Generated {len(peaks)} R-peaks over {peaks[-1]/1000:.1f} seconds.")
    
    rr = calculate_rr_intervals(peaks)
    metrics = calculate_hrv_metrics(rr)
    
    print("\n--- Cardiovascular Dynamics Report ---")
    print(f"Mean RR Interval: {metrics['mean_rr_ms']:.1f} ms")
    print(f"Mean Heart Rate:  {metrics['bpm']:.1f} BPM")
    print(f"SDNN:             {metrics['sdnn_ms']:.1f} ms  (Resting reference: 30 - 100 ms)")
    print(f"RMSSD:            {metrics['rmssd_ms']:.1f} ms  (Resting reference: 20 - 75 ms)")
    
    print("\nPhysiological Interpretation:")
    if metrics['rmssd_ms'] < 20:
        print("[ANS Alert] Low RMSSD suggests dominance of Sympathetic active state (stress, fatigue).")
    elif metrics['rmssd_ms'] > 75:
        print("[ANS Info] High RMSSD suggests strong Parasympathetic activation (relaxed, high fitness).")
    else:
        print("[ANS Info] Normal balanced autonomic regulation of heart rate.")
        
    print("=" * 60)

if __name__ == "__main__":
    run_hrv_analysis()
