import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# Load CSV data into DataFrames
df = pd.read_csv('golang-bench/grpc-data-1257B.csv')  # Replace with actual file path
df2 = pd.read_csv('golang-bench/ttrpc-data-1257B.csv')  # Replace with actual file path
df3 = pd.read_csv('golang-bench/grpc-data-20162B.csv')  # Replace with actual file path
df4 = pd.read_csv('golang-bench/ttrpc-data-20162B.csv')  # Replace with actual file path
df5 = pd.read_csv('golang-bench/grpc-data-63000B.csv')  # Replace with actual file path
df6 = pd.read_csv('golang-bench/ttrpc-data-63000B.csv')  # Replace with actual file path
# Convert memory values from KiB to MiB
df['go_app_memory'] = df['go_app_memory'] / 1024
df2['go_app_memory'] = df2['go_app_memory'] / 1024
df3['go_app_memory'] = df3['go_app_memory'] / 1024
df4['go_app_memory'] = df4['go_app_memory'] / 1024
df5['go_app_memory'] = df5['go_app_memory'] / 1024
df6['go_app_memory'] = df6['go_app_memory'] / 1024
# Apply Gaussian blur to smooth the data
sigma = 20  # Adjust as needed

df['smoothed_memory'] = gaussian_filter1d(df['go_app_memory'], sigma=sigma)
df2['smoothed_memory'] = gaussian_filter1d(df2['go_app_memory'], sigma=sigma)
df3['smoothed_memory'] = gaussian_filter1d(df3['go_app_memory'], sigma=sigma)
df4['smoothed_memory'] = gaussian_filter1d(df4['go_app_memory'], sigma=sigma)
df5['smoothed_memory'] = gaussian_filter1d(df5['go_app_memory'], sigma=sigma)
df6['smoothed_memory'] = gaussian_filter1d(df6['go_app_memory'], sigma=sigma)

# Plotting
plt.figure(figsize=(12, 8))

# Plot the smoothed data for each dataset
plt.plot(df5['request_count'], df5['smoothed_memory'], linestyle='-', color='purple', label='gRPC - 4 MiB')
plt.plot(df6['request_count'], df6['smoothed_memory'], linestyle='-', color='black', label='ttRPC - 4 MiB')
plt.plot(df3['request_count'], df3['smoothed_memory'], linestyle='-', color='green', label='gRPC - 1 MiB')
plt.plot(df4['request_count'], df4['smoothed_memory'], linestyle='-', color='orange', label='ttRPC - 1 MiB')
plt.plot(df['request_count'], df['smoothed_memory'], linestyle='-', color='blue', label='gRPC - 64 KiB')
plt.plot(df2['request_count'], df2['smoothed_memory'], linestyle='-', color='red', label='ttRPC - 64 KiB')


plt.xlabel('Request Number')
plt.ylabel('Go App Memory')
plt.title('gRPC vs ttRPC Memory Usage in golang')
plt.grid(True)
plt.legend()
plt.show()

# Save the plot as a PNG file
plt.savefig('plot_golang.png')  # You can specify the path where you want to save the PNG file
plt.show()
