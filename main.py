import google.generativeai as genai
import os
import json
import pandas as pd

companies = [
    {"Company ID": 5875, "Company name": "Solarkal", "Company website": "https://www.solarkal.com/"},
    {"Company ID": 11917, "Company name": "H2Scan", "Company website": "https://h2scan.com/"},
    {"Company ID": 34005, "Company name": "Eo Charging", "Company website": "https://www.eocharging.com/"},
    {"Company ID": 65212, "Company name": "Prewave", "Company website": "https://www.prewave.com/"},
    {"Company ID": 18533, "Company name": "Viriciti", "Company website": "https://www.chargepoint.com/"},
    {"Company ID": 2805, "Company name": "EasyMile", "Company website": "https://www.easymile.com/"},
    {"Company ID": 101741, "Company name": "Everstream", "Company website": "https://www.everstream.ai/"},
    {"Company ID": 110133, "Company name": "Altus Power", "Company website": "https://www.altuspower.com/"},
    {"Company ID": 12605, "Company name": "Charm Industrial", "Company website": "https://www.charmindustrial.com/"},
    {"Company ID": 105894, "Company name": "Isotropic Systems", "Company website": "https://www.all.space/"},
    {"Company ID": 400, "Company name": "Caban Systems", "Company website": "https://www.cabanenergy.com/"},
    {"Company ID": 34204, "Company name": "BioBTX", "Company website": "https://biobtx.com/"},
    {"Company ID": 6134, "Company name": "Hydrogenious LOHC", "Company website": "https://hydrogenious.net/"},
    {"Company ID": 12008, "Company name": "Iogen", "Company website": "https://www.iogen.com/"},
    {"Company ID": 6997, "Company name": "Infinited Fiber Company", "Company website": "https://infinitedfiber.com/"}
]

final_list=[]

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash',generation_config={"response_mime_type": "application/json"})
for i in companies:
    print(i['Company website'])
    response = model.generate_content("""scrape this website for description, products, headquarters, \
                locations, clients, news:- %s Using this JSON schema:\
                comp_web = {"description": str,"headquarters":str,"products":list,"clients":list,"locations":list, \
                    "news":["news_title":str,"news_date":str,"news_url":str,"news_summary":str] \
                """% i['Company website'])
    json_data= json.loads(response.text)
    json_data['Company ID']= i['Company ID']
    json_data['Company name']= i['Company name']
    json_data['Company website']= i['Company website']
    final_list.append(json_data)
    

print(final_list)

# Create DataFrames for general information and news information
company_data = []
news_data = []

for entry in final_list:
    company_data.append({
        "Company website": entry["Company website"],
        "Company name": entry["Company name"],
        "Company ID": entry["Company ID"],
        "Description": entry["description"],
        "Headquarters": entry["headquarters"],
        "Products": ", ".join(entry["products"]),
        "Clients": ", ".join(entry["clients"]),
        "Locations": ", ".join(entry["locations"]),
    })
    
    for news in entry["news"]:
        news_data.append({
            "Company ID": entry["Company ID"],
            "News Title": news["news_title"],
            "News Date": news["news_date"],
            "News URL": news["news_url"],
            "News Summary": news["news_summary"],
        })

#Create DataFrames
df_company = pd.DataFrame(company_data)
df_news = pd.DataFrame(news_data)

#Write to excel file
with pd.ExcelWriter('company_data.xlsx', engine='openpyxl') as writer:
    df_company.to_excel(writer, sheet_name='Company Info', index=False)
    df_news.to_excel(writer, sheet_name='News Info', index=False)
