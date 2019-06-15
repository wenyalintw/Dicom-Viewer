import sys
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import os
import cv2


class CtwoD(QDialog):
    def __init__(self):
        super().__init__()
        path = os.getcwd()
        os.chdir(path+'/twoD')
        loadUi('twoD_module.ui', self)
        self.setWindowTitle('2D Processing')
        self.image = None
        self.setMouseTracking(False)
        self.loadButton.clicked.connect(self.load_clicked)
        self.saveButton.clicked.connect(self.save_clicked)
        self.drawButton.setCheckable(True)
        self.drawButton.clicked.connect(self.draw_clicked)
        self.seedButton.clicked.connect(self.seed_clicked)
        self.thresholdButton.clicked.connect(self.threshold_clicked)
        self.imgLabel_1.window = 1
        self.imgLabel_2.window = 2
        self.morButton.clicked.connect(self.mor_clicked)
        self.kersizeEdit.setText(str(self.imgLabel_2.mor_Kersize))
        self.iterEdit.setText(str(self.imgLabel_2.mor_Iter))
        self.edgeButton.clicked.connect(self.edge_clicked)
        self.undoButton.clicked.connect(self.undo_clicked)
        self.undoButton.setIcon(QIcon('resources/undo.png'))
        self.undoButton.setText('')
        self.grayButton.clicked.connect(self.gray_clicked)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.imgLabel_1.processedImage is not None:
            self.imgLabel_1.display_image()
        if self.imgLabel_2.processedImage is not None:
            self.imgLabel_2.display_image()

    def gray_clicked(self):
        try:
            self.imgLabel_1.processedImage = cv2.cvtColor(self.imgLabel_1.processedImage, cv2.COLOR_BGR2GRAY)
            self.imgLabel_2.processedImage = cv2.cvtColor(self.imgLabel_2.processedImage, cv2.COLOR_BGR2GRAY)
        except Exception:
            QMessageBox.about(None, 'Information', 'Already converted to grayscaled!')
        self.imgLabel_1.display_image()
        self.imgLabel_2.display_image()

    def undo_clicked(self):
        self.imgLabel_1.processedImage = self.imgLabel_1.image.copy()
        self.imgLabel_1.display_image()
        self.imgLabel_2.processedImage = self.imgLabel_2.image.copy()
        self.imgLabel_2.display_image()

    def edge_clicked(self):
        self.imgLabel_2.edge_detection(self.edgeBox.itemText(self.edgeBox.currentIndex()))

    def mor_clicked(self):
        self.imgLabel_2.mor_Kersize = int(self.kersizeEdit.text())
        self.imgLabel_2.mor_Iter = int(self.iterEdit.text())
        self.imgLabel_2.morthology(self.morBox.itemText(self.morBox.currentIndex()))

    def threshold_clicked(self):
        threshold = int(self.thresholdValue.text())
        self.imgLabel_2.thresholding(threshold)

    def seed_clicked(self):
        self.imgLabel_2.seed = True

    def draw_clicked(self, status):
        if status:
            self.imgLabel_2.drawornot = True
            self.drawButton.setText('Start drawimg')
        else:
            self.imgLabel_2.drawornot = False
            self.drawButton.setText('Stop drawimg')

    def save_clicked(self):
        fname, _filter = QFileDialog.getSaveFileName(self, 'save file', '~/untitled', "Image Files (*.jpg)")
        if fname:
            cv2.imwrite(fname, self.imgLabel_2.processedImage)
        else:
            print('Error')

    def load_clicked(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'open file', '~/Desktop',
                                                     "Image Files (*.jpg *.png *.bmp *.dcm *DCM)")
        name, extension = os.path.splitext(fname)
        print(extension)
        if extension.lower() == '.dcm':
            self.imgLabel_1.load_dicom_image(fname)
            self.imgLabel_2.load_dicom_image(fname)
        else:
            try:
                self.imgLabel_1.load_image(fname)
                self.imgLabel_2.load_image(fname)
            except Exception:
                print('Error')
            finally:
                print('Finish loading')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CtwoD()
    ex.show()
    sys.exit(app.exec_())
