import argparse
import importlib.util

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def parser():
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--train', action='store_true',
                       help='Entrenar el modelo')
    group.add_argument('--solve', action='store_true',
                       help='Resolver un Sudoku')
    group.add_argument('--test', action='store_true',
                       help='Probar los métodos de resolución')
    parser.add_argument('--method', type=str, choices=['cnn', 'back', 'gen'],
                        default='back', help='Método para resolver el Sudoku (por defecto: back)')
    parser.add_argument('--model', type=str, help='Ruta al modelo de CNN')
    parser.add_argument('-i', type=int, help='Índice del Sudoku a resolver')
    args = parser.parse_args()
    if args.solve and args.method == 'cnn' and not args.model:
        parser.error(
            "--model es obligatorio cuando se usa --solve con --method=cnn")
    return args


if __name__ == '__main__':
    args = parser()
    if args.train:
        spec = importlib.util.spec_from_file_location(
            'train', 'cnn/train.py')
        train = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(train)
        train.train_model()
    if args.solve:
        spec = importlib.util.spec_from_file_location(
            'board', 'game/board.py')
        board = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(board)
        board.run_game(method=args.method, model_path=args.model, index=args.i)
