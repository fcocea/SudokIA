### Descripción del problema
Sudoku es un juego de lógica en el que se debe rellenar una cuadrícula de 9x9 celdas dividida en subcuadrículas de 3x3 celdas con números del 1 al 9. La cuadrícula inicialmente contiene algunos números. El objetivo es rellenar las celdas vacías con números que no se repitan en ninguna fila, columna o subcuadrícula de 3x3 celdas. En este problema, se le proporciona una cuadrícula parcialmente rellenada y se le pide que la complete.

Se plantea inicialmente la resolución del problema de una manera visual implementando una interfaz gráfica [PyGame](https://www.pygame.org/docs/), para luego implementar un algoritmo de resolución de Sudoku, para los cuales se busca realizar un benchmark entre diferentes maneras de resolver el tablero de Sudoku, como lo son:
- Backtracking
- Red neuronal convolucional (CNN)
- Algoritmos genéticos

### Descripción de los datos
La entrada consiste en una sentencia de 81 caracteres que representan una cuadrícula de Sudoku parcialmente rellenada. Los dígitos del 1 al 9 representan los números en la cuadrícula y el número cero representa las celdas vacia. Para luego convertir a un *numpy array* de 9x9, utilizando la función *reshape* de *numpy*.

Se considera este tipo de entrada para el problema, ya que es la forma más común de representar un Sudoku. Además de incorporar facilmente
dataset de millones de juegos, con su respectiva solución, para afrontar de mejor manera el problema.
- [1 million Sudoku games - (bryanpark)](https://www.kaggle.com/datasets/bryanpark/sudoku)
- [9 Million Sudoku Puzzles and Solutions - (rohanrao)](https://www.kaggle.com/datasets/rohanrao/sudoku)

<details><summary>Extra </summary>
Se podría pensar también en utilizar procesamiento de imagenes para obtener la cuadrícula de Sudoku, y luego resolverlo
</details>