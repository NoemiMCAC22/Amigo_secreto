from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import json
import os

app = Flask(__name__)

nomes = []
nomes_sorteados = []

def load_data():
    global nomes_sorteados
    if os.path.exists("sorteio_data.json"):
        with open("sorteio_data.json", "r") as file:
            data = json.load(file)
            nomes_sorteados = data.get("nomes_sorteados", [])

def save_data():
    with open("sorteio_data.json", "w") as file:
        json.dump({"nomes_sorteados": nomes_sorteados}, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    global nomes
    if request.method == 'POST':
        nomes_input = request.form['nomes']
        nomes = [nome.strip() for nome in nomes_input.split(",") if nome.strip()]
        return redirect(url_for('index'))
    return render_template('index.html', nomes=nomes, nomes_sorteados=nomes_sorteados)

@app.route('/sorteio', methods=['POST'])
def sorteio():
    usuario = request.form['usuario']
    if usuario not in nomes:
        return jsonify({"error": "Seu nome não está na lista!"})

    nomes_disponiveis = [nome for nome in nomes if nome not in nomes_sorteados and nome != usuario]
    
    if not nomes_disponiveis:
        return jsonify({"info": "Todos os nomes já foram sorteados!"})

    sorteado = random.choice(nomes_disponiveis)
    nomes_sorteados.append(sorteado)
    save_data()
    return jsonify({"sorteado": sorteado})

if __name__ == '__main__':
    load_data()
    app.run(debug=True)
