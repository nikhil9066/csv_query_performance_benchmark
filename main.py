import os
import sqlite3
import pandas as pd
import time
import matplotlib.pyplot as plt

# Normalize CSV into multiple tables
def normalize_csv_and_create_schema(csv_file, db_name='salary_tracker_normalized.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)

    # Normalize tables
    person = df[['PersonID', 'PersonName', 'BirthDate']].drop_duplicates()
    employment = df[['PersonID', 'JobTitle', 'DepartmentName', 'Earnings', 'StillWorking']].drop_duplicates()
    school = df[['SchoolName', 'SchoolCampus', 'PersonID']].drop_duplicates()

    # Write to database
    person.to_sql('Person', conn, if_exists='replace', index=False)
    employment.to_sql('Employment', conn, if_exists='replace', index=False)
    school.to_sql('School', conn, if_exists='replace', index=False)

    print(f"Normalized {csv_file} and created schema in {db_name}")
    return conn

# Load CSV into SQLite
def load_csv_to_db(csv_file, db_name='salary_tracker.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)
    df.to_sql('salary_tracker', conn, if_exists='replace', index=False)
    print(f"Loaded {csv_file} into database {db_name}")
    return conn

# Execute a single query and measure the time taken
def execute_query(conn, query):
    start_time = time.time()
    result = conn.execute(query).fetchall()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, result

# Run all queries from a text file and record execution times
def run_queries(conn, query_file):
    with open(query_file, 'r') as file:
        queries = file.readlines()

    times = []
    for query in queries:
        query = query.strip()  # Remove any leading/trailing whitespace
        execution_time, result = execute_query(conn, query)
        times.append(execution_time)
        print(f"Query: {query}\nExecution Time: {execution_time:.4f} seconds\n")
    
    return times

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
    # Define dataset files relative to the script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets = [
        os.path.join(base_dir, 'datasets', 'salary_tracker_1MB.csv'),
        os.path.join(base_dir, 'datasets', 'salary_tracker_10MB.csv'),
        os.path.join(base_dir, 'datasets', 'salary_tracker_100MB.csv')
    ]
    file_sizes = [1, 10, 100]  # File sizes in MB

    query_file = os.path.join(base_dir, 'queries.txt')  # File with SQL queries
    all_times = [[] for _ in range(len(open(query_file).readlines()))]  # List to hold times for each query

    # Directory to save the plots
    image_dir = os.path.join(base_dir, 'images')

    # Loop through datasets, load them, run queries, and collect execution times
    for dataset in datasets:
        print(f"Processing {dataset}...")
        conn = load_csv_to_db(dataset)
        execution_times = run_queries(conn, query_file)
        
        # Collect execution times for each query
        for i, execution_time in enumerate(execution_times):
            all_times[i].append(execution_time)  # Append time for this dataset to the corresponding query
        
        conn.close()

    # Save the results plots for each query
    queries = open(query_file).readlines()  # Read queries again to use for titles
    save_query_performance_plots(file_sizes, all_times, image_dir, queries)
