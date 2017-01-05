import numpy as np
import cv2
__latestEigValues1, __latestEigValues2 = [], []
__latestEigValues1.append([]), __latestEigValues1.append([])
__latestEigValues2.append([]), __latestEigValues2.append([])

def calculate_pca(contour):
    # Re-organize data set (Matrix X = rowvector n x p variabels)
    contour = np.reshape(contour, (contour.shape[0], contour.shape[2]))

    # Calculate d-dimensional empirical mean vector
    mean_x = np.mean(contour[:,0])
    mean_y = np.mean(contour[:,1])
    vec_center = np.array([[mean_x], [mean_y]]).reshape(1, -1)

    # Calculate deviations from mean
    mean_dev = []
    for row in contour:
        mean_dev.append(row - vec_center)
    
    mean_dev = np.asarray(mean_dev)
    mean_dev = np.reshape(mean_dev, (mean_dev.shape[0], mean_dev.shape[2]))

    # Get the covariance matrix
    cov_mat = np.cov([mean_dev[:,0], mean_dev[:,1]])

    # Find eigenvectors and eigenvalues of covariance matrix
    mean, eigenvectors = cv2.PCACompute(cov_mat, vec_center)
    retval, eigenvalues, eigenvectors2 = cv2.eigen(cov_mat)
    eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)

    # Pair vectors and values and sort desc (get biggest first)
    eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
    eig_pairs.sort(key=lambda x: x[0], reverse=True)
    eig_pairs = eig_pairs[0:2]

    return eig_pairs, vec_center


def get_latest_eig_vectors(eig_pairs):
    index = 0
    for pair in eig_pairs:
        eig_vec = pair[1]
        if index is 0:
            __latestEigValues1[0].append(eig_vec[0])
            __latestEigValues1[1].append(eig_vec[1])
            index += 1
        else:
            __latestEigValues2[0].append(eig_vec[0])
            __latestEigValues2[1].append(eig_vec[1])
            if len(__latestEigValues2[0]) > 10:
                __latestEigValues1[0].pop(0)
                __latestEigValues1[1].pop(0)
                __latestEigValues2[0].pop(0)
                __latestEigValues2[1].pop(0)

    direction1 = [np.mean(__latestEigValues1[0]), np.mean(__latestEigValues1[1])]
    direction2 = [np.mean(__latestEigValues2[0]), np.mean(__latestEigValues2[1])]
    return [direction1, direction2]

def draw_pca_on_image2(eig_vecs, mean_vec, axis_length, src):
    startpoint = mean_vec[0]
    isfirst = True

    for direction in eig_vecs:
        x_add, y_add = direction[0] * axis_length, direction[1] * axis_length
        add = np.array([[x_add], [y_add]]).reshape(1, -1)[0]
        endpoint = startpoint + add

        color = (0, 0, 255) if isfirst is True else (0, 255, 0)
        cv2.line(src, (int(startpoint[0]), int(startpoint[1])), (int(endpoint[0]), int(endpoint[1])), color, 5)
        isfirst = False

    return src

def draw_pca_on_image(points, src):
    isfirst = True
    for point_combination in points:
        color = (0, 0, 255) if isfirst is True else (0, 255, 0)
        cv2.line(src, (int(point_combination[0][0]), int(point_combination[0][1])), (int(point_combination[1][0]), int(point_combination[1][1])), color, 5)
        isfirst = False

    return src