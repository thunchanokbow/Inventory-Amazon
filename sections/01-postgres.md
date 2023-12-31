PostgreSQL Database
============
[Azure Database for PostgreSQL - Flexible Server.](https://azure.microsoft.com/en-gb/free/) If you don’t have one, create a free account before you begin.
- [Create Server](01-postgres.md#Create-Server)
- [Create Database](01-postgres.md#Create-Database)
- [Import dataset](01-postgres.md#Import-dataset)
- [Connect Database to Google cloud platform](01-postgres.md#Connect-Database-to-Google-cloud-platform)


## Create Server
1. To create a PostgreSQL Flexible Server database, search for and select _Azure Database for PostgreSQL servers_.<br>
2. Select Create.<br>
3. On the Select Azure Database for PostgreSQL deployment option page, select **Flexible Server**.<br>
4. Enter the basic settings for a new _Flexible Server_.<br>
5. For Compute + storage setting, keep the default values populated upon selecting **Development** workload type.<br>
6. Select Save to continue with the configuration.<br>
![3](/images/azure-3.png)
![4](/images/azure-4.png)

7. Select Networking tab to configure how to reach your server. <br>
8. On the Networking tab, for Connectivity method select **Public access (allowed IP addresses)**. <br>
9. For configuring **Firewall rules**, select Add current client _IP address_.<br>

![5](/images/azure-5.png)
![A](/images/azure-0.png)

## Create Database
Once the server is created, you can create a database on it by following these steps.<br>
1. Go to the server overview page.<br>
2. Click the Databases tab.<br>
3. Click the + Add database button.<br>
4. Enter the following information:
- Database name: The name of the database.
- Owner: The user who will own the database.
- Collation: The collation for the database.
 
5. Click the **Create** button.
![7](/images/azure-7.png)

## Import dataset
The easiest and most convenient tool to add a dataset is **pgAdmin 4**. <br>
### Connecting to the Server
1. Open pgAdmin. <br>
2. Right-click on the Servers node in the tree control and select **Create** > **Server**.<br>
3. In the **Create Server** dialog, enter the following information:<br>
- **Name**: Enter a name for the server connection.<br>
- **Type**: Select PostgreSQL from the drop-down menu.<br>
- **Host**: Enter the hostname or IP address of the PostgreSQL server.<br>
- **Port**: Enter the port number of the PostgreSQL server.<br>
- **Maintenance database**: Enter the name of the maintenance database. This is optional.<br>
- **Username**: Enter the username for the PostgreSQL user that you want to connect with.<br>
- **Password**: Enter the password for the PostgreSQL user that you want to connect with.<br>

4. Click **Save**.
![8](/images/Azure-pgAdmin.png)

### Creating and importing 
How to creating a Table [Click](https://github.com/thunchanokbow/Postgresql-database/blob/main/section/create-table.md) <br>
How to importing a CSV file into a table [Click](https://github.com/thunchanokbow/Postgresql-database/blob/main/section/import-data.md)

## Connect Database to Google cloud platform
If you created your flexible server with Public access (allowed IP addresses), you can add your local IP address to the list of firewall rules on your server, **The Google IP address** is in the **Compute Engine** that was created when you created the environment in **Google Cloud Composer**.
<br>
<br>
![C](/images/compute-engine.png)
<br>
<br>
1.Copy **External IP** from Google Compute Engine. <br>
2.In the Azure portal, on the Networking pane. <br>
3.Enter the firewall rule name, **start IP address**, **end IP adress**. <br>
![B](/images/azure-6.png)

