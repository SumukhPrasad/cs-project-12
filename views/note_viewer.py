import tempfile
import folium
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class NoteViewer(QDialog):
    def __init__(self, note_id, note_text, latitude, longitude, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Note")

        # Create map view
        self.map_view = QWebEngineView()
        self.map_file = self.create_map_html(latitude, longitude)
        self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))

        # Create labels for note details
        self.note_label = QLabel(f"Note: {note_text}")
        self.lat_label = QLabel(f"Latitude: {latitude}")
        self.lon_label = QLabel(f"Longitude: {longitude}")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.map_view)
        layout.addWidget(self.note_label)
        layout.addWidget(self.lat_label)
        layout.addWidget(self.lon_label)

        self.setLayout(layout)

    def create_map_html(self, latitude, longitude):
        # Create a temporary file for the map
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        temp_file.close()

        # Create a folium map centered on the given latitude and longitude
        folium_map = folium.Map(location=[latitude, longitude], zoom_start=13)
        folium.Marker(location=[latitude, longitude], popup="Note location").add_to(folium_map)

        # Save the map to the temp HTML file
        folium_map.save(temp_file.name)

        return temp_file.name