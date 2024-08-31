import json
import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()


class ApplicationController:
	def __init__(self):
		self.mysql_password = os.getenv('MYSQL_PASSWORD')
		self.conn = mysql.connector.connect(
			host='localhost',
			user='root',
			password=self.mysql_password
		)
		self.cursor = self.conn.cursor()

		self.create_database()

		self.conn.database = 'mapnotes'
		self.cursor = self.conn.cursor()

		self.create_table()

	def create_database(self):
		try:
			self.cursor.execute("CREATE DATABASE IF NOT EXISTS mapnotes")
			print("Database 'mapnotes' created or already exists.")
		except mysql.connector.Error as err:
			print(f"Failed creating database: {err}")
			exit(1)

	def create_table(self):
		table_creation_query = """
		CREATE TABLE IF NOT EXISTS notes (
			id INT AUTO_INCREMENT PRIMARY KEY,
			note TEXT,
			latitude DOUBLE,
			longitude DOUBLE
		)
		"""
		try:
			self.cursor.execute(table_creation_query)
			print("Table 'notes' created or already exists.")
		except mysql.connector.Error as err:
			print(f"Failed creating table: {err}")
			exit(1)

	
	def get_notes(self):
		self.cursor.execute("SELECT id, note, latitude, longitude FROM notes")
		return [{'id': row[0], 'note': row[1], 'latitude': row[2], 'longitude': row[3]} for row in self.cursor.fetchall()]

	def add_note(self, note_data):
		sql = "INSERT INTO notes (note, latitude, longitude) VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (note_data['note'], note_data['latitude'], note_data['longitude']))
		self.conn.commit()

	def delete_note(self, note_id):
		sql = "DELETE FROM notes WHERE id = %s"
		self.cursor.execute(sql, (note_id,))
		self.conn.commit()

	def close(self):
		self.cursor.close()
		self.conn.close()

	def run(self):
		from views.main_window import MainWindow
		from PyQt5.QtWidgets import QApplication
		import sys

		app = QApplication(sys.argv)
		main_window = MainWindow(self)
		main_window.show()
		sys.exit(app.exec_())