import math

import numpy as np


class MovementCorrectnessModel():

    def __init__(self):
        pass

    def calculate_angles(self, landmarks):
        angles = {}

        if landmarks:
            # Calculate angles for each specified joint
            angles['left_shoulder'] = self.calculate_angle(landmarks['left_elbow'], landmarks['left_shoulder'],
                                                           landmarks['left_hip'])
            angles['right_shoulder'] = self.calculate_angle(landmarks['right_elbow'], landmarks['right_shoulder'],
                                                            landmarks['right_hip'])
            angles['left_elbow'] = self.calculate_angle(landmarks['left_shoulder'], landmarks['left_elbow'],
                                                        landmarks['left_wrist'])
            angles['right_elbow'] = self.calculate_angle(landmarks['right_shoulder'], landmarks['right_elbow'],
                                                         landmarks['right_wrist'])
            angles['spine'] = self.calculateSpineAngle(landmarks)

            return angles
        else:
            return None

    def calculateDistance(self, a, b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def calculateSpineAngle(self, landmarks):
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']

        # Calculate angle between shoulders and hips
        #mid_shoulder = ((left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2)
        #mid_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
        # spine_angle_degrees = self.calculateAngle(mid_shoulder,mid_hip,right_hip)
        left_distance = self.calculateDistance(left_shoulder, right_hip)
        right_distance = self.calculateDistance(right_shoulder, left_hip)
        #spine_mid_distance = self.calculateDistance(mid_shoulder, mid_hip)
        return abs(left_distance- right_distance) < 5

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def calculate_distance(self, a, b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def is_linear(self, p1, p2, p3, tolerance=15):
        return self.calculate_angle(p1, p2, p3) < tolerance
