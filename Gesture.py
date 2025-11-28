class Gesture :
    def __init__(self) :
        self.activate_gestures = 0
        self.go_back_gesture = 0
        self.next_gesture = 0

    def check_gesture(self, pose_landmarks):
        if (pose_landmarks.get("right_wrist") and pose_landmarks.get("right_elbow")) is not None:
            if pose_landmarks.get("right_wrist")[0] < pose_landmarks.get("right_elbow")[0]:
                if (pose_landmarks.get("RIGHT_THUMB_TIP") and pose_landmarks.get("RIGHT_THUMB_CMC")
                    and pose_landmarks.get("RIGHT_INDEX_FINGER_TIP") and pose_landmarks.get("RIGHT_INDEX_FINGER_MCP")) is not None:
                    if (pose_landmarks.get("RIGHT_THUMB_TIP")[1] > pose_landmarks.get("RIGHT_THUMB_IP")[1]) and (
                            pose_landmarks.get("RIGHT_INDEX_FINGER_TIP")[0] > pose_landmarks.get("RIGHT_INDEX_FINGER_MCP")[0]):
                        self.activate_gestures += 1
                    # if not (pose_landmarks.get("RIGHT_THUMB_TIP")[1] > pose_landmarks.get("RIGHT_THUMB_CMC")[1]) and (
                    #         pose_landmarks.get("RIGHT_INDEX_FINGER_TIP")[0] > pose_landmarks.get("RIGHT_INDEX_FINGER_MCP")[0]) \
                    #         and self.activate_gestures > 30:
                    #     self.go_back_gesture += 1
                    # if (pose_landmarks.get("RIGHT_THUMB_TIP")[1] > pose_landmarks.get("RIGHT_THUMB_CMC")[1]) and not (
                    #         pose_landmarks.get("RIGHT_INDEX_FINGER_TIP")[0] > pose_landmarks.get("RIGHT_INDEX_FINGER_MCP")[0]) \
                    #         and self.activate_gestures > 4:
                    #     self.next_gesture += 1

    def reset_gesture(self) :
        self.activate_gestures = 0
        self.next_gesture = 0
        self.go_back_gesture = 0
