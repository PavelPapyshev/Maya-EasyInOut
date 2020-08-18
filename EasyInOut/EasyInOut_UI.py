from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import maya.cmds as mc
import EasyInOut_Utility


class EasyInOut_MainWindow(MayaQWidgetBaseMixin, QtWidgets.QDialog):
	
	"""
	creates a dialog window
	"""
	
	def __init__(self):
		
		super(EasyInOut_MainWindow, self).__init__()
		self.createUI()
		
	
	def createUI(self):
		
		"""
		sets the window and its elements settings
		"""
		
		#window------------------------
		self.setObjectName("EasyInOut")
		self.setWindowTitle("Easy In/Out")
		self.setFixedSize(400,100)
		
		#main layout------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		
		#comboBox----------------------------------
		self.comboBox = QtWidgets.QComboBox()
		self.comboBox.addItem("In/Out")
		self.comboBox.addItem("In")
		self.comboBox.addItem("Out")
		self.mainLayout.addWidget(self.comboBox)
		
		#slider------------------------
		self.slider = QtWidgets.QSlider()
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		self.slider.setMinimum(-1000)
		self.slider.setMaximum(1000)
		self.slider.setValue(0)
		self.slider.sliderMoved.connect(self.slMove)
		self.slider.sliderPressed.connect(self.slMove)
		self.slider.sliderReleased.connect(self.slReleased)
		self.mainLayout.addWidget(self.slider)
	
	
	def slMove(self, value=0):
		
		"""
		triggered by moving the slider
		
		accepts arguments:
			@value[int] - slider value
		"""
		
		EasyInOut_Utility.newSliderValue(value, comboText=self.comboBox.currentText())
		
	
	def slReleased(self):
	
		"""
		triggered when the mouse button is released over the selected slider
		"""

		self.slider.setValue(0)



#----------------------------END MainWindow	


def EasyInOut_Main():
	
	"""
	shows a dialog window
	"""
	
	if mc.window("EasyInOut", exists=1):
		mc.deleteUI("EasyInOut")
	
	"""
	if mc.windowPref("EasyInOut", exists=1):
		mc.windowPref("EasyInOut", remove=1)
	"""
	
	ui = EasyInOut_MainWindow()
	ui.show()
