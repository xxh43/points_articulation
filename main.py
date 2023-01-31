
import copy
import numpy as np

def getRotMatrixHomo(axis, center, angle):

    u = axis[0]
    v = axis[1]
    w = axis[2]
    a = center[0]
    b = center[1]
    c = center[2]
    sin_theta = np.sin(angle)
    cos_theta = np.cos(angle)

    m00 = u*u + (v*v + w*w)*cos_theta
    m01 = u*v*(1-cos_theta)-w*sin_theta
    m02 = u*w*(1-cos_theta)+v*sin_theta
    m03 = (a*(v*v+w*w) - u*(b*v+c*w))*(1-cos_theta)+(b*w-c*v)*sin_theta
    
    m10 = u*v*(1-cos_theta)+w*sin_theta
    m11 = v*v+(u*u+w*w)*cos_theta
    m12 = v*w*(1-cos_theta)-u*sin_theta
    m13 = (b*(u*u+w*w) - v*(a*u+c*w))*(1-cos_theta)+(c*u-a*w)*sin_theta

    m20 = u*w*(1-cos_theta)-v*sin_theta
    m21 = v*w*(1-cos_theta)+u*sin_theta
    m22 = w*w+(u*u+v*v)*cos_theta
    m23 = (c*(u*u+v*v) - w*(a*u+b*v))*(1-cos_theta)+(a*v-b*u)*sin_theta
    
    rot_mat = np.stack((

        np.stack((m00, m01, m02, m03)),

        np.stack((m10, m11, m12, m13)),

        np.stack((m20, m21, m22, m23)),
    ))
    
    return rot_mat

def transform_with_homo_matrix(pc, mat):
    pad = np.ones((len(pc), 1))
    pc_homo = np.concatenate((pc, pad), axis=1)
    pc_homo = pc_homo.transpose(1, 0)
    pc_transformed = np.matmul(mat, pc_homo)
    pc_transformed = pc_transformed.transpose(1, 0)
    return pc_transformed

def translate_with_vector(pc, vector):
    translated_pc = pc + vector
    return translated_pc

def rotate_with_axis_center_angle(pc, axis, center, angle):
    axis = axis/np.linalg.norm(axis)
    mat_homo = getRotMatrixHomo(axis, center, angle)
    return transform_with_homo_matrix(pc, mat_homo)

def add_motion_to_segment(pc, motion_type, motion_axis, motion_center, motion_range):

    if motion_type == 'rotation':
        moved_pc = rotate_with_axis_center_angle(pc, motion_axis, motion_center, motion_range)
    elif motion_type == 'translation':          
        moved_pc = translate_with_vector(pc, motion_axis * motion_range)
    elif motion_type == 'static':
        moved_pc = pc
    else:
        print('wrong motion type')
        exit()

    return moved_pc

def add_motion_to_pc(pc, segment_indices, motion_types, motion_axes, motion_centers, motion_ranges):

    moved_pc = copy.deepcopy(pc)

    for i in range(len(segment_indices)):
        segment_pc = pc[segment_indices[i]]
        motion_type = motion_types[i]
        motion_axis = motion_axes[i]
        motion_center = motion_centers[i]
        motion_range = motion_ranges[i]
        moved_segment = add_motion_to_segment(segment_pc, motion_type, motion_axis, motion_center, motion_range)
        moved_pc[segment_indices[i]] = moved_segment

    return moved_pc

if __name__ == "__main__":

    pc = np.array([np.array([0, 0, 0]), np.array([0.5, 0, 0]), np.array([1.0, 0, 0]), np.array([1.5, 0, 0]), np.array([2.0, 0, 0])])
    segment_indices = [np.array([0,1]), np.array([2,3,4])]
    motion_types = ['rotation', 'translation']
    motion_axes = [np.array([0, 1, 0]), np.array([1,0,0])]
    motion_centers = [np.array([0, 0, 0]), None]
    motion_ranges = [0.25 * np.pi, 0.5]

    moved_pc = add_motion_to_pc(pc, segment_indices, motion_types, motion_axes, motion_centers, motion_ranges)

