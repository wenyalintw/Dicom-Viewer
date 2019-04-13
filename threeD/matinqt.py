from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class CFigureCanvas(FigureCanvas):

    def __init__(self, parent=None):
        # 直接不要給figsize就會自己fit了
        fig = Figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111, projection='3d')

    def plt_3d(self, verts, faces, alpha=0.5):
        print("Drawing")
        x, y, z = zip(*verts)
        mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=alpha)
        face_color = [1, 1, 0.9]
        mesh.set_facecolor(face_color)
        self.axes.add_collection3d(mesh)
        self.axes.set_xlim(0, max(x))
        self.axes.set_ylim(0, max(y))
        self.axes.set_zlim(0, max(z))
        self.axes.set_facecolor((0.7, 0.7, 0.7))
