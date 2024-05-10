import argparse
import os
from glob import glob

"""
Use your classifier from Task 3 to perform activity detection 
on a data sample that contains more than one activity, outputting
labels on a 3-second sliding window in 1-second intervals.

Usage:
    
    python3 Python/predict_shallow.py <sensor .csv sample> \
        --output <output .txt file with labels for 3-second windows on each line>

    python3 Python/predict_shallow.py --label_folder <folder with sensor .csv samples> \
        --output <output folder>
"""


def predict_continuous(sensor_data: str):
    """Run prediction on an sensor data sample, returning an array of labels
    for each 3-second sliding window in the file, using 1-second intervals.

    Replace the return value of this function your sliding window classification.
    Feel free to load any files and write helper functions as needed.
    """
    return ["JOG", "JOG", "TWS", "STD", "STD"]


def predict_continuous_folder(data_folder: str, output_folder: str):
    """Run the model's prediction on all the sensor data in data_folder, writing labels
    in sequence to an output folder."""

    data_files = sorted(glob(f"{data_folder}/*.csv"))
    for file in data_files:
        filename = os.path.basename(file)[:-4]
        file_labels = predict_continuous(data_files)

        with open(f"{output_folder}/{filename}_labels.txt", "w+") as out:
            out.write("\n".join(file_labels))


if __name__ == "__main__":
    # Parse arguments to determine whether to predict on a file or a folder
    # You should not need to modify the below starter code, but feel free to
    # add more arguments for debug functions as needed.
    parser = argparse.ArgumentParser()

    sample_input = parser.add_mutually_exclusive_group(required=True)
    sample_input.add_argument(
        "sample", nargs="?", help="A .csv sensor data file to run predictions on"
    )
    sample_input.add_argument(
        "--label_folder",
        type=str,
        required=False,
        help="Folder of .csv data files to run predictions on",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="Data/Lab2/Labels/Continuous/",
        help="Output filename of labels when running predictions on a directory",
    )

    args = parser.parse_args()

    if args.sample:
        if ".txt" not in args.output:
            output = args.output + ".txt"
        else:
            output = args.output
        with open(output, "w+") as out:
            out.write("\n".join(predict_continuous(args.sample)))

    elif args.label_folder:
        predict_continuous_folder(args.label_folder, args.output)