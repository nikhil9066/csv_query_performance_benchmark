import os
import sqlite3
import pandas as pd
import time
import matplotlib.pyplot as plt

# Before Normalization: Single table schema
def load_csv_to_db_before_normalization(csv_file, db_name='salary_tracker_before_normalization.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)
    df.to_sql('salary_tracker', conn, if_exists='replace', index=False)
    print(f"Loaded {csv_file} into database {db_name} with single table schema")
    return conn

# Normalize CSV into multiple tables and create schema
def normalize_csv_and_create_schema(csv_file, db_name='salary_tracker_normalized.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)

    # Normalize tables
    person = df[['PersonID', 'PersonName', 'BirthDate']].drop_duplicates()
    school = df[['SchoolID', 'SchoolName', 'SchoolCampus']].drop_duplicates()
    employment = df[['PersonID', 'JobID', 'JobTitle', 'DepartmentName', 'Earnings', 'EarningsYear', 'StillWorking']].drop_duplicates()

    # Write to database
    person.to_sql('Person', conn, if_exists='replace', index=False)
    school.to_sql('School', conn, if_exists='replace', index=False)
    employment.to_sql('Employment', conn, if_exists='replace', index=False)

    print(f"Normalized {csv_file} and created schema in {db_name}")
    return conn

# Execute a single query and measure the time taken
def execute_query(conn, query):
    start_time = time.time()
    result = conn.execute(query).fetchall()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, result

# Run all queries from a list and record execution times
def run_queries(conn, queries):
    execution_times = []
    
    for query in queries:
        start_time = time.time()
        
        # Execute query based on the normalized schema
        result = conn.execute(query).fetchall()
        
        execution_time = time.time() - start_time
        execution_times.append(execution_time)
        
        # Optionally, you can print the results of the query
        print(f"Query: {query}")
        print(f"Execution Time: {execution_time:.4f} seconds")
        print(f"Results: {result}")
        
    return execution_times

#  def run_queries(conn, queries):
#     times = []
#     for query in queries:
#         query = query.strip()  # Remove any leading/trailing whitespace
#         execution_time, result = execute_query(conn, query)
#         times.append(execution_time)
#         print(f"Query: {query}\nExecution Time: {execution_time:.4f} seconds\n")
    
#     return times

# Load queries from the queries.txt file
def load_queries_from_file(query_file):
    with open(query_file, 'r') as file:
        queries = file.readlines()
    queries = [query.strip() for query in queries]  # Remove leading/trailing whitespace
    return queries

# Plot individual query execution times against file sizes and save as images
def save_query_performance_plots(file_sizes, all_times, save_dir, queries, schema):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Plot each query's performance
    for i, query_times in enumerate(all_times):
        plt.figure()
        plt.plot(file_sizes, query_times, marker='o', label=f'Execution Time ({schema})')
        plt.xlabel('File Size (MB)')
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'Query {i + 1} Execution Time vs File Size ({schema})')
        plt.xticks(file_sizes)  # Ensure x-ticks match file sizes
        plt.grid(True)
        plt.legend()
        
        # Save the plot to the specified file
        image_path = os.path.join(save_dir, f'{schema}_query_{i + 1}_performance.png')
        plt.savefig(image_path)
        plt.close()
        
        print(f"Plot for Query {i + 1} ({schema}) saved to {image_path}")

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
    queries = load_queries_from_file(query_file)  # Load queries from the file

    all_times_before = [[] for _ in range(len(queries))]  # List for pre-normalized times
    all_times_after = [[] for _ in range(len(queries))]  # List for post-normalized times

    # Directory to save the plots
    image_dir = os.path.join(base_dir, 'images')

    # # Load queries for the single-table schema
    # query_file = os.path.join(base_dir, 'queries.txt')  # File with single-table schema SQL queries
    # queries = load_queries_from_file(query_file)  # Load single-table queries

    # # Load queries for the normalized schema
    # query_file_normalized = os.path.join(base_dir, 'normalized_queries.txt')  # File with normalized schema SQL queries
    # queries_normalized = load_queries_from_file(query_file_normalized)  # Load normalized queries

    # # Loop through datasets, load them, run queries, and collect execution times for both schemas
    # for dataset in datasets:
    #     # Processing Before Normalization (Single Table Schema)
    #     print(f"Processing {dataset} - Before Normalization...")
    #     conn_before = load_csv_to_db_before_normalization(dataset)
    #     execution_times_before = run_queries(conn_before, queries)
        
    #     # Collect execution times for each query for the pre-normalized schema
    #     for i, execution_time in enumerate(execution_times_before):
    #         all_times_before[i].append(execution_time)  # Append time for this dataset to the corresponding query
        
    #     conn_before.close()

    #     # Processing After Normalization (Normalized Schema)
    #     print(f"Processing {dataset} - After Normalization...")
    #     conn_after = normalize_csv_and_create_schema(dataset)
    #     execution_times_after = run_queries(conn_after, queries)
        
    #     # Collect execution times for each query for the normalized schema
    #     for i, execution_time in enumerate(execution_times_after):
    #         all_times_after[i].append(execution_time)  # Append time for this dataset to the corresponding query
        
    #     conn_after.close()


    # Directory to save the plots
    image_dir = os.path.join(base_dir, 'images')

    # Load queries for the single-table schema
    query_file = os.path.join(base_dir, 'queries.txt')  # Single-table queries
    queries = load_queries_from_file(query_file)

    # Load queries for the normalized schema
    query_file_normalized = os.path.join(base_dir, 'normalized_queries.txt')  # Normalized schema queries
    queries_normalized = load_queries_from_file(query_file_normalized)

    queries_normalized = [
    "SELECT p.PersonName FROM Person p JOIN Employment e ON p.PersonID = e.PersonID WHERE p.BirthDate < '1975-01-01' AND e.Earnings = (SELECT MAX(Earnings) FROM Employment WHERE PersonID = e.PersonID) AND e.Earnings > 130000;",
    ]

    # Loop through datasets, run queries, and collect execution times for both schemas
    # Loop through datasets, run queries, and collect execution times for both schemas
    for dataset in datasets:
        # Before Normalization (Single Table Schema)
        print(f"Processing {dataset} - Before Normalization...")
        conn_before = load_csv_to_db_before_normalization(dataset)
        execution_times_before = run_queries(conn_before, queries)
        
        # After Normalization (Normalized Schema)
        print(f"Processing {dataset} - After Normalization...")
        conn_after = normalize_csv_and_create_schema(dataset)

        # Run queries for the normalized schema (including your custom query)
        execution_times_after = run_queries(conn_after, queries_normalized)
        
        # Collect execution times for the normalized schema
        for i, execution_time in enumerate(execution_times_after):
            all_times_after[i].append(execution_time)  # Append time for this dataset to the corresponding query
        
        conn_after.close()


    # Save the results plots for both schemas
    save_query_performance_plots(file_sizes, all_times_before, image_dir, queries, schema='Before Normalization')
    save_query_performance_plots(file_sizes, all_times_after, image_dir, queries, schema='After Normalization')