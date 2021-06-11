import cv2
import glob
import gui
import numpy as np
import os
import pandas as pd
from PyQt5 import QtGui, QtCore, QtWidgets
import sys

class Progress(QtCore.QThread):
    """
    Runs ProgressBar in a thread
    """
    progress_percent = QtCore.pyqtSignal(int)

    def __init__(self, dir_name):
        super().__init__()
        self.dir_name = dir_name

    def calculate_black(self, img):
        rows,cols,channels = img.shape

        bk = 0

        for i in range(rows):
            for j in range(cols):
                if img[i,j][0]==0:
                    bk+=1
                else:
                    pass

        rate = bk/(rows*cols)
        # round() 到小數第二位
        bk_percent = round(rate*100,2)
        return bk_percent


    def run(self):
        results = []
        files = glob.glob(self.dir_name+"/*")
        total = len(files)
        for num, img_path in enumerate(files, start=1):
            img_name = os.path.basename(img_path)
            img = cv2.imdecode(np.fromfile(img_path ,dtype=np.uint8), 1)
            bk_rate = self.calculate_black(img)
            results.append([img_name, bk_rate])
            progress_rate = num/total
            progress_percent = round(progress_rate*100)
            self.progress_percent.emit(progress_percent)

        img_folder = os.path.dirname(self.dir_name+"/*").split('/')[-1] 
        final = pd.DataFrame(results,columns=['image_name','black_rate'])
        os.makedirs("./results/", exist_ok=True)
        final.to_csv("./results/"+ img_folder +"_results.csv", index = False)

class MainUIClass(QtWidgets.QMainWindow, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dir_name = None
        self.pushButton.clicked.connect(self.main_progress)
        self.pushButton_2.clicked.connect(self.get_dir_name)

    def reset(self):
        self.progressBar.setValue(0)
        self.pushButton.setEnabled(False)
        self.pushButton.setText("Calculating")

    def main_progress(self):
        self.reset()
        self.calc = Progress(self.dir_name)
        self.calc.start()
        self.calc.progress_percent.connect(self.setProgress)

    def setProgress(self, value):
        self.progressBar.setValue(value)
        if (value == 100):
            self.pushButton.setEnabled(True)
            self.pushButton.setText("Calculate")
    
    def get_dir_name(self):
        self.dir_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.label_3.setText(self.dir_name)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainUIClass()
    window.show()
    sys.exit(app.exec_())