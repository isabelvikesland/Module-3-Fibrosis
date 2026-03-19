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

depths = [15, 1000, 3000, 5300, 7000, 9900]

results = []

for filename, depth in zip(filenames, depths):

    # Load grayscale image
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    # Vectorized threshold (faster than cv2.threshold)
    binary = img >= 127

    white = np.sum(binary)
    black = binary.size - white
    white_percent = 100 * white / (white + black)

    results.append({
        "Filename": filename,
        "Depth": depth,
        "White Pixels": white,
        "Black Pixels": black,
        "White Percent": white_percent
    })

    print(colored(f"{filename}", "red"))
    print(f"White: {white} | Black: {black}")
    print(f"{white_percent:.2f}% White | Depth: {depth} microns\n")

# Convert to DataFrame and save
df = pd.DataFrame(results)
df.to_csv("Percent_White_Pixels.csv", index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")