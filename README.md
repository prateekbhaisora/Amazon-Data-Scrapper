# Data Scrapper for Amazon Products

This project scraps data for products over Amazon, using playwright and stores them in a CSV file.

## Basic Setup

1. Setup a Python virtual environment using the commands:

```python
python3 -m venv py_3.13.12
pip3 install -r requirements.txt
playwright install
```

2. Store all your Amazon product URLs in a file called `input-urls.txt`.

3. Run the python script using the command:

```python
python3 data-scrapper.py
```

4. The output is stored in a CSV named `output-data.csv`.