import Constants
import pygame

def draw_avatar(window, pose_landmarks):
    for connection in Constants.CONNECTIONS:
        start_name, end_name = connection
        start_point = pose_landmarks.get(start_name)
        end_point = pose_landmarks.get(end_name)
        if start_point and end_point:
            pygame.draw.line(window, (0, 255, 0), (start_point[1], start_point[0]),
                             (end_point[1], end_point[0]), 5)  # Draw a line between the points
    for connection in Constants.point_list:
        start_name, end_name = connection
        start_point = pose_landmarks.get(start_name)
        end_point = pose_landmarks.get(end_name)
        if start_point and end_point:
            pygame.draw.line(window, (0, 255, 0), (start_point[1], start_point[0]),
                             (end_point[1], end_point[0]), 1)  # Draw a line between the points

    # Draw circles on detected pose landmarks
    for name, point in pose_landmarks.items():
        if point:
            if name not in ["nose", "left_eye_inner", "left_eye_outer",
                            "right_eye_inner", "right_eye_outer", "left_ear",
                            "right_ear", "mouth_left", "mouth_right", "left_pinky",
                            "right_pinky", "left_index", "right_index", "left_thumb",
                            "RIGHT_WRIST", "LEFT_WRIST", "right_thumb"]:
                pygame.draw.circle(window, (0, 255, 255), (int(point[1]), int(point[0])),
                                   2)  # Draw a circle at the point