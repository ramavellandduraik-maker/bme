#!/usr/bin/env python3
import math
import random

def moving_average_filter(signal: list[float], window_size: int) -> list[float]:
    if window_size < 1:
        raise ValueError("Window size must be at least 1.")
        
    filtered_signal = []
    for i in range(len(signal)):
        start_idx = max(0, i - window_size + 1)
        window = signal[start_idx:i + 1]
        avg = sum(window) / len(window)
        filtered_signal.append(avg)
        
    return filtered_signal

def generate_noisy_temperature_data(length: int = 40) -> list[float]:
    data = []
    random.seed(42)
    
    for i in range(length):
        base_temp = 36.8
        variation = 0.4 * math.sin(i / 6.0)
        hf_noise = random.normalvariate(0, 0.08)
        temp = base_temp + variation + hf_noise
        
        if i in [15, 28]:
            temp += 0.9
        elif i in [8, 33]:
            temp -= 0.7
            
        data.append(temp)
    return data

def draw_ascii_chart(raw: list[float], filtered: list[float]):
    print("\n" + "=" * 70)
    print("      ASCII PLOT: RAW SIGNAL (R) VS. FILTERED SIGNAL (F) OVER TIME")
    print("=" * 70)
    print("  Time   Temp (C)    [35.5 C] ------------------------------ [38.5 C]")
    print("-" * 70)
    
    min_plot_val = 35.5
    max_plot_val = 38.5
    width = 40
    
    for i, (r_val, f_val) in enumerate(zip(raw, filtered)):
        r_pos = int((r_val - min_plot_val) / (max_plot_val - min_plot_val) * width)
        f_pos = int((f_val - min_plot_val) / (max_plot_val - min_plot_val) * width)
        
        r_pos = max(0, min(width - 1, r_pos))
        f_pos = max(0, min(width - 1, f_pos))
        
        line_chars = [" "] * width
        norm_pos = int((36.8 - min_plot_val) / (max_plot_val - min_plot_val) * width)
        if 0 <= norm_pos < width:
            line_chars[norm_pos] = "|"
            
        if r_pos == f_pos:
            line_chars[r_pos] = "X"
        else:
            line_chars[r_pos] = "r"
            line_chars[f_pos] = "#"
            
        line_str = "".join(line_chars)
        print(f"t={i:02d}    {r_val:.2f} C      [{line_str}]  (Filtered: {f_val:.2f} C)")
        
    print("-" * 70)
    print("Legend:  'r' = Raw Noisy Data   '#' = Filtered Smooth Data   'X' = Overlap")
    print("=" * 70)

def run_filter_demo():
    raw_signal = generate_noisy_temperature_data(45)
    window_sz = 5
    filtered_signal = moving_average_filter(raw_signal, window_size=window_sz)
    
    print("Biomedical Signal Processing Demo")
    print(f"Algorithm: Causal Moving Average Filter (Window Size: {window_sz})")
    print(f"Target: Noise Reduction in Body Temperature Sensor data.")
    
    draw_ascii_chart(raw_signal, filtered_signal)
    
    raw_var = sum((x - sum(raw_signal)/len(raw_signal))**2 for x in raw_signal) / len(raw_signal)
    filt_var = sum((x - sum(filtered_signal)/len(filtered_signal))**2 for x in filtered_signal) / len(filtered_signal)
    print(f"\nSignal Statistics:")
    print(f"Raw Signal Variance:       {raw_var:.5f}")
    print(f"Filtered Signal Variance:  {filt_var:.5f}")
    print(f"Noise reduction factor:    {raw_var / filt_var:.1f}x")

if __name__ == "__main__":
    run_filter_demo()
