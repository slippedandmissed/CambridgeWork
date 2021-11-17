import numpy as np
import matplotlib.pyplot as plt

def rxy():
    N = 10000
    face_radius = 1
    eye_radius = 0.1
    mouth_radius = 0.3
    mouth_height = -0.1
    line_thickness = 0.05
    eye_separation = 0.2
    eye_height = 0.3
    
    
    part = np.random.randint(low=0, high=4, size=(N))
    outer_ring = np.where(part == 0, 1, 0)
    left_eye = np.where(part == 1, 1, 0)
    right_eye = np.where(part == 2, 1, 0)
    mouth = np.where(part == 3, 1, 0)


    face_angle = np.random.uniform(low=0, high=2*np.pi, size=(N))
    face_r = np.random.uniform(low=face_radius, high=face_radius+line_thickness, size=(N))
    face_x = face_r * np.cos(face_angle)
    face_y = face_r * np.sin(face_angle)

    mouth_angle = face_angle/2.0
    mouth_r = np.random.uniform(low=mouth_radius, high=mouth_radius+line_thickness, size=(N))
    mouth_x = mouth_r * np.cos(mouth_angle)
    mouth_y = mouth_height - mouth_r * np.sin(mouth_angle)

    left_eye_x = eye_radius * np.cos(face_angle) + eye_separation
    right_eye_x = left_eye_x - (2 * eye_separation)
    eye_y = eye_radius * np.sin(face_angle) + eye_height

    x = (outer_ring * face_x) + (left_eye * left_eye_x) + (right_eye * right_eye_x) + (mouth * mouth_x)
    y = (outer_ring * face_y) + (left_eye * eye_y) + (right_eye * eye_y) + (mouth * mouth_y)

    return (x, y)

x, y = rxy()


#plt.scatter(x, y)

#plt.hist(x)
plt.hist(y)

plt.show()
