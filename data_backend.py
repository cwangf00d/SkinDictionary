import csv

from cs50 import SQL

open("skindict.db", "w").close()
db = SQL("sqlite:///skindict.db")

db.execute("CREATE TABLE users (user_id INTEGER, name TEXT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL,user_age INTEGER NOT NULL, user_gender TEXT NOT NULL, user_skintype TEXT NOT NULL, PRIMARY KEY(user_id))")
db.execute("CREATE TABLE chemicals (chem_id INTEGER, chem_name TEXT NOT NULL, PRIMARY KEY(chem_id))")
db.execute("CREATE TABLE products (prod_id INTEGER, prod_name TEXT NOT NULL, prod_brand TEXT NOT NULL, prod_price NUMERIC NOT NULL, prod_link TEXT NOT NULL, prod_loves NUMERIC NOT NULL, PRIMARY KEY(prod_id))")
db.execute("CREATE TABLE symptoms (symp_id INTEGER, symp_name TEXT NOT NULL, PRIMARY KEY(symp_id))")
db.execute("CREATE TABLE user_requests (request_id INTEGER, user_id INTEGER NOT NULL, symp_id INTEGER NOT NULL, date DATETIME, PRIMARY KEY(request_id), FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(user_id) REFERENCES symptoms(symp_id))")
db.execute("CREATE TABLE symp_to_chem (symp_id INTEGER NOT NULL, chem_id INTEGER NOT NULL, FOREIGN KEY(symp_id) REFERENCES symptoms(symp_id), FOREIGN KEY(chem_id) REFERENCES chemicals(chem_id))")
db.execute("CREATE TABLE chem_to_prod (chem_id INTEGER NOT NULL, prod_id INTEGER NOT NULL, FOREIGN KEY(chem_id) REFERENCES chemicals(chem_id), FOREIGN KEY(prod_id) REFERENCES products(prod_id))")
db.execute("CREATE TABLE user_recs (user_id INTEGER NOT NULL, request_id INTEGER NOT NULL, symp_id INTEGER NOT NULL, prod_id INTEGER NOT NULL, prod_name INTEGER NOT NULL, prod_price NUMERIC NOT NULL, prod_link TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(request_id) REFERENCES requests(request_id), FOREIGN KEY(symp_id) REFERENCES symptoms(symp_id), FOREIGN KEY(prod_id) REFERENCES products(prod_id), FOREIGN KEY(prod_name) REFERENCES products(prod_name), FOREIGN KEY(prod_price) REFERENCES products(prod_price), FOREIGN KEY(prod_link) REFERENCES products(prod_link))")

## WE ARE TRYING TO TRANSFER DATA FROM CSV TO SQL TABLES

# Setting up the chemical table
chem_name_to_id = {}
with open("data/chem_full.csv", "r") as file1:
    reader = csv.DictReader(file1)
    for row in reader:
        chem_name = row["name"].strip()
        if chem_name != "":
            chem_name_to_id[chem_name] = db.execute("INSERT INTO chemicals (chem_name) VALUES (?)", chem_name)

file1.close()

# Setting up the symptoms table
symptoms = ['uneven skintone', 'acne', 'dullness', 'dryness', 'redness', 'aging', 'sun protectant', 'wound', 'itchiness', 'oiliness', 'exfoliator/cleanser', 'rough', 'discomfort']
symp_name_to_id = {}

for symptom in symptoms:
    symp_name_to_id[symptom] = db.execute("INSERT INTO symptoms (symp_name) VALUES (?)", symptom)

#Setting up products table
prod_name_to_id = {}
with open("data/prod_sephora_full.csv", "r") as file2:
    reader = csv.DictReader(file2)
    for row in reader:
        prod_name = row["name"].strip()
        prod_price = row["price"]
        prod_link = row["link"].strip()
        prod_loves = row["loves"]
        prod_brand = row["brand"].strip()
        if prod_name != "":
            prod_name_to_id[prod_name] = db.execute("INSERT INTO products (prod_name, prod_brand, prod_price, prod_link, prod_loves) VALUES (?, ?, ?, ?, ?)", prod_name, prod_brand, prod_price, prod_link, prod_loves)
file2.close()

# Setting up symp_to_chem table
with open("data/symp_to_chem_names.csv", "r") as file3:
    reader = csv.DictReader(file3)
    for row in reader:
        chem_name = row["chem_name"].strip()
        symp_name = row["chem_symptoms"].strip()
        if chem_name != "" and symp_name != "" and chem_name in chem_name_to_id and symp_name in symp_name_to_id:
            chem_id = chem_name_to_id[chem_name]
            symp_id = symp_name_to_id[symp_name]
            db.execute("INSERT INTO symp_to_chem (symp_id, chem_id) VALUES (?, ?)", symp_id, chem_id)
file3.close()

# Setting up chem_to_prod table
with open("data/chem_to_sephora_prod.csv", "r") as file4:
    reader = csv.DictReader(file4)
    for row in reader:
        chem_name = row["chem_name"].strip()
        prod_name = row["prod_name"].strip()
        if chem_name != "" and symp_name != "" and chem_name in chem_name_to_id and prod_name in prod_name_to_id:
            chem_id = chem_name_to_id[chem_name]
            prod_id = prod_name_to_id[prod_name]
            db.execute("INSERT INTO chem_to_prod (chem_id, prod_id) VALUES (?, ?)", chem_id, prod_id)
file4.close()

