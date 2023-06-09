import cv2
import mediapipe as mp
import pyfiglet as pyg  
import time
import json

welcome=pyg.figlet_format("Welcome to the MediaPipe Camera")
print(welcome)
# import threading
# from audio import checkVoice
    
# threading.Thread(target=checkVoice).start()
# checkVoice()

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("test.mp4")
# cap = cv2.imread("hands.jpg")

pTime=0

mpDraw=mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mpholistic=mp.solutions.holistic
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=3)
mp_hands = mp.solutions.hands


holistic=mpholistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7)
facelms=None
hand_landmarks=None

student1='Abnormal'
student2='Abnormal'
student3='Abnormal'
print("Started")
with mp_hands.Hands(
    max_num_hands=6,
    
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while True:
        while cap.isOpened():
            img=cap
            success, image = cap.read()
            # if not success:
            #     # print("Ignoring empty camera frame.")
            # # If loading a video, use 'break' instead of 'continue'.
            #     continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            # image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            multiHandResults = hands.process(image)
            results=faceMesh.process(image)
            # Draw the hand annotations on the image.
            if multiHandResults.multi_hand_landmarks:
                for hand_landmarks in multiHandResults.multi_hand_landmarks:
                    mpDraw.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            else:
                hand_landmarks=None

            if results.multi_face_landmarks:
                
                for facelms in results.multi_face_landmarks:
                    mpDraw.draw_landmarks(image, facelms, mpFaceMesh.FACEMESH_TESSELATION, mpDraw.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                            mpDraw.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                            )
            
                    # handResults = holistic.process(imgRGB)
                    # mpDraw.draw_landmarks(img, handResults.right_hand_landmarks, mpholistic.HAND_CONNECTIONS, 
                    #                         mpDraw.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                    #                         mpDraw.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                    #                         )
                    # mpDraw.draw_landmarks(img, handResults.left_hand_landmarks, mpholistic.HAND_CONNECTIONS, 
                    #                         mpDraw.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                    #                         mpDraw.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                    #                         )
            else:
                facelms=None
            
            
            ctime=time.time()
            fps=1/(ctime-pTime)
            pTime=ctime
            # cv2.putText(img, f"FPS: {int(fps)}", (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
            start_point = (200, 0)
        
            # End coordinate, here (250, 250)
            # represents the bottom right corner of image
            end_point = (200, 1024)
            
            # Green color in BGR
            color = (0, 255, 0)
            
            # Line thickness of 9 px
            thickness = 3
            
            # Using cv2.line() method
            # Draw a diagonal green line with thickness of 9 px
            cv2.line(image, start_point, end_point, color, thickness)
            start_point = (400, 0)
        
            # End coordinate, here (250, 250)
            # represents the bottom right corner of image
            end_point = (400, 1024)
            
            # Green color in BGR
            color = (0, 255, 0)
            
            # Line thickness of 9 px
            thickness = 3
            
            # Using cv2.line() method
            # Draw a diagonal green line with thickness of 9 px
            cv2.line(image, start_point, end_point, color, thickness)
        
            
            if facelms == None or hand_landmarks !=None:
                        # print(handResults.right_hand_landmarks[0])
                        # tempData="Abnormal"
                        # file=open("time.txt","w")
                        # file.write(str(handResults.right_hand_landmarks[0].landmark[0]))
                        # file.close()
                        tempData="Normal"
                        
                        student1=tempData
                        student2=tempData
                        student3=tempData
                        try:
                            RightHandPath=json.dumps(str(hand_landmarks.landmark[0]))[4:14]
                        except Exception as e:
                            # print(e)
                            RightHandPath=None
                        try:
                            LeftHandPath=json.dumps(str(hand_landmarks.landmark[0]))[4:14]
                        except Exception as e:
                            # print(e)
                            LeftHandPath=None
                        try:
                            if RightHandPath!=None:
                                
                                if float(RightHandPath) <0.3:
                                    student1="Abnormal"
                                    student2="Normal"
                                    student3="Normal"
                                    print("Abnormal student1")
                                elif float(RightHandPath) >0.3 and float(RightHandPath)<0.6:
                                    student2="Abnormal"
                                    student3="Normal"
                                    student1="Normal"
                                    print("Abnormal student2")
                                elif float(RightHandPath) >0.6 and float(RightHandPath) <1 :
                                    print("Abnormal student3")
                                    student3="Abnormal"
                                    student1="Normal"
                                    student2="Normal"
                            if LeftHandPath!=None:
                                if float(LeftHandPath) <0.3:
                                    student1="Abnormal"
                                    student2="Normal"
                                    student3="Normal"
                                    print("Abnormal student1")
                                elif float(LeftHandPath) >0.3 and float(LeftHandPath)<0.6:
                                    student2="Abnormal"
                                    student3="Normal"
                                    student1="Normal"
                                    print("Abnormal student2")
                                elif float(LeftHandPath) >0.6 and float(LeftHandPath) <1 :
                                    print("Abnormal student3")
                                    student3="Abnormal"
                                    student1="Normal"
                                    student2="Normal"
                        except Exception as e:
                            pass  
            else:
                    tempData="Normal"
                    student1=tempData
                    student2=tempData
                    student3=tempData
                    print(tempData)
                    
            cv2.putText(image, f"{student1}", (0,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)

            cv2.putText(image, student2, (220,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
            cv2.putText(image, student3, (420,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
            
            cv2.imshow('MediaPipe Hands', image)
        #         print(mp_drawing.draw_landmarks)                        
                # cv2.imshow('Raw Webcam Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
