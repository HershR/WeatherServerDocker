from .models import OwmCities
from .weather import add_city
from flask import (
    current_app, Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('cities', __name__)

owm_api_key = current_app.config['OPENWEATHERMAP_API_KEY']



@bp.route('/')
def index():
    cities = OwmCities.query.order_by(OwmCities.city_name.asc()).all()
    return render_template('cities/index.html', cities=cities)


# search and add city by its coordinates
@bp.route('/search/coordinates', methods=('GET', 'POST'))
def search_by_coordinates():
    if request.method == 'POST':
        error = None
        coordinate = str(request.form['coordinate'])
        coord = []
        if not coordinate:
            error = 'Enter Coordinates'
        elif ',' not in coordinate:
            error = 'Check format'
        else:
            coordinate = coordinate.replace(" ", "")
            coord = coordinate.split(',')

        #check for proper coordinate format
        if len(coord) != 2:
            error = 'Check format'
        else:
            latitude = float(coord[0])
            longitude = float(coord[1])
            if not latitude:
                error = 'Latitude is required.'
            if not longitude:
                error = 'Longitude is required.'
        if error is None:
            add_city(latitude, longitude)
            return redirect(url_for('cities.index'))
        flash(error)
    return render_template('cities/searchcoordinates.html')
