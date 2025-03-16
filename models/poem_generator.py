from typing import List, Tuple, Dict, Optional
import random
from ..models.markov_model import MarkovModel
from ..utils.text_processor import TextProcessor
from ..utils.file_handler import FileHandler
from ..config import (
    DEFAULT_LINES, DEFAULT_MIN_WORDS, DEFAULT_MAX_WORDS,
    LINE_BREAK_TOKEN, TITLE_LENGTH_MIN, TITLE_LENGTH_MAX,
    LINE_ENDING_PROBABILITY
)

class PoemGenerator:
    
    def __init__(self, model: Optional[MarkovModel] = None):

        self.model = model if model else MarkovModel()
        self.text_processor = TextProcessor()
    
    def set_model(self, model: MarkovModel) -> None:

        self.model = model
    
    def generate_title(self) -> str:

        if not self.model.trained:
            raise ValueError("Model has not been trained yet")
        
        title_length = random.randint(TITLE_LENGTH_MIN, TITLE_LENGTH_MAX)
        
        current = self.model.get_random_beginning()
        title_words = list(current)[:1]  
        
        for _ in range(title_length - 1):
            next_word = self.model.get_next_word(current)
            
            if not next_word or next_word == LINE_BREAK_TOKEN:
                continue
                
            title_words.append(next_word)
            
            current = tuple(list(current)[1:]) + (next_word,)
        
        title = ' '.join(title_words)
        title = title.strip()
        
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title
    
    def generate_line(self, min_words: int, max_words: int) -> str:

        if not self.model.trained:
            raise ValueError("Model has not been trained yet")
        
        current = self.model.get_random_beginning()
        line_words = list(current)
        
        word_count = len(current)
        target_length = random.randint(min_words, max_words)
        
        while word_count < target_length:
            next_word = self.model.get_next_word(current)
            
            if not next_word:
                break
                
            if next_word == LINE_BREAK_TOKEN:
                current = tuple(list(current)[1:]) + (next_word,)
                continue
                
            line_words.append(next_word)
            
            current = tuple(list(current)[1:]) + (next_word,)
            word_count += 1
            
            if (word_count >= min_words and 
                self.model.is_line_ending(next_word) and 
                random.random() < LINE_ENDING_PROBABILITY):
                break
        
        # Clean up the line
        line = ' '.join(line_words)
        line = line.replace(f' {LINE_BREAK_TOKEN}', '').strip()
        
        return line
    
    def generate_poem(
        self, 
        lines: int = DEFAULT_LINES, 
        min_words: int = DEFAULT_MIN_WORDS, 
        max_words: int = DEFAULT_MAX_WORDS, 
        include_title: bool = True,
        style: str = "default"
    ) -> str:

        if not self.model.trained:
            raise ValueError("Model has not been trained yet")
        
        poem_lines = []
        
        if include_title:
            poem_title = self.generate_title()
            poem_lines.append(poem_title)
            poem_lines.append("")  
        
        generated_lines = []
        for _ in range(lines):
            line = self.generate_line(min_words, max_words)
            if line:  # Only add non-empty lines
                generated_lines.append(line)
        
        if style == "haiku":
            generated_lines = self._generate_haiku_style()
        elif style == "sonnet":
            generated_lines = self._generate_sonnet_style(14)
        elif style == "free_verse":
            generated_lines = self._generate_free_verse_style(lines)
        
        poem_lines.extend(generated_lines)
        
        poem = LINE_BREAK_TOKEN.join(poem_lines)
        poem = self.text_processor.clean_output(poem)
        
        poem = self.text_processor.add_variety(poem)
        
        return poem
    
    def _generate_haiku_style(self) -> List[str]:

        return [
            self.generate_line(2, 3), 
            self.generate_line(3, 4),  
            self.generate_line(2, 3)  
        ]
    
    def _generate_sonnet_style(self, line_count: int = 14) -> List[str]:

        lines = []
        for _ in range(line_count):
            lines.append(self.generate_line(8, 12))
        return lines
    
    def _generate_free_verse_style(self, line_count: int) -> List[str]:

        lines = []
        for _ in range(line_count):
            # Mix of short and long lines
            if random.random() < 0.3:
                lines.append(self.generate_line(1, 3))  # Shorter line
            elif random.random() < 0.7:
                lines.append(self.generate_line(4, 7))  # Medium line
            else:
                lines.append(self.generate_line(8, 12))  # Longer line
        return lines
    
    def save_poem(
        self, 
        file_path: str, 
        lines: int = DEFAULT_LINES, 
        min_words: int = DEFAULT_MIN_WORDS, 
        max_words: int = DEFAULT_MAX_WORDS, 
        include_title: bool = True,
        style: str = "default"
    ) -> str:

        poem = self.generate_poem(lines, min_words, max_words, include_title, style)
        
        FileHandler.write_file(file_path, poem)
        
        return poem