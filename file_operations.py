import os
import shutil
import json
import glob
import re
import hashlib
from utils import get_value_from_dict

def get_single_json_file_path(source_dir):
    """
    Returns the path of a single JSON file in the specified directory.

    Args:
        source_dir (str): The directory path where the JSON files are located.

    Returns:
        str: The path of the single JSON file.

    Raises:
        FileNotFoundError: If no JSON file is found in the directory.
        FileExistsError: If multiple JSON files are found in the directory.
    """
    json_files = glob.glob(os.path.join(source_dir, '*.json'))
    
    if len(json_files) == 0:
        raise FileNotFoundError("No JSON file found in the directory.")
    elif len(json_files) > 1:
        raise FileExistsError("Multiple JSON files found in the directory.")
    
    return json_files[0]

def set_destination_folder(destination_root_dir, test_id):
    """
    Sets the destination folder for copying files based on the given test ID.

    Args:
        destination_root_dir (str): The root directory where the destination folders are located.
        test_id (str): The test ID used to identify the destination folder.

    Returns:
        str: The path of the destination folder.

    """
    existing_folders = os.listdir(destination_root_dir)
    count = 0
    pattern = re.compile(rf"^{re.escape(test_id)}_(\d+)$")
    
    for folder in existing_folders:
        match = pattern.match(folder)
        if match:
            folder_count = int(match.group(1))
            if folder_count > count:
                count = folder_count
    
    count += 1
    destination_folder = os.path.join(destination_root_dir, f"{test_id}_{count}")
    return destination_folder


def compute_checksum(file_path, algorithm='sha256'):
    """
    Compute the checksum of a file.

    Parameters:
    file_path (str): The path to the file.
    algorithm (str, optional): The hashing algorithm to use. Defaults to 'sha256'.

    Returns:
    str: The computed checksum of the file.
    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def safe_copy(file_path, destination_folder):
    """
    Copy a file and verify its integrity using checksums.

    Parameters:
    - file_path (str): The path of the file to be copied.
    - destination_folder (str): The destination folder where the file will be copied to.

    Returns:
    - str: The path of the copied file.

    Raises:
    - ValueError: If the checksum of the source file does not match the checksum of the copied file.
    """
    # Compute checksum of the source file
    source_checksum = compute_checksum(file_path)
    
    # Perform the copy operation
    destination_path = shutil.copy(file_path, destination_folder)
    
    # Compute checksum of the copied file
    destination_checksum = compute_checksum(destination_path)
    
    # Verify the checksums
    if source_checksum != destination_checksum:
        raise ValueError("Checksum mismatch: the file was not copied correctly.")
    
    return destination_path

def copy_files(source_dir, destination_root_dir, json_file_path):
    """
    Copy files from the source directory to the destination directory based on the provided JSON file.

    Args:
        source_dir (str): The path to the source directory.
        destination_root_dir (str): The path to the root directory where the files will be copied.
        json_file_path (str): The path to the JSON file containing the necessary information.

    Raises:
        ValueError: If the key 'test_sequence_id' is not found in the JSON file.

    Returns:
        None
    """
    with open(json_file_path) as json_file:
        data = json.load(json_file)
    
    test_id = get_value_from_dict(data, 'test_sequence_id')
    if not test_id:
        raise ValueError("The key 'test_sequence_id' is not found in the JSON file.")
    
    destination_folder = set_destination_folder(destination_root_dir, test_id)
    os.makedirs(destination_folder, exist_ok=True)
    
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            safe_copy(file_path, destination_folder)