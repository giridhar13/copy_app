import os
import tempfile
import json
from unittest import TestCase
from unittest.mock import patch
import shutil
from copy_app.file_operations import get_single_json_file_path, copy_files, set_destination_folder, compute_checksum, safe_copy


class GetSingleJsonFilePathTestCase(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.temp_dir = tempfile.mkdtemp()
        self.json_file_path = os.path.join(self.test_dir, 'test_file.json')
        with open(self.json_file_path, 'w') as json_file:
            json_file.write('{"key": "value"}')

    def tearDown(self):
        # Ensure all files are removed before removing the directories
        shutil.rmtree(self.test_dir)

    def test_get_single_json_file_path(self):
        # Call the get_single_json_file_path function
        result = get_single_json_file_path(self.test_dir)

        # Assert that the correct file path is returned
        self.assertEqual(result, self.json_file_path)

    def test_get_single_json_file_path_no_file(self):
        # Call the function and expect FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            get_single_json_file_path(self.temp_dir)


class GetMultipleJsonFilePathTestCase(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create multiple JSON files in the temporary directory
        self.json_file_1 = os.path.join(self.temp_dir, 'test_file_1.json')
        self.json_file_2 = os.path.join(self.temp_dir, 'test_file_2.json')
        with open(self.json_file_1, 'w') as f:
            f.write('{"key": "value1"}')
        with open(self.json_file_2, 'w') as f:
            f.write('{"key": "value2"}')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_single_json_file_path_multiple_files(self):
        with self.assertRaises(FileExistsError):
            get_single_json_file_path(self.temp_dir)


class SetDestinationFolderTestCase(TestCase):
    def setUp(self):
        self.destination_root_dir = tempfile.mkdtemp()
        self.test_id = "test_1"
        self.existing_folders = [
            "test_1_1",
            "test_1_2",
            "test_2_1",
            "test_2_2",
            "test_3_1"
        ]
        for folder in self.existing_folders:
            os.makedirs(os.path.join(self.destination_root_dir, folder))

    def tearDown(self):
        for folder in self.existing_folders:
            os.rmdir(os.path.join(self.destination_root_dir, folder))
        os.rmdir(self.destination_root_dir)

    def test_set_destination_folder(self):
        # Call the function and get the destination folder
        destination_folder = set_destination_folder(self.destination_root_dir, self.test_id)

        # Assert that the destination folder is created correctly
        expected_folder = os.path.join(self.destination_root_dir, "test_1_3")
        self.assertEqual(destination_folder, expected_folder)


class ComputeChecksumTestCase(TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.write(b'Test file content')
        self.test_file.close()

    def tearDown(self):
        os.remove(self.test_file.name)

    def test_compute_checksum(self):
        # Expected checksum for the content 'Test file content'
        expected_checksum = '6c76f7bd4b84eb68c26d2e8f48ea76f90b9bdf8836e27235a0ca4325f8fe4ce5'
        actual_checksum = compute_checksum(self.test_file.name)
        self.assertEqual(actual_checksum, expected_checksum)


class SafeCopyTestCase(TestCase):
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.destination_dir = tempfile.mkdtemp()
        self.source_file_path = os.path.join(self.source_dir, 'test_file.txt')
        self.destination_file_path = os.path.join(self.destination_dir, 'test_file.txt')
        with open(self.source_file_path, 'w') as source_file:
            source_file.write('Test file content')

    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.destination_dir)

    @patch('file_operations.compute_checksum')
    def test_safe_copy(self, mock_compute_checksum):
        mock_compute_checksum.return_value = 'f3c8c4b7e8b7b6e8e8b7b6e8e8b7b6e8e8b7b6e8e8b7b6e8e8b7b6e8e8b7b6'

        # Call the safe_copy function
        safe_copy(self.source_file_path, self.destination_file_path)

        # Assert that the destination file was created
        self.assertTrue(os.path.exists(self.destination_file_path))

        # Assert that compute_checksum was called with the correct arguments
        mock_compute_checksum.assert_called_with(self.destination_file_path)

    @patch('file_operations.compute_checksum')
    def test_safe_copy_checksum_mismatch(self, mock_compute_checksum):
        # Mock the compute_checksum function to return different checksums
        mock_compute_checksum.side_effect = ['checksum1', 'checksum2']

        # Call the safe_copy function and assert that it raises a ValueError
        with self.assertRaises(ValueError):
            safe_copy(self.source_file_path, self.destination_file_path)

         
class CopyFilesTestCase(TestCase):
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.destination_root_dir = tempfile.mkdtemp()
        self.json_file_path = os.path.join(self.source_dir, 'test.json')
        self.destination_folder = os.path.join(self.destination_root_dir, 'test_1')
        os.makedirs(self.destination_folder)

    def tearDown(self):
        shutil.rmtree(self.destination_folder)
        shutil.rmtree(self.destination_root_dir)
        shutil.rmtree(self.source_dir)

    def test_copy_files(self):
        # Create a test JSON file
        data = {
            "test_sequence_id": "test_1"
        }
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file)

        # Patch the safe_copy function to avoid actual file copying
        with patch('file_operations.safe_copy') as mock_safe_copy:
            copy_files(self.source_dir, self.destination_root_dir, self.json_file_path)

            # Assert that safe_copy was called with the correct arguments
            mock_safe_copy.assert_called_once()


if __name__ == '__main__':
    unittest.main()