import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import os
import cv2
import threeD.loaddicomfile as ldf
import numpy as np
from threeD.vol_view_module import C3dView


class CthreeD(QDialog):
    def __init__(self):
        super().__init__()
        path = os.getcwd()
        os.chdir(path + '/threeD')
        self.directory = os.getcwd()
        loadUi('threeD_module.ui', self)
        self.setWindowTitle('3D Processing')
        self.image = None
        # self.draw=False
        self.setMouseTracking(False)
        self.voxel = None
        self.processedvoxel = None
        self.v1, self.v2, self.v3 = None, None, None
        self.volWindow = None
        self.dicomButton.clicked.connect(self.dicom_clicked)
        self.axial_hSlider.valueChanged.connect(self.axial_hslider_changed)
        self.axial_vSlider.valueChanged.connect(self.axial_vslider_changed)
        self.axialmoveUD = 0
        self.axialmoveLR = 0
        self.sagittal_hSlider.valueChanged.connect(self.sagittal_hslider_changed)
        self.sagittal_vSlider.valueChanged.connect(self.sagittal_vslider_changed)
        self.sagittalmoveUD = 0
        self.sagittalmoveLR = 0
        self.coronal_hSlider.valueChanged.connect(self.coronal_hslider_changed)
        self.coronal_vSlider.valueChanged.connect(self.coronal_vslider_changed)
        self.coronalmoveUD = 0
        self.coronalmoveLR = 0
        self.colormap = None
        # 這樣可以把"被activate"的Item轉成str傳入connect的function（也可以用int之類的，會被enum）
        self.colormapBox.activated[str].connect(self.colormap_choice)
        self.colormapDict = {'GRAY': None,
                             'AUTUMN': cv2.COLORMAP_AUTUMN,
                             'BONE': cv2.COLORMAP_BONE,
                             'COOL': cv2.COLORMAP_COOL,
                             'HOT': cv2.COLORMAP_HOT,
                             'HSV': cv2.COLORMAP_HSV,
                             'JET': cv2.COLORMAP_JET,
                             'OCEAN': cv2.COLORMAP_OCEAN,
                             'PINK': cv2.COLORMAP_PINK,
                             'RAINBOW': cv2.COLORMAP_RAINBOW,
                             'SPRING': cv2.COLORMAP_SPRING,
                             'SUMMER': cv2.COLORMAP_SUMMER,
                             'WINTER': cv2.COLORMAP_WINTER
                             }
        self.volButton.clicked.connect(self.open_3dview)
        # 試過：setRowStretch, setSpacing, setGeometry, addWidget, addItem, addStretch，最後採用insertSpacerItem
        self.axialGrid.setSpacing(0)
        self.saggitalGrid.setSpacing(0)
        self.coronalGrid.setSpacing(0)

        h = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        v = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.axial_vBox.setSpacing(0)
        self.axial_vBox.insertSpacerItem(0, v)
        self.axial_vBox.insertSpacerItem(2, v)
        self.axial_hBox.setSpacing(0)
        self.axial_hBox.insertSpacerItem(0, h)
        self.axial_hBox.insertSpacerItem(2, h)
        self.saggital_vBox.setSpacing(0)
        self.saggital_vBox.insertSpacerItem(0, v)
        self.saggital_vBox.insertSpacerItem(2, v)
        self.saggital_hBox.setSpacing(0)
        self.saggital_hBox.insertSpacerItem(0, h)
        self.saggital_hBox.insertSpacerItem(2, h)
        self.coronal_vBox.setSpacing(0)
        self.coronal_vBox.insertSpacerItem(0, v)
        self.coronal_vBox.insertSpacerItem(2, v)
        self.coronal_hBox.setSpacing(0)
        self.coronal_hBox.insertSpacerItem(0, h)
        self.coronal_hBox.insertSpacerItem(2, h)

        self.colormap_hBox.insertStretch(2)
        self.colormap_hBox.insertSpacerItem(0, QSpacerItem(30, 0, QSizePolicy.Fixed,  QSizePolicy.Fixed))

        self.savesliceButton.clicked.connect(self.saveslice_clicked)
        self.dcmInfo = None
        self.imgLabel_1.mpsignal.connect(self.cross_center_mouse)
        self.imgLabel_2.mpsignal.connect(self.cross_center_mouse)
        self.imgLabel_3.mpsignal.connect(self.cross_center_mouse)

        self.cross_recalc = True
        self.savenpyButton.clicked.connect(self.save_npy_clicked)
        self.loadnpyButton.clicked.connect(self.load_npy_clicked)
        self.downscaled = 2
        self.dsampleButton.clicked.connect(self.downsample)




    def downsample(self):
        self.processedvoxel = self.processedvoxel[::self.downscaled, ::self.downscaled, ::self.downscaled]
        self.updateimg()

    def save_npy_clicked(self):
        fname, _filter = QFileDialog.getSaveFileName(self, 'save file', '~/untitled', "Image Files (*.npy)")
        if fname:
            np.save(fname, self.processedvoxel)
        else:
            print('Error')

    def load_npy_clicked(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'open file', '~/Desktop', "Image Files (*.NPY *.npy)")
        self.processedvoxel = np.load(fname)
        self.savetemp()
        self.updateimg()

    def set_directory(self):
        os.chdir(self.directory)

    def cross_center_mouse(self, _type):
        self.cross_recalc = False
        if _type == 'axial':
            self.axial_hSlider.setValue(self.imgLabel_1.crosscenter[0] *
                                        self.axial_hSlider.maximum() / self.imgLabel_1.width())
            self.axial_vSlider.setValue(self.imgLabel_1.crosscenter[1] *
                                        self.axial_vSlider.maximum() / self.imgLabel_1.height())
        elif _type == 'sagittal':
            self.sagittal_hSlider.setValue(self.imgLabel_2.crosscenter[0] *
                                           self.sagittal_hSlider.maximum() / self.imgLabel_2.width())
            self.sagittal_vSlider.setValue(self.imgLabel_2.crosscenter[1] *
                                           self.sagittal_vSlider.maximum() / self.imgLabel_2.height())

        elif _type == 'coronal':
            self.coronal_hSlider.setValue(self.imgLabel_3.crosscenter[0] *
                                          self.coronal_hSlider.maximum() / self.imgLabel_3.width())
            self.coronal_vSlider.setValue(self.imgLabel_3.crosscenter[1] *
                                          self.coronal_vSlider.maximum() / self.imgLabel_3.height())
            pass
        else:
            pass

        self.imgLabel_1.crosscenter = [
            self.axial_hSlider.value() * self.imgLabel_1.width() / self.axial_hSlider.maximum(),
            self.axial_vSlider.value() * self.imgLabel_1.height() / self.axial_vSlider.maximum()]
        self.imgLabel_2.crosscenter = [
            self.sagittal_hSlider.value() * self.imgLabel_2.width() / self.sagittal_hSlider.maximum(),
            self.sagittal_vSlider.value() * self.imgLabel_2.height() / self.sagittal_vSlider.maximum()]
        self.imgLabel_3.crosscenter = [
            self.coronal_hSlider.value() * self.imgLabel_3.width() / self.coronal_hSlider.maximum(),
            self.coronal_vSlider.value() * self.imgLabel_3.height() / self.coronal_vSlider.maximum()]
        self.updateimg()

        self.cross_recalc = True

    def saveslice_clicked(self):
        fname, _filter = QFileDialog.getSaveFileName(self, 'save file', '~/untitled', "Image Files (*.jpg)")
        if fname:
            if self.savesliceBox.currentText() == 'Axial':
                cv2.imwrite(fname, self.imgLabel_1.processedImage)
            elif self.savesliceBox.currentText() == 'Saggital':
                cv2.imwrite(fname, self.imgLabel_2.processedImage)
            elif self.savesliceBox.currentText() == 'Coronal':
                cv2.imwrite(fname, self.imgLabel_3.processedImage)
            else:
                print('No slice be chosen')
        else:
            print('Error')
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # resize的時候兩個都要重畫，才會維持一樣大小
        if self.processedvoxel is not None:
            self.updateimg()

    def open_3dview(self):
        self.volWindow.setWindowTitle('3D View')
        self.volWindow.vol_show()
        self.volWindow.show()

    def colormap_choice(self, text):
        self.colormap = self.colormapDict[text]
        self.updateimg()

    def coronal_hslider_changed(self):
        _max = self.coronal_hSlider.maximum()
        _min = self.coronal_hSlider.minimum()
        mid = (_max-_min)/2
        self.coronalmoveLR = int((self.coronal_hSlider.value()-mid) * (self.v3 / (2*mid)))
        self.updateimg()
        self.axial_hSlider.setValue(self.coronal_hSlider.value())

    def coronal_vslider_changed(self):
        _max = self.coronal_vSlider.maximum()
        _min = self.coronal_vSlider.minimum()
        mid = (_max-_min)/2
        self.coronalmoveUD = int((self.coronal_vSlider.value()-mid) * (self.v1 / (2*mid)))
        self.updateimg()
        self.sagittal_vSlider.setValue(self.coronal_vSlider.value())

    def sagittal_hslider_changed(self):
        _max = self.sagittal_hSlider.maximum()
        _min = self.sagittal_hSlider.minimum()
        mid = (_max-_min)/2
        self.sagittalmoveLR = int((self.sagittal_hSlider.value()-mid) * (self.v2 / (2*mid)))
        self.updateimg()
        self.axial_vSlider.setValue(self.sagittal_hSlider.value())

    def sagittal_vslider_changed(self):
        _max = self.sagittal_vSlider.maximum()
        _min = self.sagittal_vSlider.minimum()
        mid = (_max-_min)/2
        self.sagittalmoveUD = int((self.sagittal_vSlider.value()-mid) * (self.v1 / (2*mid)))
        self.updateimg()
        self.coronal_vSlider.setValue(self.sagittal_vSlider.value())

    def axial_hslider_changed(self):
        _max = self.axial_hSlider.maximum()
        _min = self.axial_hSlider.minimum()
        mid = (_max-_min)/2
        self.axialmoveLR = int((self.axial_hSlider.value()-mid) * (self.v3 / (2*mid)))
        self.updateimg()
        self.coronal_hSlider.setValue(self.axial_hSlider.value())

    def axial_vslider_changed(self):
        _max = self.axial_vSlider.maximum()
        _min = self.axial_vSlider.minimum()
        mid = (_max-_min)/2
        self.axialmoveUD = int((self.axial_vSlider.value()-mid) * (self.v2 / (2*mid)))
        self.updateimg()
        self.sagittal_hSlider.setValue(self.axial_vSlider.value())

    def dicom_clicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'choose dicom directory')
        print(fname)
        self.load_dicomfile(fname)

    def load_dicomfile(self, dname):
        self.dcmList.clear()
        patient = ldf.load_scan(dname)
        imgs = ldf.get_pixels_hu(patient)
        self.voxel = self.linear_convert(imgs)
        self.processedvoxel = self.voxel.copy()

        self.imgLabel_1.type = 'axial'
        self.imgLabel_2.type = 'sagittal'
        self.imgLabel_3.type = 'coronal'

        self.updateimg()
        self.set_directory()
        self.volWindow = C3dView()
        self.volWindow.imgs = imgs
        self.volWindow.patient = patient
        self.dcmInfo = ldf.load_dcm_info(dname, self.privatecheckBox.isChecked())
        self.updatelist()

    def updatelist(self):
        for item in self.dcmInfo:
            # 單純字串的話，可以不需要QListWidgetItem包裝也沒關係
            self.dcmList.addItem(QListWidgetItem('%-20s\t:  %s' % (item[0], item[1])))

    def updateimg(self):
        v1, v2, v3 = self.processedvoxel.shape
        self.v1, self.v2, self.v3 = v1, v2, v3

        a_loc = int(v1/2)-self.sagittalmoveUD
        s_loc = int(v3/2)+self.axialmoveLR
        c_loc = int(v2/2)+self.axialmoveUD

        if a_loc >= v1:
            a_loc = v1-1
        if s_loc >= v3:
            s_loc = v3-1
        if c_loc >= v2:
            c_loc = v2-1

        axial = (self.processedvoxel[a_loc, :, :]).astype(np.uint8).copy()
        sagittal = np.flipud((self.processedvoxel[:, :, s_loc]).astype(np.uint8)).copy()
        coronal = np.flipud((self.processedvoxel[:, c_loc, :]).astype(np.uint8)).copy()

        self.imgLabel_1.slice_loc = [s_loc, c_loc, a_loc]
        self.imgLabel_2.slice_loc = [s_loc, c_loc, a_loc]
        self.imgLabel_3.slice_loc = [s_loc, c_loc, a_loc]

        if self.cross_recalc:
            self.imgLabel_1.crosscenter = [self.imgLabel_1.width()/2+self.axialmoveLR*(self.imgLabel_1.width()/v3),
                                           self.imgLabel_1.height()/2+self.axialmoveUD*(self.imgLabel_1.height()/v2)]
            self.imgLabel_2.crosscenter = [self.imgLabel_2.width()/2+self.sagittalmoveLR*(self.imgLabel_2.width()/v2),
                                           self.imgLabel_2.height()/2+self.sagittalmoveUD*(self.imgLabel_2.height()/v1)]
            self.imgLabel_3.crosscenter = [self.imgLabel_3.width()/2+self.coronalmoveLR*(self.imgLabel_3.width()/v3),
                                           self.imgLabel_3.height()/2+self.coronalmoveUD*(self.imgLabel_3.height()/v1)]

        # 因AUTUMN的code是0，所以不用not self.colormap
        if self.colormap is None:
            self.imgLabel_1.processedImage = axial
            self.imgLabel_2.processedImage = sagittal
            self.imgLabel_3.processedImage = coronal
        else:
            self.imgLabel_1.processedImage = cv2.applyColorMap(axial, self.colormap)
            self.imgLabel_2.processedImage = cv2.applyColorMap(sagittal, self.colormap)
            self.imgLabel_3.processedImage = cv2.applyColorMap(coronal, self.colormap)

        self.imgLabel_1.setMouseTracking(True)
        self.imgLabel_2.setMouseTracking(True)
        self.imgLabel_3.setMouseTracking(True)

        self.imgLabel_1.display_image(1)
        self.imgLabel_2.display_image(1)
        self.imgLabel_3.display_image(1)

    @staticmethod
    def linear_convert(img):
        convert_scale = 255.0 / (np.max(img) - np.min(img))
        converted_img = convert_scale * img - (convert_scale * np.min(img))
        return converted_img


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CthreeD()
    ex.show()
    sys.exit(app.exec_())
