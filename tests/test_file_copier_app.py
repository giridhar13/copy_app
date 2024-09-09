import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from copy_app.file_copier_app import FileCopierApp

class TestFileCopierApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = FileCopierApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('file_copier_app.filedialog.askdirectory', return_value='/mock/source/dir')
    def test_browse_source_dir(self, mock_askdirectory):
        self.app.browse_source_dir()
        self.assertEqual(self.app.source_dir_entry.get(), '/mock/source/dir')

    @patch('file_copier_app.filedialog.askdirectory', return_value='/mock/destination/dir')
    def test_browse_destination_dir(self, mock_askdirectory):
        self.app.browse_destination_dir()
        self.assertEqual(self.app.destination_dir_entry.get(), '/mock/destination/dir')

    @patch('file_copier_app.get_single_json_file_path', return_value='/mock/source/dir/file.json')
    @patch('file_copier_app.copy_files')
    @patch('file_copier_app.messagebox.showinfo')
    def test_copy_files_success(self, mock_showinfo, mock_copy_files, mock_get_single_json_file_path):
        self.app.source_dir_entry.insert(0, '/mock/source/dir')
        self.app.destination_dir_entry.insert(0, '/mock/destination/dir')
        
        self.app.copy_files()
        
        mock_get_single_json_file_path.assert_called_once_with('/mock/source/dir')
        mock_copy_files.assert_called_once_with('/mock/source/dir', '/mock/destination/dir', '/mock/source/dir/file.json')
        mock_showinfo.assert_called_once_with("Success", "Files copied successfully!")

    @patch('file_copier_app.get_single_json_file_path', side_effect=Exception('Test Exception'))
    @patch('file_copier_app.messagebox.showwarning')
    def test_copy_files_failure(self, mock_showwarning, mock_get_single_json_file_path):
        self.app.source_dir_entry.insert(0, '/mock/source/dir')
        self.app.destination_dir_entry.insert(0, '/mock/destination/dir')
        
        with patch.object(self.app.root, 'quit', MagicMock()), patch.object(self.app.root, 'destroy', MagicMock()):
            with self.assertRaises(SystemExit):
                self.app.copy_files()
        
        mock_get_single_json_file_path.assert_called_once_with('/mock/source/dir')
        mock_showwarning.assert_called_once_with("Warning", "Test Exception")

if __name__ == '__main__':
    unittest.main()