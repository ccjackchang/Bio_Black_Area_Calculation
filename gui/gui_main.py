import cv2
import glob
import gui
import numpy as np
import os
import pandas as pd
from PyQt5 import QtGui, QtCore, QtWidgets
import sys

class MainUIClass(QtWidgets.QMainWindow, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dir_name = None
        self.step = 0

        self.pushButton.clicked.connect(self.main_progress)
        self.pushButton_2.clicked.connect(self.get_dir_name)

    def reset(self):
        self.step = 0
        self.progressBar.setValue(0)

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
    
    def main_progress(self):
        self.reset()
        results = []
        progress_percent = 0
        files = glob.glob(self.dir_name+"/*")
        total = len(files)
        for num, img_path in enumerate(files, start=1):
            img_name = os.path.basename(img_path)
            img = cv2.imread(img_path)
            bk_rate = self.calculate_black(img)
            results.append([img_name, bk_rate])
            progress_rate = num/total
            progress_percent = round(progress_rate*100)
            self.progressBar.setValue(progress_percent)
        
        img_folder = os.path.dirname(self.dir_name+"/*").split('/')[-1] 
        final = pd.DataFrame(results,columns=['image_name','black_rate'])
        os.makedirs("./results/", exist_ok=True)
        final.to_csv("./results/"+ img_folder +"_results.csv", index = False)
        
    def get_dir_name(self):
        self.dir_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.label_3.setText(self.dir_name)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainUIClass()
    window.show()
    sys.exit(app.exec_())