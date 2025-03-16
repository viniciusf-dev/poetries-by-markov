import argparse
import os
import time
from models.markov_model import MarkovModel
from models.poem_generator import PoemGenerator
from utils.file_handler import FileHandler
from config import DEFAULT_OUTPUT_DIR

def parse_arguments():

    parser = argparse.ArgumentParser(description='Markov Chain Poetry Generator')
    
    
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--generate', action='store_true', help='Generate poems')
    parser.add_argument('--stats', action='store_true', help='Show model statistics')
    
    
    parser.add_argument('--data-dir', type=str, help='Directory containing training data')
    parser.add_argument('--model-file', type=str, default='model.json', help='Path to save/load the model')
    parser.add_argument('--order', type=int, default=2, help='Order of the Markov chain')
    

    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR, help='Directory to save generated poems')
    parser.add_argument('--count', type=int, default=1, help='Number of poems to generate')
    parser.add_argument('--lines', type=int, default=10, help='Number of lines per poem')
    parser.add_argument('--min-words', type=int, default=3, help='Minimum words per line')
    parser.add_argument('--max-words', type=int, default=8, help='Maximum words per line')
    parser.add_argument('--style', type=str, default='default', 
                        choices=['default', 'haiku', 'sonnet', 'free_verse'], 
                        help='Style of poem to generate')
    parser.add_argument('--no-title', action='store_true', help='Generate poems without titles')
    
    return parser.parse_args()

def train_model(args):

    print(f"Training model with order {args.order}...")
    
    model = MarkovModel(order=args.order)
    
    start_time = time.time()
    model.train_from_directory(args.data_dir)
    training_time = time.time() - start_time
    
    print(f"Training completed in {training_time:.2f} seconds")
    
    model.save(args.model_file)
    print(f"Model saved to {args.model_file}")
    
    return model

def generate_poems(model, args):
    
    generator = PoemGenerator(model)
    
    FileHandler.ensure_output_directory(args.output_dir)
    
    print(f"Generating {args.count} poems...")
    
    for i in range(args.count):
        filename = f"poem_{i+1}.txt"
        file_path = os.path.join(args.output_dir, filename)
        
        poem = generator.save_poem(
            file_path=file_path,
            lines=args.lines,
            min_words=args.min_words,
            max_words=args.max_words,
            include_title=not args.no_title,
            style=args.style
        )
        
        print(f"Generated poem saved to {file_path}")
        print("\nSample of the generated poem:")
        print("------------------------------")
        
        sample_lines = poem.split('\n')[:5]
        print('\n'.join(sample_lines))
        print("...")
        print("------------------------------\n")

def show_model_stats(model):

    stats = model.get_model_stats()
    
    print("\nModel Statistics:")
    print("----------------")
    print(f"Order: {stats['order']}")
    print(f"Total words processed: {stats['total_words']}")
    print(f"Unique words: {stats['unique_words']}")
    print(f"Vocabulary size: {stats['vocabulary_size']}")
    print(f"Beginning sequences: {stats['beginning_sequences']}")
    print(f"Line endings: {stats['line_endings']}")
    
    print("\nMost common words:")
    for word, count in stats['most_common_words'][:10]:
        print(f"  {word}: {count}")
    print()

def main():

    args = parse_arguments()
    
    if args.train and not args.data_dir:
        print("Error: --data-dir is required for training")
        return
    
    model = None

    if args.train:
        model = train_model(args)
    elif os.path.exists(args.model_file):
        print(f"Loading model from {args.model_file}...")
        model = MarkovModel()
        model.load(args.model_file)
        print("Model loaded successfully")
    else:
        print(f"Error: Model file {args.model_file} not found. Train a model first or specify a valid model file.")
        return
    
    if args.stats and model:
        show_model_stats(model)
    
    if args.generate and model:
        generate_poems(model, args)

if __name__ == "__main__":
    main()