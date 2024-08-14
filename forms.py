from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class NuevoEquipoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    modelo_id = SelectField('Modelo', coerce=int)
    categoria_id = SelectField('Categoría', coerce=int)
    costo = FloatField('Costo', validators=[DataRequired()])
    stock_id = SelectField('Stock', coerce=int)
    marca_id = SelectField('Marca', coerce=int)
    caracteristicas = SelectMultipleField('Características', coerce=int)
    accesorios = SelectMultipleField('Accesorios', coerce=int)
