import sqlite3
import csv

sqlite_file = 'ebay_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

start_date = input("Input the start date for the report, for example 2018-10-11:")
end_date = input("Input the end date for the report, for example 2018-11-11:")

query = '''SELECT
  present_table.name,
  past_table.orders,
  present_table.orders,
  present_table.orders - past_table.orders AS dif,
  present_table.url as url_present,
  past_table.url as url_past,
  past_table.Timestamp,
  present_table.Timestamp
FROM
  (SELECT * FROM products WHERE DATE(Timestamp)="{}") as past_table
JOIN
  (SELECT * FROM products WHERE DATE(Timestamp)="{}") as present_table
ON
  past_table.id = present_table.id
ORDER BY dif DESC'''.format(start_date, end_date)

c.execute(query)

with open("out.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in c.description])
    csv_writer.writerows(c)

conn.close()

print("Report generated and saved to out.csv")