# Module 6 Homework — Batch Processing with Spark

# Question 1: Install Spark and PySpark

### Task
- Install Apache Spark
- Run PySpark
- Create a local Spark session
- Execute `spark.version`

### Code
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("spark-homework") \
        .getOrCreate()

    spark.version

### Explanation
This code initializes a **local Spark session** and prints the installed Spark version.

### Answer
Spark Version (example):

    4.1.1

### Jupyter Notebook
[Question 1 Notebook](./data/Question1.ipynb)

---

# Question 2: Yellow November 2025
Read the November 2025 Yellow into a Spark Dataframe.
Repartition the Dataframe to 4 partitions and save it to parquet.
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB
- 75MB
- 100MB

### Task
1. Read the Yellow Taxi dataset
2. Repartition the DataFrame into 4 partitions
3. Save the dataset to parquet
4. Calculate the average size of the parquet files

### Code

    df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

    df_repartitioned = df.repartition(4)

    df_repartitioned.write.parquet("yellow_output")

Check file sizes:

    !ls -lh yellow_output

### Explanation
Spark splits the dataset into **4 partitions**, producing **4 parquet files**.

### Answer
25 MB

### Jupyter Notebook
[Question 2 Notebook](./data/Question2.ipynb)

---

# Question 3: Count Records
How many taxi trips were there on the 15th of November?
Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- 162,604
- 225,768

### Task
Count how many taxi trips **started on 15 November 2025**.

### Code

    from pyspark.sql.functions import col, to_date

    df.filter(
        to_date(col("tpep_pickup_datetime")) == "2025-11-15"
    ).count()

### Explanation
We filter rows where pickup date equals **2025-11-15**, then count the records.

### Answer
162,604

### Jupyter Notebook
[Question 3 Notebook](./data/Question3.ipynb)

---

# Question 4: Longest Trip
What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- 90.6
- 134.5

### Task
Find the **longest trip duration in hours**.

### Code

    from pyspark.sql.functions import unix_timestamp

    df_duration = df.withColumn(
        "trip_duration_hours",
        (unix_timestamp("tpep_dropoff_datetime") -
         unix_timestamp("tpep_pickup_datetime")) / 3600
    )

    df_duration.orderBy("trip_duration_hours", ascending=False).show(1)

### Explanation
Trip duration is calculated by subtracting pickup time from dropoff time and converting seconds to hours.

### Answer
90.6

### Jupyter Notebook
[Question 4 Notebook](./data/Question4.ipynb)

---

# Question 5: Spark User Interface
Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080

### Task
Identify the port where the Spark UI runs locally.

### Explanation
When a Spark application runs, it launches a **web UI dashboard** displaying:

- Jobs
- Stages
- Executors
- Storage
- Environment

Default Spark UI URL:

    http://localhost:4040

If that port is busy, Spark uses:

    4041, 4042, 4043...

### Answer
4040

---

# Question 6: Least Frequent Pickup Location Zone
Load the zone lookup data into a temp view in Spark:

wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay
If multiple answers are correct, select any

### Task
Using the taxi zone lookup table, determine the **least frequent pickup zone**.

Zone lookup dataset:

    wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

### Code

    zones = spark.read.option("header", "true").csv("taxi_zone_lookup.csv")

    df_join = df.join(
        zones,
        df.PULocationID == zones.LocationID
    )

    zone_counts = df_join.groupBy("Zone") \
        .count() \
        .orderBy("count")

    zone_counts.show(5)

### Explanation
We join the taxi dataset with the zone lookup table using **PULocationID**, then count trips per zone and sort by frequency.

### Answer
- Governor's Island/Ellis Island/Liberty Island
- Arden Heights

### Jupyter Notebook
[Question 6 Notebook](./data/Question6.ipynb)

