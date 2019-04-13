import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from twoD.twoD_module import CtwoD
from threeD.threeD_module import CthreeD


class CMainWindow(QMainWindow):
    def __init__(self):
        super(CMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
        self.showMaximized()
        self.twoDaction.changed.connect(self.activate_2d)
        self.threeDaction.changed.connect(self.activate_3d)
        self.maindirectory = os.getcwd()
        self.ui_2D = None
        self.ui_3D = None
        self.refresh2D = True
        self.refresh3D = True
        self.justclose = False
        self.first2D = True
        self.first3D = True

    def close2d(self):
        os.chdir(self.maindirectory)
        self.justclose = True
        self.twoDaction.setChecked(False)
        self.ui_2D.__init__()
        self.refresh2D = True
        self.justclose = False

    def close3d(self):
        os.chdir(self.maindirectory)
        self.justclose = True
        self.threeDaction.setChecked(False)
        self.ui_3D.__init__()
        self.refresh3D = True
        self.justclose = False

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # 設定透明度
        painter.setOpacity(0.5)
        w, h = self.width(), self.height()
        painter.drawPixmap(self.rect(), QPixmap(self.maindirectory+'/resources/background.png').scaled(w, h, Qt.KeepAspectRatio))
        self.label.setText('<span style="background-color:red; color:white">Dicom Viewer Project</span><br><br>'
                           '<span style="background-color:	#7FFFD4; color:#8A2BE2">2D & 3D Processing Included</span>')

    def activate_2d(self):
        # setChecked會被視為一種toggled, rejected也會被視為一種toggled
        os.chdir(self.maindirectory)
        if self.refresh2D:
            if self.first2D:
                self.ui_2D = CtwoD()
                self.first2D = False
            self.ui_2D.show()
            self.refresh2D = False
            self.ui_2D.rejected.connect(self.close2d)
        elif self.justclose:
            pass
        else:
            if not self.twoDaction.isChecked():
                self.twoDaction.setChecked(True)
            self.ui_2D.raise_()

    def activate_3d(self):
        os.chdir(self.maindirectory)
        if self.refresh3D:
            if self.first3D:
                self.ui_3D = CthreeD()
                self.first3D = False
            self.ui_3D.show()
            self.refresh3D = False
            self.ui_3D.rejected.connect(self.close3d)
        elif self.justclose:
            pass
        else:
            if not self.threeDaction.isChecked():
                self.threeDaction.setChecked(True)
            self.ui_3D.raise_()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication eats argv in constructor
    window = CMainWindow()
    window.setWindowTitle('Dicom Viewer Project')
    window.show()
    sys.exit(app.exec_())
