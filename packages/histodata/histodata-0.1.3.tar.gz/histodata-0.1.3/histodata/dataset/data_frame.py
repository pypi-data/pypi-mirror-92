import math
import os
import re

import cv2
import numpy as np
import pandas as pd
from scipy.ndimage.measurements import center_of_mass
from skimage import morphology
from skimage.segmentation import slic


class DataFrameCreator:
    def __init__(self):
        pass

    def __call__(self, path_to_image):
        pass


class CreateDFDummy(DataFrameCreator):
    def __init__(self, num_of_entries=100):
        super().__init__()
        self.num_of_entries = num_of_entries

    def __call__(self, path_to_image):
        df = pd.DataFrame({"id": range(self.num_of_entries)})
        df["fold"] = df.apply(lambda row: row["id"] % 10, 1)
        df["is_even"] = df.apply(lambda row: (row["id"] % 2) == 0, 1)
        return df


class CreateDFFromCSV(DataFrameCreator):
    def __init__(self, path_to_csv, sep=","):
        super().__init__()
        self.path_to_csv = path_to_csv
        self.sep = sep

    def __call__(self, path_to_image):
        if isinstance(self.path_to_csv, list):
            df = pd.DataFrame()
            for path in self.path_to_csv:
                tmp_df = pd.read_csv(path, sep=self.sep)
                tmp_df["__from_csv__"] = path
                df = df.append(tmp_df)
            return df
        else:
            return pd.read_csv(self.path_to_csv, sep=self.sep)


class CreateDFFromFolder(DataFrameCreator):
    def __init__(self, file_of_interest):
        super().__init__()
        self.file_of_interest = file_of_interest

        regex = ""
        tmp = file_of_interest
        self.var_names = []
        counter_unnamed = 0
        while len(tmp) > 0:
            var_start = tmp.find("{")
            var_unnamed_start = tmp.find("(")
            if (
                var_unnamed_start != -1
                and (var_unnamed_start < var_start or var_start == -1)
                and (var_unnamed_start == 0 or tmp[var_unnamed_start - 1] != "\\")
            ):
                regex += tmp[: var_unnamed_start + 1]
                tmp = tmp[var_unnamed_start + 1 :]
                self.var_names.append("unnamed_" + str(counter_unnamed))
                counter_unnamed += 1
            elif var_start == -1:  # No Variable could be found
                regex += tmp
                tmp = ""
            else:
                # ignore this var start
                if var_start > 0 and tmp[var_start - 1] == "\\":
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                else:
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                    var_end = tmp.find("}")
                    self.var_names.append(tmp[1:var_end])
                    # self.regex += '(?=.*)'
                    # regex += '(^[^/]*)'
                    regex += "(.*)"
                    tmp = tmp[var_end + 1 :]
        self.regex = re.compile(regex)

    def __call__(self, path_to_image):
        rows = {name: [] for name in self.var_names}
        rows["__path__"] = []
        for root, _, files in os.walk(path_to_image):
            for file in files:
                path = os.path.join(root, file)[len(path_to_image) :]
                result = self.regex.search(path)
                if result is not None:
                    path_as_variable = False
                    row = {}
                    for vname, var in zip(self.var_names, result.groups()):
                        row[vname] = var
                        if var.find("/") != -1:
                            path_as_variable = True
                    if path_as_variable is False:
                        for k in row:
                            rows[k].append(row[k])
                        rows["__path__"].append(path)

        return pd.DataFrame(rows)


class DataFrameEditor:
    def __init__(self):
        pass

    def __call__(self, df, path_to_image):
        pass


class EditDFImageGrid(DataFrameEditor):
    def __init__(self, return_image_size, perc_overlapping=0.0, input_im_size=None):
        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping
        self.input_im_size = input_im_size

    def get_points(self, im_size1d):
        im_size_center = im_size1d - self.return_image_size
        shift = self.return_image_size * (1 - self.perc_overlapping)
        locations = np.arange(0, im_size_center + 0.0001, shift)

        return np.array(locations + (im_size1d - locations[-1]) / 2, dtype=int)

    def __call__(self, df, path_to_image, reader):
        if self.input_im_size is not None:
            input_im_size = self.input_im_size

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        for _, row in df.iterrows():
            if self.input_im_size is None:
                input_im_size = reader.get_image_size(row, path_to_image)
            xs = self.get_points(input_im_size[0])
            ys = self.get_points(input_im_size[1])

            for x in xs:
                for y in ys:
                    row = dict(row)
                    row["__x__"] = x
                    row["__y__"] = y

                    for k in row:
                        rows[k].append(row[k])

        return pd.DataFrame(rows)


# an example function using intensity thresholding and morphological
# operations to obtain tissue regions
def simple_get_mask(rgb):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  # threshold using OTSU method
    mask = morphology.remove_small_objects(mask == 0, min_size=100, connectivity=2)
    mask = morphology.remove_small_holes(mask, area_threshold=100)
    mask = morphology.binary_dilation(mask, morphology.disk(5))
    return mask


class EditDFWSIGrid(DataFrameEditor):
    def __init__(self, return_image_size, perc_overlapping=0.0):
        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping

    def __get_coordinates__(self, thumbnail, thumbnail_mpp, return_mpp):
        print(thumbnail.shape)
        # see: https://colab.research.google.com/github/TIA-Lab
        # /tiatoolbox/blob/master/examples/example_wsiread.ipynb#scrollTo=MZ_yqoGJ_-6i
        wsi_thumb_mask = simple_get_mask(thumbnail)

        lores_patch_size = int(self.return_image_size / (thumbnail_mpp / return_mpp))
        nr_expected_rois = math.ceil(np.sum(wsi_thumb_mask) / (lores_patch_size ** 2))

        print(lores_patch_size, nr_expected_rois)

        wsi_rois_mask = slic(
            thumbnail, mask=wsi_thumb_mask, n_segments=nr_expected_rois, compactness=1000, sigma=1
        )

        lores_rois_center = center_of_mass(
            wsi_rois_mask, labels=wsi_rois_mask, index=np.unique(wsi_rois_mask)[1:]
        )
        lores_rois_center = np.array(lores_rois_center)  # coordinates is Y, X
        lores_rois_center = lores_rois_center.astype(np.int32)
        selected_indices = wsi_thumb_mask[lores_rois_center[:, 0], lores_rois_center[:, 1]]
        lores_rois_center = lores_rois_center[selected_indices]

        return lores_rois_center * (thumbnail_mpp / return_mpp)

    def __call__(self, df, path_to_image, reader):

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        for _, row in df.iterrows():

            thumbnail = reader.read_thumbnail(row, path_to_image, 50)
            coordinates = self.__get_coordinates__(thumbnail, 50, reader.mpp)

            for c in coordinates:
                row = dict(row)
                row["__x__"] = int(c[0])
                row["__y__"] = int(c[1])

                for k in row:
                    rows[k].append(row[k])

        return pd.DataFrame(rows)
