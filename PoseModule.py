import cv2
import mediapipe as mp

from Constants import LANDMARK_NAMES, RIGHT_HAND_LANDMARK_NAMES, LEFT_HAND_LANDMARK_NAMES


class PoseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, detection=0.5, trackCon=0.7):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detection = detection
        self.trackCon = trackCon
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic.Holistic(self.mode, model_complexity=2, enable_segmentation=self.upBody,
                                                  smooth_segmentation=self.smooth,
                                                  min_detection_confidence=self.detection,
                                                  min_tracking_confidence=self.trackCon, refine_face_landmarks=False)

    def detectPose(self, frame, draw=True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        self.result = self.holistic.process(frame_rgb)

        if self.result.face_landmarks and draw:
            self.mp_drawing.draw_landmarks(frame, self.result.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
        # Draw the pose landmarks on the frame
        if self.result.pose_landmarks and draw:
            self.mp_drawing.draw_landmarks(frame, self.result.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)

        return frame

    def getPosition(self, frame, draw=False):
        landmarkDict = dict()
        i = 0
        if self.result.pose_landmarks:
            for id, lm in enumerate(self.result.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkDict[LANDMARK_NAMES[id]] = (cx, cy)
                if draw:
                    cv2.circle(frame, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
        if self.result.face_landmarks:
            for id, lm in enumerate(self.result.face_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkDict[str(i)] = (cx, cy)
                i = i + 1
                if draw:
                    cv2.circle(frame, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
        if self.result.right_hand_landmarks:
            for id, lm in enumerate(self.result.right_hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkDict[RIGHT_HAND_LANDMARK_NAMES[id]] = (cx, cy)
                if draw:
                    cv2.circle(frame, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
        if self.result.left_hand_landmarks:
            for id, lm in enumerate(self.result.left_hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarkDict[LEFT_HAND_LANDMARK_NAMES[id]] = (cx, cy)
                if draw:
                    cv2.circle(frame, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
        return landmarkDict
