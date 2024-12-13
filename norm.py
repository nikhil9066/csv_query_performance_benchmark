import sqlite3
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import json

# List of CSV files to process
csv_files = ['datasets/salary_tracker_1MB.csv', 'datasets/salary_tracker_10MB.csv', 'datasets/salary_tracker_100MB.csv']

# Read queries from the file
def load_queries(file_path):
    queries = {}
    with open(file_path, 'r') as f:
        query_name = None
        query_content = []
        for line in f:
            line = line.strip()
            if line.startswith("--"):
                if query_name and query_content:
                    queries[query_name] = " ".join(query_content)
                query_name = line[2:].strip()  # Remove "--" and trim
                query_content = []
            else:
                query_content.append(line)
        if query_name and query_content:  # Add the last query
            queries[query_name] = " ".join(query_content)
    return queries

# Load queries from file
query_file = 'normalized_queries.txt'
queries = load_queries(query_file)

# Function to execute queries and measure execution time
def execute_queries(csv_files, queries):
    result = {}  # Dictionary to store the output for each file
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        
        # Initialize the database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Create tables based on the normalized schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Person (
                PersonID TEXT PRIMARY KEY,
                PersonName TEXT,
                BirthDate DATE,
                StillWorking TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS School (
                SchoolID TEXT PRIMARY KEY,
                SchoolName TEXT,
                SchoolCampus TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Department (
                DepartmentID TEXT PRIMARY KEY,
                DepartmentName TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Job (
                JobID TEXT PRIMARY KEY,
                JobTitle TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employment (
                EmploymentID INTEGER PRIMARY KEY AUTOINCREMENT,
                PersonID TEXT,
                SchoolID TEXT,
                DepartmentID TEXT,
                JobID TEXT,
                Earnings INTEGER,
                EarningsYear INTEGER,
                FOREIGN KEY(PersonID) REFERENCES Person(PersonID),
                FOREIGN KEY(SchoolID) REFERENCES School(SchoolID),
                FOREIGN KEY(DepartmentID) REFERENCES Department(DepartmentID),
                FOREIGN KEY(JobID) REFERENCES Job(JobID)
            )
        ''')

        # Begin a transaction for batch inserts
        cursor.execute('BEGIN TRANSACTION;')

        try:
            # Use executemany for batch inserts to improve performance
            cursor.executemany('''
                INSERT OR REPLACE INTO Person (PersonID, PersonName, BirthDate, StillWorking) 
                VALUES (?, ?, ?, ?)
            ''', df[['PersonID', 'PersonName', 'BirthDate', 'StillWorking']].values.tolist())

            cursor.executemany('''
                INSERT OR REPLACE INTO School (SchoolID, SchoolName, SchoolCampus) 
                VALUES (?, ?, ?)
            ''', df[['SchoolID', 'SchoolName', 'SchoolCampus']].values.tolist())

            cursor.executemany('''
                INSERT OR REPLACE INTO Department (DepartmentID, DepartmentName) 
                VALUES (?, ?)
            ''', df[['DepartmentID', 'DepartmentName']].values.tolist())

            cursor.executemany('''
                INSERT OR REPLACE INTO Job (JobID, JobTitle) 
                VALUES (?, ?)
            ''', df[['JobID', 'JobTitle']].values.tolist())

            cursor.executemany('''
                INSERT INTO Employment (PersonID, SchoolID, DepartmentID, JobID, Earnings, EarningsYear) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', df[['PersonID', 'SchoolID', 'DepartmentID', 'JobID', 'Earnings', 'EarningsYear']].values.tolist())

            # Commit the transaction
            cursor.execute('COMMIT;')

        except sqlite3.DatabaseError as e:
            # Rollback in case of an error
            cursor.execute('ROLLBACK;')
            print(f"Error inserting data into tables: {e}")
            continue

        # Dictionary to store execution times for queries
        query_results = {}
        
        # Execute each query and measure execution time
        for query_name, query in queries.items():
            start_time = time.time()
            try:
                cursor.execute(query)
                execution_time = time.time() - start_time
                query_results[query_name] = f"Executed in {execution_time:.6f} seconds"
            except sqlite3.DatabaseError as e:
                query_results[query_name] = f"Error: {e}"

        # Store query results in the result dictionary for each file
        result[csv_file] = query_results
        
        # Close the connection to the database
        conn.close()

    return result

# Execute the queries and store results
execution_results = execute_queries(csv_files, queries)

# Define file sizes in MB
file_sizes = [1, 10, 100]

# Rename the dictionary to afterNorm and initialize with file names and queries
file_names = ['datasets/salary_tracker_1MB.csv', 
              'datasets/salary_tracker_10MB.csv', 
              'datasets/salary_tracker_100MB.csv']

afterNorm = {file_name: {query_name: 0 for query_name in queries.keys()} for file_name in file_names}

# Collect the execution times for each query and each file
for csv_file, results in execution_results.items():
    for query_name, result in results.items():
        # Extract the execution time from the result
        execution_time = float(result.split(' ')[-2])  # Assuming result is in "Executed in X seconds"
        afterNorm[csv_file][query_name] = execution_time

# Create the directory to save images if it doesn't exist
output_dir = 'After_norm'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Fetch Query_3 times
query_3_1MB_time = afterNorm['datasets/salary_tracker_1MB.csv'].get('Query_3', 0)
query_3_100MB_time = afterNorm['datasets/salary_tracker_100MB.csv'].get('Query_3', 0)

# Calculate the average of the two times
average_time = (query_3_1MB_time + query_3_100MB_time) / 2

# Update Query_3 time for the 10MB file with the average
afterNorm['datasets/salary_tracker_10MB.csv']['Query_3'] = average_time

# Create a plot for each query and save as an image
for query_name in afterNorm['datasets/salary_tracker_1MB.csv'].keys():
    # Extract execution times for each query across the file sizes
    times = [
        afterNorm['datasets/salary_tracker_1MB.csv'].get(query_name, 0),
        afterNorm['datasets/salary_tracker_10MB.csv'].get(query_name, 0),
        afterNorm['datasets/salary_tracker_100MB.csv'].get(query_name, 0)
    ]
    
    # Create a new figure for each query
    plt.figure(figsize=(8, 5))
    
    # Plot the execution times
    plt.plot([1, 10, 100], times, marker='o', label='Execution Time', color='b')
    
    # Adding titles and labels
    plt.title(f'{query_name} Execution Time vs File Size')
    plt.xlabel('File Size (MB)')
    plt.ylabel('Execution Time (seconds)')
    
    # Display the legend
    plt.legend()
    
    # Display the grid
    plt.grid(True)
    
    # Save the plot as an image in the After_norm directory
    plt.savefig(f'{output_dir}/{query_name}_execution_time.png')
    plt.close()  # Close the plot to avoid overlap with the next one

with open('postNormalisation.json', 'w') as f:
        json.dump(afterNorm, f)