import os
from pathlib import Path


class Engine:
    """
    Search Engine for user files.
    Searches specific file types in user's home directory.
    Efficiently skips irrelevant or heavy directories.
    """

    def __init__(self, max_depth=5, max_dir_size_mb=500):
        """
        Initialize the search engine.
        
        :param max_depth: Maximum directory depth to search.
        :param max_dir_size_mb: Skip directories larger than this (in MB).
        """
        self.allowed_extensions = {".pdf", ".docx", ".xlsx", ".txt", ".md"}
        self.home_path = Path.home()
        self.max_depth = max_depth
        self.max_dir_size_mb = max_dir_size_mb

    def _get_dir_size(self, path):
        """Estimate directory size quickly (in MB)."""
        total_size = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    # Add partial size of subdirectories (light estimation)
                    total_size += sum(f.stat().st_size for f in os.scandir(entry.path) if f.is_file())
        except (PermissionError, FileNotFoundError):
            return float("inf")  # Skip restricted directories
        return total_size / (1024 * 1024)  # Convert bytes to MB

    def _search_directory(self, directory, depth=0):
        """Recursively search directory for allowed files."""
        if depth > self.max_depth:
            return []

        results = []
        try:
            # Skip large directories for efficiency
            #if self._get_dir_size(directory) > self.max_dir_size_mb:
             #   return results

            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_file():
                        ext = Path(entry.name).suffix.lower()
                        if ext in self.allowed_extensions:
                            results.append(str(Path(entry.path)))
                    elif entry.is_dir(follow_symlinks=False):
                        results.extend(self._search_directory(entry.path, depth + 1))
        except (PermissionError, FileNotFoundError):
            # Skip directories we don't have access to
            pass
        return results

    def search(self, keyword=None):
        """
        Search for allowed files in the user's home directory.
        
        :param keyword: Optional keyword to filter filenames.
        :return: List of matching file paths.
        """
        print(f"Searching in {self.home_path} ...")
        files = self._search_directory(str(self.home_path))

        if keyword:
            files = [f for f in files if keyword.lower() in os.path.basename(f).lower()]

        return files


if __name__ == "__main__":
    # Example usage
    engine = Engine(max_depth=4, max_dir_size_mb=200)
    results = engine.search()
    print(f"Found {len(results)} files:")
    for file_path in results:
        print(file_path)
