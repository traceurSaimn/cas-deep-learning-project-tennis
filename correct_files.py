import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image

mpl.use("TkAgg")

def adjust_box_with_aspect_ratio(xmin, ymin, xmax, ymax, img_width, img_height, margin_factor=1.5, aspect_ratio=1 / 2):
    # Original width and height
    box_width = xmax - xmin
    box_height = ymax - ymin

    box_width_with_margin = box_width * margin_factor

    # Center of the box
    center_x = xmin + box_width / 2
    center_y = ymin + box_height / 2

    # Determine new dimensions
    if aspect_ratio > 1:  # Wider
        new_width = max(box_width_with_margin, box_height * aspect_ratio)
        new_height = new_width / aspect_ratio
    else:  # Taller or square
        new_height = max(box_height, box_width_with_margin / aspect_ratio)
        new_width = new_height * aspect_ratio

    # Calculate new coordinates
    new_xmin = max(0, center_x - new_width / 2)
    new_ymin = max(0, center_y - new_height / 2)
    new_xmax = min(img_width, center_x + new_width / 2)
    new_ymax = min(img_height, center_y + new_height / 2)

    return int(new_xmin), int(new_ymin), int(new_xmax), int(new_ymax)

# (xmin, ymin, xmax, ymax)
coordinates = [
    (1039,574,1130,343),
    (91, 617, 239, 334),
    (75,620,206,312),
    (681,506,793,274),
    (470, 600, 563, 394)
]

faulty_file_paths = [
    r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\backhand\seq_001\B_001_002.jpeg",
    r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\backhand\seq_024\B_024_003.jpeg",
    r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\backhand\seq_024\B_024_004.jpeg",
    r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\backhand\seq_025\B_025_004.jpeg",
    r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\serve\seq_011\S_011_004.jpeg",
]
# index = 4
# image = Image.open(Path(faulty_file_paths[index]))
#
# # fig, ax = plt.subplots()
# # ax.set_axis_off()
# # ax.imshow(image)
# # plt.show()
#
# original_width, original_height = image.size
# margin_factor = 1.5
# width_to_heigt_ratio = 1 / 2
#
# xmin, ymin, xmax, ymax = coordinates[index]
#
# x_start, y_start, x_end, y_end = adjust_box_with_aspect_ratio(xmin, ymin, xmax, ymax, original_width, original_height,
#                                                               margin_factor=margin_factor,
#                                                               aspect_ratio=width_to_heigt_ratio)
#
# image_new = image.crop((x_start, y_start, x_end, y_end))
#
# fig, ax = plt.subplots()
# ax.set_axis_off()
# ax.imshow(image_new)
# plt.show()

for ((xmin, ymin, xmax, ymax), file_path) in zip(coordinates, faulty_file_paths):
    image_path = Path(file_path).as_posix()
    new_file_path = Path(image_path.replace("/images/", "/images_cropped/"))
    if not new_file_path.parent.exists():
        os.makedirs(new_file_path.parent)

    image = Image.open(image_path)

    original_width, original_height = image.size
    margin_factor = 1.5
    width_to_heigt_ratio = 1 / 2

    x_start, y_start, x_end, y_end = adjust_box_with_aspect_ratio(xmin, ymin, xmax, ymax, original_width,
                                                                  original_height,
                                                                  margin_factor=margin_factor,
                                                                  aspect_ratio=width_to_heigt_ratio)

    new_image = image.crop((x_start, y_start, x_end, y_end))

    new_image.save(new_file_path)
    print(f"saved file to {new_file_path}")




