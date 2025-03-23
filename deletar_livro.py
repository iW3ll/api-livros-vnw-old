import requests

# URL da API
url = "http://localhost:5000/deletar/1"  # Substitua 1 pelo ID do livro que deseja deletar

# Envia a requisição DELETE
response = requests.delete(url)

# Exibe a resposta
print("Status Code:", response.status_code)
print("Resposta:", response.json())