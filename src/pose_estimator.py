import cv2 as cv
import numpy as np
from math import *
from wpimath.geometry import *

def translation_to_point3d(translation):
  return np.array([-translation.Y(), -translation.Z(), +translation.X()])

def solve_corner_to_object(translation, tagPose):
  corner_translation = tagPose.translation() + translation.rotateBy(tagPose.rotation())
  return translation_to_point3d(corner_translation)

def solve_tag_corners(tag_pose):
    return np.array([solve_corner_to_object(Translation3d(0, -0.0762, -0.0762), tag_pose),
                     solve_corner_to_object(Translation3d(0, +0.0762, -0.0762), tag_pose),
                     solve_corner_to_object(Translation3d(0, +0.0762, +0.0762), tag_pose),
                     solve_corner_to_object(Translation3d(0, -0.0762, +0.0762), tag_pose),
                     ])

def solve_pose(calibration, corners, ids, tag_map):
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
      print("No corners detected")
      return None
    
    if len(image_points) < 8:
      print("Less than eight corners detected")
      return None

    _, rvec, tvec = cv.solvePnP(object_points, image_points, calibration[0], calibration[1], flags=cv.SOLVEPNP_SQPNP)

    rotation_matrix, _ = cv.Rodrigues(rvec)
    translation_vector = -np.dot(np.transpose(rotation_matrix), tvec)
    
    rot3d = Rotation3d(np.array([+rvec[2][0], -rvec[0][0], +rvec[1][0]]),
                       sqrt(pow(rvec[0][0], 2) + pow(rvec[1][0], 2) + pow(rvec[2][0], 2)))

    return Pose3d(Translation3d(+translation_vector[2], 
                                -translation_vector[0], 
                                -translation_vector[1]), rot3d)
