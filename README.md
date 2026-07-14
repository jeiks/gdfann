# Distributed Genetic Algorithm for FANN (Fast Artificial Neural Network)

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-under%20development-orange.svg)

A distributed and parallelized Genetic Algorithm (GA) implemented in Python, specifically designed to optimize and tune parameters for the **FANN (Fast Artificial Neural Network)** library. 

While its primary focus is hyperparameter tuning for Artificial Neural Networks (ANNs), the core Genetic Algorithm engine is modular and can be adapted to other optimization problems as well.

---

## Academic Background

The foundation of this project was developed as part of a Master's degree thesis. For theoretical details and the original implementation context, you can access the full paper here:

[Master's Dissertation - Jacson Rodrigues Correia da Silva (UFV)](https://locus.ufv.br/items/8fa11085-9765-4ee4-857c-4cb512713851)

---

## Features

* **ANN Parameter Tuning:** Automatically search for the best topology and parameters for FANN.
* **Distributed & Parallel Computing:** Designed to run evaluations in parallel across multiple nodes/threads to significantly reduce execution time.
* **Flexibility:** Easily adaptable core GA for non-neural network optimization tasks.

---

## Configuration & Usage

To set up and run the Genetic Algorithm, you need to configure two main files:

### 1. Gene and Evaluation Setup (`config_cromossomo.py`)

* **Define Gene Types:** Open the file and populate the `tipoGenes` matrix with the types and ranges of genes (parameters) that the algorithm should optimize.
* **Fitness Function:** Implement your evaluation logic inside the `avaliacaoRNA` function. This function evaluates each chromosome and **must** return or print the output exactly in the following format:
  ``Resultado: FITNESS_NUMBER``

### 2. Main GA Parameters (`config.py`)

* Open `config.py` to adjust global Genetic Algorithm parameters such as mutation rate, crossover rate, population size, and number of generations.

---

## Important Notes & Status

1. **Active Development:** This project is currently under development. While the parallel and distributed execution is fully functional, the codebase is being refactored to make setup and usage more intuitive.
2. **Language:** The source code and internal comments are currently written in **Portuguese**.
3. **Localization:** A full translation of the code and documentation to English is planned for future releases.
