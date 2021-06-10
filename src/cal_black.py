import cv2
import glob
import numpy as np
import os
import pandas as pd
from tqdm import tqdm

def calculate_black(img):
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


if __name__=='__main__':
    results = []
    
    with tqdm(total=len(glob.glob("./pic/*"))) as pbar:
        for img_path in glob.glob("./pic/*"):
            img_name = os.path.basename(img_path)
            img = cv2.imread(img_path)
            bk_rate = calculate_black(img)
            results.append([img_name,bk_rate])
            pbar.update(1)
    
    final = pd.DataFrame(results,columns=['image_name','black_rate'])
    print(final)
    final.to_csv("./black_area.csv", index = False)
