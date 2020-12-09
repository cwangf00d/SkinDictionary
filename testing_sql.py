from cs50 import SQL

db = SQL("sqlite:///skindict.db")
products = ['7 Day Scrub Cream Rinse-Off Formula', 'A-Passioni™ Retinol Cream', 'Acne Solutions™ Clarifying Lotion', 'Acne Solutions™ Cleansing Foam']
all_info = []
for product in products:
        all_info.append(db.execute("SELECT * FROM products WHERE prod_name = ?", product))
print(all_info)
for symptom in all_info:
        for product in symptom:
                print(product['prod_name'])
# prod_inventory = db.execute("SELECT prod_name, prod_id FROM products")
# for product in prod_inventory:s
#         print(product['prod_id'])
# symptoms = ["rough", "dullness"]
# products = []
# symptom_ids = []
# all_recs = []
# low_user_recommendations = []
# mid_user_recommendations = []
# high_user_recommendations = []
# for symptom in symptoms:
#     symptom_id = db.execute("SELECT symp_id FROM symptoms WHERE symp_name = ?", symptom)[0]
#     symptom_ids.append(symptom)

# for req in symptom_ids:
#     low_count = 0
#     mid_count = 0
#     high_count = 0
#     to_add_low = db.execute("select a.*, b.chem_id, c.symp_id from products a, chem_to_prod b, symp_to_chem c, symptoms d where d.symp_name=? and d.symp_id=c.symp_id and c.chem_id=b.chem_id and b.prod_id=a.prod_id and a.prod_price < 15 ORDER BY a.prod_loves DESC", req)
#     to_add_mid = db.execute("select a.*, b.chem_id, c.symp_id from products a, chem_to_prod b, symp_to_chem c, symptoms d where d.symp_name=? and d.symp_id=c.symp_id and c.chem_id=b.chem_id and b.prod_id=a.prod_id and a.prod_price > 14 and a.prod_price < 35 ORDER BY a.prod_loves DESC", req)
#     to_add_high = db.execute("select a.*, b.chem_id, c.symp_id from products a, chem_to_prod b, symp_to_chem c, symptoms d where d.symp_name=? and d.symp_id=c.symp_id and c.chem_id=b.chem_id and b.prod_id=a.prod_id and a.prod_price > 34 ORDER BY a.prod_loves DESC", req)
#     #to_add = db.execute("SELECT prod_loves, prod_price, prod_link, prod_name, prod_brand FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) ORDER BY prod_loves DESC", req)
#     for product in to_add_low:
#         if product not in all_recs and low_count < 2:
#             low_user_recommendations.append(product)
#             all_recs.append(product)
#             low_count +=1
#             print(product)
#     for product in to_add_mid:
#         if product in all_recs:
#             print("yes")
#         if product not in all_recs and mid_count < 2:
#             mid_user_recommendations.append(product)
#             all_recs.append(product)
#             mid_count +=1
#             print(product)
#     for product in to_add_high:
#         if product in all_recs:
#             print("yes")
#         if product not in all_recs and high_count < 2:

#             high_user_recommendations.append(product)
#             all_recs.append(product)
#             high_count +=1
#             print(product)
# product_one = {'prod_id': 271, 'prod_name': 'Truth Serum®', 'prod_brand': 'OLEHENRIKSEN', 'prod_price': 50, 'prod_link': 'https://www.sephora.com/product/truth-serum-P42343?icid2=products', 'prod_loves': 213198, 'chem_id': 80, 'symp_id': 3}
# print(to_add_high[2] in all_recs)
# print(to_add_high[2])
# product_two = {'prod_id': 254, 'prod_name': 'Hyaluronic Acid 2% + B5', 'prod_brand': 'The Ordinary', 'prod_price': 6.8, 'prod_link': 'https://www.sephora.com/product/the-ordinary-deciem-hyaluronic-acid-2-b5-P427419?icid2=products', 'prod_loves': 349481, 'chem_id': 61, 'symp_id': 12}
# print(product_two in all_recs)


# big list -> list of dictionaires of products for each symptom
# counter = 0
# for symp_list in user_recommendations:
#     for prod_dict in symp_list:
#         print(prod_dict)
#         print(symptom_ids[counter])
#         print(prod_dict['prod_name'])
#     counter +=1
# added = db.execute("SELECT prod_name, prod_price, prod_link FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_name = ?))) LIMIT 3", "uneven skintone")
# for product in added:
#     print(product)
#     print(product['prod_name'])
# print(added)
## ME GOING INSANE
        # user_recommendations = []
        # symptom_ids = []
        # symptoms = []
        # symptoms = ['uneven skintone', 'acne', 'dullness', 'dryness', 'redness', 'aging', 'sun protectant', 'wound', 'itchiness', 'oiliness', 'exfoliator/cleanser', 'rough', 'discomfort']
        # date = datetime.datetime.now()
        # # getting which symptoms are being requested
        # for symptom in symptoms:
        #     if request.form.get(symptom):
        #         symptom_id = db.execute("SELECT symp_id FROM symptoms WHERE symp_name = ?", symptom)[0]
        #         symptom_ids.append(symptom_id['symp_id'])
        #         symptoms.append(symptom)
        #         #db.execute("INSERT INTO user_requests (user_id, symp_id, date) VALUES (?, ?, ?)", session["user_id"], symptom_id['symp_id'], date)

        # # iterating through symptoms requested to gather products
        # for curr_id in symptom_ids:
        #     user_recommendations.append(db.execute("SELECT prod_id, prod_name, prod_price, prod_link FROM products WHERE prod_id IN (SELECT prod_id FROM chem_to_prod WHERE chem_id IN (SELECT chem_id FROM symp_to_chem WHERE symp_id IN (SELECT symp_id FROM symptoms WHERE symp_id = ?)) LIMIT 3)", curr_id))
        # return render_template("recs.html", recommendations = user_recommendations, big_symptom = symptoms, date = date)

        # #inserting in new product recommendations to table
        # # counter = 0
        # # for symp_list in user_recommendations:
        # #     for prod_dict in symp_list:
        # #         db.execute("INSERT INTO user_recs (user_id, request_id, symp_id, prod_id, prod_name, prod_price, prod_link) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], req_ids[counter], symptom_ids[counter], prod_dict['prod_id'], prod_dict['prod_name'], prod_dict['prod_price'], prod_dict['prod_link'])
        # #     counter +=1



# counter = 0
# for symp_id in user_recommendations:
#     print(symp_id)
#     print(symptom_ids[counter])
#     counter +=1
#     for product in symp_id[0].keys():
#         print(product)
# # for symp_id in user_recommendations.keys():
# #     print(user_recommendations[symp_id]['prod_name'])
# #     for product in user_recommendations[symp_id].keys():
# #         print(user_recommendations[symp_id][product])