from threading import Thread
import time

from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Signal,QObject
from am import AM


am = AM('zhangqingrong', 'c516f13f01', '3336')
am.login()


@Slot()
def send():
    msg = send_msg.toPlainText()
    am.send_msg(qbox.itemData(qbox.currentIndex()), msg)


@Slot(str)
def show_msg(msg):
    mbox.about(window, "A",msg)

class RcveSignal(QObject):
    sig = Signal(str)

rsig = RcveSignal()
rsig.sig.connect(show_msg)


def recv():
    while True:
        msg = am.recv_msg()
        print(msg)
        rsig.sig.emit(msg)
        #QMessageBox.about(self, "Title", "Message")
        #mbox.about(window, "A", msg)
        


app = QApplication([])
window = QWidget()
hlayout = QHBoxLayout()
vlayout = QVBoxLayout()
mbox = QMessageBox()

#slider = QSlider(Qt.Horizontal)

button = QPushButton("Send")
label = QLabel('用户:')
send_msg = QTextEdit()
qbox = QComboBox()
qbox.addItem('张清荣', 'zhangqingrong')
qbox.addItem('段云丰', 'duanyunfeng')

button.clicked.connect(send)
hlayout.addWidget(qbox)
#hlayout.addWidget(label)
#hlayout.addWidget(receiver)
hlayout.addWidget(button)
vlayout.addLayout(hlayout)
vlayout.addWidget(send_msg)
#vlayout.addWidget(qbox)

#layout.addWidget(slider)
window.setLayout(vlayout)
window.show()
recv_thread = Thread(target=recv, daemon=True)
recv_thread.start()
app.exec_()
