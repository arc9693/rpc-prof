import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data into a DataFrame
df = pd.read_csv('rust-bench/grpc-data-65536B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df2 = pd.read_csv('rust-bench/ttrpc-data-65536B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df3 = pd.read_csv('rust-bench/grpc-data-1048576B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df4 = pd.read_csv('rust-bench/ttrpc-data-1048576B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df5 = pd.read_csv('rust-bench/grpc-data-4194204B.csv')  # Replace 'dataB.csv' with the path to your CSV file
df6 = pd.read_csv('rust-bench/ttrpc-data-4194204B.csv')  # Replace 'dataB.csv' with the path to your CSV file
# Plotting
# Plot the first memory RSS column with a solid line
plt.plot(df['request_number'], df['memory_rss'], linestyle='-', color='blue', label='gRPC - 64 KiB')
plt.plot(df3['request_number'], df3['memory_rss'], linestyle='-', color='grey', label='gRPC - 1 MiB')
plt.plot(df5['request_number'], df5['memory_rss'], linestyle='-', color='yellow', label='gRPC - 4 MiB')

# Plot the second memory RSS column with a solid line
plt.plot(df['request_number'], df2['memory_rss'], linestyle='-', color='red', label='ttRPC - 64 KiB')
plt.plot(df4['request_number'], df4['memory_rss'], linestyle='-', color='green', label='ttRPC - 1 MiB')
plt.plot(df6['request_number'], df6['memory_rss'], linestyle='-', color='black', label='ttRPC - 4 MiB')

plt.xlabel('Request Number')
plt.ylabel('Memory RSS')
plt.title('Memory RSS vs Request Number')
plt.grid(True)
plt.legend()

# Save the plot as a PNG file
plt.savefig('plot_rust.png')  # You can specify the path where you want to save the PNG file
plt.show()
