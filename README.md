# CSV Query Performance Benchmark

## Table of Contents
1. [Introduction](#introduction)
2. [Dataset Overview](#dataset-overview)
3. [Schema](#schema)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Results](#results)
8. [Query Performance Summary](#query-performance-summary)
9. [Graphs](#graphs)
10. [Post-Normalization Results](#post-normalization-results)
11. [Conclusion](#conclusion)

## Introduction
This project benchmarks the performance of SQL queries executed on a set of CSV files of varying sizes. The goal is to evaluate how query execution time varies with dataset size. The project involves loading CSV files into an SQLite database, executing a series of queries, and visualizing the execution time for each query.

### Dataset Overview
The dataset used in this project is a simulated salary tracker, containing information about individuals, their job titles, earnings, and employment status. This dataset serves to illustrate how various queries can be used to extract meaningful insights regarding faculty members' earnings and employment details in educational institutions.

### Schema
The schema for the `salary_tracker` dataset is as follows:

| Column Name     | Data Type   | Description                                                |
|-----------------|-------------|------------------------------------------------------------|
| `PersonID`      | INTEGER     | Unique identifier for each individual.                     |
| `PersonName`    | TEXT        | Full name of the individual.                               |
| `JobTitle`      | TEXT        | Title of the individual's job position.                    |
| `DepartmentName`| TEXT        | Name of the department where the individual works.         |
| `SchoolName`    | TEXT        | Name of the school where the individual is employed.       |
| `SchoolCampus`  | TEXT        | Campus location of the school.                             |
| `Earnings`      | INTEGER     | Annual earnings of the individual.                         |
| `BirthDate`     | DATE        | Birthdate of the individual.                               |
| `StillWorking`  | TEXT        | Employment status (`'yes'` or `'no'`).                     |

## Requirements
- Python 3.x
- Pandas
- SQLite3
- Matplotlib

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required libraries:
   ```bash
   pip install pandas matplotlib

## Usage
Run the main script to execute the benchmarking process:
```bash
python main.py
```

## Results
The following outputs were generated during the execution of the queries on the different dataset sizes:

### Query Performance Summary

1. **Query 1**: 
   ```sql
   SELECT PersonName 
   FROM salary_tracker 
   WHERE BirthDate < '1975-01-01' AND Earnings > 130000;
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0788 seconds  |
   | 10 MB File     | 0.0430 seconds  |
   | 100 MB File    | 0.0446 seconds  |

2. **Query 2**: 
   ```sql
   SELECT PersonName, SchoolName 
   FROM salary_tracker 
   WHERE Earnings > 400000 AND StillWorking = 'no';
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0427 seconds  |
   | 10 MB File     | 0.0418 seconds  |
   | 100 MB File    | 0.0755 seconds  |

3. **Query 3**: 
   ```sql
   SELECT PersonName 
   FROM salary_tracker 
   WHERE JobTitle = 'Lecturer' AND SchoolName = 'University of Texas' AND StillWorking = 'no';
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0423 seconds  |
   | 10 MB File     | 0.0366 seconds  |
   | 100 MB File    | 0.0727 seconds  |

4. **Query 4**: 
   ```sql
   SELECT SchoolName, SchoolCampus, COUNT(*) AS ActiveFacultyCount 
   FROM salary_tracker 
   WHERE StillWorking = 'yes' 
   GROUP BY SchoolName, SchoolCampus 
   ORDER BY ActiveFacultyCount DESC LIMIT 1;
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0432 seconds  |
   | 10 MB File     | 0.0453 seconds  |
   | 100 MB File    | 0.0856 seconds  |

5. **Query 5**: 
   ```sql
   SELECT PersonName, JobTitle, DepartmentName, SchoolName, MAX(Earnings) AS MostRecentEarnings 
   FROM salary_tracker 
   WHERE PersonName = 'Nikhil Premachandra Rao' 
   GROUP BY PersonName, JobTitle, DepartmentName, SchoolName;
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0421 seconds  |
   | 10 MB File     | 0.0419 seconds  |
   | 100 MB File    | 0.0845 seconds  |

6. **Query 6**: 
   ```sql
   SELECT DepartmentName, AVG(Earnings) AS AverageEarnings 
   FROM salary_tracker 
   GROUP BY DepartmentName 
   ORDER BY AverageEarnings DESC LIMIT 1;
   ```
   | File Size      | Execution Time |
   |----------------|----------------|
   | 1 MB File      | 0.0678 seconds  |
   | 10 MB File     | 0.0582 seconds  |
   | 100 MB File    | 0.0936 seconds  |

## Graphs

The performance graphs for each query are saved in the `images/` folder:

- *Query 1 Performance*  
  ![Query 1 Performance](images/query_1_performance.png)

- *Query 2 Performance*  
  ![Query 2 Performance](images/query_2_performance.png)

- *Query 3 Performance*  
  ![Query 3 Performance](images/query_3_performance.png)

- *Query 4 Performance*  
  ![Query 4 Performance](images/query_4_performance.png)

- *Query 5 Performance*  
  ![Query 5 Performance](images/query_5_performance.png)

- *Query 6 Performance*  
  ![Query 6 Performance](images/query_6_performance.png)

## Post-Normalization Results

### Overview
The post-normalization results illustrate the execution time for each query after applying normalization techniques to the dataset. By comparing these results with the pre-normalization execution times, the impact of normalization on query performance can be assessed. The results are visualized for each query and across varying dataset sizes (1 MB, 10 MB, and 100 MB).

### Key Findings
1. **Improvement for Small Datasets**:
   - Queries executed on the 1 MB dataset generally showed slight improvements in performance after normalization.
   - The normalized schema's improved structure likely contributed to reduced processing overhead for small datasets.

2. **Marginal Impact on Large Datasets**:
   - For the 100 MB dataset, the impact of normalization was less pronounced. Query execution times remained similar, indicating that the dataset size overshadowed schema-related optimizations.

3. **Query-Specific Observations**:
   - Queries involving aggregations or filtering with group-by clauses showed consistent performance gains.
   - Simple lookups and joins displayed negligible differences.

### Visual Results
The execution times for all queries post-normalization are saved in the `After_norm` directory:

#### Query Execution Times:
- **Query 1 Execution Time**:
  ![Query 1 Execution Time](After_norm/Query_1_execution_time.png)

- **Query 2 Execution Time**:
  ![Query 2 Execution Time](After_norm/Query_2_execution_time.png)

- **Query 3 Execution Time**:
  ![Query 3 Execution Time](After_norm/Query_3_execution_time.png)

- **Query 4 Execution Time**:
  ![Query 4 Execution Time](After_norm/Query_4_execution_time.png)

- **Query 5 Execution Time**:
  ![Query 5 Execution Time](After_norm/Query_5_execution_time.png)

- **Query 6 Execution Time**:
  ![Query 6 Execution Time](After_norm/Query_6_execution_time.png)

### Comparison with Pre-Normalization Results
The combined comparison plot, located in the `comparison` directory, provides a side-by-side visualization of pre- and post-normalization performance for all queries across dataset sizes:

- **Combined Comparison Plot**:
  ![Combined Comparison Plot](comparison/combined_comparison.png)

### Summary
Normalization enhances query performance for smaller datasets and complex queries by improving database structure and reducing redundancy. However, for larger datasets, the benefits diminish, suggesting that other optimization techniques (e.g., indexing or partitioning) may be needed to further improve performance.

The results highlight the importance of balancing normalization with practical considerations, such as dataset size and query complexity, when designing a database schema.

## Conclusion
Normalization proves to be an effective technique for improving query performance, especially for small and medium-sized datasets. It minimizes data redundancy and optimizes storage, leading to enhanced performance for queries involving joins and aggregations. However, its impact diminishes with larger datasets where query execution times are more influenced by data volume rather than schema design.

Future database designs should consider combining normalization with other optimization techniques, such as indexing and partitioning, to handle large-scale datasets efficiently. Additionally, understanding the specific query workload can help in determining the right balance between normalization and denormalization to achieve the desired performance outcomes.