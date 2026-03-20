'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

import cv2
import numpy as np
import pandas as pd
from termcolor import colored

filenames = [
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_Sk658 Llobe ch010019.jpg",
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_Sk658 Llobe ch010168.jpg",
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_SK658 Slobe ch010096.jpg",
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_SK658 Slobe ch010098.jpg",
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_SK658 Slobe ch010111.jpg",
    r"C:\\Users\\karin\\OneDrive - University of Virginia\\Second Year\\Comp BME\\Module-3-Fibrosis\\images\\Chosen Images\\MASK_SK658 Slobe ch010140.jpg",
]

depths = [60, 6000, 3000, 9400, 10000, 8300]

results = []

for filename, depth in zip(filenames, depths): # zip() function iterates over two lists at once and adds the two values into a tuple

    # Load grayscale image
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    # Vectorized threshold (faster than cv2.threshold)
    binary = img >= 127 # if the pixel value is at least 127, it is given the value of True (white) 

    white = np.sum(binary) # add how many values are true
    black = binary.size - white
    white_percent = 100 * white / (white + black)

    results.append({"Filename": filename, "Depth": depth, "White Pixels": white, "Black Pixels": black,"White Percent": white_percent})

    print(colored(f"{filename}", "red"))
    print(f"White: {white} | Black: {black}")
    print(f"{white_percent:.2f}% White | Depth: {depth} microns\n")

# Convert to DataFrame and save
df = pd.DataFrame(results)
df.to_csv("Percent_White_Pixels.csv", index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")


##############
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

# interpolate_depth = float(input(colored(
#     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# x = depths
# y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# i = interp1d(x, y, kind='linear')
# interpolate_point = i(interpolate_depth)
# print(colored(
#     f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# depths_i = depths[:]
# depths_i.append(interpolate_depth)
# white_percents_i = white_percents[:]
# white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# fig, axs = plt.subplots(2, 1)

# axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
# axs[0].set_title('Plot of depth of image vs percentage white pixels')
# axs[0].set_xlabel('depth of image (in microns)')
# axs[0].set_ylabel('white pixels as a percentage of total pixels')
# axs[0].grid(True)


# axs[1].scatter(depths_i, white_percents_i, marker='o',
#                linestyle='-', color='blue')
# axs[1].set_title(
#     'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
# axs[1].set_xlabel('depth of image (in microns)')
# axs[1].set_ylabel('white pixels as a percentage of total pixels')
# axs[1].grid(True)
# axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
#                color='red', s=100, label='Highlighted point')


# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
