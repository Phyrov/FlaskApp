from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import googlemaps
import os

app = Flask(__name__)

####################
# Conexión a la bd #
####################
app.config['MYSQL_HOST'] = 'eu-cdbr-west-01.cleardb.com'
app.config['MYSQL_USER'] = 'bab80682b3d3c1'
app.config['MYSQL_PASSWORD'] = '5e39c98b'
app.config['MYSQL_DB'] ='heroku_dc7f8cd26302a96'
mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/comparador', methods=['POST','GET'])
def Comparador():
    if(request.method == 'POST'):
        nombre1=request.form['nombre1']
        nombre2=request.form['nombre2']

        cur2=mysql.connection.cursor()
        cur2.execute("SELECT * FROM productos3 WHERE nombre LIKE %s", [nombre1])
        movil1 = cur2.fetchone()

        cur2.execute("SELECT * FROM productos3 WHERE nombre LIKE %s", [nombre2])
        movil2 = cur2.fetchone()

        return render_template('comparador.html', datos1 = movil1, datos2 = movil2)

    if(request.method=='GET'):
        return render_template('comparador.html')

@app.route('/busqueda', methods=['POST','GET'])
def Busqueda():
    if(request.method == 'POST'):
        nombre=request.form['marca']
        preciomin=request.form['preciomin']
        preciomax=request.form['preciomax']
        memoriamin=request.form['memoriamin']
        memoriamax=request.form['memoriamax']
        rammin=request.form['rammin']
        rammax=request.form['rammax']
        
        nombre= "%"+nombre+"%"

        cur=mysql.connection.cursor()
        
        consulta = "SELECT * FROM productos3 WHERE (precio BETWEEN %s AND %s) AND (almacenamiento BETWEEN %s AND %s) AND (ram BETWEEN %s AND %s) AND (nombre LIKE %s)"
        cur.execute(consulta, (preciomin, preciomax, memoriamin, memoriamax, rammin, rammax, nombre))
        datos = cur.fetchall()

        # Para redireccionar 
        return render_template('busqueda.html', moviles = datos)
    if(request.method=='GET'):
        return render_template('busqueda.html')


@app.route('/mapa')
def mapaa():
    return render_template('mapa.html')

@app.route("/latlng")
def Prueba():

    ###############################################################
    # API que obtiene latitud y longitud a patir de una dirección #
    ###############################################################

    os.environ['GOOGLE_MAPS_API_KEY'] = 'AIzaSyDKiveQ01pccKu3Y-mV2KFz4_FrvlEdTUY'
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    gmaps_client = googlemaps.Client(api_key)
    geocode_result = gmaps_client.geocode('Calle Hipócrates, s/n, 18100, Granada')
    result = geocode_result[0]
    
    lat1 = result['geometry']['location']['lat']
    lon1 = result['geometry']['location']['lng']

    #print('Latitude: ',lat1)
    #print('Longitud: ',lon1)
    
    geocode_result2 = gmaps_client.geocode('Calle Luis Buñuel, 18197 Pulianas, Granada')
    result2 = geocode_result2[0]

    lat2 = result2['geometry']['location']['lat']
    lon2 = result2['geometry']['location']['lng']

    #print('Latitude: ',lat2)
    #print('Longitud: ',lon2)

    return render_template('latlng.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)