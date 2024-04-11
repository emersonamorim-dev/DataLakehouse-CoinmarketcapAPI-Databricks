from flask import Flask, render_template_string
import plotly.graph_objects as go
from pymongo import MongoClient
import pandas as pd

# Conectar ao MongoDB 
client = MongoClient("mongodb://localhost:27017/")
db = client['your_db']
collection = db['your_collection']
data_dash = pd.DataFrame(list(collection.find()))

# Configuração inicial do Flask
app = Flask(__name__)

@app.route('/')
def visualize_data():

    # Dados simulados substituindo a variável 'data' original
    import random
    data = [[day, hour, random.randint(1, 10)] for day in range(7) for hour in range(24)]

    # Inicializando a figura
    fig = go.Figure()

    hours = [
        '12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a',
        '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p'
    ]

    days = ['Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday', 'Sunday']

    for idx, day in enumerate(days):
        day_data = [d for d in data if d[0] == idx]
        x_data = [hours[d[1]] for d in day_data]
        y_data = [d[2] for d in day_data]
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='markers',
            marker=dict(size=[d[2]*4 for d in day_data]),  
            name=day
        ))

    fig.update_layout(
        title="Visualização de Preços do Bitcoin",
        xaxis_title="Hora",
        yaxis_title="Valor",
        legend_title="Dia da Semana"
    )
    

    # Converte a figura para HTML e renderizar com Flask
    plot_div = fig.to_html(full_html=False)

    # Template HTML para renderização diretamente com Flask
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Flask Plotly - Streamlit</title>
    </head>
    <body>
        <h1>Dashboard de Dados</h1>
        {{ plot_div|safe }}
    </body>
    </html>
    """

    return render_template_string(template, plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
