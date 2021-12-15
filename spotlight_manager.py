#
# Created by Samuele Roversi (samuele dot rove at gmail dot com)
# This software is released under the MIT license.
# Project at -> github.com/rov/windows-spotlight-manager
#

import os

# Initialize

path = "%LocalAppData%\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"

os.system("cd " + path + " & rename * *.jpg")

path = "%LocalAppData%\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"

images = []

for file in os.listdir(os.path.expandvars(path)):
	images.append(os.path.expandvars(path) + "\\" + file)


import sys
from shutil import copy

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QAction, qApp, QMainWindow, QPushButton, QGridLayout, QWidget, QScrollArea, QFileDialog
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

	def __init__(self):

		super().__init__()

		self.setWindowTitle("Spotlight Manager")

		self.buttons = []

		for image in images:

			if image[-4:] == ".jpg":

				button = QPushButton()
				button.setFlat(True)
				button.setCheckable(True)

				button.setIcon(QIcon(image))
				button.setIconSize(QtCore.QSize(200, 360))
				button.setStyleSheet("padding: 10px; height: 100%")

				self.buttons.append( { 'btn_obj' : button, 'img' : image } )


		# Quick guide (:
		#    scroll -> ---------------------------+
		#     widget -> ----------------------+  ^|
		#      toolbar -> [_________________] |  ║|
		#                  --+----+----+----+ |  ║|
		#                    |    |    |    | |  ║|
		#        layout -> --+----+----+----+ |  ║|
		#                    |    |    |    | |  ║|
		#                  --+----+----+----+ |  ║|
		#                    |    |    |    | |  ║|
		#                                     |  v|

		scroll = QScrollArea()
		widget = QWidget()
		layout = QGridLayout()

		# --- Toolbar buttons ---

		# Save
		saveAct = QAction('Save selection', self)
		saveAct.setShortcut('Ctrl+S')
		saveAct.setToolTip("CTRL + S")
		saveAct.triggered.connect(self.save)

		# Select all
		selectAllAct = QAction('Select all', self)
		selectAllAct.setShortcut('Ctrl+A')
		selectAllAct.setToolTip("CTRL + A")
		selectAllAct.triggered.connect(self.select_all)

		# Deselect all
		deSelectAllAct = QAction('Deselect all', self)
		deSelectAllAct.setShortcut('Ctrl+D')
		deSelectAllAct.setToolTip("CTRL + D")
		deSelectAllAct.triggered.connect(self.deselect_all)

		# Invert selection
		invertSelectionAct = QAction('Invert selection', self)
		invertSelectionAct.setShortcut('Ctrl+I')
		invertSelectionAct.setToolTip("CTRL + I")
		invertSelectionAct.triggered.connect(self.invert_selection)

		# --- Toolbar ---
		toolbar = self.addToolBar('Toolbar (:')
		toolbar.setMovable(False)
		toolbar.setStyleSheet("border-bottom: none; font-size: 10pt;")
		toolbar.addAction(saveAct)
		toolbar.addAction(selectAllAct)
		toolbar.addAction(deSelectAllAct)
		toolbar.addAction(invertSelectionAct)

		row = 0
		col = 0

		for element in self.buttons:

			if col > 2: col = 0; row += 1

			layout.addWidget(element['btn_obj'], row, col)

			col += 1

		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll.setWidgetResizable(True)
		scroll.setWidget(widget)

		widget.setLayout(layout)

		self.resize(1000, 600)
		self.setCentralWidget(scroll)


	def save(self):
		dest_folder = str(QFileDialog.getExistingDirectory(self, "Select a folder"))

		if dest_folder:
			for element in self.buttons:
				if element['btn_obj'].isChecked() is True:
					copy(element['img'], dest_folder)


	def select_all(self):
		[ element['btn_obj'].setChecked(True) for element in self.buttons ]


	def deselect_all(self):
		[ element['btn_obj'].setChecked(False) for element in self.buttons ]


	def invert_selection(self):
		for element in self.buttons:
			if element['btn_obj'].isChecked() is False:
				element['btn_obj'].setChecked(True)
			else:
				element['btn_obj'].setChecked(False)
			

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()