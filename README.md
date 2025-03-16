# Markov Poetry Generator

A sophisticated non-LLM-based poetry generator that uses Markov chains to create original poems.

## Features

- Generate poems in multiple styles (default, haiku, sonnet, free verse)
- Train on any text corpus
- Customizable parameters for poem structure
- Save and load trained models
- Command-line interface for easy use

## Installation

1. Clone this repository:
```bash
git clone https://github.com/viniciusf-dev/poetries-by-markov
cd markov-poetry-generator
```

2. Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Train a model:

```bash
python main.py --train --data-dir path/to/poetry/files --model-file model.json --order 2
```

#### Generate poems:

```bash
python main.py --generate --model-file model.json --count 5 --lines 10 --style default
```

#### Show model statistics:

```bash
python main.py --stats --model-file model.json
```

### Dataset Used

This project works best with a diverse collection of poetry. You can use:

1. Project Gutenberg's collection of public domain poetry
2. Poetry Foundation's open access poems
3. Your own collection of poetry texts

In my tests, I used a Kaggle dataset that can be exported here: [Kaggle Poems Dataset](https://www.kaggle.com/datasets/michaelarman/poemsdataset?resource=download)

## Examples

Here's an example of a poem generated using this system:

```
The Silent Whisper

Distant echoes fade away
Through shimmering leaves and golden light
Memories linger in the breeze
As shadows dance on ancient walls

Time stands still in this moment
When dreams and reality merge
In the silent whisper of your name
```

## Configuration

You can modify the `config.py` file to change default settings:

- Text processing parameters
- Generation parameters
- Default paths and filenames


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
