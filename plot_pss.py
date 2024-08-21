import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.ndimage import gaussian_filter1d

def apply_gaussian_smoothing(data, sigma=1):
    return gaussian_filter1d(data, sigma=sigma)

def plot_memory_usage(grpc_log_file, ttrpc_log_file, output_file, sigma=1):
    # Read the log files into DataFrames
    df_grpc = pd.read_csv(grpc_log_file, names=['Timestamp', 'PSS'], parse_dates=['Timestamp'], date_parser=pd.to_datetime)
    df_ttrpc = pd.read_csv(ttrpc_log_file, names=['Timestamp', 'PSS'], parse_dates=['Timestamp'], date_parser=pd.to_datetime)

    # Convert PSS to numeric, coercing errors
    df_grpc['PSS'] = pd.to_numeric(df_grpc['PSS'], errors='coerce')
    df_ttrpc['PSS'] = pd.to_numeric(df_ttrpc['PSS'], errors='coerce')

    # Generate counts as x-axis values
    df_grpc['Count'] = range(len(df_grpc))
    df_ttrpc['Count'] = range(len(df_ttrpc))

    # Apply Gaussian smoothing
    df_grpc['PSS_smoothed'] = apply_gaussian_smoothing(df_grpc['PSS'].fillna(0), sigma)
    df_ttrpc['PSS_smoothed'] = apply_gaussian_smoothing(df_ttrpc['PSS'].fillna(0), sigma)

    # Plotting
    plt.figure(figsize=(12, 8))

    # Plot gRPC with smoothing
    plt.plot(df_grpc['Count'], df_grpc['PSS_smoothed'], label='gRPC PSS (Smoothed)', color='b', linestyle='-')

    # Plot ttrpc with smoothing
    plt.plot(df_ttrpc['Count'], df_ttrpc['PSS_smoothed'], label='ttrpc PSS (Smoothed)', color='r', linestyle='-')

    plt.title('Memory Usage Over Time for gRPC and ttrpc (Smoothed)')
    plt.xlabel('Count')
    plt.ylabel('PSS (KB)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python plot_memory_usage.py <grpc_log_file> <ttrpc_log_file> <output_file> <sigma>")
        sys.exit(1)

    grpc_log_file = sys.argv[1]
    ttrpc_log_file = sys.argv[2]
    output_file = sys.argv[3]
    sigma = float(sys.argv[4])
    
    plot_memory_usage(grpc_log_file, ttrpc_log_file, output_file, sigma)
