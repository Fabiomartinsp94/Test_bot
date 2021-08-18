### Devnology_RPA_Test:

O desafio é:
Acessar esse site e pegar todos notebooks Lenovo ordenando do mais barato para o mais caro. Pegar todos os dados disponíveis dos produtos.

É interessante que o robô possa ser consumido por outros serviços. Recomendamos a criação de uma pequena REST Ful API JSON para deixar mais otimizado.

#### Dependencias do bot:

python==3.9.1
fastapi==0.68.0
selenium==3.141.0
selenium-wire==4.2.4
uvicorn==0.15.0
webdriver-manager==3.4.2

#### Funcionamento:
1- Entrar na root folder e usar o comando **uvicorn main:app --reload**
2- acessar a **localhost:8000/**, isso dará inicio ao bot
3- assim que o bot for finalizado, a rota de resultados **localhost:8000/results** estará pronta para ser acessada

