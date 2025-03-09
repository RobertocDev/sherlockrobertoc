from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/sherlock', methods=['GET'])
def sherlock():
    # Pegar o nome de usuário da requisição
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Por favor, forneça um nome de usuário."}), 400

    # Caminho do script Sherlock
    sherlock_script = 'sherlock.py'

    # Verificar se o script Sherlock existe
    if not os.path.exists(sherlock_script):
        return jsonify({"error": "O script Sherlock não foi encontrado no servidor."}), 500

    try:
        # Executar o Sherlock e salvar os resultados em um arquivo de texto
        command = ['python', sherlock_script, username, '--output', f'{username}.txt']
        result = subprocess.run(command, capture_output=True, text=True)

        # Verificar se o comando foi bem-sucedido
        if result.returncode != 0:
            return jsonify({"error": f"Erro ao executar o Sherlock: {result.stderr}"}), 500

        # Verificar se o arquivo de texto foi criado
        output_file = f'{username}.txt'
        if not os.path.exists(output_file):
            return jsonify({"error": f"Nenhum resultado encontrado para o usuário '{username}'."}), 404

        # Ler o arquivo de texto gerado
        with open(output_file, "r", encoding="utf-8") as file:
            content = file.read()

            # Verificar se o arquivo está vazio
            if not content.strip():
                return jsonify({"error": f"Nenhum resultado encontrado para o usuário '{username}'."}), 404

            # Processar o conteúdo do arquivo de texto
            results = [{"url": line.strip()} for line in content.splitlines() if line.strip()]

        # Retornar os resultados
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"Erro ao executar o Sherlock: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
