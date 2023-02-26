import cv2 as cv
import numpy as np
from math import *
from wpimath.geometry import *
import json

# Camera calibration constants
camera_matrix = np.array([[742.483468466319, 0.0,              637.2421086110966], 
                          [0.0,              741.833232408462, 401.5930628745256], 
                          [0.0,              0.0,              1.0              ]])
dist_coeffs = np.array([ 0.10050662325551381,
                        -0.048995749738143635, 
                        -0.0014568776758625078, 
                         0.0012852294132110506,
                        -0.15731800217755504])

def load_field_layout():
  pose_map = {}
  field = json.load(open('assets/2023-chargedup.json'))
  for object in field['tags']:
    pose = object['pose']
    translation = pose['translation']
    quat = pose['rotation']['quaternion']
    pose_map[object['ID']] = Pose3d(Translation3d(translation['x'], translation['y'], translation['z']), 
                                    Rotation3d(Quaternion(quat['W'], quat['X'], quat['Y'], quat['Z'])))
  return pose_map

def translation_to_point3d(translation):
  return np.array([-translation.Y(), -translation.Z(), +translation.X()])

def solve_corner_to_object(cornerX, cornerY, tagPose):
  corner_translation = tagPose.translation() + Translation3d(0, cornerX, cornerY).rotateBy(tagPose.rotation())
  return translation_to_point3d(corner_translation)

def solve_tag_corners(tag_pose):
    return np.array([solve_corner_to_object(+0.0762, -0.0762, tag_pose),
                     solve_corner_to_object(-0.0762, -0.0762, tag_pose),
                     solve_corner_to_object(-0.0762, +0.0762, tag_pose),
                     solve_corner_to_object(+0.0762, +0.0762, tag_pose)])

def solve_pose(corners, ids, tag_map):
    # Estimate the pose using cv2.solvePnP
    image_points = None
    object_points = None
    for tag_index in range(0, len(ids)):
      id = ids[tag_index][0]
      if id in tag_map.keys():
        if image_points is None:
          image_points = corners[tag_index][0]
          object_points = solve_tag_corners(tag_map[id])
        else:
          image_points = np.concatenate((image_points, corners[tag_index][0]), axis=0)
          object_points = np.concatenate((object_points, solve_tag_corners(tag_map[id])))
    
    if image_points is None:
      return None

    _, rvec, tvec = cv.solvePnP(object_points, image_points, camera_matrix, dist_coeffs, flags=0)

    rotation_matrix, _ = cv.Rodrigues(rvec)
    translation_vector = -np.dot(np.transpose(rotation_matrix), tvec)

    rot3d = Rotation3d(np.array([+rvec[2][0], -rvec[0][0], +rvec[1][0]]),
                       sqrt(pow(rvec[0][0], 2) + pow(rvec[1][0], 2) + pow(rvec[2][0], 2)))

    return Pose3d(Translation3d(+translation_vector[2], 
                                -translation_vector[0], 
                                -translation_vector[1]), rot3d)