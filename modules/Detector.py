## Author          : Jolo Tolentino
## Project Name    : SEER-V2
## Project Started : January 25,2022



### Detecor.py uses the YOLO object detection model by default but can be changed


import numpy as np 
import os 
import cv2 
import yaml 



class Detector:
    def __init__(self,threshold):
        CFG_File = open(str(os.path.dirname(os.getcwd()+'\config\config.yaml')))
        Parsed_CFG = yaml.load(CFG_File,Loader=yaml.FullLoader)

        #Load Yolo Model Configurations from CFG file
        Yolo_Model_CFG = Parsed_CFG['Yolo CFG']
        Yolo_Model_Weights = Parsed_CFG['Yolo Weights']
        Yolo_Model_Names = Parsed_CFG['Yolo Names']
        self.Yolo_Labels = Parsed_CFG['Yolo Labels']

        ##
        self.Thresh = threshold

        #Scaling 
        self.Image_Scale_Factor = Parsed_CFG["Image Scale"]
        self.Image_Size = Parsed_CFG['Image Size']

        #Load Model onto memory using OpenCV
        self.Yolo_Model = cv2.dnn.readNetFromDarknet(Yolo_Model_CFG,Yolo_Model_Weights)

    

        if self.Yolo_Model:
            print("Object Detection Model Loaded")
            Layer_Names = self.Yolo_Model.getLayerNames()
            self.Necessary_Layers = [Layer_Names[layers-1] for layers in self.Yolo_Model.getUnconnectedOutLayers()] 
        else: 
            print("Object Detection Model Not Found...")






    def Detect(self,data, draw = False):
        
        # STORAGE VARIABLES Initialize every Use when detecting
        self.Boxes, self.Confidences, self.Classification_ID = [],[],[]
        Height,Width = data.shape[0],data.shape[1]
        #Blob from Image preprocesses input data (mean subtraction, normalizing(Image Scale Factor), OPTIONAL (Channel Swapping))
        self.BLOB = cv2.dnn.blobFromImage(data,self.Image_Scale_Factor,self.Image_Size,swapRB = True)
        self.Yolo_Model.setInput(self.BLOB)
        self.Predictions = self.Yolo_Model.forward(self.Necessary_Layers)

        for predictions in self.Predictions:
            for objects in predictions: 

                Scores = objects[5:]
                Classification = np.argmax(Scores)
                Confidence  = Scores[Classification]

                if Confidence>self.Thresh:
                    Box = objects[:4]*np.array(Width,Height,Width,Height)
                    (CenterX,CenterY,Width,Height) = Box.astype('int')
                    XMin, YMin = CenterX-Width//2 , CenterY-Height//2
                    

                    self.Boxes.append([XMin,YMin,Width,Height])
                    self.Confidences.append(float(Confidence))
                    self.Classification_ID.append(float(Classification))


        self.Indexes=cv2.dnnNMSBoxes(self.Boxes,self.Confidences,self.Thresh,self.Thresh)

        if draw: 
            self.OverLay(data)
            

    def OverLay(self,Yolo_Video_Feed):
        try:
            for i in self.Indexes.flatten():
                (x, y) = (self.Boxes[i][0],self.Boxes[i][1])
                (w, h) = (self.Boxes[i][2], self.Boxes[i][3])          
                ## checking corresponding color for Class Predicted
                color = [int(c) for c in self.COLORS[self.Classification_IDs[i]]]
                ## Drawing Information into copied Video Frame 
                cv2.rectangle(Yolo_Video_Feed, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.2f}".format(self.Yolo_Labels[self.Classification_IDs[i]], self.Confidences[i])
                cv2.putText(Yolo_Video_Feed, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)  

        except: 
            print("Model has low confidence in the Environment....")
            return 


    def Find(self,target):

        

        se
        pass


        