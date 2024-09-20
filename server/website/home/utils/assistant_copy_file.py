import os
import shutil
from flask import current_app

def handle_file_copies(files):
    copied_files = []
    try:
        for file in files:
            # Construimos las rutas originales y las copias
            original_path = os.path.join('website', file.path, file.name)
            new_name = f'{file.id}-{file.name}'
            copy_path = os.path.join('website', file.path, new_name)

            # Creamos la copia del archivo
            shutil.copy2(original_path, copy_path)
            copied_files.append(copy_path)

        return copied_files

    except Exception as e:
        current_app.logger.error(f"Error copying file: {str(e)}")
        raise e


    
    
    
     