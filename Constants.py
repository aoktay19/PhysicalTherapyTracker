#
# Constants, shared by all scenes
#
WINDOW_WIDTH = 2560
WINDOW_HEIGHT = 1440

# Scene keys (any unique values):
LOGIN_SCENE = 'Login'
CAMERA_SCENE = 'Camera'
EXERCISE_SCENE = "Excercise"

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
silhouette = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176,
    149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
point_list = [(str(silhouette[i]), str(silhouette[i + 1])) for i in range(len(silhouette) - 1)]
point_list.append((str(silhouette[-1]), str(silhouette[0])))
CONNECTIONS = [("left_shoulder", "right_shoulder"), ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"),
               ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"), ("left_shoulder", "left_hip"),
               ("left_hip", "left_knee"), ("left_knee", "left_ankle"), ("right_shoulder", "right_hip"),
               ("right_hip", "right_knee"), ("right_hip", "left_hip"), ("right_knee", "right_ankle"),
               ("left_ankle", "left_heel"), ("right_ankle", "right_heel"), ("left_ankle", "left_foot_index"),
               ("right_ankle", "right_foot_index"), ("left_heel", "left_foot_index"),
               ("right_heel", "right_foot_index"), ("right_wrist", "RIGHT_THUMB_CMC"),
               ("RIGHT_THUMB_CMC", "RIGHT_THUMB_MCP"), ("RIGHT_THUMB_MCP", "RIGHT_THUMB_IP"),
               ("RIGHT_THUMB_IP", "RIGHT_THUMB_TIP"),  # Thumb
               ("right_wrist", "RIGHT_INDEX_FINGER_MCP"), ("RIGHT_INDEX_FINGER_MCP", "RIGHT_INDEX_FINGER_PIP"),
               ("RIGHT_INDEX_FINGER_PIP", "RIGHT_INDEX_FINGER_DIP"),
               ("RIGHT_INDEX_FINGER_DIP", "RIGHT_INDEX_FINGER_TIP"),  # Index finger
               ("right_wrist", "RIGHT_MIDDLE_FINGER_MCP"), ("RIGHT_MIDDLE_FINGER_MCP", "RIGHT_MIDDLE_FINGER_PIP"),
               ("RIGHT_MIDDLE_FINGER_PIP", "RIGHT_MIDDLE_FINGER_DIP"),
               ("RIGHT_MIDDLE_FINGER_DIP", "RIGHT_MIDDLE_FINGER_TIP"),  # Middle finger
               ("right_wrist", "RIGHT_RING_FINGER_MCP"), ("RIGHT_RING_FINGER_MCP", "RIGHT_RING_FINGER_PIP"),
               ("RIGHT_RING_FINGER_PIP", "RIGHT_RING_FINGER_DIP"), ("RIGHT_RING_FINGER_DIP", "RIGHT_RING_FINGER_TIP"),
               # Ring finger
               ("right_wrist", "RIGHT_PINKY_MCP"), ("RIGHT_PINKY_MCP", "RIGHT_PINKY_PIP"),
               ("RIGHT_PINKY_PIP", "RIGHT_PINKY_DIP"), ("RIGHT_PINKY_DIP", "RIGHT_PINKY_TIP"),  # Pinky
               ("left_wrist", "LEFT_THUMB_CMC"), ("LEFT_THUMB_CMC", "LEFT_THUMB_MCP"),
               ("LEFT_THUMB_MCP", "LEFT_THUMB_IP"), ("LEFT_THUMB_IP", "LEFT_THUMB_TIP"),  # Thumb
               ("left_wrist", "LEFT_INDEX_FINGER_MCP"), ("LEFT_INDEX_FINGER_MCP", "LEFT_INDEX_FINGER_PIP"),
               ("LEFT_INDEX_FINGER_PIP", "LEFT_INDEX_FINGER_DIP"), ("LEFT_INDEX_FINGER_DIP", "LEFT_INDEX_FINGER_TIP"),
               # Index finger
               ("left_wrist", "LEFT_MIDDLE_FINGER_MCP"), ("LEFT_MIDDLE_FINGER_MCP", "LEFT_MIDDLE_FINGER_PIP"),
               ("LEFT_MIDDLE_FINGER_PIP", "LEFT_MIDDLE_FINGER_DIP"),
               ("LEFT_MIDDLE_FINGER_DIP", "LEFT_MIDDLE_FINGER_TIP"),  # Middle finger
               ("left_wrist", "LEFT_RING_FINGER_MCP"), ("LEFT_RING_FINGER_MCP", "LEFT_RING_FINGER_PIP"),
               ("LEFT_RING_FINGER_PIP", "LEFT_RING_FINGER_DIP"), ("LEFT_RING_FINGER_DIP", "LEFT_RING_FINGER_TIP"),
               # Ring finger
               ("left_wrist", "LEFT_PINKY_MCP"), ("LEFT_PINKY_MCP", "LEFT_PINKY_PIP"),
               ("LEFT_PINKY_PIP", "LEFT_PINKY_DIP"), ("LEFT_PINKY_DIP", "LEFT_PINKY_TIP")  # Pinky
               ]



ARM_CONNECTIONS_WITH_NAMES = [("right_shoulder", "right_elbow"), ("right_elbow", "RIGHT_WRIST"), ("RIGHT_WRIST", "RIGHT_THUMB_CMC"), ("RIGHT_THUMB_CMC", "RIGHT_THUMB_MCP"),
    ("RIGHT_THUMB_MCP", "RIGHT_THUMB_IP"), ("RIGHT_THUMB_IP", "RIGHT_THUMB_TIP"),  # Thumb
    ("RIGHT_WRIST", "RIGHT_INDEX_FINGER_MCP"), ("RIGHT_INDEX_FINGER_MCP", "RIGHT_INDEX_FINGER_PIP"),
    ("RIGHT_INDEX_FINGER_PIP", "RIGHT_INDEX_FINGER_DIP"), ("RIGHT_INDEX_FINGER_DIP", "RIGHT_INDEX_FINGER_TIP"),
    # Index finger
    ("RIGHT_WRIST", "RIGHT_MIDDLE_FINGER_MCP"), ("RIGHT_MIDDLE_FINGER_MCP", "RIGHT_MIDDLE_FINGER_PIP"),
    ("RIGHT_MIDDLE_FINGER_PIP", "RIGHT_MIDDLE_FINGER_DIP"), ("RIGHT_MIDDLE_FINGER_DIP", "RIGHT_MIDDLE_FINGER_TIP"),
    # Middle finger
    ("RIGHT_WRIST", "RIGHT_RING_FINGER_MCP"), ("RIGHT_RING_FINGER_MCP", "RIGHT_RING_FINGER_PIP"),
    ("RIGHT_RING_FINGER_PIP", "RIGHT_RING_FINGER_DIP"), ("RIGHT_RING_FINGER_DIP", "RIGHT_RING_FINGER_TIP"),
    # Ring finger
    ("RIGHT_WRIST", "RIGHT_PINKY_MCP"), ("RIGHT_PINKY_MCP", "RIGHT_PINKY_PIP"), ("RIGHT_PINKY_PIP", "RIGHT_PINKY_DIP"),
    ("RIGHT_PINKY_DIP", "RIGHT_PINKY_TIP")  # Pinky
]

HAND_CONNECTIONS_WITH_NAMES = [("RIGHT_WRIST", "RIGHT_THUMB_CMC"), ("RIGHT_THUMB_CMC", "RIGHT_THUMB_MCP"),
    ("RIGHT_THUMB_MCP", "RIGHT_THUMB_IP"), ("RIGHT_THUMB_IP", "RIGHT_THUMB_TIP"),  # Thumb
    ("RIGHT_WRIST", "RIGHT_INDEX_FINGER_MCP"), ("RIGHT_INDEX_FINGER_MCP", "RIGHT_INDEX_FINGER_PIP"),
    ("RIGHT_INDEX_FINGER_PIP", "RIGHT_INDEX_FINGER_DIP"), ("RIGHT_INDEX_FINGER_DIP", "RIGHT_INDEX_FINGER_TIP"),
    # Index finger
    ("RIGHT_WRIST", "RIGHT_MIDDLE_FINGER_MCP"), ("RIGHT_MIDDLE_FINGER_MCP", "RIGHT_MIDDLE_FINGER_PIP"),
    ("RIGHT_MIDDLE_FINGER_PIP", "RIGHT_MIDDLE_FINGER_DIP"), ("RIGHT_MIDDLE_FINGER_DIP", "RIGHT_MIDDLE_FINGER_TIP"),
    # Middle finger
    ("RIGHT_WRIST", "RIGHT_RING_FINGER_MCP"), ("RIGHT_RING_FINGER_MCP", "RIGHT_RING_FINGER_PIP"),
    ("RIGHT_RING_FINGER_PIP", "RIGHT_RING_FINGER_DIP"), ("RIGHT_RING_FINGER_DIP", "RIGHT_RING_FINGER_TIP"),
    # Ring finger
    ("RIGHT_WRIST", "RIGHT_PINKY_MCP"), ("RIGHT_PINKY_MCP", "RIGHT_PINKY_PIP"), ("RIGHT_PINKY_PIP", "RIGHT_PINKY_DIP"),
    ("RIGHT_PINKY_DIP", "RIGHT_PINKY_TIP")  # Pinky
]

LANDMARK_NAMES = (
    "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear", "mouth_left", "mouth_right", "left_shoulder", "right_shoulder", "left_elbow",
    "right_elbow", "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index", "right_index", "left_thumb",
    "right_thumb", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel",
    "right_heel", "left_foot_index", "right_foot_index",)

LEFT_HAND_LANDMARK_NAMES = (
    "LEFT_WRIST", "LEFT_THUMB_CMC", "LEFT_THUMB_MCP", "LEFT_THUMB_IP", "LEFT_THUMB_TIP", "LEFT_INDEX_FINGER_MCP",
    "LEFT_INDEX_FINGER_PIP", "LEFT_INDEX_FINGER_DIP", "LEFT_INDEX_FINGER_TIP", "LEFT_MIDDLE_FINGER_MCP",
    "LEFT_MIDDLE_FINGER_PIP", "LEFT_MIDDLE_FINGER_DIP", "LEFT_MIDDLE_FINGER_TIP", "LEFT_RING_FINGER_MCP",
    "LEFT_RING_FINGER_PIP", "LEFT_RING_FINGER_DIP", "LEFT_RING_FINGER_TIP", "LEFT_PINKY_MCP", "LEFT_PINKY_PIP",
    "LEFT_PINKY_DIP", "LEFT_PINKY_TIP")

RIGHT_HAND_LANDMARK_NAMES = (
    "RIGHT_WRIST", "RIGHT_THUMB_CMC", "RIGHT_THUMB_MCP", "RIGHT_THUMB_IP", "RIGHT_THUMB_TIP", "RIGHT_INDEX_FINGER_MCP",
    "RIGHT_INDEX_FINGER_PIP", "RIGHT_INDEX_FINGER_DIP", "RIGHT_INDEX_FINGER_TIP", "RIGHT_MIDDLE_FINGER_MCP",
    "RIGHT_MIDDLE_FINGER_PIP", "RIGHT_MIDDLE_FINGER_DIP", "RIGHT_MIDDLE_FINGER_TIP", "RIGHT_RING_FINGER_MCP",
    "RIGHT_RING_FINGER_PIP", "RIGHT_RING_FINGER_DIP", "RIGHT_RING_FINGER_TIP", "RIGHT_PINKY_MCP", "RIGHT_PINKY_PIP",
    "RIGHT_PINKY_DIP", "RIGHT_PINKY_TIP")
EXERCISE_INDEX = ["final_test"]

PROFILES = [["Assets/Images/gordon_ramsey.png", "Golden Remzi"],
            ["Assets/Images/women_chef.png", "Clare Simit"],
            ["Assets/Images/dobby.jpeg", "Çağrı Savran"]]