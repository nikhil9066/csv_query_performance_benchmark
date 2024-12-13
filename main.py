# import os
# import sqlite3
# import pandas as pd
# import time
# import matplotlib.pyplot as plt

# # Define dataset files relative to the script's location
# base_dir = os.path.dirname(os.path.abspath(__file__))
# datasets = [
#     os.path.join(base_dir, 'datasets', 'salary_tracker_1MB.csv'),
#     os.path.join(base_dir, 'datasets', 'salary_tracker_10MB.csv'),
#     os.path.join(base_dir, 'datasets', 'salary_tracker_100MB.csv')
# ]

# # Define the query file
# query_file = os.path.join(base_dir, 'queries.txt')  # File with SQL queries

# # Load CSV into SQLite
# def load_csv_to_db(csv_file, db_name='salary_tracker.db'):
#     conn = sqlite3.connect(db_name)
#     df = pd.read_csv(csv_file)
#     df.to_sql('salary_tracker', conn, if_exists='replace', index=False)
#     print(f"Loaded {csv_file} into database {db_name}")
#     return conn

# # Execute a single query and measure the time taken
# def execute_query(conn, query):
#     try:
#         start_time = time.time()
#         result = conn.execute(query).fetchall()
#         end_time = time.time()
#         execution_time = end_time - start_time
#         return execution_time, result
#     except Exception as e:
#         print(f"Error executing query: {query}")
#         print(f"Error message: {e}")
#         return None, None

# # Run all queries from a text file and record execution times
# # Dictionary to store execution times before normalization
# before_norm = {}

# # Modify the run_queries function to record execution times in the dictionary
# def run_queries(conn, query_file):
#     with open(query_file, 'r') as file:
#         queries = file.readlines()

#     times = []
#     for query in queries:
#         query = query.strip()  # Remove any leading/trailing whitespace
#         execution_time, result = execute_query(conn, query)
#         times.append(execution_time)
#         print(f"Query: {query}\nExecution Time: {execution_time:.4f} seconds\n")
    
#     return times

# # Loop through datasets, load them, run queries, and collect execution times
# for dataset in datasets:
#     print(f"Processing {dataset}...")
#     conn = load_csv_to_db(dataset)
#     execution_times = run_queries(conn, query_file)
    
#     # Store the execution times for this dataset in the before_norm dictionary
#     before_norm[dataset] = execution_times
    
#     conn.close()

# # Output the before_norm dictionary for verification
# print("Execution times before normalization:", before_norm)


# # Plot individual query execution times against file sizes and save as images
# def save_query_performance_plots(file_sizes, all_times, save_dir, queries):
#     # Ensure the save directory exists
#     os.makedirs(save_dir, exist_ok=True)
    
#     # Plot each query's performance
#     for i, query_times in enumerate(all_times):
#         plt.figure()
#         plt.plot(file_sizes, query_times, marker='o', label='Execution Time')
#         plt.xlabel('File Size (MB)')
#         plt.ylabel('Execution Time (seconds)')
#         plt.title(f'Query {i + 1} Execution Time vs File Size')
#         plt.xticks(file_sizes)  # Ensure x-ticks match file sizes
#         plt.grid(True)
#         plt.legend()
        
#         # Save the plot to the specified file
#         image_path = os.path.join(save_dir, f'query_{i + 1}_performance.png')
#         plt.savefig(image_path)
#         plt.close()
        
#         print(f"Plot for Query {i + 1} saved to {image_path}")

# if __name__ == '__main__':

#     file_sizes = [1, 10, 100]  # File sizes in MB

#     all_times = [[] for _ in range(len(open(query_file).readlines()))]  # List to hold times for each query

#     # Directory to save the plots
#     image_dir = os.path.join(base_dir, 'images')

#     # Loop through datasets, load them, run queries, and collect execution times
#     for dataset in datasets:
#         print(f"Processing {dataset}...")
#         conn = load_csv_to_db(dataset)
#         execution_times = run_queries(conn, query_file)
        
#         # Collect execution times for each query
#         for i, execution_time in enumerate(execution_times):
#             all_times[i].append(execution_time)  # Append time for this dataset to the corresponding query
        
#         conn.close()

#     # Save the results plots for each query
#     queries = open(query_file).readlines()  # Read queries again to use for titles
#     save_query_performance_plots(file_sizes, all_times, image_dir, queries)

#     # Output the before_norm dictionary for verification
#     print("Execution times before normalization:", before_norm)


import os
import sqlite3
import pandas as pd
import time
import matplotlib.pyplot as plt

# Define dataset files relative to the script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
datasets = [
    os.path.join(base_dir, 'datasets', 'salary_tracker_1MB.csv'),
    os.path.join(base_dir, 'datasets', 'salary_tracker_10MB.csv'),
    os.path.join(base_dir, 'datasets', 'salary_tracker_100MB.csv')
]

# Define the query file
query_file = os.path.join(base_dir, 'queries.txt')  # File with SQL queries

# Load CSV into SQLite
def load_csv_to_db(csv_file, db_name='salary_tracker.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)
    df.to_sql('salary_tracker', conn, if_exists='replace', index=False)
    print(f"Loaded {csv_file} into database {db_name}")
    return conn

# Execute a single query and measure the time taken
def execute_query(conn, query):
    try:
        start_time = time.time()
        result = conn.execute(query).fetchall()
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time, result
    except Exception as e:
        print(f"Error executing query: {query}")
        print(f"Error message: {e}")
        return None, None

# Run all queries from a text file and record execution times
# Dictionary to store execution times before normalization
preNorm = {}

# Modify the run_queries function to record execution times in the dictionary
def run_queries(conn, query_file):
    with open(query_file, 'r') as file:
        queries = file.readlines()

    query_times = {}
    for idx, query in enumerate(queries):
        query = query.strip()  # Remove any leading/trailing whitespace
        execution_time, result = execute_query(conn, query)
        if execution_time is not None:
            query_times[f'Query_{idx + 1}'] = f'Executed in {execution_time:.6f} seconds'
        else:
            query_times[f'Query_{idx + 1}'] = 'Error executing query'

    return query_times

# Loop through datasets, load them, run queries, and collect execution times
execution_summary = {}

for dataset in datasets:
    print(f"Processing {dataset}...")
    conn = load_csv_to_db(dataset)
    execution_times = run_queries(conn, query_file)
    
    # Store the execution times for this dataset in the preNorm dictionary
    preNorm[dataset] = execution_times
    
    conn.close()

# Output the preNorm dictionary for verification
print("Execution times:", preNorm)

# Plot individual query execution times against file sizes and save as images
def save_query_performance_plots(file_sizes, all_times, save_dir, queries):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Plot each query's performance
    for i, query_times in enumerate(all_times):
        plt.figure()
        plt.plot(file_sizes, query_times, marker='o', label='Execution Time')
        plt.xlabel('File Size (MB)')
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'Query {i + 1} Execution Time vs File Size')
        plt.xticks(file_sizes)  # Ensure x-ticks match file sizes
        plt.grid(True)
        plt.legend()
        
        # Save the plot to the specified file
        image_path = os.path.join(save_dir, f'query_{i + 1}_performance.png')
        plt.savefig(image_path)
        plt.close()
        
        print(f"Plot for Query {i + 1} saved to {image_path}")

if __name__ == '__main__':

    file_sizes = [1, 10, 100]  # File sizes in MB

    all_times = [[] for _ in range(len(open(query_file).readlines()))]  # List to hold times for each query

    # Directory to save the plots
    image_dir = os.path.join(base_dir, 'images')

    # Loop through datasets, load them, run queries, and collect execution times
    for dataset in datasets:
        print(f"Processing {dataset}...")
        conn = load_csv_to_db(dataset)
        execution_times = run_queries(conn, query_file)
        
        # Collect execution times for each query
        for i, execution_time in enumerate(execution_times.values()):
            all_times[i].append(float(execution_time.split()[2]))  # Extract execution time value
        
        conn.close()

    # Save the results plots for each query
    queries = open(query_file).readlines()  # Read queries again to use for titles
    save_query_performance_plots(file_sizes, all_times, image_dir, queries)

    # Output the preNorm dictionary for verification
    print("Execution times:", preNorm)
