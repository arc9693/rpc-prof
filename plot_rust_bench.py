import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# Load CSV data into a DataFrame
df = pd.read_csv('rust-bench/grpc-data-65536B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df2 = pd.read_csv('rust-bench/ttrpc-data-65536B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df3 = pd.read_csv('rust-bench/grpc-data-1048576B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df4 = pd.read_csv('rust-bench/ttrpc-data-1048576B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df5 = pd.read_csv('rust-bench/grpc-data-4194204B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df6 = pd.read_csv('rust-bench/ttrpc-data-4194204B.csv')  # Replace 'dataB.csv' with the path to your CSV file
# Convert memory values from KiB to MiB
df['memory_rss'] = df['memory_rss'] / (1024*1024)
df2['memory_rss'] = df2['memory_rss'] / (1024*1024)
df3['memory_rss'] = df3['memory_rss'] / (1024*1024)
df4['memory_rss'] = df4['memory_rss'] / (1024*1024)
df5['memory_rss'] = df5['memory_rss'] / (1024*1024)
df6['memory_rss'] = df6['memory_rss'] / (1024*1024)
# Apply Gaussian blur to smooth the data
sigma = 20  # Adjust as needed

df['smoothed_memory'] = gaussian_filter1d(df['memory_rss'], sigma=sigma)
df2['smoothed_memory'] = gaussian_filter1d(df2['memory_rss'], sigma=sigma)
df3['smoothed_memory'] = gaussian_filter1d(df3['memory_rss'], sigma=sigma)
df4['smoothed_memory'] = gaussian_filter1d(df4['memory_rss'], sigma=sigma)
df5['smoothed_memory'] = gaussian_filter1d(df5['memory_rss'], sigma=sigma)
df6['smoothed_memory'] = gaussian_filter1d(df6['memory_rss'], sigma=sigma)

# Plotting
plt.figure(figsize=(12, 8))

# Plot the smoothed data for each dataset
plt.plot(df5['request_number'], df5['smoothed_memory'], linestyle='-', color='purple', label='gRPC - 4 MiB')
plt.plot(df6['request_number'], df6['smoothed_memory'], linestyle='-', color='black', label='ttRPC - 4 MiB')
plt.plot(df3['request_number'], df3['smoothed_memory'], linestyle='-', color='green', label='gRPC - 1 MiB')
plt.plot(df4['request_number'], df4['smoothed_memory'], linestyle='-', color='orange', label='ttRPC - 1 MiB')
plt.plot(df['request_number'], df['smoothed_memory'], linestyle='-', color='blue', label='gRPC - 64 KiB')
plt.plot(df2['request_number'], df2['smoothed_memory'], linestyle='-', color='red', label='ttRPC - 64 KiB')


plt.xlabel('Request Number')
plt.ylabel('Memory_RSS (MiB)')
plt.title('gRPC vs ttRPC Memory Usage in rust')
plt.grid(True)
plt.legend()
plt.show()

# Save the plot as a PNG file
plt.savefig('plot_rust.png')  # You can specify the path where you want to save the PNG file
plt.show()
