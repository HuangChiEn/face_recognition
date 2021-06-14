## Face Recognition with GUI, ( v1.0 )

## The development life cycle mainly divided into 3 stage :
1. Build the Page functionality GUI, and embedding the kernel functions, s.t. face detection, face recognition into the GUI component. 
   (GUI building will be the main point in this stage and kernel function fork by lightweight open-source project)
   version v1.x

2. Improved the kernel functions and replace the CV-based part (s.t. SVM classifier) into deep-learning network, but taking the efficiency into account.
   (Network building will be the main point in this stage and self-design network is possible) 
   version v2.x

3. Package the software via suitable way (s.t. exe file, docker image, web-service) and reveal the spark point via the profile.
   (Package the software will be the min point and realiable profile will be build as the objective metric). 
   version v3.x

# After service and Dev-Ops still on the blue print. 

## pre-requirement

# important version of package (more info -- conda_env.txt) : 
 ( python == 3.7.0 )
 ( pip == 20.2.4 )

# do the following command on your virtual-env
pip install -r requirement.txt


## execute the GUI
(1) on the command line
	python main.py  
(2) on the jupyter notebook
	open jupyter_lab_hook -> choice the corresponding kernel -> execute the first cell.

## GUI kernel function :

# Face Registration -- 
  1. type your name into the prompt entry and then submit.
  system reply > open a window to record the webcam source (can be extended from other source).
  
  2. press '　' (space key) for take the shot and save the cropped image into image_gallery dir.
  system show > The bounding box will locate your face, and you're free to take a photo.
    
  3. press 'q' key for quit the face shot.
  system reply > close the window which record the webcam source.

# Face Recognition --
  1. when you register the face (run Face Registration), you need to Update the recognition system.
  2. press the recognition buttom.

# Update System
  1. when you register the face (run Face Registration), you need to Update the recognition system.
  2. press the update system buttom. 

# Face Gallery Set --
  1. just show all the name of registered face.
  (Not build yet..)

# Login History --
  (Not build yet..)

# Quit --
  Quit all software and close the window.
