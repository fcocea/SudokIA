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
    return parser.parse_args()


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
        board.run_game(method=args.method)
