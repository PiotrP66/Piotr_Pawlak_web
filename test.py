import os
from dotenv import find_dotenv, load_dotenv
import glob

"""
path = 'static/figures'
figures = {}

for item in glob.glob(os.path.join(path, '*.html')):
    file_name = item[15:].replace('.html', '')

    with open(item, 'r', encoding='utf-8') as file:
        figures[file_name] = file.read()

print(figures['bar_pierwotny_cena_dzielnica'])
"""

# Find and load environment variables
dotenv_patch = find_dotenv()
load_dotenv(dotenv_patch)

key = os.getenv('SECRET_KEY')
print('key: ', key)
