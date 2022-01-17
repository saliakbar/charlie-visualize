import glob
import os
import shutil
from pathlib import Path

from pyspark.sql import dataframe
from pyspark.sql.session import SparkSession

output_dir = "../data/"
spark_dir = "../data/spark/"
data_dir = "../data/data/data_"
analyzed_data_dir = "../data/analyzed_data/"
repositories_selected_dir = "../data/repositories_selected/"
characterization_dir = "../data/characterization/"
visualization_dir = "../data/visualization/"
repos_with = "repositories_with_"
api_proportion_file = "api_proportion_"
api_sets_file = "api_sets_"
characterization_file = "characterization_"
visualization_file = "visualization_"

filePath = "filePath"
packageName = "packageName"
className = "className"
methodName = "methodName"
isAPIClass = "isAPIClass"
api = "api"
mcrCategories = "mcrCategories"
mcrTags = "mcrTags"
count = "count"
countAll = "countAll"
proportion = "proportion"
apis = "apis"
dependencies = "dependencies"


def read_csv(spark: SparkSession, file_path: str):
    """
    Reads a CSV file with the path `file_path` into a dataframe 
    using the spark session `spark`.
    """
    return spark.read.option("inferSchema", "true").option(
        "header", "true").csv(file_path)


def write_csv(df: dataframe, folder_path: str):
    """
    Writes the dataframe `df` into a folder with the path `folder_path`.
    """
    df.write.format("csv").option(
        "header", "true").save(folder_path)


def copy_csv(input_folder: str, output_file_path: str):
    """
    Copies the CSV file from the folder `input_folder` to the file with the 
    file path `output_file_path`.
    """
    Path(os.path.dirname(output_file_path)).mkdir(parents=True, exist_ok=True)
    for file in glob.glob(input_folder + "/*.csv"):
        f = open(file, 'r')
        shutil.copy(f.name, output_file_path)
        f.close()


def delete_dir(dir: str):
    """
    Deletes the directory `dir`.
    """
    path = Path(dir)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
