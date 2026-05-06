"""Demostración de la dificultad alcanzable con Python.

Este programa muestra:
- algoritmos avanzados (criba, backtracking, Mandelbrot)
- programación asíncrona y concurrencia
- metaprogramación y decoradores
- generación de texto simple tipo IA
"""

import asyncio
import concurrent.futures
import math
import random
import textwrap
import time
from typing import Callable, List, Optional, Tuple


def menu() -> None:
    print("\n=== Demostración de la dificultad alcanzable con Python ===")
    print("1. Criba de Eratóstenes y verificación de primos")
    print("2. Resolver N-Reinas con backtracking")
    print("3. Dibujar el conjunto de Mandelbrot en ASCII")
    print("4. Ejecutar tareas asíncronas y concurrentes")
    print("5. Texto generado con un modelo de Markov simple")
    print("6. Demo de ajedrez: caballo y recorrido")
    print("7. Salir")


def sieve_of_eratosthenes(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for current in range(2, int(math.isqrt(limit)) + 1):
        if sieve[current]:
            for multiple in range(current * current, limit + 1, current):
                sieve[multiple] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return False
    return True


def n_queens(n: int) -> List[List[int]]:
    solutions: List[List[int]] = []
    columns = set()
    diag1 = set()
    diag2 = set()
    board: List[int] = []

    def backtrack(row: int) -> None:
        if row == n:
            solutions.append(board.copy())
            return
        for col in range(n):
            if col in columns or (row - col) in diag1 or (row + col) in diag2:
                continue
            columns.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board.append(col)
            backtrack(row + 1)
            board.pop()
            columns.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return solutions


def algebraic_to_coords(square: str, size: int = 8) -> Optional[Tuple[int, int]]:
    if len(square) != 2:
        return None
    file, rank = square[0].lower(), square[1]
    if file < 'a' or file > chr(ord('a') + size - 1):
        return None
    if not rank.isdigit():
        return None
    row = int(rank) - 1
    col = ord(file) - ord('a')
    if row < 0 or row >= size:
        return None
    return row, col


def coords_to_algebraic(row: int, col: int) -> str:
    return f"{chr(ord('a') + col)}{row + 1}"


def knight_moves(square: str, size: int = 8) -> List[str]:
    coords = algebraic_to_coords(square, size)
    if coords is None:
        return []
    row, col = coords
    moves = []
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in offsets:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size:
            moves.append(coords_to_algebraic(nr, nc))
    return sorted(moves)


def render_chessboard(path: Optional[List[str]] = None, current: Optional[str] = None) -> str:
    size = 8
    board = [['.' for _ in range(size)] for _ in range(size)]
    if path:
        for i, square in enumerate(path, start=1):
            coords = algebraic_to_coords(square, size)
            if coords:
                row, col = coords
                board[row][col] = str(i % 10)
    if current:
        coords = algebraic_to_coords(current, size)
        if coords:
            row, col = coords
            board[row][col] = 'K'
    lines = []
    for row in range(size - 1, -1, -1):
        lines.append(f"{row + 1} " + ' '.join(board[row]))
    lines.append('  ' + ' '.join(chr(ord('a') + c) for c in range(size)))
    return '\n'.join(lines)


def find_knights_tour(start: str, size: int = 8) -> Optional[List[str]]:
    start_coords = algebraic_to_coords(start, size)
    if start_coords is None:
        return None

    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    board = [[False] * size for _ in range(size)]
    path: List[str] = []

    def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        result = []
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and not board[nr][nc]:
                result.append((nr, nc))
        return result

    def backtrack(r: int, c: int, step: int) -> bool:
        board[r][c] = True
        path.append(coords_to_algebraic(r, c))
        if step == size * size:
            return True
        next_moves = sorted(neighbors(r, c), key=lambda p: len(neighbors(*p)))
        for nr, nc in next_moves:
            if backtrack(nr, nc, step + 1):
                return True
        board[r][c] = False
        path.pop()
        return False

    if backtrack(start_coords[0], start_coords[1], 1):
        return path
    return None


def render_mandelbrot(width: int, height: int, max_iter: int = 50) -> str:
    chars = ' .:-=+*#%@'
    result_lines = []
    for row in range(height):
        line = []
        for col in range(width):
            x0 = (col / width) * 3.5 - 2.5
            y0 = (row / height) * 2.0 - 1.0
            x = y = 0.0
            iteration = 0
            while x * x + y * y <= 4.0 and iteration < max_iter:
                x, y = x * x - y * y + x0, 2 * x * y + y0
                iteration += 1
            line.append(chars[iteration * len(chars) // max_iter - 1])
        result_lines.append(''.join(line))
    return '\n'.join(result_lines)


async def fake_io_bound_task(task_id: int) -> str:
    delay = random.uniform(0.3, 1.0)
    await asyncio.sleep(delay)
    return f'Tarea asincrónica {task_id} completada en {delay:.2f}s'


def cpu_bound_work(x: int) -> int:
    return sum(i * i for i in range(1, x + 1))


def timing_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'[{func.__name__}] tiempo: {elapsed:.4f} s')
        return result
    return wrapper


def make_power_function(exponent: int) -> Callable[[float], float]:
    def power(value: float) -> float:
        return value ** exponent
    power.__name__ = f'potencia_{exponent}'
    return power


def markov_text(seed_text: str, length: int = 50) -> str:
    words = seed_text.split()
    if len(words) < 3:
        return seed_text
    transitions = {}
    for a, b, c in zip(words, words[1:], words[2:]):
        transitions.setdefault((a, b), []).append(c)
    current = (words[0], words[1])
    generated = [current[0], current[1]]
    for _ in range(length - 2):
        options = transitions.get(current)
        if not options:
            break
        next_word = random.choice(options)
        generated.append(next_word)
        current = (current[1], next_word)
    return ' '.join(generated)


@timing_decorator
def run_concurrent_tasks() -> None:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        values = [100_000 + i * 5_000 for i in range(4)]
        results = list(executor.map(cpu_bound_work, values))
    print('Resultados CPU bound:', results)


async def run_async_tasks() -> None:
    tasks = [fake_io_bound_task(i) for i in range(1, 6)]
    for completed in asyncio.as_completed(tasks):
        print(await completed)


def main() -> None:
    while True:
        menu()
        choice = input('Selecciona una opción: ').strip()
        if choice == '1':
            limit = int(input('Calcular primos hasta: '))
            primes = sieve_of_eratosthenes(limit)
            print(f'Primos hasta {limit}:', primes[:20], '...')
            test_value = int(input('Verificar si un número es primo: '))
            print(f'{test_value} es primo:', is_prime(test_value))
        elif choice == '2':
            n = int(input('Tamaño de tablero N para N-Reinas: '))
            solutions = n_queens(n)
            print(f'Se encontraron {len(solutions)} soluciones para N={n}')
            if solutions:
                print('Ejemplo de solución:', solutions[0])
        elif choice == '3':
            width = int(input('Ancho ASCII: '))
            height = int(input('Alto ASCII: '))
            print(render_mandelbrot(width, height))
        elif choice == '4':
            print('Ejecutando tareas concurrentes (CPU) y asincrónicas...')
            run_concurrent_tasks()
            asyncio.run(run_async_tasks())
        elif choice == '5':
            seed = input('Escribe una frase base para Markov: ').strip()
            print('\nTexto generado:')
            print(textwrap.fill(markov_text(seed, 40), width=70))
        elif choice == '6':
            start_square = input('Casilla inicial del caballo (ej. g1): ').strip()
            moves = knight_moves(start_square)
            if not moves:
                print('Casilla inválida. Usa formato como e4 o h1.')
            else:
                print(f'Movimientos posibles desde {start_square}:', ', '.join(moves))
                tour = find_knights_tour(start_square)
                if tour:
                    print('\nEncontrado un recorrido completo del caballo:')
                    print(' -> '.join(tour[:12]) + (' ...' if len(tour) > 12 else ''))
                    print('\nTablero con los primeros pasos del recorrido:')
                    print(render_chessboard(tour[:12], start_square))
                else:
                    print('No se encontró un recorrido completo desde esa casilla en este intento.')
        elif choice == '7':
            print('Saliendo...')
            break
        else:
            print('Opción no válida. Intenta de nuevo.')


if __name__ == '__main__':
    main()
