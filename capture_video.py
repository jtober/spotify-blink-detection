#import necessary libraries
import cv2
import dlib
import math
import spotify

BLINK_RATIO_THRESHOLD = 5.7

#Understand blink ratio
def midpoint(point1 ,point2):
    return int((point1.x + point2.x)/2), int((point1.y + point2.y)/2)

def euclidean_distance(point1 , point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_blink_ratio(eye_points, facial_landmarks):
    
    #loading all the required points
    corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                    facial_landmarks.part(eye_points[0]).y)
    corner_right = (facial_landmarks.part(eye_points[3]).x, 
                    facial_landmarks.part(eye_points[3]).y)
    
    center_top    = midpoint(facial_landmarks.part(eye_points[1]), 
                             facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), 
                             facial_landmarks.part(eye_points[4]))

    #calculating distance
    horizontal_length = euclidean_distance(corner_left,corner_right)
    vertical_length = euclidean_distance(center_top,center_bottom)

    ratio = horizontal_length / vertical_length

    return ratio

#get the livestream video from webcam
stream = cv2.VideoCapture(0)

#name the window that will pop up
cv2.namedWindow("Test Window")

#face detection
detector = dlib.get_frontal_face_detector()

#Detecting the eyes using landmarks in dlib
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#these landmarks are based on the image above 
left_eye_landmarks = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]

while True:
    #capturing frame
    retval, frame = stream.read()
    
    #exit the application if frame not found
    if not retval:
        print("Can't receive frame. Closing the window.")
        break 
    
    #covert to grayscale to better work with blink detection later
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detecting faces in the frame 
    faces,_,_ = detector.run(image = frame, upsample_num_times = 0, adjust_threshold = 0.0)

    #look at the face
    for face in faces:
        landmarks = predictor(frame, face)

        #Calculate blink ratio for one eye
        left_eye_ratio  = get_blink_ratio(left_eye_landmarks, landmarks)
        right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
        blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2

        if blink_ratio > BLINK_RATIO_THRESHOLD:
            #This means that a blink was detected
            cv2.putText(frame,"BLINKING",(10,50), cv2.FONT_HERSHEY_SIMPLEX,
            2,(255,255,255),2,cv2.LINE_AA)
            
            #now we incorate the spotipy API to pause or play our current song
            #we just need to call our play/pause function from the spotify file
            song = spotify.pause_play()

            if song:
                print("Paused the song!")
            else:
                print("Played the song!")
            

    cv2.imshow('Video Stream', frame)
    key = cv2.waitKey(1)
    #if the user presses the esc key, then the program will stop and close the window
    if key == 27:
        break

#releasing the VideoCapture object and closing the window
stream.release()
cv2.destroyAllWindows()

