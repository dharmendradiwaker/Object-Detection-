# -*- coding: utf-8 -*-
"""car_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tX1ZVEAcnbNiebYi69qQCIQlK-lhUMB4

# Importing the library
"""

#Checking the GPU
!nvidia-smi

#save the home folder
import os
HOME = os.getcwd()
print(HOME)

# Pip install method (recommended)
#import required libraries

!pip install ultralytics==8.0.196

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

#import yolo model to train on dataset
from ultralytics import YOLO

from IPython.display import display, Image

"""#Import label data from roboflow by api"""

#import data
!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="your api")
project = rf.workspace("carproject-4fzh7").project("car-project-vlhuw")
version = project.version(3)
dataset = version.download("yolov8")

"""#Training the dataset"""

# Commented out IPython magic to ensure Python compatibility.
#train the dataset on yolov8s model.with 50 epochs to get the best result
# %cd {HOME}


!yolo task=detect mode=train model=yolov8s.pt data={dataset.location}/data.yaml epochs=1 imgsz=800 plots=True

#checking the files
!ls {HOME}/runs/detect/train/

# Commented out IPython magic to ensure Python compatibility.
#checking the confusion matrix
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/confusion_matrix.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
#checking the losses
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
#checking model on training dataset
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/val_batch0_pred.jpg', width=600)

# Commented out IPython magic to ensure Python compatibility.
#run model on validation dataset
# %cd {HOME}

!yolo task=detect mode=val model={HOME}/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml

"""#Test the dataset"""

# Commented out IPython magic to ensure Python compatibility.
#checking the model on test dataset
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.25 source={dataset.location}/test/images save=True

# predict the images after run on model
import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/detect/predict/*.jpg')[:5]:
      display(Image(filename=image_path, width=600))
      print("\n")

video_path_1 = '/content/5.mp4'

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.25 source={video_path_1} save=True