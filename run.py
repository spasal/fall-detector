''''
Abstract - algorithm for real-time detection of human fall from video
Applications - support elderly people living alone in their home
Goal - shorten the time between the fall and the arrival of aid
How - intelligent video suveillance is the simplest way of detecting the fall
Algorithm -
    1 background estimation
    2 extraction of moving objects
    3 motion feature extraction
    4 fall detection
Accuracy goal - at least 85%% of cases (100% is impossible)
'''


def main():
    import cv2
    import core
    import helper

    # 1 prepare frame for shape analysis
    def background_estimation(src):
        ''''
        prepares the frame for further analysis.
        1: frame --> gray and blur
        2: mask, bin_treshold --> MOG2 background substraction
        3: find biggest contour inside bin_treshold
        '''

        src, gray = helper.frame_operations.prepare_frame(src)
        backgroundmask, bintreshold = core.background_substraction(gray)
        largest_contour = helper.frame_operations.find_largest_contour(bintreshold)

        if largest_contour is not None:
            bintreshold = helper.frame_operations.clean_frame_within_contour(
                bintreshold, largest_contour)
            backgroundmask = helper.frame_operations.clean_frame_within_contour(
                backgroundmask, largest_contour)

        return src, backgroundmask, bintreshold, largest_contour


    # 2 shape analysis for further feature exraction
    def shape_analysis(binary_threshold, contour):
        ''''
        1: calculate ellipse around contour
        2: calculate pca around contour
            a: get mean_vector
            b: get median direction vector
        3: calculate motion history image
        '''

        ellipse = helper.calculus.calculate_ellipse(contour)
        big_axis_length = ellipse[0][1]/2

        eig_pairs, mean_vec = core.pca_methods.calculate_pca(contour)

        if mean_vec is not None and eig_pairs is not None:
            # 1 eig vectors
            eig_vecs = core.pca_methods.get_latest_eig_vectors(eig_pairs)
            points = helper.calculus.calculate_points(
                eig_vecs, mean_vec, big_axis_length)

            # 2 calculate motion history image
            mhi = core.motion_history.calculate_mhi_frame(
                binary_threshold, frame)

        return points, mean_vec, mhi


    # 3 feature extraction from shape analysis
    def feature_extraction(contour, eig_vecs_points, binary_threshold, mhi):
        ''''
        1: calculate both PCA angles
        2: calculate delta angle between the 2 vectors
        3: calculate motion coefficient
        '''

        vector_angles = helper.calculus.calculate_vectors_angle(
            eig_vecs_points)

        delta_angle = helper.calculus.calculate_delta_angle(
            eig_vecs_points[0], eig_vecs_points[1])

        movement_coeff = core.motion_history.calculate_movement_coeff(
            contour, binary_threshold, mhi)

        return vector_angles, delta_angle, movement_coeff


    # 4 the fall detection algorithm
    def fall_detection(mean_vec, vector_angles, delta_angle, movement_coeff):
        ''''
        1: movement of centrum
        2: speed of change pca
        3: mate van verandering
        '''

        (mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas) = core.fall_detection.calculate_values(
            mean_vec, delta_angle, vector_angles)

        is_fall = core.fall_detection.is_fall()

        return mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas, is_fall


    # extra: draw relevant data
    def draw_primary_values(contour, eig_vecs_points, vector_angles, delta_angle, movement_coeff, is_fall, src):
        helper.frame_operations.draw_ellipse(
            src, contour, is_fall)

        core.pca_methods.draw_pca_on_image(
            eig_vecs_points, src)

        helper.frame_operations.draw_feature_extraction(
            vector_angles, delta_angle, movement_coeff, src)

    def draw_secondary_values(mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas):
        print(mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas)


    # main: here runs the code
    cap = cv2.VideoCapture(0)
    grabbed = False
    while not grabbed:
        (grabbed, frame) = cap.read()
        if grabbed:
            core.motion_history.initialze_mhi(frame)


    while cap.isOpened():
        (grabbed, frame) = cap.read()
        if not grabbed: break

        frame, background_mask, binary_threshold, largest_contour = background_estimation(frame)

        if largest_contour is not None:
            (eig_vecs_points, mean_vec, mhi) = shape_analysis(
                background_mask, largest_contour)

            (vector_angles, delta_angle, movement_coeff) = feature_extraction(
                largest_contour, eig_vecs_points, background_mask, mhi)

            (mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas, is_fall) = fall_detection(
                mean_vec, vector_angles, delta_angle, movement_coeff)

            draw_primary_values(
                largest_contour, eig_vecs_points, vector_angles, delta_angle, movement_coeff, is_fall, frame)

            draw_secondary_values(
                mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas)

        cv2.imshow('feed', frame)
        cv2.imshow('backgroundmask', background_mask)
        cv2.imshow('binTreshold', binary_threshold)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
