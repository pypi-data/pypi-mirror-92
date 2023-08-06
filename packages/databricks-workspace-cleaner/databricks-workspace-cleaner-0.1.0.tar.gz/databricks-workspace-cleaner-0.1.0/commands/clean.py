from firehelper import CommandRegistry
from tabulate import tabulate
from utils.db import (delete_empty_folders, list_all_notebooks, ws_export,
                      ws_import)


def clean_notebooks():
    notebook_list = list_all_notebooks()
    notebook_objs = ws_export(notebook_list)
    for notebook_obj in notebook_objs:
        ws_import(notebook_obj)
    print(tabulate(notebook_list))

def clean_empty_folders():
    folders = delete_empty_folders()
    print(tabulate(folders))



clean_commands = {
    'clean': {
        'notebooks': clean_notebooks,
        'folders': clean_empty_folders
    }
}

CommandRegistry.register(clean_commands)
