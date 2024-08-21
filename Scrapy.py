import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
url = "https://www.freshersworld.com/jobs"
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
divs = soup.find_all("div", class_="job-container")
print(len(divs))
# Create an empty list to hold job dictionaries
joblist = []
for item in divs:
  title = item.find('span', class_='wrap-title').text.strip()
  company = item.find('h3', class_='company-name').text.strip()
  location = item.find('span', class_='job-location').text.strip()
  job = {
  'title': title,
  'company': company,
  'location': location
  }
  joblist.append(job)
# Print the list of job dictionaries
#print(joblist)
# Connection URI. Modify this to match your MongoDB deployment.
uri = "mongodb://localhost:27017"
client = MongoClient(uri)
# Access a database
db = client["mydatabase"]
# Access a collection
collection = db["mycollection"]
# Prepare dictionary data
my_dict =joblist
# Insert data into the collection
collection.insert_many(my_dict)
# Close the connection
client.close()