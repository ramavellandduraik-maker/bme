#!/usr/bin/env python3
"""
Biomedical Sensor Noise Filter (Moving Average)
-----------------------------------------------
This is a pure Python script demonstrating digital signal processing (DSP):
1. Generating a simulated noisy biosensor stream (body temperature in Celsius).
2. Implementing a causal Moving Average Filter from scratch.
3. Visualizing raw vs. filtered data in the terminal using a custom ASCII chart.

Physiological Background:
- Biomedical signals are often contaminated by electrical interference, movement artifacts,
  and thermal noise.
- A Moving Average Filter is a low-pass filter that smooths data by averaging adjacent points
  within a sliding window. It is commonly used for baseline wander removal or noise reduction
  in slow-changing signals (like body temperature or galvanic skin response).

No external dependencies are required. Run directly with:
    python moving_average_filter.py
"""
import math
import random

def moving_average_filter(signal: list[float], window_size: int) -> list[float]:
    """
    Applies a moving average filter with a specified window size.
    This is a causal implementation (averages previous 'window_size' points).
    """
    if window_size < 1:
        raise ValueError("Window size must be at least 1.")
        
    filtered_signal = []
    for i in range(len(signal)):
        # Determine the boundaries of the sliding window
        start_idx = max(0, i - window_size + 1)
        window = signal[start_idx:i + 1]
        
        # Calculate mean of current window
        avg = sum(window) / len(window)
        filtered_signal.append(avg)
        
    return filtered_signal


def generate_noisy_temperature_data(length: int = 40) -> list[float]:
    """
    Generates a mock skin temperature signal:
    - Baseline temperature: 37.0 degrees Celsius.
    - Slow circadian cycle variation: sinus modulation.
    - High-frequency random noise (muscle/electrical noise).
    - Random outlier spikes (sensor loose contact).
    """
    data = []
    random.seed(42)  # For reproducible results
    
    for i in range(length):
        # 1. Base physiological temperature
        base_temp = 36.8
        
        # 2. Slow physiological variation (0.2°C amplitude)
        variation = 0.4 * math.sin(i / 6.0)
        
        # 3. High-frequency random noise
        hf_noise = random.normalvariate(0, 0.08)
        
        # Combine
        temp = base_temp + variation + hf_noise
        
        # 4. Add an occasional extreme artifact/spike (e.g. sensor wiggle)
        if i in [15, 28]:
            temp += 0.9  # Positive spike
        elif i in [8, 33]:
            temp -= 0.7  # Negative spike
            
        data.append(temp)
    return data


def draw_ascii_chart(raw: list[float], filtered: list[float]):
    """
    Renders a text-based ASCII plot in the console showing the raw signal (R)
    and the filtered smoothed signal (F) overlaid.
    """
    print("\n" + "=" * 70)
    print("      ASCII PLOT: RAW SIGNAL (R) VS. FILTERED SIGNAL (F) OVER TIME")
    print("=" * 70)
    print("  Time   Temp (C)    [35.5 C] ------------------------------ [38.5 C]")
    print("-" * 70)
    
    # Range of plot mapping
    min_plot_val = 35.5
    max_plot_val = 38.5
    width = 40  # Character width of the plotting canvas
    
    for i, (r_val, f_val) in enumerate(zip(raw, filtered)):
        # Map values to character positions (0 to width-1)
        r_pos = int((r_val - min_plot_val) / (max_plot_val - min_plot_val) * width)
        f_pos = int((f_val - min_plot_val) / (max_plot_val - min_plot_val) * width)
        
        # Clamp bounds
        r_pos = max(0, min(width - 1, r_pos))
        f_pos = max(0, min(width - 1, f_pos))
        
        # Construct line representation
        line_chars = [" "] * width
        
        # Add baseline marker at 36.8°C (middle region)
        norm_pos = int((36.8 - min_plot_val) / (max_plot_val - min_plot_val) * width)
        if 0 <= norm_pos < width:
            line_chars[norm_pos] = "|"
            
        if r_pos == f_pos:
            line_chars[r_pos] = "X"  # Overlap marker
        else:
            line_chars[r_pos] = "r"  # Raw noise point
            line_chars[f_pos] = "#"  # Filtered smooth point (ASCII hash)
            
        line_str = "".join(line_chars)
        print(f"t={i:02d}    {r_val:.2f} C      [{line_str}]  (Filtered: {f_val:.2f} C)")
        
    print("-" * 70)
    print("Legend:  'r' = Raw Noisy Data   '#' = Filtered Smooth Data   'X' = Overlap")
    print("=" * 70)


def run_filter_demo():
    # 1. Generate noisy baseline data
    raw_signal = generate_noisy_temperature_data(45)
    
    # 2. Filter using different window sizes
    window_sz = 5
    filtered_signal = moving_average_filter(raw_signal, window_size=window_sz)
    
    # 3. Output comparison values
    print("Biomedical Signal Processing Demo")
    print(f"Algorithm: Causal Moving Average Filter (Window Size: {window_sz})")
    print(f"Target: Noise Reduction in Body Temperature Sensor data.")
    
    # 4. Draw ASCII graph
    draw_ascii_chart(raw_signal, filtered_signal)
    
    # 5. Summary metrics
    raw_var = sum((x - sum(raw_signal)/len(raw_signal))**2 for x in raw_signal) / len(raw_signal)
    filt_var = sum((x - sum(filtered_signal)/len(filtered_signal))**2 for x in filtered_signal) / len(filtered_signal)
    print(f"\nSignal Statistics:")
    print(f"Raw Signal Variance:       {raw_var:.5f} (High variance due to noise/spikes)")
    print(f"Filtered Signal Variance:  {filt_var:.5f} (Reduced variance -> smoother signal)")
    print(f"Noise reduction factor:    {raw_var / filt_var:.1f}x")


if __name__ == "__main__":
    run_filter_demo()
