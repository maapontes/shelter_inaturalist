import requests
import json
import csv
import time

API_DOMAIN = "https://www.inaturalist.org"

def get_request_to_api(route):
    data = requests.get(f'{API_DOMAIN}/{route}')
    try:
        return (data.json())
    except:
        return ("Error")

def post_request_to_api(route, access_token=None, json={}):
    data = requests.post(f'{API_DOMAIN}/{route}')
    return (data.json())

frogs = [
    [
        "id_observation",
        "species",
        "lat",
        "long",
        "hour"
    ]
]

pass_first = True

with open("URLs_list.csv", encoding='ISO-8859-1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    ct=0
    sleep_each = 20
    rows=[]
    for row in csv_reader:
        rows.append(row)
    for row in rows:
        if pass_first==True and ct==0:
            ct+=1
            print(f"Ignoring row {ct}", "                                  ", end="\r")
        else:
            id_observation = row[0]
            id_link = row[1].split("/")[-1]
            if "+" in id_link:
                id_link = id_link.replace("+", "")
            inaturalist_reponse = get_request_to_api(f"observations/{id_link}.json")
            if inaturalist_reponse != "Error" and not "error" in inaturalist_reponse.keys():           
                try:
                    tempo = inaturalist_reponse["observed_on_string"]
                except:
                    if "observed_on_string" in inaturalist_reponse.keys():
                        tempo = inaturalist_reponse["observed_on_string"]
                    else:
                        tempo = "NA"
                the_row = [
                        id_observation,
                        inaturalist_reponse["taxon"]["name"],
                        inaturalist_reponse["latitude"],
                        inaturalist_reponse["longitude"],
                        tempo
                ]
                frogs.append(the_row)
                ct+=1
                if ct%sleep_each==0:
                    sec = 20
                    print(f"20 requests, sleeping {sec} seconds", "                  ", end="\r")
                    time.sleep(sec)
                print(f"row: {ct} of {len(rows)}", "                                  ", end="\r")
            else:
                print(f"Error on row {ct}, link: observations/{id_link}")
                print(inaturalist_reponse)

with open('output_sheet.csv', mode='w') as output_sheet:
    output_writer = csv.writer(output_sheet, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for frog in frogs:
        output_writer.writerow(frog)
        
print("Done!                                  ", end="\r")

