import os
from typing import List, Tuple
from werkzeug.utils import secure_filename

class FileUtils:
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'}
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if file extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileUtils.ALLOWED_EXTENSIONS

    @staticmethod
    def save_file_safely(file, upload_folder: str) -> Tuple[bool, str]:
        """
        Safely save uploaded file
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if file and FileUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            try:
                file.save(filepath)
                return True, filepath
            except Exception as e:
                return False, str(e)
        return False, "Invalid file type"

    @staticmethod
    def cleanup_temp_file(filepath: str) -> bool:
        """
        Remove temporary file
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception:
            return False