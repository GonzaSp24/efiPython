from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cellphoneSpStore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Equipo, Modelo, Marca, Categoria, Stock, Caracteristica, Accesorio

@app.route('/')
def index():
    equipos = Equipo.query.filter_by(eliminado=False).all()  # Filtrar los equipos eliminados
    return render_template('index.html', equipos=equipos)

@app.route('/equipos')
def listar_equipos():
    equipos = Equipo.query.filter_by(eliminado=False).all()  # Filtrar los equipos eliminados
    return render_template('listar_equipos.html', equipos=equipos)
@app.route('/equipo/nuevo', methods=['GET', 'POST'])
def nuevo_equipo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        modelo_id = request.form['modelo_id']
        categoria_id = request.form['categoria_id']
        costo = request.form['costo']
        stock_id = request.form['stock_id']
        marca_id = request.form['marca_id']
        caracteristicas_ids = request.form.getlist('caracteristicas')  # Se espera una lista de IDs
        accesorios_ids = request.form.getlist('accesorios')  # Se espera una lista de IDs

        nuevo_equipo = Equipo(
            nombre=nombre,
            modelo_id=modelo_id,
            categoria_id=categoria_id,
            costo=costo,
            stock_id=stock_id,
            marca_id=marca_id
        )
        db.session.add(nuevo_equipo)
        db.session.commit()

        # Procesar características
        for caracteristica_id in caracteristicas_ids:
            caracteristica = Caracteristica.query.get(int(caracteristica_id))
            if caracteristica:
                nuevo_equipo.caracteristicas.append(caracteristica)

        # Procesar accesorios
        for accesorio_id in accesorios_ids:
            accesorio = Accesorio.query.get(int(accesorio_id))
            if accesorio:
                nuevo_equipo.accesorios.append(accesorio)

        db.session.commit()
        return redirect(url_for('listar_equipos'))
    else:
        modelos = Modelo.query.all()
        categorias = Categoria.query.all()
        marcas = Marca.query.all()
        stocks = Stock.query.all()
        caracteristicas = Caracteristica.query.all()  # Obtener todas las características
        accesorios = Accesorio.query.all()
        return render_template('nuevo_equipo.html', modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks, caracteristicas=caracteristicas, accesorios=accesorios)


@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get(id)
    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.modelo_id = request.form['modelo_id']
        equipo.categoria_id = request.form['categoria_id']
        equipo.costo = request.form['costo']
        equipo.stock_id = request.form['stock_id']
        equipo.marca_id = request.form['marca_id']

        # Actualizar características
        caracteristicas = request.form['caracteristicas']
        equipo.caracteristicas.clear()
        for caracteristica in caracteristicas.split(','):
            if caracteristica.strip():
                nueva_caracteristica = Caracteristica(
                    tipo=caracteristica.strip(),
                    descripcion='',
                    equipo_id=equipo.id
                )
                db.session.add(nueva_caracteristica)

        # Actualizar accesorios
        accesorios = request.form.getlist('accesorios')
        equipo.accesorios = []
        for accesorio_id in accesorios:
            accesorio = Accesorio.query.get(int(accesorio_id))
            equipo.accesorios.append(accesorio)

        db.session.commit()
        return redirect(url_for('listar_equipos'))
    else:
        modelos = Modelo.query.all()
        categorias = Categoria.query.all()
        marcas = Marca.query.all()
        stocks = Stock.query.all()
        accesorios = Accesorio.query.all()
        return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, categorias=categorias, marcas=marcas, stocks=stocks, accesorios=accesorios)


@app.route('/equipo/eliminar/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get(id)
    if equipo:
        equipo.eliminado = True
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
