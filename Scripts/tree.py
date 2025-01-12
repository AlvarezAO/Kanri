import os


def tree(dir_path, prefix=''):
    print(prefix + os.path.basename(dir_path) + '/')
    prefix += '    '
    for item in os.listdir(dir_path):
        if item in ('__pycache__', '.git', '.venv', 'env'):
            continue
        path = os.path.join(dir_path, item)
        if os.path.isdir(path):
            tree(path, prefix)
        else:
            print(prefix + item)


tree('..')
