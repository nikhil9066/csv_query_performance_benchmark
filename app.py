import subprocess
import sys
import json
import matplotlib.pyplot as plt
import os

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"Output from {script_name}:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}:")
        print(e.stderr)
        sys.exit(1)

# Function to load pre and post normalization data from JSON files
def load_normalization_data():
    with open('preNormalisation.json', 'r') as pre_file:
        pre_data = json.load(pre_file)
    with open('postNormalisation.json', 'r') as post_file:
        post_data = json.load(post_file)

    # Normalize the keys to be relative paths
    pre_data = {key.replace('/Users/nikhilprao/Documents/csv_query_performance_benchmark/', ''): value for key, value in pre_data.items()}
    post_data = {key.replace('/Users/nikhilprao/Documents/csv_query_performance_benchmark/', ''): value for key, value in post_data.items()}

    return pre_data, post_data

def plot_comparison(pre_data, post_data):
    datasets = ['datasets/salary_tracker_1MB.csv', 'datasets/salary_tracker_10MB.csv', 'datasets/salary_tracker_100MB.csv']
    queries = ['Query_1', 'Query_2', 'Query_3', 'Query_4', 'Query_5', 'Query_6']

    # Ensure the directory exists
    output_dir = 'comparision'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for query in queries:
        pre_times = [pre_data[dataset].get(query, 0) for dataset in datasets]
        post_times = [post_data[dataset].get(query, 0) for dataset in datasets]

        # Plotting comparison using line chart
        plt.figure(figsize=(10, 6))
        plt.plot(datasets, pre_times, label='Pre-Normalization', color='red', marker='o', linestyle='--', linewidth=2, markersize=8)
        plt.plot(datasets, post_times, label='Post-Normalization', color='blue', marker='o', linestyle='-', linewidth=2, markersize=8)

        plt.xlabel('Datasets')
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.title(f'Comparison of {query} Execution Times (Pre vs Post Normalization)', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        # Save the plot in the 'comparision' directory
        image_path = os.path.join(output_dir, f'{query}_execution_time.png')
        plt.savefig(image_path)
        plt.close()

    print(f"Comparison plots saved in '{output_dir}' directory.")



def plot_combined_comparison(pre_data, post_data):
    datasets = ['datasets/salary_tracker_1MB.csv', 'datasets/salary_tracker_10MB.csv', 'datasets/salary_tracker_100MB.csv']
    queries = ['Query_1', 'Query_2', 'Query_3', 'Query_4', 'Query_5', 'Query_6']

    # Ensure the directory exists
    output_dir = 'comparison'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(14, 8))

    # Define distinct colors for each query
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

    for idx, query in enumerate(queries):
        pre_times = [float(pre_data[dataset][query].split()[2]) for dataset in datasets]
        post_times = [post_data[dataset].get(query, 0) for dataset in datasets]

        # Plot pre-normalization with a dotted line
        plt.plot(datasets, pre_times, label=f'{query} (Pre-Normalization) [Dotted line]', color=colors[idx], marker='o', linestyle=(0, (3, 5, 1, 5)), linewidth=2.5, markersize=10)
        # Plot post-normalization with a solid line
        plt.plot(datasets, post_times, label=f'{query} (Post-Normalization)', color=colors[idx], marker='o', linestyle='-', linewidth=2.5, markersize=10)

    plt.xlabel('Datasets', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Comparison of All Query Execution Times (Pre vs Post Normalization)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1), frameon=True, shadow=True, borderpad=1.2)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Adjust layout to fit legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Save the combined plot
    image_path = os.path.join(output_dir, 'combined_comparison.png')
    plt.savefig(image_path)
    plt.close()
    # plt.show()

    print(f"Combined comparison plot saved in '{output_dir}/combined_comparison.png'.")

def main():
    # Run the scripts first
    scripts = ["main.py", "norm.py"]
    for script in scripts:
        run_script(script)

    # Load the pre and post normalization data
    pre_data, post_data = load_normalization_data()

    # Plot comparison graphs
    plot_comparison(pre_data, post_data)
    plot_combined_comparison(pre_data, post_data)


if __name__ == "__main__":
    main()
