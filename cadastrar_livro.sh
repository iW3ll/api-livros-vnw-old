curl -X POST http://localhost:5000/doar \
-H "Content-Type: application/json" \
-d '{
    "titulo": "Dom Quixote",
    "categoria": "Literatura Clássica",
    "autor": "Miguel de Cervantes",
    "imagem_url": "http://exemplo.com/capa_dom_quixote.jpg"
}'