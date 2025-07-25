import numpy as np

class Map:
    def __init__(self) -> None:
        self.data = []  # Map data
        self.size = 0   # Map dimensions

    def load_map_file(self, file_path):
        '''
        Load map data from a file.

        Parameters
        ----------
        file_path : str
            Path to the map file.

        Returns
        -------
        None
        '''
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = list(lines[i].strip('\n'))
        self.data = np.array(lines).astype(np.int64)
        self.size = self.data.shape[0]