# BindCraft

BindCraft is a computational tool designed to simulate and analyze protein binding interactions. It provides researchers with a streamlined workflow for studying protein-ligand interactions, enabling insights into binding affinities and molecular dynamics.

## Overview of Protein Binding

Protein binding is a fundamental biological process where proteins interact with other molecules, such as ligands, DNA, or other proteins. These interactions are critical for various biological functions, including enzyme activity, signal transduction, and molecular transport. BindCraft simplifies the computational modeling of these interactions, making it accessible for researchers.

## Features

- **Simulation of protein-ligand interactions**  
- **Analysis of binding affinities**  
- **Support for high-performance computing environments**  

## Getting Started

To set up and launch BindCraft on the High-Performance Computing (HPC) environment (e.g., HEC), follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/st7ma784/ProteinBinder.git
    cd ProteinBinder/code/bindcraft
    ```

2. Run the setup and launch script:
    ```bash
    sbatch setup.com
    ```
    This script will install the necessary dependencies and configure the environment for BindCraft.
3. Submit the job to the HPC queue:
    ```bash
    sbatch launch.com
    ```

This script will handle the installation of dependencies, configuration of the environment, and submission of jobs to the HPC queue.

## Requirements

- Python 3.8+
- HPC environment with SLURM or equivalent job scheduler
- Required libraries (installed via the setup script)

## Contributing

Contributions are welcome! Please submit issues or pull requests via the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please contact the development team at [support@bindcraft.org](mailto:support@bindcraft.org).  