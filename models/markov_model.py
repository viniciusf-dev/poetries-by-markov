from collections import defaultdict
from typing import List, Dict, Tuple, Set, Optional
import random
import json
import os
from ..utils.text_processor import TextProcessor
from ..utils.file_handler import FileHandler
from ..config import LINE_BREAK_TOKEN, DEFAULT_ORDER

class MarkovModel:
    
    def __init__(self, order: int = DEFAULT_ORDER):

        self.order = order
        self.transitions = defaultdict(list)
        self.beginnings = []
        self.line_endings = []
        self.trained = False
        
        self.word_frequency = defaultdict(int)
        self.total_words = 0
        self.unique_words = set()
    
    def train(self, text: str) -> None:

        words = TextProcessor.tokenize(text)
        
        for word in words:
            if word != LINE_BREAK_TOKEN:
                self.word_frequency[word] += 1
                self.unique_words.add(word)
        
        self.total_words += len(words)
        
        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])
            
            next_word = words[i+self.order]
            self.transitions[key].append(next_word)
            
            if i == 0 or words[i-1] == LINE_BREAK_TOKEN:
                self.beginnings.append(key)
                
            if next_word == LINE_BREAK_TOKEN:
                self.line_endings.append(words[i])
        
        self.trained = True
    
    def train_from_directory(self, directory_path: str) -> None:

        file_handler = FileHandler()
        file_paths = file_handler.get_files_in_directory(directory_path)
        
        if not file_paths:
            raise ValueError(f"No text files found in directory: {directory_path}")
        
        for file_path in file_paths:
            text = file_handler.read_file(file_path)
            self.train(text)
            print(f"Trained on: {os.path.basename(file_path)}")
    
    def get_next_word(self, current_sequence: Tuple[str, ...]) -> Optional[str]:

        if current_sequence not in self.transitions:
            return None
        
        next_words = self.transitions[current_sequence]
        
        return random.choice(next_words)
    
    def get_random_beginning(self) -> Tuple[str, ...]:

        if not self.beginnings:
            raise ValueError("Model has not been trained yet")
        
        return random.choice(self.beginnings)
    
    def is_line_ending(self, word: str) -> bool:

        return word in self.line_endings
    
    def get_model_stats(self) -> Dict:

        if not self.trained:
            return {"error": "Model has not been trained yet"}
        
        most_common = sorted(
            self.word_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:20]
        
        return {
            "order": self.order,
            "total_words": self.total_words,
            "unique_words": len(self.unique_words),
            "vocabulary_size": len(self.transitions),
            "beginning_sequences": len(self.beginnings),
            "line_endings": len(self.line_endings),
            "most_common_words": most_common
        }
    
    def save(self, file_path: str) -> None:

        model_data = {
            "order": self.order,
            "transitions": self.transitions,
            "beginnings": self.beginnings,
            "line_endings": self.line_endings
        }
        
        FileHandler.save_model(model_data, file_path)
    
    def load(self, file_path: str) -> None:

        model_data = FileHandler.load_model(file_path)
        
        self.order = model_data["order"]
        self.transitions = defaultdict(list, model_data["transitions"])
        self.beginnings = model_data["beginnings"]
        self.line_endings = model_data["line_endings"]
        self.trained = True
    
    def clear(self) -> None:

        self.transitions = defaultdict(list)
        self.beginnings = []
        self.line_endings = []
        self.word_frequency = defaultdict(int)
        self.total_words = 0
        self.unique_words = set()
        self.trained = False