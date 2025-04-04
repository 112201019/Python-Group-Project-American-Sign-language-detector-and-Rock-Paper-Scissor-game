def download_modules():
    print("You do not have the necessary modules installed!")
    input("Press any key to start installation!!")

    while True:

        try:
            #Runs the following in command prompt of system
            os.system("py -m pip install --user opencv-python")
            os.system("py -m pip install --user cvzone")
            os.system("py -m pip install --user mediapipe")
            os.system("py -m pip install --user numpy")
            os.system("py -m pip install --user scikit-learn")

            #Import after installation
            import cv2
            import mediapipe as mp
            import numpy as np
            import pickle

            print("Modules successfully installed")
            input("Press enter to continue")
            break

        except ModuleNotFoundError:
            #If internet connection isn't there it raises this error
            print("Are you connected to the internet?")
            print("Please check your internet and try again")
            input("Press enter to try again")

import os
def mainASL():
    try:
        #Imports modules if available
        import cv2
        import mediapipe as mp
        import numpy as np
        import pickle


    except ModuleNotFoundError:
        #If module isnt downloaded, starts installation
        download_modules()
        import cv2
        import mediapipe as mp
        import numpy as np
        import pickle


    #Loads trained model for comparision
    model_dict = pickle.load(open('American-Sign-Language-Detector-main/American-Sign-Language-Detector-main/ASL/trained_model.p', 'rb'))
    model = model_dict['model']

    cap = cv2.VideoCapture(0)

    #Drawing function on hands initialization
    drawing = mp.solutions.drawing_utils
    drawing_styles = mp.solutions.drawing_styles

    #Initialise hands class
    hand = mp.solutions.hands

    #Sets up hand detection, if comp is sure above 30% then it reads image as hand
    hands = hand.Hands(static_image_mode=True, min_detection_confidence=0.3)

    #Sets label values(letters)
    labels_dict = {0: 'A',
                    1: 'B',
                    2: 'C',
                    3: 'D',
                    4: 'E',
                    5: 'F',
                    6: 'G',
                    7: 'H',
                    8: 'I',
                    9: 'J',
                    10: 'K',
                    11: 'L',
                    12: 'M',
                    13: 'N',
                    14: 'O',
                    15: 'P',
                    16: 'Q',
                    17: 'R',
                    18: 'S',
                    19: 'T',
                    20: 'U',
                    21: 'V',
                    22: 'W',
                    23: 'X',
                    24: 'Y',
                    25: 'Z'}
    while True:

        #Initialize variables, stores image captured, changes BGR to RGB
        data_aux, x_, y_ = [],[],[]

        success, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        #Checks if handmarks are detected then iterates through them all 
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #Draws landmarks on hands visible
                drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    hand.HAND_CONNECTIONS,  # hand connections
                    drawing_styles.get_default_hand_landmarks_style(),
                    drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    #Saves x,y coordinate of every handpoint as array
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    #For normalisation of dataset, takes only distance between data
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            #Takes points of start and end points of hands
            x1 = int(min(x_) * w) - 10
            y1 = int(min(y_) * h) - 10

            x2 = int(max(x_) * w) - 10
            y2 = int(max(y_) * h) - 10

            #Predicts the character using model as reference
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            #Makes a frame with 10 pixel offset and places predicted character above it
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                        (0, 0, 0), 3, cv2.LINE_AA)

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)

        #Esc key closes all windows
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
