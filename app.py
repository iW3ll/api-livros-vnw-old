from flask import Flask, jsonify, request, render_template
import sqlite3
import os  
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # Seu frontend local
            "https://giveaway-books.vercel.app"  # Seu frontend em produção
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

@app.before_request
def before_request():
    time.sleep(0.1)  # Evita que o Render coloque a API em sleep

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Rota inicial (/)
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o index.html

# Rota para cadastrar um livro (POST /doar)
@app.route('/doar', methods=['POST'])
def doar_livro():
    dados = request.json

    # Verifica se todos os campos obrigatórios estão presentes
    if not all(key in dados for key in ['titulo', 'categoria', 'autor', 'imagem_url']):
        return jsonify({"erro": "Todos os campos são obrigatórios (titulo, categoria, autor, imagem_url)"}), 400

    # Conecta ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insere o livro no banco de dados
    cursor.execute('''
        INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
        VALUES (?, ?, ?, ?)
    ''', (dados['titulo'], dados['categoria'], dados['autor'], dados['imagem_url']))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

# Rota para listar todos os livros (GET /livros)
@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca todos os livros no banco de dados
    cursor.execute('SELECT id, titulo, categoria, autor, imagem_url FROM LIVROS')
    livros = cursor.fetchall()
    conn.close()

    # Converte os resultados para um formato JSON
    livros_json = [dict(livro) for livro in livros]
    return jsonify(livros_json)

# Rota para deletar um livro (DELETE /deletar/<id>)
@app.route('/deletar/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se o livro existe
    cursor.execute('SELECT id FROM LIVROS WHERE id = ?', (id,))
    livro = cursor.fetchone()

    if livro is None:
        conn.close()
        return jsonify({"erro": "Livro não encontrado"}), 404

    # Deleta o livro
    cursor.execute('DELETE FROM LIVROS WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Livro deletado com sucesso"}), 200

# Inicialização do banco de dados (cria a tabela LIVROS se não existir)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIVROS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Garante que o banco de dados esteja inicializado
    # Configurações para o Render:
    port = int(os.environ.get('PORT', 10000))  # Render usa a porta 10000
    app.run(host='0.0.0.0', port=port)