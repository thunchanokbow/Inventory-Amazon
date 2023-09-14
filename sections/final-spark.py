import os
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
import pyspark.sql.functions as f

# Read data into Spark dataframe from CSV file available in GCS bucket.
product_price = spark.read.option("header",True).csv('gs://dataproc-spark-demo/postgresql/product_price.csv')
sales_report = spark.read.option("header",True).csv('gs://dataproc-spark-demo/postgresql/sales_report.csv')

# Convert the Amount column to integer.
product_price = product_price.withColumn("Amount", product_price["Amount"].cast("Integer"))

"""
Analyze Best and worst selling SKU items.
"""
# Convert the Qty column to integer.
sales_report = sales_report.withColumn("Qty", sales_report["Qty"].cast("Integer"))
# Group the data by SKU and calculate the sum of Qty.
best_items = sales_report.groupBy("SKU").sum("Qty")
# Sort the DataFrame by Qty column in descending order.
best_items = best_items.sort("sum(Qty)", ascending=False)


"""
Analyze Peak periods with highest sales of the year.
"""
# Read Spark Dataframe                                     
high_report = spark.read.option("header",True).csv('gs://dataproc-spark-demo/postgresql/high_report.csv')
# Create a new column called order_month use the month function to extract the month of the date column.
high_report = high_report.withColumn("order_month",
                                     f.month(high_report["New_date"]))
# Convert the Qty column to integer.
high_report = high_report.withColumn("Qty", high_report["Qty"].cast("Integer"))
# Group the data by order_month and calculate the sum of quantity.
monthly_sales = high_report.groupBy("order_month").sum("Qty")
monthly_sales = monthly_sales.sort("order_month", ascending=True)
# Save to monthly_sales format CSV in the jobs bucket.
monthly_sales.coalesce(1).write.csv('gs://dataproc-spark-demo/jobs/monthly_sales', header = True)


"""
Best Products Revenue 
"""
# Join Inner product_price to best_revenue dataframe
best_revenue = best_items.join(product_price,
                               on=["SKU"], how="inner")
# Save to best_revenue format CSV in the jobs bucket.
best_revenue.coalesce(1).write.csv('gs://dataproc-spark-demo/jobs/best_revenue', header = True)


"""
Analyze Excess Inventory Value
"""
# Sort the DataFrame by Qty column in ascending order.
worst_items = best_items.sort("sum(Qty)", descending=False)
# Filter the sum(Qty) column is equal to 0 and display the SKU column.
worst_list = worst_items.where(worst_items["sum(Qty)"] == 0).select("SKU")
# Matching rows in product_price that have a same value of the SKU column
worst_list_price = worst_list.join(product_price,
                                   on=["SKU"], how="inner")
# Convert the Stock column to integer.
worst_list_price = worst_list_price.withColumn("Stock", worst_list_price["Stock"].cast("Integer"))
# Calculate the total value of the product and put it in the total column.
worst_list_price = worst_list_price.withColumn("Inventory_value", worst_list_price["Stock"] * worst_list_price["Amount"])
# Save to monthly_sales format CSV in the jobs bucket.
worst_list_price.coalesce(1).write.csv('gs://dataproc-spark-demo/jobs/Inventory_Value', header = True)
spark.stop()