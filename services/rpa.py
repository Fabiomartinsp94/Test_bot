### IMPORTS####
from seleniumwire import webdriver as wd #pip install selenium
from selenium.webdriver.chrome.options import Options #mostrando que o driver do selenium vai ser o chrome
from operator import itemgetter
from webdriver_manager.chrome import ChromeDriverManager

import json


###FUNCTION_BOT###

def rpa():

###VARIABLES###
    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    lenovo_links = []
    list_json = []

###OPTIONS/CONFIGS###

    option = Options()
    option.headless = True
    option.add_argument("window-size=1920x1080")

    driver = wd.Chrome(ChromeDriverManager().install(), options=option) #automaticamente instalar o Chromium correto


    driver.implicitly_wait(60) #limite de tempo de espera do selenium

###BOT_START###

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

        validation = True #Favorece o looping while true, para não aceitar informações vazias. 

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
        

        reviews_div = lenovo_especification.find_element_by_class_name("ratings")
        reviews = reviews_div.find_element_by_tag_name("p").text
        
        rating = len(reviews_div.find_elements_by_class_name("glyphicon-star"))
        #conto quantos elementos "estrela" tem no produto

        #transformo em numeral, e adiciono a quantidade de review 

        mydict["rating"] =  str(rating) + "/5"
        mydict["review"] =  reviews

        buttons = lenovo_especification.find_elements_by_class_name("btn")

        #looping para clicar em todos os botões, pegar os numeros de hdd, o preço e se tem em estoque [disabled]
        for button in buttons:
            button.click()

            #Cópia para inserção de dados, sem sobreescrever os dados do dict anterior
            loop_dict = mydict.copy()

            hdd_number = button.text
            value_hdd_number = hdd_number

            #pega o preço, tira o $ e transforma em float para dar SORT
            price = lenovo_especification.find_element_by_class_name("pull-right").text
            price_float = float(price.replace('$',""))
            value_price_float = price_float

            loop_dict["price"] = value_price_float
            loop_dict["hdd"] = value_hdd_number

            all_classes = button.get_attribute("class")
            #pego todas as classes e se houver "disabled" entre elas, passo pro dict
           
            if "disabled" in all_classes:
                loop_dict["stock"] = "out_of_stock"
            else:
                loop_dict["stock"] = "in_stock"

            #insiro o dicionário em uma lista
            list_json.append(loop_dict)


    #fecho o chrome
    driver.quit()

    #dou sort na list pela key "price"   
    list_sorted = sorted(list_json, key=itemgetter("price"))

    #monto um Json com a lista atualizada
    with open(r'files/lenovo.json', 'w') as f:
        json.dump(list_sorted, f)

