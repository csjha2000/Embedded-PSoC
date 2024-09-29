import pandas as pd
import matplotlib.pyplot as plt

# Some basic settings
bit_time = 0.104  # bit period in seconds
volt_limit = 0.25  # threshold for voltage
start_val = 0  # start bit should be LOW
stop_val = 1   # stop bit should be HIGH

# Reading CSV file
data_path = r"C:\Users\LENOVO\Desktop\Assignment_1_UART.CSV"
data = pd.read_csv(data_path, header=None, skiprows=2)

# Get time and voltage columns
time_vals = pd.to_numeric(data[3], errors='coerce').dropna()
volt_vals = pd.to_numeric(data[4], errors='coerce').dropna()

# Ensure same size for time and voltage
shortest_len = min(len(time_vals), len(volt_vals))
time_vals = time_vals[:shortest_len]
volt_vals = volt_vals[:shortest_len]

# Plot waveform
plt.figure(figsize=(30,15))
plt.plot(time_vals, volt_vals, color='k')

# Labeling and font adjustments
plt.title('Waveform', fontsize=50, fontweight='bold')
plt.xlabel('Time (s)', fontsize=30, fontweight='bold')
plt.ylabel('Volt (V)', fontsize=30, fontweight='bold')

# Ticks size and grid
plt.xticks(fontsize=15, fontweight='bold')
plt.yticks(fontsize=15, fontweight='bold')
plt.grid()
plt.show()

# Decoding function
def byte_decoder(signal, bit_duration, sample_rate):
    result_bytes = []
    idx = 0
    while idx < len(signal):
        if signal[idx] < volt_limit:  # start bit found
            temp_byte = 0
            for bit in range(8):
                sample_idx = idx + int(bit_duration * sample_rate * (bit + 2))
                if sample_idx < len(signal) and signal[sample_idx] > volt_limit:
                    temp_byte |= (1 << bit)
            result_bytes.append(temp_byte)
            idx += int(bit_duration * sample_rate * 10)  # next byte
        else:
            idx += 1
    return result_bytes

# Guessing the sample rate based on time
sample_rate = 1 / (time_vals[10] - time_vals[9])

# Decode the data
decoded_stream = byte_decoder(volt_vals, bit_time, sample_rate)

# Output the decoded bytes
print("Decoded Stream: ", [hex(x) for x in decoded_stream])
