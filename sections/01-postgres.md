PostgreSQL Database
============
[Azure Database for PostgreSQL - Flexible Server.](https://azure.microsoft.com/en-gb/free/) If you don’t have one, create a free account before you begin.
- [Create a PostgreSQL database](01-postgres.md#Create-a-PostgreSQL-database)
- [Connect Database to Google cloud platform](01-postgres.md#Connect-Database-to-Google-cloud-platform)


## Create a PostgreSQL database
1.To create a PostgreSQL Flexible Server database, search for and select _Azure Database for PostgreSQL servers_.<br>
2.Select Create.<br>
3.On the Select Azure Database for PostgreSQL deployment option page, select **Flexible Server**.<br>
4.Enter the basic settings for a new _Flexible Server_.<br>
5.For Compute + storage setting, keep the default values populated upon selecting **Development** workload type.<br>
6.Select Save to continue with the configuration.<br>
![3](/images/azure-3.png)
![4](/images/azure-4.png)

7.Select Networking tab to configure how to reach your server. <br>
8.On the Networking tab, for Connectivity method select **Public access (allowed IP addresses)**. <br>
9.For configuring **Firewall rules**, select Add current client _IP address_.<br>

![5](/images/azure-5.png)
![A](/images/azure-0.png)

## Connect Database to Google cloud platform
If you created your flexible server with Public access (allowed IP addresses), you can add your local IP address to the list of firewall rules on your server, **The Google IP address** is in the **Compute Engine** that was created when you created the environment in **Google Cloud Composer**.
<br>
![C](/images/compute-engine.png)
<br>
<br>
1.Copy **External IP** from Google Compute Engine. <br>
2.In the Azure portal, on the Networking pane. <br>
3.Enter the firewall rule name, **start IP address**, **end IP adress**. <br>
![B](/images/azure-6.png)

