#%%
'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

import cv2
import numpy as np
import pandas as pd
from termcolor import colored
import time
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

#start_time = time.perf_counter()
filenames = [
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_Sk658 Llobe ch010019.jpg",
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_Sk658 Llobe ch010168.jpg",
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_SK658 Slobe ch010096.jpg",
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_SK658 Slobe ch010098.jpg",
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_SK658 Slobe ch010111.jpg",
    r"C:\Users\karin\OneDrive - University of Virginia\Second Year\Comp BME\Module-3-Fibrosis\images\Chosen Images\MASK_SK658 Slobe ch010140.jpg"
]

depths = [60, 6000, 3000, 9400, 10000, 8300]
white_percents = []

results = []

for filename, depth in zip(filenames, depths): # zip() function iterates over two lists at once and adds the two values into a tuple

    # Load grayscale image
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    # Vectorized threshold (faster than cv2.threshold)
    binary = img >= 127 # if the pixel value is at least 127, it is given the value of True (white) 

    white = np.sum(binary) # add how many values are true
    black = binary.size - white
    white_percent = 100 * white / (white + black)
    white_percents.append(white_percent)

    results.append({"Filename": filename, "Depth": depth,"White Percent": white_percent})

    #print(colored(f"{filename}", "red"))
    #print(f"White: {white} | Black: {black}")
    #print(f"{white_percent:.2f}% White | Depth: {depth} microns\n")

# Convert to DataFrame and save
df = pd.DataFrame(results)
df.to_csv("Percent_White_Pixels.csv", index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

#end_time = time.perf_counter()
#print(f"Execution time: {end_time - start_time:0.4f} seconds")

#%% 
##############
#LECTURE 2: UNCOMMENT BELOW

# Interpolate a point: given a depth, find the corresponding white pixel percentage
number_depths = int(input(colored("Enter the number of depths at which you want to interpolate a point: ")))
interpolate_depths = []
counter = 0
while counter < number_depths:

    depths_addition = float(input(colored("Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))
    if (depths_addition > min(depths)) and (depths_addition < max(depths)):
        interpolate_depths.append(depths_addition)
        counter += 1

    else:
        print(colored("Please enter a depth between 60 and 10000 microns.", 'red'))


x = depths
y = white_percents

depths_i1 = depths[:]
white_percents_i1 = white_percents[:]
depths_i2 = depths[:]
white_percents_i2 = white_percents[:]

# linear  

for i in range(number_depths):
    i1 = interp1d(x, y, kind = 'linear')
    interpolate_point1 = i1(interpolate_depths[i])
    depths_i1.append(interpolate_depths[i])
    white_percents_i1.append(interpolate_point1)

# quadratic 
for i in range(number_depths):
    i2 = interp1d(x, y, kind = 'quadratic')
    interpolate_point2 = i2(interpolate_depths[i])
    depths_i2.append(interpolate_depths[i])
    white_percents_i2.append(interpolate_point2)


print("Linearly interpolated points: ")
for i in range(number_depths):
    print(f"Point {i+1}: ({depths_i1[-(i+1)]}, {white_percents_i1[-(i+1)]})")

print("Quadratically interpolated points: ")
for i in range(number_depths):
    print(f"Point {i+1}: ({depths_i2[-(i+1)]}, {white_percents_i2[-(i+1)]})")

fig, axs = plt.subplots(3, 1) # make 3 plots

# plot without interpolated points
axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)

# plot with linearly interpolated points
axs[1].scatter(depths_i1, white_percents_i1, marker='o',linestyle='-', color='blue')
axs[1].set_title('Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)

for i in range(number_depths):
    axs[1].scatter(depths_i1[len(depths_i2)-(i+1)], white_percents_i1[len(white_percents_i2)-(i+1)], color='red', s=100, label='Highlighted point')

# plot for quadratically interpolated points
axs[2].scatter(depths_i2, white_percents_i2, marker='o',linestyle='-', color='blue')
axs[2].set_title('Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[2].set_xlabel('depth of image (in microns)')
axs[2].set_ylabel('white pixels as a percentage of total pixels')
axs[2].grid(True)

for i in range(number_depths):
    axs[2].scatter(depths_i2[len(depths_i1)-(i+1)], white_percents_i2[len(white_percents_i1)-(i+1)], color='red', s=100, label='Highlighted point')


# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
