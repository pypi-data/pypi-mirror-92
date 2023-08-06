""" Functions to post process the reconstructed 3D data """

import numpy as np
from skimage import measure, registration


def get_shifted_area_segmentation(area, shift):
    """Area is image with nonzero values that should be shifted and shift is a vector with the length of shift for each dimension of the area array"""
    shape = area.shape
    coordinates = np.where(area)
    valid_rows = np.ones(len(coordinates[0]))
    shifted_coordinates = np.zeros((len(shape), len(valid_rows)))
    for i, c in enumerate(coordinates):
        shifted_c = c + shift[i]
        # remove coordinates that are outside of the image
        valid_rows = valid_rows & (shifted_c >= 0) & (shifted_c < shape[i])
        shifted_coordinates[i] = shifted_c
    # print(np.sum(valid_rows) / len(valid_rows))
    shifted_coordinates = shifted_coordinates[valid_rows]

    shifted_area = np.zeros(shape, dtype=bool)
    shifted_area[tuple(shifted_coordinates)] = True
    return shifted_area


def temporal_alignment(reconstructions):
    """Attempt to temporally align the reconstructions by tracking blobs.
    This will only be applied to blobs that get disconnected from the main area with pixels that are connected to the absolute_phase pixel in calibration.
    All reconstructions should have the same original shape of images and absolute_phase_coordinates set for their calibration. If not these are met, an assertion error is raised.

    This function is not that robust but works ok if the objects are moving less than 10 pixels per frame

    :reconstructions: list of dicts
        all reconstructions to align, each reconstruction is a dict with at least the keys grid and calibration
    :returns: None
    """
    # Check that all reconstructions have absolute_phase_coordinates
    # and check that the reconstructions all have the same shape
    absolute_phase_coordinates = []
    shape = reconstructions[0]["grid"].shape
    for reconstruction in reconstructions[1:]:
        if "absolute_phase" in reconstruction["calibration"]:
            absolute_phase_coordinates.append(
                reconstruction["calibration"]["absolute_phase"][:2]
            )
        assert (
            shape == reconstruction["grid"].shape
        ), "All shapes must be the same for temporal alignment"
    assert len(absolute_phase_coordinates) == len(
        reconstructions
    ), "Without absolute_phase_coordinates for all reconstructions it does not make sense to use --temporal-alignment"
    absolute_phase_coordinates = np.array(absolute_phase_coordinates)

    last_last_threed_values = reconstructions[0]["grid"][2]

    last_threed_values = reconstructions[1]["grid"][2]
    if np.ma.isMaskedArray(last_threed_values):
        last_segmentation = ~last_threed_values.mask
    else:
        last_segmentation = np.ones(last_threed_values.shape, dtype=bool)
    last_labels, last_n_labels = measure.label(
        last_segmentation.astype(int), return_num=True
    )
    last_velocities = (
        {}
    )  # this is some kind on mean velocity in the third dimension for each area in the image

    absolute_phase_label = last_labels[tuple(absolute_phase_coordinates[0][::-1])]
    last_velocities[absolute_phase_label] = "absolute"

    # to estimate velocity in 3D at least two previous reconstructions are required
    for i in range(2, len(reconstructions)):
        reconstruction = reconstructions[i]

        threed_values = reconstruction["grid"][2]
        if np.ma.isMaskedArray(threed_values):
            segmentation = ~threed_values.mask
        else:
            segmentation = np.ones(threed_values.shape, dtype=bool)

        # Using labeled connected components to find the different areas in the image
        labels, n_labels = measure.label((segmentation).astype(int), return_num=True)
        absolute_phase_label = labels[tuple(absolute_phase_coordinates[i][::-1])]
        velocities = {absolute_phase_label: "absolute"}

        for j in range(1, n_labels + 1):
            if j == absolute_phase_label:
                continue  # no tracking required for areas with known absolute phase
            area = labels == j
            shift, error, diffphase = registration.phase_cross_correlation(
                last_segmentation, area
            )

            # Tracking to find where this area was in the last image
            shifted_area = get_shifted_area_segmentation(area, shift)

            tracked_labels, lengths = np.unique(
                last_labels[shifted_area], return_counts=True
            )
            best_track_ind = np.argmax(lengths)
            tracked_trueness = lengths[best_track_ind] / np.sum(lengths)
            if tracked_trueness < 0.5:
                print(
                    "Warning, tracking match in temporal_alignment found to be too low, {} for label {}".format(
                        tracked_trueness, j
                    )
                )
                continue
            tracked_label = tracked_labels[best_track_ind]  # area found

            if tracked_label in last_velocities:
                if isinstance(last_velocities[tracked_label], float):
                    velocity = last_velocities[tracked_label]
                elif last_velocities[tracked_label] == "absolute":
                    # This is the first time the area is released from the area with absolute phase
                    # First the threed velocity is estimated by looking one frame further back and same shift again
                    shifted_shifted_area = get_shifted_area_segmentation(
                        shifted_area, shift
                    )
                    velocity = np.median(
                        np.ma.compressed(
                            last_threed_values[shifted_area]
                            - last_last_threed_values[shifted_shifted_area]
                        )
                    )

                velocity[j] = velocity
                # estimating the difference between the areas
                diff = threed_values[area] - last_threed_values[shifted_area]
                # median difference is used to set them at the same place
                l = np.median(np.ma.compressed(diff))
                # remove median difference to last area and add the estimated 3D velocity
                threed_values[area] = threed_values[area] - l + velocity

        reconstruction["grid"][2] = threed_values

        # Setting for next iteration
        last_last_threed_values = last_threed_values
        last_threed_values = threed_values
        last_segmentation = segmentation
        last_labels = labels
        last_velocities = velocities
