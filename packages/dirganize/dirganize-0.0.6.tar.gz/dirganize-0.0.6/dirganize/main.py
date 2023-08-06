''' the main script to get the job done '''

import os
import logging
import yaml
from rich.progress import track
from rich.logging import RichHandler
import typer

app = typer.Typer()


@app.command()
def main(path: str = os.getcwd(), loud: bool = False):
    ''' Organizes files into folders
    '''

    if loud:
        logging.basicConfig(level=logging.INFO,
                            format='[dim]%(name)s[/dim]\t%(message)s',
                            handlers=[RichHandler(markup=True, show_path=False,)])

    os.chdir(path)

    logging.info(f'Current working directory is {os.getcwd()}')

    structure = {'images': ['png', 'jpg', 'jpeg','svg','webp'],
                 'videos': ['mp4','mov','avi','webm','mkv'],
                 'audios':['mp3','aac','wav'],
                 'docs': ['pdf', 'txt', 'md'],
                 'animations': ['gif'],
                 'ebooks': ['epub'],
                 'archives': ['zip', 'tar', 'gz'],
                 'databases': ['csv', 'xlsx', 'xls', 'db'],
                 'configs': ['yaml', 'ini', 'env', 'yml'],
                 'android': ['apk'],
                 'webpages': ['html'],
                 'scripts': ['py', 'sh', 'java', 'cpp', 'c', 'js']}

    config_file = '.dirganize.yml'

    if os.path.isfile(config_file):
        with open(config_file) as stream:
            structure = (yaml.full_load(stream))

    logging.info(structure)

    mapping = {}
    for folder, extensions in track(structure.items(), description='Creating mapping '):
        for ext in extensions:
            mapping[ext] = folder

    logging.info(mapping)

    all_files = [file for file in os.listdir() if os.path.isfile(file)]

    logging.info(all_files)

    for file in track(all_files, description='Moving files '):
        ext = file.split('.')[-1]
        new_parent_dir = mapping.get(ext)

        if new_parent_dir:
            new_file = os.path.join(new_parent_dir, file)

            if not os.path.isdir(new_parent_dir):
                os.makedirs(new_parent_dir)

            os.rename(file, new_file)
            logging.info('%s renamed to %s', file, new_file)


if __name__ == "__main__":
    app()
