# This is Scene B
import pygame
import pygwidgets
import pyghelpers
import pygame
from MovementCorrectnessModel import MovementCorrectnessModel
from Constants import *

class CameraScene():
    def __init__(self, window):
        self.window = window
        self.movement_model = MovementCorrectnessModel()
        self.font = pygame.font.SysFont(None, 24)
    def draw(self, frame_with_pose, pose_landmarks):
        # Display the frame
        self.window.blit(frame_with_pose, (0,0))

        # Calculate angles using MovementCorrectnessModel
        angles = self.movement_model.calculateAngles(pose_landmarks)

        # Draw angles on the frame
        if angles is not None:
            for joint, angle in angles.items():
                if angle is not None:
                    if joint != 'spine':
                        x, y = int(pose_landmarks[joint][0]), int(pose_landmarks[joint][1])
                        text_surface = self.font.render(f"{joint}: {angle:.2f} degrees", True, GREEN)
                        self.window.blit(text_surface, (y, x))
                    else:
                        text_surface = self.font.render(
                            f"{joint}: \n left distance:{angle[0]:.2f} \n right distance:{angle[1]:.2f} ", True, GREEN)
                        self.window.blit(text_surface, (40, 200))

            # Analyze spine pose
            spine_info = angles['spine']
            if spine_info is not None:
                if abs(spine_info[0] - spine_info[1]) <= 10:  # Tolerance of 10 degrees
                    text_surface = self.font.render("Spine Straight", True, GREEN)
                    self.window.blit(text_surface, (20, 100))
                else:
                    text_surface = self.font.render("Spine Not Straight", True, RED)
                    self.window.blit(text_surface, (20, 100))
        return "camera_view"