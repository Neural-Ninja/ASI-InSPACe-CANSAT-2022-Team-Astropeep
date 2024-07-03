import os
import time
import math
import logo_rc
import sys
import requests
import serial
import csv
import folium
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.vtkImageImportFromArray import vtkImageImportFromArray
from vtkmodules.util.colors import tomato
from vtk import vtkOBJReader, vtkPolyDataMapper, vtkActor, vtkRenderer, vtkTransform, vtkCamera

class OpenCameraWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Astropeep CANSAT Live View")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        self.setCentralWidget(self.browser)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Astropeep Ground Station")
        self.setupUi()

    def setupUi(self):
        loadUi("cansat_gui_final1_ui.ui", self)
        
        self.start_tele_button = self.findChild(QPushButton, "start_tele_button")
        self.stop_tele_button_2 = self.findChild(QPushButton, "stop_tele_button_2")
        self.save_csv_button = self.findChild(QPushButton, "save_csv_button")
        self.camera_button = self.findChild(QPushButton, "camera_button")
        self.battery_value = self.findChild(QLabel, "battery_value")
        self.fsw_state = self.findChild(QLabel, "fsw_state")
        self.tele_value = self.findChild(QListView, "tele_value")
        self.frame_cansat_view = self.findChild(QFrame, "frame_cansat_view")
        self.mission_time = self.findChild(QLabel, "mission_time")
        self.model = QStandardItemModel()
        self.tele_value.setModel(self.model)
        
        self.frame_alti = QtWidgets.QFrame(self)
        self.frame_pres = QtWidgets.QFrame(self)
        self.frame_temp = QtWidgets.QFrame(self)
        self.frame_accelo = QtWidgets.QFrame(self)
        self.frame_gyro = QtWidgets.QFrame(self)
        self.frame_map = QtWidgets.QFrame(self)
        
        
        self.frame_alti.setGeometry(QtCore.QRect(61, 193, 461, 251))
        self.frame_pres.setGeometry(QtCore.QRect(529, 193, 461, 251))
        self.frame_temp.setGeometry(QtCore.QRect(997, 193, 461, 251))
        self.frame_accelo.setGeometry(QtCore.QRect(61, 503, 461, 251))
        self.frame_gyro.setGeometry(QtCore.QRect(529, 503, 461, 251))
        self.frame_map.setGeometry(QtCore.QRect(997, 503, 461, 251))
    
        
        
        self.frame_alti.setLayout(QtWidgets.QVBoxLayout())
        self.frame_pres.setLayout(QtWidgets.QVBoxLayout())
        self.frame_temp.setLayout(QtWidgets.QVBoxLayout())
        self.frame_accelo.setLayout(QtWidgets.QVBoxLayout())
        self.frame_gyro.setLayout(QtWidgets.QVBoxLayout())
        self.frame_map.setLayout(QtWidgets.QVBoxLayout())
        
        self.vtk_cansat_view = QVTKRenderWindowInteractor(self.frame_cansat_view)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(0, 181, 226)
        self.vtk_cansat_view.GetRenderWindow().AddRenderer(self.renderer)
        self.load_obj_file("CANSAT@2 v7 v16.obj")
        
        
        
        self.graphWidget_alti = pg.PlotWidget()
        self.graphWidget_pres = pg.PlotWidget()
        self.graphWidget_temp = pg.PlotWidget()
        self.graphWidget_accelo = pg.PlotWidget()
        self.graphWidget_gyro = pg.PlotWidget()
        self.map = QtWebEngineWidgets.QWebEngineView()
        
        self.graphWidget_alti.setBackground('w')
        self.graphWidget_pres.setBackground('w')
        self.graphWidget_temp.setBackground('w')
        self.graphWidget_accelo.setBackground('w')
        self.graphWidget_gyro.setBackground('w')
        
        

        self.frame_alti.layout().addWidget(self.graphWidget_alti)
        self.frame_pres.layout().addWidget(self.graphWidget_pres)
        self.frame_temp.layout().addWidget(self.graphWidget_temp)
        self.frame_accelo.layout().addWidget(self.graphWidget_accelo)
        self.frame_gyro.layout().addWidget(self.graphWidget_gyro)
        self.frame_map.layout().addWidget(self.map)
        
        
        
        self.pc = []
        self.alti = []
        self.pres = []
        self.temp = []
        self.accelo_x = []
        self.accelo_y = []
        self.accelo_z = []
        self.gyro_x = []
        self.gyro_y = []
        self.gyro_z = []
        
        
        
        pen_alti = pg.mkPen(color=(70, 59, 237), width = 1.3)
        pen_pres = pg.mkPen(color=(236, 74, 237), width = 1.3)
        pen_temp = pg.mkPen(color=(237, 74, 78), width = 1.3)
        pen_accelo_x = pg.mkPen(color=(255, 0, 0), width = 1.3)
        pen_accelo_y = pg.mkPen(color=(0, 255, 0), width = 1.3)
        pen_accelo_z = pg.mkPen(color=(0, 0, 255), width = 1.3)
        pen_gyro_x = pg.mkPen(color=(255, 0, 0), width = 1.3)
        pen_gyro_y = pg.mkPen(color=(0, 255, 0), width = 1.3)
        pen_gyro_z = pg.mkPen(color=(0, 0, 255), width = 1.3)
        
        
        self.label_font = QFont("Times", 10, QFont.Bold)
        
        self.graphWidget_alti.setLabel('bottom', "Packet Count")
        self.graphWidget_alti.setLabel('left', "Altitude (m)")
        
        self.graphWidget_pres.setLabel('bottom', "Packet Count")
        self.graphWidget_pres.setLabel('left', "Pressure (Pascal)")
        
        self.graphWidget_temp.setLabel('bottom', "Packet Count")
        self.graphWidget_temp.setLabel('left', "Temperature (\N{SUPERSCRIPT ZERO}C)")
        
        self.graphWidget_accelo.setLabel('bottom', "Packet Count")
        self.graphWidget_accelo.setLabel('left', "Acceleration (m/s\N{SUPERSCRIPT TWO})")
        
        self.graphWidget_gyro.setLabel('bottom', "Packet Count")
        self.graphWidget_gyro.setLabel('left', "Gyro Spin (\N{SUPERSCRIPT ZERO}/s)")
        
        self.graphWidget_accelo.addLegend((330, 0.05))
        self.graphWidget_gyro.addLegend((330, 0.05))
        
        

        self.data_line_alti = self.graphWidget_alti.plot(self.pc, self.alti, pen=pen_alti)
        self.data_line_pres = self.graphWidget_pres.plot(self.pc, self.pres, pen=pen_pres)
        self.data_line_temp = self.graphWidget_temp.plot(self.pc, self.temp, pen=pen_temp)
        self.data_line_accelo_x = self.graphWidget_accelo.plot(self.pc, self.accelo_x, pen=pen_accelo_x, name = "a_x")
        self.data_line_accelo_y = self.graphWidget_accelo.plot(self.pc, self.accelo_y, pen=pen_accelo_y, name = "a_y")
        self.data_line_accelo_z = self.graphWidget_accelo.plot(self.pc, self.accelo_z, pen=pen_accelo_z, name = "a_z")
        self.data_line_gyro_x = self.graphWidget_gyro.plot(self.pc, self.gyro_x, pen=pen_gyro_x, name = "g_x")
        self.data_line_gyro_y = self.graphWidget_gyro.plot(self.pc, self.gyro_y, pen=pen_gyro_y, name = "g_y")
        self.data_line_gyro_z = self.graphWidget_gyro.plot(self.pc, self.gyro_z, pen=pen_gyro_z, name = "g_z")
        
        
        self.map_view = folium.Map(location = [23.001880, 72.620190], zoom_start=13)
        folium.TileLayer('stamenterrain').add_to(self.map_view)
        folium.Marker(location=[23.001880, 72.620190],popup="TEAM ASTROPEEP",).add_to(self.map_view)
        self.map.setHtml(self.map_view.get_root().render())
        self.map.show()
    
        
        self.start_tele_button.clicked.connect(self.start_logging)
        self.stop_tele_button_2.clicked.connect(self.stop_logging)
        self.save_csv_button.clicked.connect(self.csv_save)
        self.camera_button.clicked.connect(self.open_camera)
        
        
    def load_obj_file(self, file_path):
        self.reader = vtkOBJReader()
        self.reader.SetFileName(file_path)
        self.reader.Update()

        self.mapper = vtkPolyDataMapper()
        self.mapper.SetInputData(self.reader.GetOutput())

        self.actor = vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(tomato)

        self.renderer.AddActor(self.actor)
        self.camera = vtkCamera()
        self.renderer.ResetCamera()
        
        
        self.transform = vtkTransform()

        self.vtk_cansat_view.Initialize()

        
    
    
    def update_camera_position(self):

        object_bounds = self.actor.GetBounds()
        x_min, x_max, y_min, y_max, z_min, z_max = object_bounds
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        center_z = (z_min + z_max) / 2
        diagonal_length = math.sqrt((x_max - x_min)**2 + (y_max - y_min)**2 + (z_max - z_min)**2)
        camera_distance = diagonal_length / math.tan(math.radians(30))
        self.camera.SetPosition(center_x, center_y, center_z + camera_distance)
        self.camera.SetFocalPoint(center_x, center_y, center_z)





    @Slot()
    def start_logging(self):

        self.serial_port = serial.Serial('COM5', 9600)
        self.read_thread = ReadThread(self.serial_port)
        self.read_thread.data_received.connect(self.update_labels)
        self.read_thread.start()
        
    @Slot()    
    def stop_logging(self):
        if self.read_thread:
            self.read_thread.stop()
            self.read_thread.wait()
            self.serial_port.close()
            self.read_thread = None
            self.serial_port = None
                
    @Slot(str)           
    def update_labels(self, data):
        values = data.split(",")
        if len(values) >= 1:
            
            # Battery and FSW
            
            self.packet_count.setText(values[2])
            # battery_value = format((float(values[6])/9)*100, ".1f")
            battery_value = 100
            battery_value = str(battery_value) + "%"
            self.battery_value.setText(battery_value)
            self.fsw_state.setText(values[18])
            self.mission_time.setText(values[1])
            
            
            # Telemetry whole data
            
            item = QStandardItem(data)
            item.setTextAlignment(Qt.AlignCenter)
            font = QFont()
            font.setFamily(u"Rockwell")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.model.appendRow(item)
            self.tele_value.scrollToBottom()
            
            # Update Cansat PinPoint
            
            self.map_view = folium.Map(location = [values[8], values[9]], zoom_start=13)
            folium.TileLayer('stamenterrain').add_to(self.map_view)
            folium.Marker(location=[values[8], values[9]],popup="TEAM ASTROPEEP",).add_to(self.map_view)
            self.map.setHtml(self.map_view.get_root().render())
            
            # Update Plots by connecting to update_plot_data
            
            self.timer = QtCore.QTimer()
            self.timer.setInterval(10)
            self.timer.timeout.connect(lambda: self.update_plot_data(data))
            self.timer.start()
            
            
            
            
    # Update Plots

    def update_plot_data(self, data):
        
        values = data.split(",")
        if len(values) >= 1:
            
            self.pc.append(int(values[2]))
            self.alti.append(float(values[3]))
            self.pres.append(float(values[4]))
            self.temp.append(float(values[5]))
            self.accelo_x.append(float(values[12]))
            self.accelo_y.append(float(values[13]))
            self.accelo_z.append(float(values[14]))
            self.gyro_x.append(float(values[15]))
            self.gyro_y.append(float(values[16]))
            self.gyro_z.append(float(values[17]))
            
    
            self.data_line_alti.setData(self.pc, self.alti)
            self.data_line_pres.setData(self.pc, self.pres)
            self.data_line_temp.setData(self.pc, self.temp)
            self.data_line_accelo_x.setData(self.pc, self.accelo_x)
            self.data_line_accelo_y.setData(self.pc, self.accelo_y)
            self.data_line_accelo_z.setData(self.pc, self.accelo_z)
            self.data_line_gyro_x.setData(self.pc, self.gyro_x)
            self.data_line_gyro_y.setData(self.pc, self.gyro_y)
            self.data_line_gyro_z.setData(self.pc, self.gyro_z)
            
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.render_vtk_widget(data))
            self.timer.start(10)
            
            
            
    def render_vtk_widget(self, data):
        
        values = data.split(",")
        if len(values) >= 1:
            
            self.renderer.SetActiveCamera(self.camera)
        
            self.pitch = float(values[19])
            self.roll = float(values[20])
            self.yaw = float(values[21])
            
            self.update_camera_position()
            self.transform.Identity()
            self.transform.RotateX(self.pitch)
            self.transform.RotateY(self.roll)
            self.transform.RotateZ(self.yaw)
            self.actor.SetUserTransform(self.transform)
            self.vtk_cansat_view.GetRenderWindow().Render()
            self.vtk_cansat_view.GetRenderWindow().Render()
        
                
        
        
                
    def csv_save(self):
        if os.path.exists('data_tele.csv'):
            os.remove('data_tele.csv')
        with open('data_tele.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in range(self.model.rowCount()):
                data = []
                for column in range(self.model.columnCount()):
                    item = self.model.item(row, column)
                    if item is not None:
                        data.append(item.text())
                    else:
                        data.append('')
                csv_writer.writerow(data)
        
    def open_camera(self):
        url = "https://www.google.com"
        self.open_camera_window = OpenCameraWindow(url)
        self.open_camera_window.show()
        

                

class ReadThread(QThread):
    data_received = Signal(str)
    stop_logging = False

    def __init__(self, serial_port):
        super(ReadThread, self).__init__()
        self.serial_port = serial_port
        
    def receivePacket(self):
        while not self.stop_logging:
            while self.serial_port.read() != b'\x7E':
                pass
    
            packet_length = int.from_bytes(self.serial_port.read(2), byteorder='big')
    
            frame_type = self.serial_port.read().hex()
    
            frame_id = self.serial_port.read().hex()
    
            source_addr = self.serial_port.read(8).hex()
    
            source_addr_16 = self.serial_port.read(2).hex()
    
            options = self.serial_port.read().hex()
    
            radius = self.serial_port.read().hex()
    
            data_length = packet_length - 14
            data = self.serial_port.read(data_length)
    
            checksum = self.serial_port.read().hex()
    
            packet = bytearray.fromhex(frame_type + frame_id + source_addr + source_addr_16 + options + radius) + data
            calculated_checksum = (0xFF - sum(packet) & 0xFF)
    
            if calculated_checksum == int(checksum, 16):
                return data
    
            return None

    def run(self):
        while not self.stop_logging:
            
            telemetry_package = {}
            field_count = 0
            expected_fields = 22
            is_team_id_received = False
            
            while True:
                data_packet = self.receivePacket()
                if data_packet is not None:
                    data_packet = data_packet.decode('latin-1')
                    data_packet = data_packet.replace("ÁÂ", "")

                    if "Team_Id" in data_packet:
                        is_team_id_received = True

                    if is_team_id_received:
                        fields = data_packet.split("\n")
                        
                        for field in fields:
                            if field:
                                key, value = field.split(":", 1)
                                value = value.strip()
                                if value.endswith("}"):
                                    value = value[:-1]
                                telemetry_package[key] = value
                                field_count += 1

                                if field_count == expected_fields:
                                    telemetry_values = ",".join(telemetry_package.values())
                                    # print(telemetry_values)
                                    telemetry_package = {}
                                    field_count = 0
                                    is_team_id_received = False
                                    data = telemetry_values
                                    print(data)
                                    self.data_received.emit(data)
                                    
                                    
                else:
                    time.sleep(0.1) 
            

    def stop(self):
        self.serial_port.close()
        self.stop_logging = True
    
    
    
    
    

# class ReadThread(QThread):
#     data_received = Signal(str)
#     stop_logging = False

#     def __init__(self, serial_port):
#         super(ReadThread, self).__init__()
#         self.serial_port = serial_port

#     def run(self):
#         while not self.stop_logging:
#             data = self.serial_port.readline().decode().strip()
#             print(data)
#             self.data_received.emit(data)

#     def stop(self):
#         self.stop_logging = True
    
    
    
      
def dashboard():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())        

if __name__  == "__main__":
   dashboard()