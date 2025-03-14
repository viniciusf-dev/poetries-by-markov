import os
from typing import List, Optional, Set, Dict
import json
import random
from ..config import DEFAULT_ENCODING, DEFAULT_OUTPUT_DIR

class FileHandler:

    
    @staticmethod
    def read_file(file_path: str, encoding: str = DEFAULT_ENCODING) -> str:

        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = DEFAULT_ENCODING) -> None:

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def get_files_in_directory(directory_path: str, file_extension: str = '.txt') -> List[str]:

        file_paths = []
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(file_extension):
                    file_paths.append(os.path.join(root, file))
        
        return file_paths
    
    @staticmethod
    def save_model(model_data: Dict, file_path: str) -> None:

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

        os.makedirs(output_dir, exist_ok=True)
        return output_dir