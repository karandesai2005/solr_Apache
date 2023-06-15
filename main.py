import pymysql
import json
import pysolr

# Establish database connection
host = 'localhost'
username = 'root'
password = ''
database = 'db1'
connection = pymysql.connect(host=host, user=username, password=password, db=database)
cursor = connection.cursor()

# Fetch data from the database
query = "SELECT * FROM sampl2"
cursor.execute(query)
rows = cursor.fetchall()

# Close the database connection
connection.close()

# Convert rows to a list of dictionaries
data = []
for row in rows:
	dict_row = {
    	"id": row[0],
    	"name": row[1],
    	"description": row[2],
    	"school": row[3],
    	"address": row[4],
    	"location": row[5]
	}
	data.append(dict_row)

# Convert data to JSON string
json_data = json.dumps(data, indent=4)

# Write JSON data to a file
file_path = 'data.json'
with open(file_path, 'w') as file:
	file.write(json_data)

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/mycore')

# Index the JSON data in Solr
solr.add(data)

# Commit the changes to make them visible in the index
solr.commit()
