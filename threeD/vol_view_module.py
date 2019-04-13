import sys
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QApplication
from PyQt5.uic import loadUi
import threeD.loaddicomfile as ldf
from threeD.matinqt import CFigureCanvas


class C3dView(QDialog):

    def __init__(self):
        super().__init__()
        loadUi('vol_view_module.ui', self)
        self.setWindowTitle('3D View')
        self.image = None
        self.setMouseTracking(False)
        self.imgs = None
        self.patient = None
        self.threshold = 1000
        self.step = 10
        self.alpha = 0.5
        self.thresholdEdit.setText(str(self.threshold))
        self.stepEdit.setText(str(self.step))
        self.alphaEdit.setText(str(self.alpha))
        self.refreshButton.clicked.connect(self.refresh_clicked)
        self.graphicsView.setMinimumSize(1, 1)


    def refresh_clicked(self):
        self.threshold = int(self.thresholdEdit.text())
        self.step = int(self.stepEdit.text())
        self.alpha = float(self.alphaEdit.text())
        self.vol_show()

    def vol_show(self):
        print("Shape before resampling\t", self.imgs.shape)
        imgs_after_resamp, spacing = ldf.resample(self.imgs, self.patient)
        print("Shape after resampling\t", imgs_after_resamp.shape)
        try:
            v, f = ldf.make_mesh(imgs_after_resamp, threshold=self.threshold, step_size=self.step)
        except Exception:
            print('re-resample...')
            imgs_after_resamp, spacing = ldf.resample(self.imgs, self.patient)
            v, f = ldf.make_mesh(imgs_after_resamp, threshold=self.threshold, step_size=self.step)

        dr = CFigureCanvas()
        dr.plt_3d(v, f, alpha=self.alpha)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(dr)
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = C3dView()
    ex.show()
    sys.exit(app.exec_())
