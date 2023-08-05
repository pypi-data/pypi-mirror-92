"""
Abitary Utils for crYOLO
"""
#
# COPYRIGHT
#
# All contributions by Ngoc Anh Huyn:
# Copyright (c) 2017, Ngoc Anh Huyn.
# All rights reserved.
#
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#
import numpy as np
import sys
import copy

from . import imagereader
import urllib.request, json
from sklearn import mixture

class Filament:
    """
    Filament object
    """

    def __init__(self, boxes=None):
        """
        Constructor
        :param boxes: Boxes of the filament
        """

        if boxes is None:
            self.boxes = []
        else:
            self.boxes = boxes

    def add_box(self, box):
        """
        Appends a box to the filament box list.
        :param box: box to append
        :return: filament object
        """
        self.boxes.append(box)
        return self

    def get_num_boxes(self):
        """
        :return: Number of boxes that belong the filament

        """
        return len(self.boxes)

    def does_overlap(self, box, threshold):
        """
        Compares a box with all other boxes in the filament box list and calculates the IOU overlap.
        This overlap if compared to a threshold.
        :param box: Box to compare
        :param threshold: IOU Threshold
        :return: True if IOU >= threshold
        """

        for filbox in self.boxes:
            if bbox_iou(filbox, box) >= threshold:
                return True
        return False


class BoundBox:
    """
    A bounding box of a particle
    """

    def __init__(self, x, y, w, h, c=None, classes=None, z=None, depth=None):
        """
        Creates a BoundBox
        :param x: x coordinate of the center
        :param y: y coordinate of the center
        :param w: width of box
        :param h: height of the box
        :param c: confidence of the box
        :param classes: Class of the BoundBox object
        """

        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.depth = depth
        self.meta = {}

        self.c = c
        self.classes = classes

        self.label = -1
        self.score = -1
        self.info = None  # helping data during processing

    def get_label(self):
        """

        :return: Class with highest probability
        """
        if self.label == -1:
            self.label = np.argmax(self.classes)

        return self.label

    def get_score(self):
        """
        :return: Probability of the class
        """
        # if self.score == -1:
        self.score = self.classes[self.get_label()]

        return self.score

from enum import Enum
class CryoloMode(Enum):

    FIXED_SIZE=1
    MIXED_ASPECT_RATIO=2
    SQUARE=3
    NON_SQUARE=4


def getEquidistantBoxes(box1, box2, num_boxes):
    """
    Create multiple boxes between box1 and box2 with equdistant boxes
    :param box1: First box
    :param box2: Second box
    :param num_boxes: number of boxes
    :return: List of N=num_boxes equidistant boxes between box1 and box2
    """
    dat = [np.linspace(box1.x, box2.x, num_boxes + 1, endpoint=True), np.linspace(box1.y, box2.y, num_boxes + 1, endpoint=True)]
    if box1.z is not None and box2.z is not None:
        dat.append(np.linspace(box1.z, box2.z, num_boxes + 1, endpoint=True))

    points = zip(*dat)
    new_boxes = []
    if box1.c is None or box2.c is None:
        c = 1
    else:
        c = (box1.c + box2.c) / 2
    classes = ""
    if box1.classes:
        classes = box1.classes
    w = box1.w
    h = box2.w
    for point in points:
        b = BoundBox(x=point[0], y=point[1], w=w, h=h, c=c, classes=classes)
        if len(point) == 3:
            b.z = int(np.round(point[2]))
        new_boxes.append(b)
    return new_boxes


def resample_filaments(new_filaments, box_distance):
    """
    Resample a list of filaments
    :param new_filaments: List of filament
    :param box_distance: Target distance between two boxes
    :return: List of resampled filaments
    """
    res_fils = [
        resample_filament(fil, box_distance) for fil in new_filaments
    ]

    res_fils = [fil for fil in res_fils if fil is not None and fil.boxes]
    return res_fils


def resample_filament(filament, distance):
    """
    Resamples a filament. The new filament will have a specified distance between the boxes.
    :param filament: Target filament
    :param distance: Distance between two adjacent boxes.
    :return: Resampeld filament
    """
    # Find two boxes with maximum distance
    boxes = filament.boxes
    max_distance = -1
    max_boxa = None
    for i in range(len(boxes)):
        for j in range(len(boxes)):
            if i == j:
                continue
            dist = box_squared_distance(boxes[i], boxes[j])
            if dist > max_distance:
                max_boxa = i

    if max_boxa is not None:
        # Construct a polyline, start from max_boxa
        polyline = []
        polyline.append(boxes[max_boxa])
        assigned_boxes = []
        assigned_boxes.append(max_boxa)
        last_appended_box = boxes[max_boxa]
        last_appended_index = max_boxa
        added_new = True

        while added_new:
            min_distance = 99999999
            nearest_box_index = None
            added_new = False
            for i in range(len(boxes)):
                if i == last_appended_index:
                    continue
                if i in assigned_boxes:
                    continue

                measured_distance = box_squared_distance(last_appended_box, boxes[i])

                if measured_distance < min_distance:
                    nearest_box_index = i
                    min_distance = measured_distance

            if nearest_box_index is not None:
                polyline.append(boxes[nearest_box_index])
                assigned_boxes.append(nearest_box_index)
                last_appended_box = boxes[nearest_box_index]
                last_appended_index = nearest_box_index
                added_new = True

        # Create new boxes based on the polyline
        new_boxes_candidates = []
        sqdistance = distance * distance

        for i in range(len(polyline) - 1):
            eq_boxes = getEquidistantBoxes(polyline[i], polyline[i + 1], num_boxes=100)
            new_boxes_candidates.extend(eq_boxes)
        new_boxes = []
        dist = -1
        for box in new_boxes_candidates:
            if dist == -1:
                new_boxes.append(box)
                dist = 0
            else:
                dist = box_squared_distance(new_boxes[len(new_boxes) - 1], box)
                if dist > sqdistance:
                    new_boxes.append(box)

        new_filament = Filament()
        for box in new_boxes:
            new_filament.add_box(box)

        return new_filament
    return None

def get_cryolo_mode(size_distr, config_input_size):
    square_data_available = any([size[0] == size[1] for size in size_distr])
    non_square_data_available = any([size[0] != size[1] for size in size_distr])

    if type(config_input_size) == list:
        return CryoloMode.FIXED_SIZE

    if (square_data_available and non_square_data_available) or \
            (non_square_data_available and len(size_distr)>1):
        return CryoloMode.MIXED_ASPECT_RATIO

    if square_data_available and not non_square_data_available:
        return CryoloMode.SQUARE

    if not square_data_available and non_square_data_available and len(size_distr)==1:
        return CryoloMode.NON_SQUARE

def get_custom_paramters_from_model(model_path):
    import h5py
    params_dict = {}
    with h5py.File(model_path, mode="r") as f:
        if "anchors" in f:
            params_dict["anchors"] = list(f["anchors"])
        if "num_free_layers" in f:
            params_dict["num_free_layers"] = int(list(f["num_free_layers"])[0])
        if "cryolo_version" in f:
            params_dict["cryolo_version"] = list(f["cryolo_version"])[0].decode("utf-8")

    return params_dict
def anchor_to_boxsize(anchor_dim,grid_dim, input_image_dim):
    """
    COnverts network anchors back to box size
    :param anchor_dim
    :param grid_dim: Grid dimension
    :param input_image_dim: Input image dimension
    :return: box width box height
    """
    import cryolo.config_tools as config_tools
    grid_w, grid_h = grid_dim #config_tools.get_gridcell_dimensions(config)
    img_width,img_height = input_image_dim
    anchor_width, anchor_height = anchor_dim
    cell_w = img_width / grid_w
    cell_h = img_height / grid_h
    box_width = anchor_width*cell_w
    box_height = anchor_height*cell_h
    return box_width,box_height

def get_anchors(config, path_weights=None, image_sizes=None):
    '''
    Calculates the anchors.
    When fixed size mode ...
    When non-square mode...
    When square-mode ...
    When mixed-size mode

    :param config:
    :param path_weights:
    :param image_size:
    :return:
    '''
    import cryolo.config_tools as config_tools

    is_single_anchor = len(config["model"]["anchors"]) == 2
    num_patches = 1
    if "num_patches" in config["model"]:
        num_patches = config["model"]["num_patches"]

    grid_w, grid_h = config_tools.get_gridcell_dimensions(config)
    anchors = None

    if path_weights:
        import h5py

        with h5py.File(path_weights, mode="r") as f:
            try:
                anchors = list(f["anchors"])
            except KeyError:
                anchors = None

    if is_single_anchor and anchors is None:

        # if single size, use the it as given
        # if multi-size, use the average length of the short side
        #
        if len(image_sizes) == 1:
            img_width = float(image_sizes[0][1]) / num_patches
            img_height = float(image_sizes[0][0]) / num_patches
        else:
            sum_size = 0
            sum_num_images = 0
            for img_info in image_sizes:
                if img_info[0]>img_info[1]:
                    sum_size += img_info[1] * img_info[2]
                else:
                    sum_size += img_info[0] * img_info[2]
                sum_num_images += img_info[2]
            mean_size = int(sum_size/sum_num_images)
            img_width = mean_size
            img_height = mean_size


        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        box_width, box_height = config_tools.get_box_size(config)

        anchor_width = 1.0 * box_width / cell_w
        anchor_height = 1.0 * box_height / cell_h
        anchors = [anchor_width, anchor_height]
    elif anchors is None:
        img_width = 4096.0 / num_patches
        img_height = 4096.0 / num_patches
        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        anchors = np.array(config["model"]["anchors"], dtype=float)
        anchors[::2] = anchors[::2] / cell_w
        anchors[1::2] = anchors[1::2] / cell_h

    return anchors


def box_squared_distance(boxa, boxb):
    """
    calculates the squared distance between the center of two boxes.
    :param boxa: First box
    :param boxb: Second box
    :return: Squared distance between boxa and boxb
    """
    sqd = np.square(boxa.x - boxb.x) + np.square(boxa.y - boxb.y)

    if boxa.z is not None and boxb.z is not None:
        sqd = sqd + np.square(boxa.z - boxb.z)
    return sqd

def get_normalization_func(normalization):
    if normalization == "STANDARD":
        norm_func = normalize
    elif normalization == "GMM":
        norm_func = normalize_gmm
    else:
        print("Normalization option ", normalization, "unknown. Check your config file.")
        import sys
        sys.exit(1)
    return norm_func

def normalize_gmm(image, margin_size=0):


    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]

    clf = mixture.GaussianMixture(n_components=2, covariance_type='diag')
    clf.fit(np.expand_dims(image[mask].ravel()[::15], axis=1))
    mean = None
    var = None
    if (clf.means_[1, 0]>clf.means_[0, 0]):
        mean = clf.means_[1, 0]
        var = clf.covariances_[1, 0]
    else:
        mean = clf.means_[0, 0]
        var = clf.covariances_[0, 0]
    #print(mean,var,np.sqrt(var))
    image = (image - mean) / (2*3*np.sqrt(var))

    return image

def normalize(image, margin_size=0):
    """
    Normalize an image. If wanted, a specified relative margin can be ignored.
    :param image: Image to normalize
    :param margin_size: Relative size of the margin to be ignored during normalization. Number between 0 - 1.
    :return: Normalized image
    """
    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]
    img_mean = np.mean(image[mask])
    img_std = np.std(image[mask])

    image = (image - img_mean) / (3 * 2 * img_std+0.000001)

    return image


def bbox_iou(box1, box2):
    """
    Calculates the intersection of union for two boxes.
    :param box1: First box
    :param box2: Second box
    :return: Intersection of union
    """
    x1_min = box1.x - box1.w / 2
    x1_max = box1.x + box1.w / 2
    y1_min = box1.y - box1.h / 2
    y1_max = box1.y + box1.h / 2

    x2_min = box2.x - box2.w / 2
    x2_max = box2.x + box2.w / 2
    y2_min = box2.y - box2.h / 2
    y2_max = box2.y + box2.h / 2

    intersect_w = interval_overlap([x1_min, x1_max], [x2_min, x2_max])
    intersect_h = interval_overlap([y1_min, y1_max], [y2_min, y2_max])

    intersect = intersect_w * intersect_h

    union = box1.w * box1.h + box2.w * box2.h - intersect

    return float(intersect) / union


def interval_overlap(interval_a, interval_b):
    """
    Calculates the overlap between two intervals
    :param interval_a: Tuple with two elements (lower and upper bound)
    :param interval_b: Tuple with two elements (lower and upper bound)
    :return: Overlap between two intervals
    """
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2, x4) - x1
    else:
        if x2 < x3:
            return 0
        else:
            return min(x2, x4) - x3


def sigmoid(x):
    """
    Sigmoid function
    :param x: argument
    :return: sigmoid of x
    """
    return 1.0 / (1.0 + np.exp(-x))


def get_num_fine_tune_layers(path_weights):
    import h5py

    with h5py.File(path_weights, mode="r") as f:
        try:
            num_free_layers = int(list(f["num_free_layers"])[0])
        except KeyError:
            num_free_layers = None
    return num_free_layers


def filter_image_noise2noise(img_path, model_path, padding=15, batch_size=4, resize_to=None):
    """
    Filters an images using JANNI (noise2noise implementation)
    :param img_path: Input image
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :return: Denoised image
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    image = imagereader.image_read(img_path)
    fitlered_img = janni_predict.predict_np(
        model, image, patch_size=(1024, 1024), padding=padding, batch_size=batch_size
    )



    return fitlered_img

def filter_images_lowpass(
    img_paths, output_dir_filtered_imgs, cutoff, num_cpus=-1, otf=False, resize_to=None
):
    import os
    import multiprocessing
    from . import lowpass

    """
    Filteres a list of images and return a new list with the paths to the filtered images.

    :param img_paths: Path to images to filter
    :param output_dir_filtered_imgs: Output directory to save the filtered images
    :param cutoff: Absolute cutoff frequency (0-0.5)
    :return: List of paths to the filtered images
    """
    if not otf and not os.path.isdir(output_dir_filtered_imgs):
        os.makedirs(output_dir_filtered_imgs)

    arg_tubles = []
    for img_id, img_pth in enumerate(img_paths):
        if os.path.basename(img_pth)[0] != ".":
            if otf:
                arg_tubles.append((img_pth, cutoff, resize_to))
            else:
                arg_tubles.append(
                    (
                        img_pth,
                        cutoff,
                        output_dir_filtered_imgs,
                        img_id + 1,
                        len(img_paths),
                        resize_to,
                    )
                )

    num_processes = int(multiprocessing.cpu_count() / 2)
    if num_cpus != -1:
        num_processes = num_cpus

    #num_processes = 1
    #maxtaskperchild = max(1,int(np.ceil(len(arg_tubles)/num_processes)))

    pool = multiprocessing.Pool(
        maxtasksperchild=None,
        processes=num_processes,
    )

    if otf:
        filtered_images = pool.starmap(
            lowpass.filter_single_image, arg_tubles, chunksize=1
        )

    else:
        filtered_images = pool.starmap(
            lowpass.filter_single_image_and_write_to_disk, arg_tubles, chunksize=1
        )
    pool.close()
    pool.join()

    filtered_images = [img for img in filtered_images if img is not None]
    return filtered_images


def filter_images_noise2noise_dir(
    img_paths,
    output_dir_filtered_imgs,
    model_path,
    padding=15,
    batch_size=4,
    resize_to=None,
):
    """
    Filters multiple images using JANNI (noise2noise implementation) and save it to disk
    :param img_paths: List of images paths
    :param output_dir_filtered_imgs: Path to write denoised images
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :param resize_to: Size to which to output is resized
    :return:
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    filtered_paths = janni_predict.predict_list(
        image_paths=img_paths,
        output_path=output_dir_filtered_imgs,
        model=model,
        patch_size=patch_size,
        padding=padding,
        batch_size=batch_size,
        output_resize_to=resize_to,
        sliceswise=True
    )

    return filtered_paths


def non_maxima_suppress_fast(boxes, number_classes, nms_threshold, obj_threshold):
    for c in range(number_classes):
        sorted_indices = list(reversed(np.argsort([box.classes[c] for box in boxes])))
        boxes_data = np.empty(shape=(len(boxes), 7))
        for i, sorted_index in enumerate(sorted_indices):
            boxes_data[i, 0] = boxes[sorted_index].x
            boxes_data[i, 1] = boxes[sorted_index].y
            boxes_data[i, 2] = boxes[sorted_index].w
            boxes_data[i, 3] = boxes[sorted_index].h
            boxes_data[i, 4] = boxes[sorted_index].classes[c]
            boxes_data[i, 5] = sorted_index
            boxes_data[i, 6] = i

        for i in range(len(boxes_data)):
            box_i = boxes_data[i, :]
            if box_i[4] == 0:
                continue
            else:
                other_box = boxes_data[(i + 1):]
                if other_box.shape[0] > 0:
                    boxes_i_rep = np.array([box_i] * len(other_box))
                    ious = bbox_iou_vec(boxes_i_rep, other_box)
                    boxes_data[other_box[ious >= nms_threshold, 6].astype(int), 4] = 0

        for row in boxes_data[boxes_data[:, 4] == 0]:
            boxes[row[5].astype(int)].classes[c] = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [copy.copy(box) for box in boxes if box.get_score() > obj_threshold]

    return boxes


def non_maxima_suppress_fast_3d(boxes, nms_threshold, obj_threshold, average=True):
    '''

    :param boxes: List of boxes
    :param nms_threshold: Non-maximum-suppression threshold.
    :param obj_threshold: Boxes with a confidence lower that threshold are removed.
    :return: Filtered boxes
    '''

    if not boxes:
        return []
    number_classes = len(boxes[0].classes)
    for c in range(number_classes):
        sorted_indices = list(reversed(np.argsort([box.meta["num_boxes"] for box in boxes])))
        boxes_data = np.empty(shape=(len(boxes), 10))
        for i, sorted_index in enumerate(sorted_indices):
            boxes_data[i, 0] = boxes[sorted_index].x
            boxes_data[i, 1] = boxes[sorted_index].y
            boxes_data[i, 2] = boxes[sorted_index].z
            boxes_data[i, 3] = boxes[sorted_index].w
            boxes_data[i, 4] = boxes[sorted_index].h
            boxes_data[i, 5] = boxes[sorted_index].depth
            boxes_data[i, 6] = boxes[sorted_index].classes[c]
            boxes_data[i, 7] = sorted_index
            boxes_data[i, 8] = i
            boxes_data[i, 9] = boxes[sorted_index].meta["num_boxes"]

        for i in range(len(boxes_data)):
            box_i = boxes_data[i, :]
            if box_i[6] == 0:
                continue
            else:
                other_box = boxes_data[(i + 1):]
                if other_box.shape[0] > 0:
                    boxes_i_rep = np.array([box_i] * len(other_box))
                    ious = bbox_iou_vec_3d(boxes_i_rep, other_box)

                    if average:
                        weightsum = boxes_data[i, 6] * boxes_data[i, 9]

                        sumx = boxes_data[i, 9] * boxes_data[i, 0]
                        sumy = boxes_data[i, 9] * boxes_data[i, 1]
                        sumz = boxes_data[i, 9] * boxes_data[i, 2]
                        sumconf = boxes_data[i, 9] * boxes_data[i, 6]
                        weights = [boxes_data[i, 9]]
                        confs = [boxes_data[i, 6]]
                        for box in boxes_data[other_box[ious >= nms_threshold, 8].astype(int)]:
                            weights.append(box[9])
                            weightsum = weightsum + boxes_data[i, 6] * box[9]
                            sumx = sumx + box[9] * box[0]
                            sumy = sumy + box[9] * box[1]
                            sumz = sumz + box[9] * box[2]
                            confs.append(box[6])
                            sumconf = sumconf + box[9] * box[6]
                        boxes_data[i, 0] = sumx / weightsum
                        boxes_data[i, 1] = sumy / weightsum
                        boxes_data[i, 2] = sumz / weightsum
                        boxes_data[i, 6] = sumconf / weightsum

                    boxes_data[other_box[ious >= nms_threshold, 8].astype(int), 6] = 0

        for row in boxes_data[boxes_data[:, 6] == 0]:
            boxes[row[7].astype(int)].classes[c] = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [copy.copy(box) for box in boxes if box.get_score() > obj_threshold]

    return boxes


def bbox_iou_vec_3d(boxesA, boxesB):
    # 0 x
    # 1 y
    # 2 z
    # 3 w
    # 4 h
    # 5 depth
    # 6 confidence
    # 7 sorted index
    # 8 i

    x1_min = boxesA[:, 0] - boxesA[:, 3] / 2
    x1_max = boxesA[:, 0] + boxesA[:, 3] / 2
    y1_min = boxesA[:, 1] - boxesA[:, 4] / 2
    y1_max = boxesA[:, 1] + boxesA[:, 4] / 2
    z1_min = boxesA[:, 2] - boxesA[:, 5] / 2
    z1_max = boxesA[:, 2] + boxesA[:, 5] / 2

    x2_min = boxesB[:, 0] - boxesB[:, 3] / 2
    x2_max = boxesB[:, 0] + boxesB[:, 3] / 2
    y2_min = boxesB[:, 1] - boxesB[:, 4] / 2
    y2_max = boxesB[:, 1] + boxesB[:, 4] / 2
    z2_min = boxesB[:, 2] - boxesB[:, 5] / 2
    z2_max = boxesB[:, 2] + boxesB[:, 5] / 2

    intersect_w = interval_overlap_vec(x1_min, x1_max, x2_min, x2_max)
    intersect_h = interval_overlap_vec(y1_min, y1_max, y2_min, y2_max)
    intersect_depth = interval_overlap_vec(z1_min, z1_max, z2_min, z2_max)
    intersect = intersect_w * intersect_h * intersect_depth
    union = boxesA[:, 3] * boxesA[:, 4] * boxesA[:, 5] + boxesB[:, 3] * boxesB[:, 4] * boxesB[:,
                                                                                       5] - intersect
    return intersect / union


def bbox_iou_vec(boxesA, boxesB):
    x1_min = boxesA[:, 0] - boxesA[:, 2] / 2
    x1_max = boxesA[:, 0] + boxesA[:, 2] / 2
    y1_min = boxesA[:, 1] - boxesA[:, 3] / 2
    y1_max = boxesA[:, 1] + boxesA[:, 3] / 2

    x2_min = boxesB[:, 0] - boxesB[:, 2] / 2
    x2_max = boxesB[:, 0] + boxesB[:, 2] / 2
    y2_min = boxesB[:, 1] - boxesB[:, 3] / 2
    y2_max = boxesB[:, 1] + boxesB[:, 3] / 2
    intersect_w = interval_overlap_vec(x1_min, x1_max, x2_min, x2_max)
    intersect_h = interval_overlap_vec(y1_min, y1_max, y2_min, y2_max)
    intersect = intersect_w * intersect_h
    union = boxesA[:, 2] * boxesA[:, 3] + boxesB[:, 2] * boxesB[:, 3] - intersect
    return intersect / union


def interval_overlap_vec(x1_min, x1_max, x2_min, x2_max):
    intersect = np.zeros(shape=(len(x1_min)))
    cond_a = x2_min < x1_min
    cond_b = cond_a & (x2_max >= x1_min)
    intersect[cond_b] = np.minimum(x1_max[cond_b], x2_max[cond_b]) - x1_min[cond_b]
    cond_c = ~cond_a & (x1_max >= x2_min)
    intersect[cond_c] = np.minimum(x1_max[cond_c], x2_max[cond_c]) - x2_min[cond_c]

    return intersect

def find_corresponding_path(list_of_paths,path):
    import pathlib
    import os
    pth = pathlib.PurePath(path)
    current_lookup_var = pth.name
    paths = [path for path in list_of_paths if current_lookup_var in path]
    while len(paths) > 1:
        current_lookup_var = os.path.join(pth.parent.name,current_lookup_var)
        pth = pth.parent
        paths = [path for path in list_of_paths if current_lookup_var in path]
    return paths[0]



def write_command(filename, txt):
    try:
        import os

        os.makedirs(os.path.dirname(filename))
    except Exception:
        pass

    text_file = open(filename, "w")
    text_file.write(txt)
    text_file.close()


def check_for_updates():
    """
    Checks if cryolo updates are available
    :return: None
    """
    try:
        import cryolo

        with urllib.request.urlopen(
            url="https://pypi.org/pypi/cryolo/json", timeout=5
        ) as url:
            data = json.loads(url.read().decode())
            from distutils.version import LooseVersion as V

            current_version = cryolo.__version__
            latest_version = current_version
            for ver in data["releases"].keys():
                vers = V(ver)
                if vers > V(latest_version) and len(vers.version) == 3:
                    latest_version = ver
            if V(latest_version) > V(current_version):
                print("###############################################")
                print("New version of crYOLO available")
                print("Local version:\t\t", current_version)
                print("Latest version:\t\t", latest_version)
                print(
                    "More information here:\n",
                    "https://cryolo.readthedocs.io/en/latest/changes.html",
                )
                print("###############################################")
    except Exception as e:
        print("###############################################")
        print("Skip version check, as it failed with the following error:")
        print(e)
        print("###############################################")
        pass
