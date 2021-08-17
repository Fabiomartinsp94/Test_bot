from seleniumwire import webdriver as wd #pip install selenium
from selenium.webdriver.chrome.options import Options #mostrando que o driver do selenium vai ser o chrome
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import FastAPI
import csv
import json

### IMPORTS####

app = FastAPI()

url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
lenovo_links = []
lenovo_json = []
list_specs = []
prices_review = []

###VARIABLES###

@app.get("/")
def read_root():

    with open(r'lenovo.json', 'r') as f:
        response = json.load(f)

    return response

###ROUTES###

option = Options()
option.headless = True

driver = wd.Chrome(ChromeDriverManager().install()) #automaticamente instalar o Chromium correto

driver.implicitly_wait(60) #limite de tempo de espera do selenium

###OPTIONS###

driver.get(url) 

product_component = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div")

products_list = product_component.find_elements_by_class_name("caption")

for product in products_list:
    data = product.find_element_by_class_name("title").get_attribute("title")

    if "lenovo" in data.lower():
        link = product.find_element_by_class_name("title").get_attribute("href")
        lenovo_links.append(link)


for link in lenovo_links:
    driver.get(link)

    validation = True


    while validation:
        lenovo_especification = driver.find_element_by_class_name("col-lg-10")
        especific_components = lenovo_especification.find_element_by_class_name("description")

        if especific_components.text != "":
            validation = False

    
    buttons = lenovo_especification.find_elements_by_class_name("btn")
    hdd = {}
    ratings = {}
    reviews_arr = []

    for button in buttons:
        button.click()
        hdd_number = button.text
        price = lenovo_especification.find_element_by_class_name("pull-right").text

        all_classes = button.get_attribute("class")

        if "disabled" in all_classes:
            hdd[hdd_number] = [price,"disabled"]
        else:
            hdd[hdd_number] = [price,"enabled"]

    reviews_div = lenovo_especification.find_element_by_class_name("ratings")
    reviews = reviews_div.find_element_by_tag_name("p").text
    
    rating = len(reviews_div.find_elements_by_class_name("glyphicon-star"))

    hdd["rating"] =  str(rating) + "/5"
    hdd["review"] =  reviews


    prices_review.append(hdd)
    lenovo_json.append(especific_components.text)
    
    #print(prices)


with open(r'lenovo.csv', 'w', encoding='UTF8') as file:
    file.write("\n".join(lenovo_json))


driver.quit()

final_json = []

with open(r'lenovo.csv', 'r') as infile:
    reader = csv.reader(infile)
    with open(r'new_lenovo.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        


        for i, row in enumerate(reader):
            mydict = {}
            mydict["components"] = []
            mydict["model"] = row[0].strip()

            for index, value in enumerate(row):
                if index >= 1:
                    mydict["components"].append(row[index].strip())

            list_specs.append(mydict)

for i, line in enumerate(list_specs):
    z = list_specs[i] | prices_review[i]
    final_json.append(z)        
 

with open(r'lenovo.json', 'w') as f:
    response_json = json.dump(final_json, f)


