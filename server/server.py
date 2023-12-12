import csv
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def read_values_from_csv(file_path, num_of_values):
    values = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i, row in enumerate(csv_reader):
            if i < num_of_values:
                try:
                    value = float(row[0].replace(',', '.'))  # Manejar decimales con punto
                    values.append(value)
                except (ValueError, IndexError):
                    pass  # Ignora los valores no numéricos o errores de índice
            else:
                break
    return values

# /api/calculate
@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        # Obtiene el número desde la solicitud
        num = float(request.get_data(as_text=True))
        
        # Lee los valores desde el archivo CSV
        csv_values = read_values_from_csv('data.csv', int(num))
        
        # Realiza las operaciones matemáticas
        results = [num + value for value in csv_values]
        
        # Devuelve los resultados como un JSON
        return jsonify({'results': results})
    except ValueError:
        return jsonify({
            'error': 'Invalid input. Please provide a valid number.'
        })

if __name__ == '__main__':
    app.run(debug=True, port=8080)