from seleniumwire import webdriver as wd #pip install selenium
from selenium.webdriver.chrome.options import Options #mostrando que o driver do selenium vai ser o chrome
from webdriver_manager.chrome import ChromeDriverManager

import csv
import json

### IMPORTS####


def rpa():

    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    lenovo_links = []
    list_specs = []

    ###VARIABLES###


    option = Options()
    option.headless = True

    driver = wd.Chrome(ChromeDriverManager().install()) #automaticamente instalar o Chromium correto

    driver.implicitly_wait(60) #limite de tempo de espera do selenium

###OPTIONS###

    driver.get(url) #Abre a url

    product_component = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div") #procura a div

    products_list = product_component.find_elements_by_class_name("caption") #procura a classe caption dentro da div supra


    #Looping para pegar todos os links dos produtos que contem lenovo no titulo

    for product in products_list: 
        data = product.find_element_by_class_name("title").get_attribute("title")

        if "lenovo" in data.lower():
            link = product.find_element_by_class_name("title").get_attribute("href")
            lenovo_links.append(link)

    #Looping principal do bot, abre link por link do array, e pega a descrição de cada notebook

    for link in lenovo_links:
        driver.get(link)

        validation = True #Favorece o looping while true, para buscar as informações sem erro

        while validation:
            lenovo_especification = driver.find_element_by_class_name("col-lg-10")
            especific_components = lenovo_especification.find_element_by_class_name("description") 
            #pego o webelement que contem a descrição

            if especific_components.text != "":
                validation = False

        #split na string webelement.text, por vírgula, já que a descrição é um csv
        array_splitted = especific_components.text.split(',')
        
        #o split() me retorna um array de elementos

        mydict = {}
        mydict["specs"] = []
        mydict["model"] = array_splitted[0].strip()
        mydict["specs"] = [spec.strip() for spec in array_splitted[1:]]
        
        #crio um dict genérico e separo o modelo(arr[0]) das specs(arr[1 até infinito]) 

        buttons = lenovo_especification.find_elements_by_class_name("btn")


        for button in buttons:
            button.click()
            hdd_number = button.text
            price = lenovo_especification.find_element_by_class_name("pull-right").text

            all_classes = button.get_attribute("class")

            if "disabled" in all_classes:
                mydict[hdd_number] = [price,"disabled"]
            else:
                mydict[hdd_number] = [price,"enabled"]

        reviews_div = lenovo_especification.find_element_by_class_name("ratings")
        reviews = reviews_div.find_element_by_tag_name("p").text
        
        rating = len(reviews_div.find_elements_by_class_name("glyphicon-star"))

        mydict["rating"] =  str(rating) + "/5"
        mydict["review"] =  reviews


        list_specs.append(mydict)



    driver.quit()
        

    with open(r'files/lenovo.json', 'w') as f:
        json.dump(list_specs, f)

    return 1
