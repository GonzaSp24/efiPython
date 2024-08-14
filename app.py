from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import NuevoEquipoForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cellphoneSpStore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave'


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
    form = NuevoEquipoForm()

    # Poblar opciones de selección
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.all()]
    form.categoria_id.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]
    form.marca_id.choices = [(marca.id, marca.nombre) for marca in Marca.query.all()]
    form.stock_id.choices = [(stock.id, stock.cantidad) for stock in Stock.query.all()]
    form.caracteristicas.choices = [(caracteristica.id, caracteristica.tipo) for caracteristica in Caracteristica.query.all()]
    form.accesorios.choices = [(accesorio.id, accesorio.tipo) for accesorio in Accesorio.query.all()]

    if form.validate_on_submit():
        nuevo_equipo = Equipo(
            nombre=form.nombre.data,
            modelo_id=form.modelo_id.data,
            categoria_id=form.categoria_id.data,
            costo=form.costo.data,
            stock_id=form.stock_id.data,
            marca_id=form.marca_id.data
        )
        db.session.add(nuevo_equipo)
        db.session.commit()

        for caracteristica_id in form.caracteristicas.data:
            caracteristica = Caracteristica.query.get(int(caracteristica_id))
            if caracteristica:
                nuevo_equipo.caracteristicas.append(caracteristica)

        for accesorio_id in form.accesorios.data:
            accesorio = Accesorio.query.get(int(accesorio_id))
            if accesorio:
                nuevo_equipo.accesorios.append(accesorio)

        db.session.commit()
        return redirect(url_for('listar_equipos'))

    return render_template('nuevo_equipo.html', form=form)


@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get(id)
    form = NuevoEquipoForm(obj=equipo)  # Cargar el formulario con datos del equipo

    # Poblar opciones de selección
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.all()]
    form.categoria_id.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]
    form.marca_id.choices = [(marca.id, marca.nombre) for marca in Marca.query.all()]
    form.stock_id.choices = [(stock.id, stock.cantidad) for stock in Stock.query.all()]
    form.caracteristicas.choices = [(caracteristica.id, caracteristica.tipo) for caracteristica in Caracteristica.query.all()]
    form.accesorios.choices = [(accesorio.id, accesorio.tipo) for accesorio in Accesorio.query.all()]

    if form.validate_on_submit():
        form.populate_obj(equipo)
        equipo.caracteristicas = [Caracteristica.query.get(int(id)) for id in form.caracteristicas.data]
        equipo.accesorios = [Accesorio.query.get(int(id)) for id in form.accesorios.data]
        db.session.commit()
        return redirect(url_for('listar_equipos'))

    return render_template('editar_equipo.html', form=form)



@app.route('/equipo/eliminar/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get(id)
    if equipo:
        equipo.eliminado = True
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
