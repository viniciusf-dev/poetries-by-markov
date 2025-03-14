import re
from typing import List, Optional
import random
from ..config import LINE_BREAK_TOKEN, PUNCTUATION_MARKS

class TextProcessor:
    
    @staticmethod
    def tokenize(text: str) -> List[str]:

        text = text.replace('\r\n', LINE_BREAK_TOKEN)
        
        text = text.replace(LINE_BREAK_TOKEN, f' {LINE_BREAK_TOKEN} ')
        
        words = text.split()
        
        return words
    
    @staticmethod
    def clean_output(text: str) -> str:

        for mark in PUNCTUATION_MARKS:
            if mark in [')', '(']:
                continue
            text = re.sub(f'\\s+([{re.escape(mark)}])', r'\1', text)
        
        text = re.sub(r'\s+\)', r')', text)
        text = re.sub(r'\(\s+', r'(', text)
        
        lines = text.split(LINE_BREAK_TOKEN)
        formatted_lines = []
        
        for line in lines:
            if not line:
                formatted_lines.append(line)
                continue
                
            formatted_line = line[0].upper() + line[1:] if line else line
            formatted_lines.append(formatted_line)
            
        return LINE_BREAK_TOKEN.join(formatted_lines)
    
    @staticmethod
    def add_variety(text: str) -> str:

        lines = text.split(LINE_BREAK_TOKEN)
        processed_lines = []
        
        seen_phrases = set()
        
        for line in lines:
            if not line.strip():
                processed_lines.append(line)
                continue
                
            words = line.split()
            if len(words) >= 3:
                phrase = ' '.join(words[:3])
                if phrase.lower() in seen_phrases and random.random() < 0.7:
                    continue
                seen_phrases.add(phrase.lower())
            
            processed_lines.append(line)
        
        return LINE_BREAK_TOKEN.join(processed_lines)