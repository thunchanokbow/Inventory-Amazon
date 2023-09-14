Google Cloud Composer
============
managed workflow orchestration service built on Apache Airflow with [Cloud Composer](https://cloud.google.com/composer?hl=en)
<br>

[Create Cloud Composer](apache-airflow.md#Create-Cloud-Composer)
- [Import the Python Package](apache-airflow.md#Import-the-Python-Package)
- [Connected PostgreSQL to Airflow](apache-airflow.md#Connected-PostgreSQL-to-Airflow)


Google Cloud Storage
============
[Cloud Storage](https://cloud.google.com/storage) managed service for storing semistructured, and unstructured data. We will create a bucket to store Spark scripts that have data collection tasks for working with Cloud Dataproc.
<br>

- [Create Bucket](apache-airflow.md#Create-Bucket)


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

