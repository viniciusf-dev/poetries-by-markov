import os
from typing import List, Optional, Set, Dict
import json
import random
from ..config import DEFAULT_ENCODING, DEFAULT_OUTPUT_DIR

class FileHandler:
    """
    Class for handling file operations for the poetry generator
    """
    
    @staticmethod
    def read_file(file_path: str, encoding: str = DEFAULT_ENCODING) -> str:
        """
        Read text from a file.
        
        Args:
            file_path (str): Path to the file
            encoding (str): File encoding
            
        Returns:
            str: File contents
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = DEFAULT_ENCODING) -> None:
        """
        Write text to a file.
        
        Args:
            file_path (str): Path to the file
            content (str): Content to write
            encoding (str): File encoding
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def get_files_in_directory(directory_path: str, file_extension: str = '.txt') -> List[str]:
        """
        Get a list of files with the specified extension in a directory.
        
        Args:
            directory_path (str): Path to the directory
            file_extension (str): File extension to filter by
            
        Returns:
            List[str]: List of file paths
        """
        file_paths = []
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(file_extension):
                    file_paths.append(os.path.join(root, file))
        
        return file_paths
    
    @staticmethod
    def save_model(model_data: Dict, file_path: str) -> None:
        """
        Save model data to a file.
        
        Args:
            model_data (Dict): Model data to save
            file_path (str): Path to save the model
        """
        serializable_data = {
            'order': model_data['order'],
            'transitions': {str(k): v for k, v in model_data['transitions'].items()},
            'beginnings': [list(b) for b in model_data['beginnings']],
            'line_endings': model_data['line_endings']
        }
        
        with open(file_path, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(serializable_data, f, indent=2)
    
    @staticmethod
    def load_model(file_path: str) -> Dict:
        """
        Load model data from a file.
        
        Args:
            file_path (str): Path to the model file
            
        Returns:
            Dict: Loaded model data
        """
        with open(file_path, 'r', encoding=DEFAULT_ENCODING) as f:
            data = json.load(f)
        
        model_data = {
            'order': data['order'],
            'transitions': {tuple(eval(k)): v for k, v in data['transitions'].items()},
            'beginnings': [tuple(b) for b in data['beginnings']],
            'line_endings': data['line_endings']
        }
        
        return model_data
    
    @staticmethod
    def ensure_output_directory(output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
        """
        Ensure the output directory exists.
        
        Args:
            output_dir (str): Output directory path
            
        Returns:
            str: Path to the output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        return output_dir