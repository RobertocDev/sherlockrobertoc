from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/sherlock', methods=['GET'])
def sherlock():
    # Pegar o nome de usuário da requisição
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Por favor, forneça um nome de usuário."}), 400

    # Executar o Sherlock
    try:
        # Comando para rodar o Sherlock e salvar os resultados em um arquivo de texto
        command = f"py sherlock.py {username} --output {username}.txt"
        os.system(command)

        # Verificar se o arquivo de texto foi criado
        if not os.path.exists(f"{username}.txt"):
            return jsonify({"error": f"Nenhum resultado encontrado para o usuário '{username}'."}), 404

        # Ler o arquivo de texto gerado
        with open(f"{username}.txt", "r", encoding="utf-8") as file:
            content = file.read()

            # Verificar se o arquivo está vazio
            if not content.strip():
                return jsonify({"error": f"Nenhum resultado encontrado para o usuário '{username}'."}), 404

            # Processar o conteúdo do arquivo de texto
            results = []
            for line in content.splitlines():
                if line.strip():  # Ignorar linhas vazias
                    results.append({"url": line.strip()})

        # Retornar os resultados
        return jsonify(results)

    except Exception as e:  # Adicionei os dois pontos aqui
        return jsonify({"error": f"Erro ao executar o Sherlock: {str(e)}"}), 500

if __name__ == '__main__':
    # Rodar a API na porta 5000
    app.run(host='0.0.0.0', port=5000)