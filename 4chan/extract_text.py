import os
import shutil
import json
import re
from lxml import html
from lxml.etree import ParserError

DEST = 'text'

def clean(comment):
    pseudo_nl = re.sub(r'<br>', '  ', comment)
    try:
        tagless = html.document_fromstring(pseudo_nl).text_content()
    except ParserError:
        pass # catches blankposts
        tagless = ""

    tokens = re.sub(r'\({2,}', 'TOKEN_MULTI_LEFT_PAREN', tagless)
    tokens = re.sub(r'\){2,}', 'TOKEN_MULTI_RIGHT_PAREN', tokens)
    tokens = re.sub(r'>>\w+', '', tokens)
    punctless = re.sub(r'[^\w\s]', '', tokens)
    punctless = re.sub(r'TOKEN_MULTI_LEFT_PAREN', '(((', punctless)
    punctless = re.sub(r'TOKEN_MULTI_RIGHT_PAREN', ')))', punctless)

    return punctless.lower()

def init(board):
    if not os.path.exists(f'{DEST}'):
        os.mkdir(f'{DEST}')
    if os.path.exists(f'{DEST}/{board}'):
        shutil.rmtree(f'{DEST}/{board}')
    os.mkdir(f'{DEST}/{board}')

boards = os.listdir('data')

for board in boards:
    print(f'/{board}/...')
    files = os.listdir(f'data/{board}')
    init(board)
    for thread in files:
        with open(f'data/{board}/{thread}', 'r') as rf:
            thread_json = rf.readline()
        loaded_json = json.loads(thread_json)
        if 'posts' in loaded_json:
            comments = [post['com'] for post in loaded_json['posts'] if 'com' in post]
            with open(f'{DEST}/{board}/comments', 'a+') as wf:
                for comment in comments:
                    cleaned = clean(comment)
                    if cleaned:
                        wf.write(cleaned + '\n')

