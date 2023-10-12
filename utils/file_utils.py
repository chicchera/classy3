from pathlib import Path

class CustomFileNotFoundError(Exception):
    def __init__(self, filename):
        self.filename = filename
        error_message = f"File '{filename}' not found."
        super().__init__(error_message)


class CustomPermissionError(Exception):
    def __init__(self, filename):
        self.filename = filename
        error_message = f"Permission denied for file '{filename}'."
        super().__init__(error_message)


class CustomValidationError(Exception):
    def __init__(self, filename, message="Validation error"):
        self.filename = filename
        error_message = "{} for file '{}'.".format(message, filename)
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
    file_path = Path(filename)
    if file_path.exists():
        if file_path.is_file():
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    return True
            except PermissionError as exc:
                raise CustomPermissionError(filename) from exc
            except Exception as e:
                raise CustomValidationError(filename, f"Error: {str(e)}")
        else:
            raise CustomValidationError(filename, "The specified path is not a file.")
    else:
        raise CustomFileNotFoundError(filename)




def diy_file_validate(filename):
    """
    Validates the existence and permission of a file.

    Args:
        filename (str): The path to the file to be validated.

    Returns:
        tuple: A tuple containing a boolean value indicating the success of the validation and a message string.
            - The first element is a boolean value indicating if the file exists and has the necessary permission.
            - The second element is a string message providing additional information about the validation result.

    Raises:
        FileNotFoundError: If the file specified by `filename` does not exist.
        PermissionError: If the file specified by `filename` cannot be accessed due to insufficient permissions.
        Exception: If an unexpected error occurs during the validation process.
    """
    try:
        with open(filename, encoding='utf-8'):
            return True, None  # Success, no message
    except FileNotFoundError:
        return False, f"File {filename} not found"
    except PermissionError:
        return False, f"Permission denied for file {filename}"
    except Exception as e:
        return False, str(e)  # Failed with a custom error message
