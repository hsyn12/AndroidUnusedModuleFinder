class SelectedDirectory:
    def __init__(self, file_name: str = 'selected_directory'):
        self._last_selected_directory: str = ''
        self._file_name = file_name

    @property
    def value(self) -> str:
        if self._last_selected_directory and not self._last_selected_directory.isspace():
            return self._last_selected_directory
        try:
            with open(self._file_name, 'r', encoding='utf-8') as file_selected_directory:
                self._last_selected_directory = file_selected_directory.read()
                return self._last_selected_directory
        except FileNotFoundError:
            return ''

    @value.setter
    def value(self, directory: str) -> None:
        self._last_selected_directory = directory
        with open(self._file_name, 'w', encoding='utf-8') as file_selected_directory:
            file_selected_directory.write(directory)
