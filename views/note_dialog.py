import tempfile
import folium
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFormLayout, QDialogButtonBox, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

class JavaScriptInterface(QObject):
    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog

    @pyqtSlot(float, float)
    def handleMapClick(self, lat, lng):
        self.dialog.lat_edit.setText(str(lat))
        self.dialog.lon_edit.setText(str(lng))

class NoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")

        # Create map view
        self.map_view = QWebEngineView()
        self.map_file = self.create_map_html()
        self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))

        # Create input fields
        self.note_edit = QLineEdit()
        self.lat_edit = QLabel()
        self.lon_edit = QLabel()

        # Layouts
        form_layout = QFormLayout()
        form_layout.addRow("Note:", self.note_edit)
        form_layout.addRow("Latitude:", self.lat_edit)
        form_layout.addRow("Longitude:", self.lon_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.map_view)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Set default values for latitude and longitude
        self.lat_edit.setText("")
        self.lon_edit.setText("")

        # Set up JavaScript interface
        self.web_channel = QWebChannel()
        self.js_interface = JavaScriptInterface(self)
        self.web_channel.registerObject("python", self.js_interface)
        self.map_view.page().setWebChannel(self.web_channel)

        # Initialize JavaScript after page load
        self.map_view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            self.map_view.page().runJavaScript('initializeMap();')

    def create_map_html(self):
        # Create a temporary file for the map
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        temp_file.close()

        # Create a folium map
        map_center = [51.5074, -0.1278]  # Default center (e.g., London)
        folium_map = folium.Map(location=map_center, zoom_start=13)

        # Add JavaScript for handling clicks
        folium_map.get_root().html.add_child(folium.Element('''
           <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
           <script>
           var python = null;
           new QWebChannel(qt.webChannelTransport, function(channel) {
               python = channel.objects.python;
           });
           var popup = L.popup();
           function initializeMap() {
               var map = window[document.querySelector('.leaflet-container').id];
               if (map) {
                   map.on('click', function(e) {
                       var lat = e.latlng.lat;
                       var lng = e.latlng.lng;
                       console.log('Clicked coordinates:', lat, lng);
                       popup
                       .setLatLng(e.latlng)
                       .setContent("You clicked the map at " + e.latlng.toString())
                       .openOn(map);
                       
                       if (window.python) {
                           python.handleMapClick(lat, lng);
                       } else {
                           console.error('Python interface not available');
                       }
                   });
               } else {
                   console.error('Map is not initialized');
               }
           }
           </script>
        '''))

        # Save the map to the temp HTML file
        folium_map.save(temp_file.name)

        return temp_file.name

    def get_data(self):
        return {
            'note': self.note_edit.text(),
            'latitude': self.lat_edit.text(),
            'longitude': self.lon_edit.text()
        }
