import requests

url = "http://localhost:5000/doar"
dados = {
    "titulo": "O Senhor dos Anéis",
    "categoria": "Fantasia",
    "autor": "J.R.R. Tolkien",
    "imagem_url": "https://images-americanas.b2w.io/produtos/01/00/img/5202808/2/5202808278_1GG.jpg"
}

response = requests.post(url, json=dados)
print("Status Code:", response.status_code)
print("Resposta:", response.json())