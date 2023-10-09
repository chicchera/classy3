class CustomFileNotFoundError(Exception):
    def __init__(self, filename):

        self.filename = filename
        super().__init__(f"File '{filename}' not found.")

class CustomPermissionError(Exception):
    def __init__(self, filename):

        self.filename = filename
        super().__init__(f"Permission denied for file '{filename}'.")

class CustomValidationError(Exception):
    def __init__(self, filename, message="Validation error"):

        self.filename = filename
        error_message = f"{message} for file '{filename}'."
        super().__init__(error_message)


def file_validate(filename):
    """
    Validates the existence and accessibility of a file.

    Parameters:
    - filename (str): The name of the file to validate.

    Returns:
    - bool: True if the file exists and is accessible, False otherwise.

    Raises:
    - CustomFileNotFoundError: If the file is not found.
    - CustomPermissionError: If the file cannot be accessed due to permissions.
    - CustomValidationError: If an unknown error occurred during validation.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return True
    except FileNotFoundError as exc:
        raise CustomFileNotFoundError(filename) from exc
    except PermissionError as exc:
        raise CustomPermissionError(filename) from exc
    except Exception as e:
        raise CustomValidationError(filename, f"Error: {str(e)}")


def diy_file_validate(filename):
    try:
        with open(filename):
            return True, None  # Success, no message
    except (FileNotFoundError, PermissionError):
        return False, f"File {filename} not found or permission denied"
    except Exception as e:
        return False, str(e)  # Failed with a custom error message