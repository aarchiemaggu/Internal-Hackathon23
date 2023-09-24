# Internal-Hackathon23


## OCR with doctr.io and Python

This Python script uses the doctr.io library to perform optical character recognition (OCR) on an image file. The output of the OCR is saved to a text file, with the text wrapped at a specified maximum width.

### Usage

1. Install the doctr.io library:

```
pip install doctr
```

2. Run the script and specify the path to the image file:

```
python ocr.py path/to/image.jpg
```

3. The output text will be saved to a file called `output.txt` in the same directory as the script.

### Example

```python
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import textwrap

image_path = input("Enter the path of image: ")
docs = DocumentFile.from_images(image_path)

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)

result = model(docs)
result.show(docs)

json_output = result.export()

output_file_path = 'output.txt'

max_line_width = 80

def extract_text(data):
    text_values = []
    if isinstance(data, dict):
        for key, value in data.items():
            text_values.extend(extract_text(value))
    elif isinstance(data, list):
        for item in data:
            text_values.extend(extract_text(item))
    elif isinstance(data, str):
        # Replace '-' with '\n' and split the text into words
        words = data.replace('-', '\n').split()
        text_values.extend(words)
    return text_values

text_values = extract_text(json_output)

formatted_text = ' '.join(text_values)

wrapped_text = textwrap.fill(formatted_text, width=max_line_width)

with open(output_file_path, 'w') as text_file:
    text_file.write(wrapped_text)
```

### Requirements

* doctr.io library
