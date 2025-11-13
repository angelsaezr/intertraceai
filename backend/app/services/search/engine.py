import os
from pathlib import Path

import app.core.config as config


class Engine:
    """
    Search Engine for user files.
    Searches specific file types in user's home directory.
    Efficiently skips irrelevant or heavy directories.
    """

    def __init__(self ):
        """
        Initialize the search engine.
        """

        self.allowed_extensions = config.ALLOWED_EXTENSIONS
        self.max_depth = config.SEARCH_MAX_DEPTH
        self.max_dir_size_mb = config.SEARCH_MAX_DIR_SIZE_MB

        # Expected Documents folder
        documents = Path.home() / "Documents"

        if not documents.exists() or not documents.is_dir():
            raise FileNotFoundError(f"Documents folder does not exist: {documents}")

        self.docs_path = documents

    def _get_dir_size(self, path):
        """
        Estimate directory size quickly (in MB).

        param path: Directory path
        return: Size in MB
        """

        total_size = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False): # follow_symlinks to avoid loops
                    # Add partial size of subdirectories (light estimation)
                    total_size += sum(f.stat().st_size for f in os.scandir(entry.path) if f.is_file())
        except (PermissionError, FileNotFoundError):
            return float("inf")  # Skip restricted directories
        return total_size / (1024 * 1024)  # Convert bytes to MB

    def _search_directory(self, directory, depth=0):
        """
        Recursively search directory for allowed files.

        param directory: Directory path
        param depth: Current recursion depth
        return: List of found file paths
        """

        if depth > self.max_depth:
            return []

        # Directories to exclude explicitly
        excluded_folders = config.EXCLUDED_FOLDERS

        results = []
        try:
            # Skip large directories for efficiency, except for the home directory
            if directory != str(self.docs_path) and self._get_dir_size(directory) > self.max_dir_size_mb:
                return results

            with os.scandir(directory) as entries:
                for entry in entries:
                    # Skip excluded directories
                    if entry.is_dir(follow_symlinks=False):
                        # Skip hidden directories (start with ".") and excluded ones
                        if entry.name.startswith(".") or entry.name in excluded_folders:
                            continue

                    if entry.is_file():
                        ext = Path(entry.name).suffix.lower() # Get file extension
                        if ext in self.allowed_extensions: # Check allowed extensions
                            results.append(str(Path(entry.path))) # Store full file path
                    elif entry.is_dir(follow_symlinks=False):
                        results.extend(self._search_directory(entry.path, depth + 1)) # Recurse into subdirectory
        except (PermissionError, FileNotFoundError):
            # Skip directories we don't have access to
            pass
        return results

    def search(self):
        """
        Search for allowed files in the user's home directory.

        return: List of found file paths
        """

        config.debug_print(f"Searching in {self.docs_path} ...")
        files = self._search_directory(str(self.docs_path))
        config.debug_print(f"Found {len(files)} files.")

        return files


if __name__ == "__main__":
    engine = Engine()
    results = engine.search()
    for file_path in results:
        config.debug_print(file_path)
    config.debug_print(f"Found {len(results)} files")
