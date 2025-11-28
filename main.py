# Your imports here
import cv2
import pygame

from Scenes.CameraScene import CameraScene
from Scenes.ExerciseScene import ExerciseScene
from Scenes.ProfileScene import ProfileScene
from Scenes.AvatarScene import  AvatarScene
from Scenes.FinalReportScene import Report
from Scenes.LoginScene import LoginScene
from Scenes.SettingsScene import SettingsScene
from MovementCorrectnessModel import MovementCorrectnessModel
from Player import Player
from PoseModule import PoseDetector
import SaveLoad
from Constants import PROFILES



# Constants
FRAMES_PER_SECOND = 60
PROFILE_SCENE = "profile_view"
AVATAR_SCENE = "avatar_view"
LOGIN_SCENE = "login_view"
CAMERA_SCENE = "camera_view"
EXERCISE_SCENE = "exercise_view"
REPORT_SCENE = "report_view"
SETTINGS_SCENE = "settings_view"

# Initialize pygame and other necessary components
pygame.init()
font = pygame.font.SysFont("Comic Sans MS", 24)
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("width: ", width)
print("h: ", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

game_window = pygame.display.set_mode((width, height))
camera_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physical Therapy Game")

# Initialize pose detector and movement correctness model
pose_detector = PoseDetector()
movement_model = MovementCorrectnessModel()

# Initialize player
save_load = SaveLoad.SaveLoad()

players = save_load.load()
picked_player = None
# Instantiate scenes
profile_scene = ProfileScene(game_window, players)
avatar_scene = AvatarScene(game_window)
login_scene = LoginScene(game_window)
settings_scene = SettingsScene(game_window)
exercise_scene = ExerciseScene(game_window)
camera_scene = CameraScene(camera_window)
report = Report(game_window)

# Set initial scene
current_scene = PROFILE_SCENE

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    # Capture frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Rotate frame if necessary and detect pose landmarks
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_with_pose = pose_detector.detectPose(frame)
    pose_landmarks = pose_detector.getPosition(frame)

    # Convert frame to Pygame surface
    frame_with_pose = cv2.cvtColor(frame_with_pose, cv2.COLOR_BGR2RGB)
    frame_with_pose = pygame.surfarray.make_surface(frame_with_pose)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update current scene and switch if necessary
    if current_scene == PROFILE_SCENE:
        player, current_scene = profile_scene.draw(pose_landmarks, players)
        if player is not None:
            if type(player) == int:
                save_load.delete_player(player)
                players = save_load.load()
                profile_scene.set_buttons(players)
                profile_scene.set_functionality(0)
            else:
                picked_player = player
        elif current_scene == AVATAR_SCENE:
            picked_player = Player()
            players.append(picked_player)
    elif current_scene == AVATAR_SCENE:
        idx, current_scene = avatar_scene.draw(pose_landmarks)
        if idx >= 0:
            picked_player.set_name(PROFILES[idx][1])
            picked_player.set_img(PROFILES[idx][0])
            profile_scene.set_buttons(players)
        profile_scene.set_functionality(0)
    elif current_scene == LOGIN_SCENE:
        current_scene = login_scene.draw(pose_landmarks)
    elif current_scene == SETTINGS_SCENE:
        picked_player, current_scene = settings_scene.draw(pose_landmarks, picked_player)
        if type(picked_player) == int:
            profile_scene.set_functionality(picked_player)
    elif current_scene == EXERCISE_SCENE:
        current_scene = exercise_scene.draw(pose_landmarks, picked_player)
    elif current_scene == REPORT_SCENE:
        current_scene = report.draw(pose_landmarks, picked_player)
    # Refresh the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FRAMES_PER_SECOND)

# Release resources
cap.release()
pygame.quit()
