from flask import Flask, render_template, request
import requests
import pycountry

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        name = request.form['name']
        response = requests.get("https://api.nationalize.io", params={"name": name})

        if response.status_code == 200:
            data = response.json()
            if data['country']:
                country_code = data['country'][0]['country_id']
                probability = data['country'][0]['probability']
                country_name = pycountry.countries.get(alpha_2=country_code).name
                resultado = f"La nacionalidad más probable de {name} es {country_name} con una probabilidad del {probability*100:.2f}%"
            else:
                resultado = "No se encontró una nacionalidad para este nombre."
        else:
            resultado = "Error al conectarse con la API."

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)

