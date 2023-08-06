
from pydicom import dcmread
import os
from skimage.measure import find_contours
import numpy as np

def load_sorted_image_series(dicom_series_path: str):
        series_data = []
        for root, _, files in os.walk(dicom_series_path):
            for file in files:
                if file.endswith('.dcm'):
                    ds = dcmread(os.path.join(root, file))
                    # Only add CT images
                    if not hasattr(ds.file_meta, 'MediaStorageSOPClassUID'):
                        continue
                    if ds.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.2': # CT Image Storage
                        series_data.append(ds)

        if len(series_data) == 0:
            raise Exception("No DICOM data found in input path")

        # Sort slices in ascending order
        series_data.sort(key=lambda ds: ds.SliceLocation, reverse=False)

        return series_data

def get_contours_coords(mask_slice: np.ndarray, series_slice):
    # Method will find multiple contours if possible. Ensure only one is found
    contours = find_contours(mask_slice)
    validate_contours(contours)
    contour = contours[0]
    translated_contour = translate_contour_to_data_coordinants(contour, series_slice)
    formated_contour = format_contour_for_dicom(translated_contour, series_slice)

    return formated_contour # Data is located in first index

def validate_contours(contours):
    if len(contours) == 0:
        raise Exception("Unable to find contour in non empty mask, please check your mask formatting"
    )
    if len(contours) > 1:
        print(
            "ERROR: unexpected number of counters in slice. " +
            f"Expected 1, got {len(contours)}"
            )

def translate_contour_to_data_coordinants(contour, series_slice):
    offset = series_slice.ImagePositionPatient
    spacing = series_slice.PixelSpacing
    contour[:, 0] = (contour[:, 0]) * spacing[0] + offset[0]
    contour[:, 1] = (contour[:, 1]) * spacing[1] + offset[1]
    return contour

def format_contour_for_dicom(contour, series_slice):
    # DICOM uses a 1d array of x, y, z coords
    z_indicies = np.ones((contour.shape[0], 1)) * series_slice.SliceLocation
    contour = np.concatenate((contour, z_indicies), axis = 1)
    contour = np.ravel(contour)
    contour = contour.tolist()
    return contour