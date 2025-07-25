# IQACO: Improved Q-Evaluation Ant Colony Optimization

This repository contains the source code for the paper "Research on Mobile Robot Path Planning Based on Improved Q-Evaluation Ant Colony Optimization Algorithm" by Dongdong Li and Lei Wang, accepted at *Engineering Applications of Artificial Intelligence* (2025). The code implements the Improved Quantum Ant Colony Optimization (IQACO) algorithm for path planning on grid-based maps, facilitating reproducibility and future research.

## Project Structure

* `Algorithm.py`: Implements the IQACO algorithm for path planning.
* `Map.py`: Handles loading and managing grid map data from text files.
* `Draw.py`: Visualizes the grid map with paths and iteration statistics.
* `main.py`: Example script demonstrating the usage of the IQACO algorithm.
* `res/`: Directory containing benchmark map files used in the paper.
  * `map_base_20.txt`: 20x20 grid map.
  * `map_base_30.txt`: 30x30 grid map.
  * `...`: Additional map files.

## Prerequisites

* Python 3.11.3
* Conda (Miniconda or Anaconda) for environment management
* Dependencies: `numpy`, `matplotlib`

## Installation

1. **Install Conda** (if not already installed):
   * Download Miniconda: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
   * Follow the installation instructions for your operating system.
2. **Clone the Repository** :

```bash
   git clone https://github.com/LiDongDong1996/IQACO.git
   cd IQACO
```

1. **Set Up the Conda Environment** :
   Create and activate the environment using the provided `environment.yml`:

```bash
   conda env create -f environment.yml
   conda activate iqaco
```

   If `environment.yml` is not available, manually install dependencies:

```bash
   conda create -n iqaco python=3.11.3
   conda activate iqaco
   conda install numpy matplotlib
```

## Usage

1. **Prepare Map Files** :

* Map files are located in the `res/` directory (e.g., `map_base_20.txt`, `map_base_30.txt`).
* Each file represents a grid map where `0` indicates a passable cell and `1` indicates an obstacle.
* Example format (for a 20x20 grid):
  ```
  00000000000000000000
  00111000000000000000
  00000000000000000000
  ...
  ```

1. **Run the Example** :
   Execute the main script to run the IQACO algorithm on a 50x50 map:

```bash
   python main.py
```

   This will:

* Load the map from `res/map_base_50.txt`.
* Run the IQACO algorithm with default parameters (50 ants, 50 iterations, start at [0,0], end at [49,49]).
* Display a plot of the optimal path and iteration statistics (average and best path lengths).

1. **Customize Parameters** :
   Modify `main.py` to use different map files or parameters (e.g., `ant_num`, `max_iter`, `start`, `end`). Example:

```python
   aco = IQACO(m.data, ant_num=100, start=[0,0], end=[29,29], max_iter=200)
```

## Visualization

* **Grid Plot** : `Draw.py` generates a visual representation of the grid map with the optimal path overlaid.
* **Iteration Graph** : Displays the average and best path lengths per iteration.

To save the plots instead of displaying them, modify `main.py` to call `fig.save('output.jpg')` instead of `fig.show()`.

## Map File Format

Map files are plain text files where each line represents a row of the grid. Each character is either:

* `0`: Passable cell
* `1`: Obstacle

The grid must be square (e.g., 20x20, 30x30, 50x50). See `res/` for examples.

## Citation

Please cite our paper if you use this code in your research:

```bibtex
@article{li2025,
  title={Research on Mobile Robot Path Planning Based on Improved Q-Evaluation Ant Colony Optimization Algorithm},
  author={Li, Dongdong and Wang, Lei},
  journal={Engineering Applications of Artificial Intelligence},
  year={2025}
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://grok.com/chat/LICENSE) file for details.

## Contact

For issues or questions, please open an issue on this repository or contact [[lddya1996@nuaa.edu.cn](mailto:lddya1996@nuaa.edu.cn)].
