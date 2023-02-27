import json
import numpy as np

from wpimath.geometry import *

def load_json(filepath):
  return json.load(open(filepath))

def load_calibration():
  calibration_map = {}
  calibration = load_json('assets/calibration.json')
  for constants in calibration['constants']:
    calibration_map[constants['ID']] = [np.array(constants['extrinsics']), np.array(constants['distortion'])]
  return calibration_map

def load_field_layout():
  pose_map = {}
  field = load_json('assets/2023-chargedup.json')
  for object in field['tags']:
    pose = object['pose']
    translation = pose['translation']
    quat = pose['rotation']['quaternion']
    pose_map[object['ID']] = Pose3d(Translation3d(translation['x'], translation['y'], translation['z']), 
                                    Rotation3d(Quaternion(quat['W'], quat['X'], quat['Y'], quat['Z'])))
  return pose_map