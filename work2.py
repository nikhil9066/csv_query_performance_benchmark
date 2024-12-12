import sqlite3
import pandas as pd
import time

# List of CSV files to process
csv_files = ['datasets/salary_tracker_1MB.csv', 'datasets/salary_tracker_10MB.csv', 'datasets/salary_tracker_100MB.csv']

# Query file
query_file = 'normalized_queries.txt'

# Loop through each CSV file
for csv_file in csv_files:
    print(f"Processing file: {csv_file}")

    # Establish connection to SQLite
    conn = sqlite3.connect('salary_tracker.db')
    cursor = conn.cursor()

    # Read the CSV file into pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert 'BirthDate' to standardized format (if needed)
    df['BirthDate'] = pd.to_datetime(df['BirthDate'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Drop and recreate tables for a fresh start
    cursor.executescript('''
        DROP TABLE IF EXISTS Person;
        DROP TABLE IF EXISTS School;
        DROP TABLE IF EXISTS Department;
        DROP TABLE IF EXISTS Job;
        DROP TABLE IF EXISTS Employment;

        CREATE TABLE Person (
            PersonID TEXT PRIMARY KEY,
            PersonName TEXT,
            BirthDate DATE,
            StillWorking TEXT
        );

        CREATE TABLE School (
            SchoolID TEXT PRIMARY KEY,
            SchoolName TEXT,
            SchoolCampus TEXT
        );

        CREATE TABLE Department (
            DepartmentID TEXT PRIMARY KEY,
            DepartmentName TEXT
        );

        CREATE TABLE Job (
            JobID TEXT PRIMARY KEY,
            JobTitle TEXT
        );

        CREATE TABLE Employment (
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
        );
    ''')

    # Insert data into the tables
    for index, row in df.iterrows():
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

    conn.commit()

    # Read the query from the file
    with open(query_file, 'r') as file:
        query = file.read()

    # Measure the execution time
    start_time = time.time()
    cursor.execute(query)
    conn.commit()
    end_time = time.time()

    # Calculate and print execution time
    execution_time = end_time - start_time
    print(f"Execution time for {csv_file}: {execution_time:.6f} seconds")

    # Close the connection
    conn.close()


# import sqlite3
# import pandas as pd
# import time
# import os

# # Directory containing the CSV files
# datasets_dir = './datasets'  # Replace with your actual directory
# csv_files = [os.path.join(datasets_dir, file) for file in os.listdir(datasets_dir) if file.endswith('.csv')]

# # File containing the SQL queries
# query_file = 'normalized_queries.txt'

# # Load queries from the file
# queries = {}
# with open(query_file, 'r') as f:
#     query_name = None
#     query_content = []
#     for line in f:
#         line = line.strip()
#         if line.startswith('#'):  # Query name starts with '#'
#             if query_name:
#                 queries[query_name] = ' '.join(query_content)
#             query_name = line[1:].strip()  # Extract query name
#             query_content = []
#         else:
#             query_content.append(line)
#     # Add the last query
#     if query_name:
#         queries[query_name] = ' '.join(query_content)

# # Dictionary to store execution times
# execution_times = {}

# # Process each CSV file
# for csv_file in csv_files:
#     print(f"Processing file: {csv_file}")

#     # Establish connection to SQLite
#     conn = sqlite3.connect('salary_tracker.db')
#     cursor = conn.cursor()

#     # Read the CSV file into pandas DataFrame
#     df = pd.read_csv(csv_file)

#     # Convert 'BirthDate' to standardized format (if needed)
#     df['BirthDate'] = pd.to_datetime(df['BirthDate'], errors='coerce').dt.strftime('%Y-%m-%d')

#     # Drop and recreate tables for a fresh start
#     cursor.executescript('''
#         DROP TABLE IF EXISTS Person;
#         DROP TABLE IF EXISTS School;
#         DROP TABLE IF EXISTS Department;
#         DROP TABLE IF EXISTS Job;
#         DROP TABLE IF EXISTS Employment;

#         CREATE TABLE Person (
#             PersonID TEXT PRIMARY KEY,
#             PersonName TEXT,
#             BirthDate DATE,
#             StillWorking TEXT
#         );

#         CREATE TABLE School (
#             SchoolID TEXT PRIMARY KEY,
#             SchoolName TEXT,
#             SchoolCampus TEXT
#         );

#         CREATE TABLE Department (
#             DepartmentID TEXT PRIMARY KEY,
#             DepartmentName TEXT
#         );

#         CREATE TABLE Job (
#             JobID TEXT PRIMARY KEY,
#             JobTitle TEXT
#         );

#         CREATE TABLE Employment (
#             EmploymentID INTEGER PRIMARY KEY AUTOINCREMENT,
#             PersonID TEXT,
#             SchoolID TEXT,
#             DepartmentID TEXT,
#             JobID TEXT,
#             Earnings INTEGER,
#             EarningsYear INTEGER,
#             FOREIGN KEY(PersonID) REFERENCES Person(PersonID),
#             FOREIGN KEY(SchoolID) REFERENCES School(SchoolID),
#             FOREIGN KEY(DepartmentID) REFERENCES Department(DepartmentID),
#             FOREIGN KEY(JobID) REFERENCES Job(JobID)
#         );
#     ''')

#     # Insert data into the tables
#     for index, row in df.iterrows():
#         cursor.execute('''
#             INSERT OR REPLACE INTO Person (PersonID, PersonName, BirthDate, StillWorking) 
#             VALUES (?, ?, ?, ?)
#         ''', (row['PersonID'], row['PersonName'], row['BirthDate'], row['StillWorking']))

#         cursor.execute('''
#             INSERT OR REPLACE INTO School (SchoolID, SchoolName, SchoolCampus) 
#             VALUES (?, ?, ?)
#         ''', (row['SchoolID'], row['SchoolName'], row['SchoolCampus']))

#         cursor.execute('''
#             INSERT OR REPLACE INTO Department (DepartmentID, DepartmentName) 
#             VALUES (?, ?)
#         ''', (row['DepartmentID'], row['DepartmentName']))

#         cursor.execute('''
#             INSERT OR REPLACE INTO Job (JobID, JobTitle) 
#             VALUES (?, ?)
#         ''', (row['JobID'], row['JobTitle']))

#         cursor.execute('''
#             INSERT INTO Employment (PersonID, SchoolID, DepartmentID, JobID, Earnings, EarningsYear) 
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', (row['PersonID'], row['SchoolID'], row['DepartmentID'], row['JobID'], row['Earnings'], row['EarningsYear']))

#     conn.commit()

#     # Execute each query and measure execution time
#     for query_name, query in queries.items():
#         start_time = time.time()
#         try:
#             cursor.execute(query)
#         except sqlite3.OperationalError as e:
#             print(f"Error executing query '{query_name}' for file {csv_file}: {e}")
#             continue
#         conn.commit()
#         end_time = time.time()

#         # Record execution time
#         execution_time = end_time - start_time
#         execution_times.setdefault(query_name, {})[os.path.basename(csv_file)] = execution_time

#     # Close the connection
#     conn.close()

# # Print execution times
# for query_name, times in execution_times.items():
#     print(f"{query_name}:")
#     for file_name, time_taken in times.items():
#         print(f"  {file_name}: {time_taken:.6f} seconds")
