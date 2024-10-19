import io
import sympy as sp
import numpy as np
import plotly.graph_objs as go
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
x = sp.Symbol('x')

def esImpar(funcion):
    return sp.simplify(funcion.subs(x, -x)) == -funcion

#Integrales definidas
def generarGrafico(funcion, a, b):
    if esImpar(funcion):
        integral_definida = sp.integrate(sp.Abs(funcion), (x, a, b))
    else:
        integral_definida = sp.integrate(funcion, (x, a, b))

    funcion_numerica = sp.lambdify(x, funcion, "numpy")

    #Calcular espacio para ejes x y
    x_vals = np.linspace(float(a) - 1, float(b) + 1, 400)
    y_vals = funcion_numerica(x_vals)
    y_min = min(y_vals) - 1
    y_max = max(y_vals) + 1

    fig = go.Figure()

    #Dibujar función
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'y = {funcion}'))

    #Dibujar área
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, fill='tozeroy', mode='none',
                             fillcolor='rgba(0, 236, 245, 71)', name=f'Área = {integral_definida}'))

    #Configuración
    fig.update_layout(
        title=f'Gráfica de la función: {funcion}',
        xaxis_title='x',
        yaxis_title='f(x)',
        hovermode="x unified",
        shapes=[
            #Dibujar je x
            dict(type="line", x0=float(a) - 1, x1=float(b) + 1, y0=0, y1=0, line=dict(color="black", width=2)),
            #Dibujar eje y
            dict(type="line", x0=0, x1=0, y0=y_min, y1=y_max, line=dict(color="black", width=2)),
        ]
    )

    return fig.to_json(), integral_definida

@app.route('/')
def index():
    return render_template('index.html')

#Endpoint que retorna gráfica o integral indefinida
@app.route('/plot', methods=['POST'])
def plot_post():
    funcion_str_global = request.form['funcion']
    funcion = sp.sympify(funcion_str_global)

    tipo_integral = request.form.get('tipo_integral')

    if tipo_integral == 'definida':
        a_global = float(request.form['a'])
        b_global = float(request.form['b'])
        grafico_json, area = generarGrafico(funcion, a_global, b_global)

        #Integral definida
        return jsonify({
            'grafico': grafico_json,
            'resultado': f''
        })
    else:
        #Integral indefinida
        integral_indefinida = sp.integrate(funcion, x)
        return jsonify({
            'grafico': None,
            'resultado': f'Integral indefinida: {integral_indefinida} + C'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
