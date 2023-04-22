import csv
import os
import json
import cv2

"""
 class 1 = resistors
 class 2 = capacitors
 class 3 = inductors
 class 4 = ICs
 class 5 = diodes
 class 6 = transistors
"""


def read_csv(path: str):
    """
        Given a path to a csv file, This method will return a dictionary that contains the columns of a csv.
        The problem with the FICS dataset is that there is a JSON file in the CSV file
    :param path: The path to the CSV file
    :return: a list rows in the CSV file
    """
    ret = []
    with open(path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            ret.append(row)
    return ret


def make_files(dictionary_to_write: dict):
    """
        method will create a txt file from a dictionary given to it. Each key in the dictionary
        coresponds to a text file with the annotations for that picture
    :param dictionary_to_write:
    :return:
    """

    for key, value in dictionary_to_write.items():
        # TODO key is the name of the file
        # TODO value is a list of strigs that should be written to a txt file


if __name__ == '__main__':
    ls = os.listdir()
    ls = [x for x in ls if (x[0] == 's' and x[1].isdigit())]
    print(ls)
    annotation_write = dict()

    for folder in ls:
        path_to_csv_folder = folder + "/DSLR/annotation/"
        path_to_img_folder = folder + "/DSLR/img/"
        csv_name = [x for x in os.listdir(path_to_csv_folder) if x.find(".csv") >= 0]
        list_of_csv_files = [path_to_csv_folder + file_name for file_name in csv_name]

        print(f"[STATUS] ---- running for folder {folder}")

        for csv_file in list_of_csv_files:
            print(f"[STATUS] ---- ---- reading file {csv_file}")
            annotation_list = read_csv(csv_file)
            for annotation in annotation_list:
                comp_loc = json.loads(annotation['component_location'])

                file_name = annotation["image_name"]
                # annotations are of the form x, y, x+w, y+h
                # YOLOv5 expects it in the form of ((center + width/2), (center + ht/2))

                top_left_x = int(comp_loc["x"])
                top_left_y = int(comp_loc["y"])
                width = int(comp_loc["width"])
                height = int(comp_loc["height"])

                # s1 / DSLR / img / s1_front.tifd
                image = cv2.imread(path_to_img_folder + file_name[:-4] + ".tif")
                if image is not None:
                    img_resolution_x = image.shape[1]
                    img_resolution_y = image.shape[0]
                else:
                    print(
                        f"*******[ERR]: 404 picture{path_to_img_folder + file_name[:-4]}.tif can't be found")
                    continue

                # print(image.shape)

                component_type = annotation["component_type"]

                # YOLO format:
                if component_type == 'resistors':
                    obj_class = 1
                elif component_type == 'capacitors':
                    obj_class = 2
                elif component_type == 'inductors':
                    obj_class = 3
                elif component_type == 'ICs':
                    obj_class = 4
                elif component_type == 'diodes':
                    obj_class = 5
                elif component_type == 'transistors':
                    obj_class = 6
                else:
                    print(
                        f"*******[ERR]: UNKNOWN component type {component_type} detected in {path_to_csv_folder + file_name}")
                    continue

                x_yolo = (top_left_x + width) / 2 * img_resolution_x
                y_yolo = (top_left_y + height) / 2 * img_resolution_y

                if file_name in annotation_write:
                    list_of_annotations = annotation_write[file_name]
                    list_of_annotations.append(f"{obj_class} {x_yolo} {y_yolo} {width} {height}")
                    annotation_write[file_name] = list_of_annotations
                else:
                    annotation_write[file_name] = []

    make_files(annotation_write)
