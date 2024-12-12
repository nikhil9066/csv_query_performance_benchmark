import os
import sqlite3
import pandas as pd
import time
import matplotlib.pyplot as plt

# Load CSV into SQLite
def load_csv_to_db(csv_file, db_name='salary_tracker.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_file)
    df.to_sql('salary_tracker', conn, if_exists='replace', index=False)
    print(f"Loaded {csv_file} into database {db_name}")
    return conn

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
        query = query.strip()
        execution_time, result = execute_query(conn, query)
        times.append(execution_time)
        print(f"Query: {query}\nExecution Time: {execution_time:.4f} seconds\n")
    
    return times

# Measure query performance for raw CSV
def execute_query_on_csv(df, query):
    start_time = time.time()
    result = df.query(query)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, result

# Compare normalized vs non-normalized performance
def compare_performance(raw_csv_file, normalized_db_file, query_file, save_dir):
    raw_df = pd.read_csv(raw_csv_file)
    conn = sqlite3.connect(normalized_db_file)

    with open(query_file, 'r') as file:
        queries = file.readlines()

    raw_times = []
    normalized_times = []

    for query in queries:
        query = query.strip()

        # Measure performance on raw CSV
        try:
            raw_time, _ = execute_query_on_csv(raw_df, query)
        except Exception as e:
            print(f"Error executing query on raw CSV: {e}")
            raw_time = None

        # Measure performance on normalized schema
        normalized_time, _ = execute_query(conn, query)

        raw_times.append(raw_time)
        normalized_times.append(normalized_time)

    # Plot comparison
    os.makedirs(save_dir, exist_ok=True)

    for i, (raw_time, normalized_time) in enumerate(zip(raw_times, normalized_times)):
        raw_time = raw_time if raw_time is not None else 0
        normalized_time = normalized_time if normalized_time is not None else 0
        plt.figure()
        plt.bar(['Raw CSV', 'Normalized'], [raw_time, normalized_time], color=['blue', 'green'])
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'Query {i + 1} Execution Time Comparison')
        image_path = os.path.join(save_dir, f'query_{i + 1}_comparison.png')
        plt.savefig(image_path)
        plt.close()

        print(f"Comparison plot for Query {i + 1} saved to {image_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets = [
        os.path.join(base_dir, 'datasets', 'salary_tracker_1MB.csv'),
        os.path.join(base_dir, 'datasets', 'salary_tracker_10MB.csv'),
        os.path.join(base_dir, 'datasets', 'salary_tracker_100MB.csv')
    ]
    file_sizes = [1, 10, 100]  # File sizes in MB

    query_file = os.path.join(base_dir, 'queries.txt')  # File with SQL queries for non-normalized schema
    query_file_normalized = os.path.join(base_dir, 'queries_normalized.txt')  # File with SQL queries for normalized schema
    image_dir = os.path.join(base_dir, 'images')

    for dataset in datasets:
        print(f"Processing {dataset}...")

        # Run queries on non-normalized schema
        conn = load_csv_to_db(dataset)
        run_queries(conn, query_file)
        conn.close()

        # Process normalized schema performance
        normalized_db_file = os.path.join(base_dir, 'salary_tracker_normalized.db')
        conn = normalize_csv_and_create_schema(dataset, normalized_db_file)
        compare_performance(dataset, normalized_db_file, query_file_normalized, image_dir)

        conn.close()