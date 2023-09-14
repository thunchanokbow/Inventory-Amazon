Google Cloud Composer
============
managed workflow orchestration service built on Apache Airflow with [Cloud Composer](https://cloud.google.com/composer?hl=en)
<br>

- [Create Cloud Composer](02-data-pipeline.md#Create-Cloud-Composer)
- [Import the Python Package](02-data-pipeline.md#Import-the-Python-Package)
- [Connected PostgreSQL to Airflow](02-data-pipeline.md#Connected-PostgreSQL-to-Airflow)
- [Automate Tasks with Airflow](02-data-pipeline.md#Automate-Tasks-with-Airflow )

Google Cloud Storage
============
[Cloud Storage](https://cloud.google.com/storage) managed service for storing semistructured, and unstructured data. We will create a bucket to store Spark scripts that have data collection tasks for working with Cloud Dataproc.
<br>

- [Create Bucket](02-data-pipeline.md#Create-Bucket)

Google Cloud Dataproc
============
[Cloud Dataproc](https://cloud.google.com/dataproc?hl=en) managed Hadoop and Spark cluster. 
<br>
- [Create Cloud Dataproc](02-data-pipeline.md#Create-Cloud-Dataproc)
- [Submit PySpark jobs](02-data-pipeline.md#Submit-PySpark-jobs)
- [Delete a Dataproc cluster](02-data-pipeline.md#Delete-a-Dataproc-cluster)
  
Google BigQury 
============
data warehouse to store data that works across clouds with [Google BigQuery](https://cloud.google.com/bigquery/?utm_source=google&utm_medium=cpc&utm_campaign=japac-TH-all-en-dr-BKWS-all-super-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_667077871611-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt%20~%20Data%20Analytics_BigQuery_big%20query_main-KWID_43700077853701054-aud-1596662388934%3Akwd-63326440124&userloc_1012728-network_g&utm_term=KW_google%20bigquery&gclid=CjwKCAjw3oqoBhAjEiwA_UaLtpFg721sXu5OaTYClS3Ctvc2SBAzMH3-iRvmO4V1-qD8z8k_ZoJ4ShoCazkQAvD_BwE&gclsrc=aw.ds)
- [Create Dataset](02-data-pipeline.md#CreateCreate-Dataset)

## Create Cloud Composer
create Google Cloud Composer environments to manage Apache Airflow workflows.<br>
1.Select your project<br>
2.Click Create environment: " Composer 1 "<br>
3.In the Create environment dialog, enter a name for your environment and select a location.<br>
4.Configure environment scale and performance parameters.<br>
5.Specify Airflow configuration overrides and environment variables.<br>

![0](/images/0.png)

SET UP Cloud Composer:
- Name : _Your Project_
- Location : asia-east2 (it will use composer in HongKong)
- Image version : composer-1.20.12-airflow-2.4.3
- Node count : 3
- Zone : asia-east2-b
- Machine type : n1-standard-2
- Disk size (GB) : 30 _minimum_
- Number of schedulers : 1
<br>

## Import the Python Package
Spectify libraries from the Python Package. _pandas_ <br>

![3](/images/3.png)

## Connected PostgreSQL to Airflow
To create an Airflow connection to the PostgreSQL instance, follow these steps.<br>

![1](/images/1.png)
### Create an Airflow connection
1.Go to the Airflow web UI.<br>
2.Click _Admin_ > _Connections._<br>
3.Select the PostgreSQL connection type.<br>
_Connection name:_ A name for the connection.<br>
_Host:_ The hostname or IP address of the Cloud SQL PostgreSQL instance.<br>
_Login:_ The postgres user name.<br>
_Password:_ The password for the postgres user.<br>
_Port:_ The port number of the Cloud SQL PostgreSQL instance.<br>

![2](/images/2.png)

Enter the following information:
- Connection name: A name for the connection.
- Host: _azure-amazon.postgres.database.azure.com_
- Schema: _db-amazon_
- Login: _myadmin_
- Password: The password for the postgres user.
- Port: 5432


## Create Bucket
1.Click the Storage tab.<br>
2.Click Buckets.<br>
3.Click Create bucket.<br>
4.Enter a name for your bucket.<br>
5.Select a location for your bucket.<br>
6.Select a storage class for your bucket.<br>
7.Click Create.<br>

![4](/images/4.png)

## Automate Tasks with Airflow

![5](/images/5.png)


### Upload files to GCS<br> 
- Select the dataproc-spark-demo > script bucket. then upload spark script file.<br>
- Click the "Open dags folder" button in the top right corner of the website.<br>
  
Keep it in mind when you create a Cloud Composer environment, Google Cloud Storage will automatically create a bucket that is connected to the environment.<br>
- Uplod DAG flie to the composer bucket.

![6](/images/6.png)

## Create Cloud Dataproc
In a [dag file](Inventory2Q2022.ipynb), airflow operators are used to create a Dataproc cluster, submit a PySpark job, and delete a Dataproc cluster using Python.


![10](/images/10.png)

## Submit PySpark jobs
![11](/images/11.png)

## Delete a Dataproc cluster
![12](/images/12.png)

## Create Dataset
1.Go to the BigQuery [page](https://console.cloud.google.com/bigquery)<br>
2.In the Explorer panel, select the project where you want to create the dataset.<br>
3.Expand the more_vert Actions option and click Create dataset.<br>
4.On the Create dataset page:<br>
- Select : _best-seller-amazon_
- Fill : _dataproc_spark_
- Location type : Region
- Region : asia-east2(Hong Kong)<br>
5.Click Create.

![9](/images/9.png)

