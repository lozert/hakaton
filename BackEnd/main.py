from flask import Flask, request, jsonify
from flask_cors import CORS

from prompt_runner_hug import main, save_json, load_prompt_from_json

app = Flask(__name__)
CORS(app)  # Разрешаем все запросы CORS

@app.route('/', methods=['POST'])
def handle_request():
    try:
        data = [request.get_json()]
        print(data)
        save_json(data, name="input")
        main()
        output = load_prompt_from_json("output.json")
        response_data = {
            "message": "JSON received successfully",
            "received_data": str(output)
        }
        return jsonify(response_data), 200
    except Exception as e:
        # Возвращаем ошибку при исключении
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ip и порт на котором запускается backend часть 
    app.run(host='192.168.31.243', port=8000, debug=True)
