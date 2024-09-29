import pandas as pd
import matplotlib.pyplot as plt

# Constants for decoding
BIT_PERIOD = 0.10416666667  # approximately 104 ms per bit 
THRESHOLD = 0.25     # Voltage threshold to differentiate between high and low
START_BIT = 0       # Expected start bit value (LOW)
STOP_BIT = 1        # Expected stop bit value (HIGH)

# Load the waveform data, skipping the first few metadata rows
file_path = r"C:\Users\LENOVO\Desktop\Assignment_1_UART.CSV"
waveform_data = pd.read_csv(file_path, header=None, skiprows=2)


time = pd.to_numeric(waveform_data[3], errors='coerce').dropna()  
voltage = pd.to_numeric(waveform_data[4], errors='coerce').dropna()  

# Ensure the time and voltage arrays are the same length
min_length = min(len(time), len(voltage))
time = time[:min_length]
voltage = voltage[:min_length]

# Plot the waveform for visual inspection with increased size and black color
plt.figure(figsize=(34,17))  # Set the figure size (width, height)
plt.plot(time, voltage, color='black')  # Change the color to black

# Set title, labels with increased font size and bold
plt.title('UART Waveform', fontsize=75, fontweight='bold')  # Title
plt.xlabel('Time (s)', fontsize=50, fontweight='bold')  # X-axis label
plt.ylabel('Voltage (V)', fontsize=50, fontweight='bold')  # Y-axis label

# Set the font size and bold for tick values using 'fontweight'
plt.xticks(fontsize=25, fontweight='bold')  # X-axis tick values
plt.yticks(fontsize=25, fontweight='bold')  # Y-axis tick values

plt.grid()  # Optional: Add a grid for better visibility
plt.show()

# Function to decode a byte from waveform data
def decode_byte(data, bit_time, sampling_rate):
    # Find the start bit (falling edge)
    decoded_bytes = []
    i = 0
    while i < len(data):
        if data[i] < THRESHOLD:  # Start bit detected (LOW)
            byte = 0
            for bit in range(8):
                sample_point = i + int(bit_time * sampling_rate * (bit + 2))
                
                # Corrected condition for checking threshold
                if sample_point < len(data) and data[sample_point] > THRESHOLD:
                    byte |= (1 << bit)  # Set the bit if voltage is HIGH
            decoded_bytes.append(byte)
            i += int(bit_time * sampling_rate * 10)  # Move to next byte (10-bit time)
        else:
            i += 1
    return decoded_bytes

# Assuming a sampling rate (adjust based on your oscilloscope's settings)
sampling_rate = 1 / (time[10] - time[9])

# Decode the waveform
decoded_bytes = decode_byte(voltage, BIT_PERIOD, sampling_rate)

# Print the decoded bytes
print("Decoded BYTE Stream is:", [hex(b) for b in decoded_bytes])
