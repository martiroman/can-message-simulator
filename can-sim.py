"""
CAN Message Simulator

This module defines a PyQt5 application for simulating the sending of CAN (Controller Area Network) messages.
It includes a graphical user interface that allows users to input message identifiers, data, and other parameters,
and to send these messages through a virtual CAN bus. The application supports sending messages in a loop with
options for random data generation and configurable intervals.

Classes:
    - CanSendThread: A QThread subclass for sending CAN messages in a separate thread.
    - MainWindow: The main application window that provides the user interface for configuring and sending CAN messages.

Dependencies:
    - can: For interacting with the CAN bus.
    - PyQt5: For the graphical user interface components.
    - threading: For managing concurrent threads.
    - random: For generating random data.

Usage:
    - Run the application, configure the message parameters in the GUI, and click "Send" to start sending CAN messages.
    - Use the "Stop" button to halt message sending.
"""

import can
import time
import random
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QMessageBox
import threading

class CanSendThread(QThread):
    """
    Thread for sending CAN messages.

    Attributes:
        finished (pyqtSignal): Signal emitted when the thread finishes.
        running (bool): Indicates whether the thread should continue running.
        semaphore (threading.Semaphore): Semaphore to control concurrent access.
        msgid (int): Identifier of the CAN message.
        data (list): Data of the CAN message.
        id (int): Thread identifier.
        random (bool): Indicates whether random data should be generated.
        seg (int): Time interval between sends in seconds.
    """

    finished = pyqtSignal()
    running = True
    
    def __init__(self, id, msgid, data, random, seg):
        """
        Initializes a new thread for sending CAN messages.

        Args:
            id (int): Thread identifier.
            msgid (int): Identifier of the CAN message.
            data (list): Data of the CAN message.
            random (bool): Indicates whether random data should be generated.
            seg (int): Time interval between sends in seconds.
        """

        super().__init__()
        self.msgid = msgid
        self.data = data
        self.id = id
        self.random = random
        self.seg = seg
        self.running = True
        self.semaphore = threading.Semaphore(value=1)

    def run(self):
        """
        Executes the thread to send CAN messages in a loop.
        """        
        while self.running:
            self.semaphore.acquire()
            window.send_can_message(self.msgid, self.data)
            
            if self.random:
                self.data = window.reset_can_message(self.id)

            if self.seg == 0:
                self.running = False
            
            self.semaphore.release()
            
            time.sleep(self.seg)
        self.finished.emit()

    def stop(self):
        """
        Stops the execution of the thread.
        """
        self.semaphore.acquire()
        self.running = False
        self.semaphore.release()

class MainWindow(QMainWindow):
    """
    Main application window for simulating the sending of CAN messages.

    Attributes:
        error (bool): Indicates if an error has occurred.
        send_threads (dict): Dictionary that stores active sending threads.
    """
    error = False
    send_threads = {}

    def __init__(self):
        """
        Initializes the main window and sets up the graphical user interface.
        """
        super().__init__()
        self.bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
        self.send_threads[0] = None

        self.setWindowTitle("Message CAN Simulator")

        # Elementos de la interfaz
        self.lblRunning = QLabel(" ")
        self.lblDevice = QLabel("Device")
        self.lblDevice.setFixedSize(80, 30)
        self.lblDato1 = QLabel("1")
        self.lblDato1.setFixedSize(50, 30)
        self.lblDato2 = QLabel("2")
        self.lblDato2.setFixedSize(50, 30)
        self.lblDato3 = QLabel("3")
        self.lblDato3.setFixedSize(50, 30)
        self.lblDato4 = QLabel("4")
        self.lblDato4.setFixedSize(50, 30)
        self.lblDato5 = QLabel("5")
        self.lblDato5.setFixedSize(50, 30)
        self.lblDato6 = QLabel("6")
        self.lblDato6.setFixedSize(50, 30)
        self.lblDato7 = QLabel("7")
        self.lblDato7.setFixedSize(50, 30)
        self.lblDato8 = QLabel("8")
        self.lblDato8.setFixedSize(50, 30)
        self.lblDato9 = QLabel("freq")
        self.lblDato9.setFixedSize(30, 30)

        self.layout_send = QVBoxLayout()
        
        row0 = QHBoxLayout()
        row0.addWidget(self.lblRunning)
        row0.addWidget(self.lblDevice)
        row0.addWidget(self.lblDato1)
        row0.addWidget(self.lblDato2)
        row0.addWidget(self.lblDato3)
        row0.addWidget(self.lblDato4)
        row0.addWidget(self.lblDato5)
        row0.addWidget(self.lblDato6)
        row0.addWidget(self.lblDato7)
        row0.addWidget(self.lblDato8)
        row0.addWidget(self.lblDato9)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        row0.addItem(spacer)

        self.layout_send.addLayout(row0)

        arb_id = 100
        for i in range(1, 5): 
            row = QHBoxLayout()
 
            lblEdit = QLabel(" ")
            setattr(self, f"lblEdit{i}", lblEdit)
            lblEdit.setStyleSheet("background-color: red")
            row.addWidget(lblEdit)            
 
            line_editDev = QLineEdit()
            setattr(self, f"txtDev{i}", line_editDev)
            line_editDev.setText(str(arb_id))
            line_editDev.setFixedSize(80, 30)
            row.addWidget(line_editDev)

            for j in range(1, 9):
                line_edit = QLineEdit()
                setattr(self, f"txtDev{i}Dato{j}", line_edit)
                random_decimal = random.randint(0, 255)
                random_hex = format(random_decimal, '02X')
                line_edit.setText(random_hex)
                line_edit.setFixedSize(50, 30)
                
                row.addWidget(line_edit)

            txtSeg = QLineEdit()
            setattr(self, f"txtSeg{i}", txtSeg)
            txtSeg.setText("3")
            txtSeg.setFixedSize(30, 20)
            row.addWidget(txtSeg)

            ckRandom = QCheckBox('Random')
            setattr(self, f"ckRandom{i}", ckRandom)
            ckRandom.setChecked(True)
            row.addWidget(ckRandom)            

            btn_Dev = QPushButton("Send")
            btn_Dev.clicked.connect(lambda _, line_number=i: self.click_send(line_number))
            row.addWidget(btn_Dev)
            
            btn_StopDev = QPushButton("Stop")
            btn_StopDev.clicked.connect(lambda _, line_number=i: self.stop_thread(line_number))
            row.addWidget(btn_StopDev)           
            
            self.layout_send.addLayout(row)

            arb_id += 10                    
        
        # Central Widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout_send)
        self.setCentralWidget(self.central_widget)

    def click_send(self, line_number):
        """
        Handles the click event of the "Send" button. Starts a thread to send the CAN message.

        Args:
            line_number (int): Line number indicating the group of input fields.
        """
        try:
            thread_id = line_number

            if thread_id in self.send_threads:
                self.stop_thread(thread_id)

            msgid = int(getattr(self, f"txtDev{line_number}").text(), 16)

            # Obtener datos del mensaje, ignorar "-" como valores no válidos
            data = [int(getattr(self, f"txtDev{line_number}Dato{j}").text(), 16) for j in range(1, 9) if getattr(self, f"txtDev{line_number}Dato{j}").text() != "-"]

            txtSeg = getattr(self, f"txtSeg{line_number}")
            ckRandom = getattr(self, f"ckRandom{line_number}")
            random = ckRandom.isChecked()
            seg = int(txtSeg.text())

            self.send_threads[thread_id] = CanSendThread(line_number, msgid, data, random, seg)
            self.send_threads[thread_id].start()
            
            lblEdit = getattr(self, f"lblEdit{line_number}")
            lblEdit.setStyleSheet("background-color: green")

            if seg == 0:
                lblEdit.setStyleSheet("background-color: red")

        except Exception as e:
            self.message_error(str(e))
            self.stop_thread(line_number)

    def send_can_message(self, message_id, data):
        """
        Sends a CAN message through the bus.

        Args:
            message_id (int): Identifier of the CAN message.
            data (list): Data of the CAN message.
        """
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
        self.bus.send(message)
        print(f"Mensaje enviado: ID={message_id}, Datos={data}")

    def reset_can_message(self, id):
        """
        Generates and returns new random data for the CAN message.

        Args:
            id (int): Identifier of the message for which data should be generated.

        Returns:
            list: Newly generated random data.
        """        
        for j in range(1, 9):
            txtDevDato = getattr(self, f"txtDev{id}Dato{j}")
            random_decimal = random.randint(0, 255)
            random_hex = format(random_decimal, '02X')
            txtDevDato.setText(random_hex)
            
            data = [int(getattr(self, f"txtDev{id}Dato{j}").text(), 16) for j in range(1, 9) if getattr(self, f"txtDev{id}Dato{j}").text() != "-"]
            
        return data

    def stop_thread(self, id):
        """
        Stops the sending thread for the given identifier.

        Args:
            id (int): Identifier of the thread to be stopped.
        """
        if id in self.send_threads:
            self.send_threads[id].stop()
            del self.send_threads[id]

            txtDev = getattr(self, f"lblEdit{id}")
            txtDev.setStyleSheet("background-color: red")

    def message_error(self, e):
        """
        Displays a message box with an error.

        Args:
            e (str): Error message to be displayed.
        """
        message_box = QMessageBox()
        message_box.setText(e)
        message_box.exec_()
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
