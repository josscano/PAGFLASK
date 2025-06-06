from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'josecano212223@gmail.com'
app.config['MAIL_PASSWORD'] = 'mmqd iwbd mwdj nnjd'

mail = Mail(app)

# Lista de productos (simulada por ahora)
productos = [
    {'id': 1, 'nombre': 'Gorra Negra', 'precio': 150},
    {'id': 2, 'nombre': 'Gorra Blanca', 'precio': 180},
    {'id': 3, 'nombre': 'Gorra Azul', 'precio': 160}
]

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Mostrar productos
@app.route('/pedidos', methods=['GET'])
def mostrar_productos():
    return render_template('pedidos.html', productos=productos)

# Agregar producto al carrito
@app.route('/agregar_carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(producto_id)
    session.modified = True
    flash('Producto agregado al carrito')
    return redirect(url_for('mostrar_productos'))

# Ver carrito
@app.route('/carrito')
def ver_carrito():
    ids = session.get('carrito', [])
    productos_en_carrito = [p for p in productos if p['id'] in ids]
    return render_template('carrito.html', productos=productos_en_carrito)

# Recibir datos del carrito y formulario desde JS y enviar correo
@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    data = request.get_json()
    datos = data.get('datos', {})
    carrito = data.get('carrito', [])

    detalle_productos = "\n".join(
        [f"{p.get('nombre', '')} - ${p.get('precio', '')}" for p in carrito]
    )

    mensaje = f"""
    Nuevo pedido:
    Nombre: {datos.get('nombre')}
    Dirección: {datos.get('direccion')}
    Teléfono: {datos.get('telefono')}
    Forma de pago: {datos.get('pago')}

    Productos:
    {detalle_productos}
    """

    msg = Message('Nuevo pedido de Style & Essence',
                  sender='Style & Essence <josecano212223@gmail.com>',
                  recipients=['antonioreyes282121@gmail.com'])
    msg.body = mensaje
    mail.send(msg)

    return jsonify({'mensaje': 'Compra recibida correctamente'})

# Enviar pedido por correo (formulario clásico)
@app.route('/pedidos', methods=['POST'])
def pedidos():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    instrucciones = request.form.get('instrucciones')
    
    ids = session.get('carrito', [])
    productos_en_carrito = [p for p in productos if p['id'] in ids]

    detalle_productos = "\n".join(
        [f"{p['nombre']} - ${p['precio']}" for p in productos_en_carrito]
    )

    mensaje = f"""
    Nuevo pedido:
    Nombre: {nombre}
    Email: {email}
    Instrucciones: {instrucciones}

    Productos:
    {detalle_productos}
    """

    msg = Message('Nuevo pedido de Style & Essence',
                  sender='Style & Essence <josecano212223@gmail.com>',
                  recipients=['antonioreyes282121@gmail.com'])
    msg.body = mensaje
    mail.send(msg)

    flash('¡Pedido enviado correctamente!')
    session.pop('carrito', None)  # Vaciar carrito después de enviar
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)