import sqlite3
import pandas as pd
import time

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

        # Insert data into the tables
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO Person (PersonID, PersonName, BirthDate, StillWorking) 
                VALUES (?, ?, ?, ?)
            ''', (row['PersonID'], row['PersonName'], row['BirthDate'], row['StillWorking']))

            cursor.execute('''
                INSERT OR REPLACE INTO School (SchoolID, SchoolName, SchoolCampus) 
                VALUES (?, ?, ?)
            ''', (row['SchoolID'], row['SchoolName'], row['SchoolCampus']))

            cursor.execute('''
                INSERT OR REPLACE INTO Department (DepartmentID, DepartmentName) 
                VALUES (?, ?)
            ''', (row['DepartmentID'], row['DepartmentName']))

            cursor.execute('''
                INSERT OR REPLACE INTO Job (JobID, JobTitle) 
                VALUES (?, ?)
            ''', (row['JobID'], row['JobTitle']))

            cursor.execute('''
                INSERT INTO Employment (PersonID, SchoolID, DepartmentID, JobID, Earnings, EarningsYear) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['PersonID'], row['SchoolID'], row['DepartmentID'], row['JobID'], row['Earnings'], row['EarningsYear']))

        # Execute each query and measure execution time
        for query_name, query in queries.items():
            start_time = time.time()
            cursor.execute(query)
            execution_time = time.time() - start_time
            print(f"{query_name} executed in {execution_time:.6f} seconds")
        
        conn.close()

# Execute the queries
execute_queries(csv_files, queries)
