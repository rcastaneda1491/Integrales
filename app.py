import io
import sympy as sp
import numpy as np
import plotly.graph_objs as go
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
x = sp.Symbol('x')

def integrar_indefinida(funcion):
    integral_indefinida = sp.integrate(funcion, x)
    return str(integral_indefinida) + ' + C'

#Integrales definidas
def generar_grafico(funcion, a, b):
    
    integral_definida = sp.integrate(funcion, (x, a, b))
    funcion_numerica = sp.lambdify(x, funcion, "numpy")

    #Rango de valores
    x_vals = np.linspace(float(a), float(b), 400)
    y_vals = funcion_numerica(x_vals)

    #Generar g´rafica
    fig = go.Figure()

    #Añadir línea de la función
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'y = {funcion}'))

    #Añadir area a la gráfica
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, fill='tozeroy', mode='none',
                             fillcolor='rgba(0, 236, 245, 71)', name=f'Área = {integral_definida}'))

    #Configuración
    fig.update_layout(
        title=f'Resultado de la integral de: {funcion}',
        xaxis_title='x',
        yaxis_title='f(x)',
        hovermode="x unified"
    )

    return fig.to_json(), integral_definida

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot_post():
    funcion_str_global = request.form['funcion']
    funcion = sp.sympify(funcion_str_global)

    tipo_integral = request.form.get('tipo_integral')

    if tipo_integral == 'definida':
        #Integral definida
        a_global = float(request.form['a'])
        b_global = float(request.form['b'])
        grafico_json, area = generar_grafico(funcion, a_global, b_global)

        return jsonify({
            'grafico': grafico_json,
            'resultado': f'Resultado de función: {funcion}'
        })
    else:
        #Integral indefinida
        integral_indefinida = integrar_indefinida(funcion)

        return jsonify({
            'grafico': None,
            'resultado': f'Integral indefinida: {integral_indefinida}'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
