# Importing required functions
import pandas
import folium
from flask import Flask, render_template, request
from fileinput import filename

# Flask constructor
app = Flask(__name__)

# Root endpoint
@app.get('/')
def upload():
	return render_template('upload-excel.html')


@app.post('/view')
def view():
	file = request.files['file']
	file.save(file.filename)
	data = pandas.read_excel(file)
	data.to_html('templates/POINTS.html')
	
	m=folium.Map(location=[data.lat.mean(), data.lon.mean()],
              zoom_start=7, height='80%', width='100%')
	for alias,lon,lat in zip(data['alias'],data['lon'],data['lat']):
		folium.Marker([lat,lon], popup="<i>"+alias+"</i>",
                tooltip='Pinchame!').add_to(m)
 
	m.save('templates/map.html')
	
	return render_template('upload-excel.html')


# Main Driver Function
if __name__ == '__main__':
	# Run the application on the local development server
	app.run(debug=True)
