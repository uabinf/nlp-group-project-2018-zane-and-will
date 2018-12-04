import os
import shutil

DEST = 'uniq_data'

def init(board):
    if not os.path.exists(f'{DEST}/'):
        os.mkdir(f'{DEST}')
    if not os.path.exists(f'{DEST}/{board}'):
        os.mkdir(f'{DEST}/{board}')

boards = os.listdir('data')

for board in boards:
    print(f'/{board}/...')
    files = os.listdir(f'data/{board}/json')
    init(board)
    uniq_threads = list({fname.split('_at_')[0] for fname in files})
    for thread in uniq_threads:
        newest = max([fname for fname in files if thread in fname])
        src = f'old_data/{board}/json/{newest}'
        dest = f'{DEST}/{board}/{newest}'
        shutil.copyfile(src, dest)
