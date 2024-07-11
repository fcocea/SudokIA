### Descripción del problema
Sudoku es un juego de lógica en el que se debe rellenar una cuadrícula de 9x9 celdas dividida en subcuadrículas de 3x3 celdas con números del 1 al 9. La cuadrícula inicialmente contiene algunos números. El objetivo es rellenar las celdas vacías con números que no se repitan en ninguna fila, columna o subcuadrícula de 3x3 celdas. En este problema, se le proporciona una cuadrícula parcialmente rellenada y se le pide que la complete.

Se plantea inicialmente la resolución del problema de una manera visual implementando una interfaz gráfica [PyGame](https://www.pygame.org/docs/), para luego implementar un algoritmo de resolución de Sudoku, para los cuales se busca realizar un benchmark entre diferentes maneras de resolver el tablero de Sudoku, como lo son:
- Backtracking
- Red neuronal convolucional (CNN)
- Algoritmos genéticos

### Descripción del ambiente:
El ambiente del Sudoku es discreto, estático y determinista. Es discreto porque el juego se desarrolla en un conjunto finito de posibles estados (cada configuración del tablero). Es estático porque el ambiente no cambia mientras se resuelve el Sudoku, es decir, no hay elementos que se muevan o evolucionen con el tiempo. Es determinista porque las acciones tomadas por el agente tienen un resultado predecible y único

Las acciones son discretas y el dominio de cada acción es un número del 1 al 9, representando el número que se quiere colocar en la celda, estas pueden ser representada por una tupla que contiene las coordenadas de la celda en la que se desea colocar el número, junto con el número mismo. Por ejemplo, para colocar un 2 en la celda (0, 2), la acción puede ser representada como (0, 2, 2).
### Descripción de los datos
La entrada consiste en una sentencia de 81 caracteres que representan una cuadrícula de Sudoku parcialmente rellenada. Los dígitos del 1 al 9 representan los números en la cuadrícula y el número cero representa las celdas vacia. Para luego convertir a un *numpy array* de 9x9, utilizando la función *reshape* de *numpy*.

Se considera este tipo de entrada para el problema, ya que es la forma más común de representar un Sudoku. Además de incorporar facilmente
dataset de millones de juegos, con su respectiva solución, para afrontar de mejor manera el problema.
- [1 million Sudoku games - (bryanpark)](https://www.kaggle.com/datasets/bryanpark/sudoku)
- [9 Million Sudoku Puzzles and Solutions - (rohanrao)](https://www.kaggle.com/datasets/rohanrao/sudoku)

### Instrucciones de uso

1. Clonar el repositorio
```bash
git clone https://github.com/fcocea/SudokIA
```
2. Creación de entorno virtual (Opcional)
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

4. Ejecutar el script
```bash
python main.py --help
```