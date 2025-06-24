"""
NOTE: Work in progress - Minesweeper bot (incomplete implementation)
Current state:
Basic board scanning works
Flag placement logic partially implemented
Win/lose conditions not yet handled
Last update: 06.24.2025



"""

import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Games\python_library\Tesseract-OCR\tesseract.exe"
import cv2
import numpy as np
import time
import threading

# Настройки
cell_size = 48  # размер клетки
board_size = (9, 9)  # размер поля (строки, столбцы)
top_left = (56, 504)  # координаты верхнего левого угла поля (будут заданы пользователем)

clicked_cells = set()
flagged_cells = set()

# Чтение клетки через OCR
def read_cell(img, i, j):
    x = j * cell_size
    y = i * cell_size
    cell_img = img[y:y+cell_size, x:x+cell_size]

    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh, config='--psm 10 digits').strip()

    if text == '':
        # если ничего не распознано — вернуть '?'
        return '?'
    if text == 'F':
        return 'F'
    return text

# Получить соседей клетки
def get_neighbors(i, j):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < board_size[0] and 0 <= nj < board_size[1]:
                neighbors.append((ni, nj))
    return neighbors

# Применить логику Minesweeper для ходов
def apply_logic(board):
    to_click = set()
    to_flag = set()

    for i in range(board_size[0]):
        for j in range(board_size[1]):
            cell = board[i][j]
            if not cell.isdigit():
                continue
            num = int(cell)
            neighbors = get_neighbors(i, j)

            unknowns = [pos for pos in neighbors if board[pos[0]][pos[1]] == '?']
            flags = [pos for pos in neighbors if board[pos[0]][pos[1]] == 'F']

            # Если флагов столько же, сколько число, кликаем по остальным неизвестным
            if len(flags) == num and unknowns:
                to_click.update([pos for pos in unknowns if pos not in clicked_cells])

            # Если неизвестных + флагов равно числу — ставим флаги на все неизвестные
            elif len(unknowns) > 0 and len(flags) + len(unknowns) == num:
                to_flag.update([pos for pos in unknowns if pos not in flagged_cells])

    # Ставим флаги
    for i,j in to_flag:
        x = top_left[0] + j * cell_size + cell_size // 2
        y = top_left[1] + i * cell_size + cell_size // 2
        pyautogui.moveTo(x, y)
        pyautogui.click(button='right')
        flagged_cells.add((i,j))
        time.sleep(0.05)

    return list(to_click)

def main():
    global top_left

    print("Наведи мышку на игровое поле. Через 5 секунд сделай первый клик мышкой по клетке.")
    time.sleep(5)
    print("Ожидание клика...")

    # Ожидаем первый клик пользователя
    first_click = None
    def on_click(x, y, button, pressed):
        nonlocal first_click
        if pressed:
            first_click = (x, y)
            return False

    import pynput.mouse
    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()

    print(f"Первый клик: {first_click}")

    # Определяем верхний левый угол поля
    # Считаем, что клик сделан по клетке (i, j) — например по центру клетки (3,3)
    # Мы можем взять верхний левый угол сдвинувшись от клика
    # Для простоты считаем, что клик по клетке (3,3)
    cell_i, cell_j = 3, 3
    top_left = (first_click[0] - cell_j * cell_size, first_click[1] - cell_i * cell_size)

    print(f"Верхний левый угол игрового поля: {top_left}")

    clicked_cells.add((cell_i, cell_j))
    pyautogui.click(first_click[0], first_click[1])

    step = 1
    while True:
        # Скриншот поля
        img = pyautogui.screenshot(region=(top_left[0], top_left[1], board_size[1]*cell_size, board_size[0]*cell_size))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Считываем поле
        board = []
        for i in range(board_size[0]):
            row = []
            for j in range(board_size[1]):
                cell_value = read_cell(img, i, j)
                row.append(cell_value)
            board.append(row)

        print(f"Ход {step}")
        for r in board:
            print(' '.join(r))

        # Пропускаем первый клик, он сделан вручную
        if step == 1:
            print(f"Пропускаю первый клик, он был сделан вручную по ({cell_i}, {cell_j})")

        moves = apply_logic(board)
        if not moves:
            print("Нет очевидных ходов, пытаюсь кликнуть на первую непосещённую клетку")
            # Кликаем на первую неизвестную
            for i in range(board_size[0]):
                for j in range(board_size[1]):
                    if (i,j) not in clicked_cells and (i,j) not in flagged_cells:
                        moves.append((i,j))
                        break
                if moves:
                    break

        if not moves:
            print("Ходы закончились, игра завершена или дальше не разобрать")
            break

        for (i,j) in moves:
            x = top_left[0] + j * cell_size + cell_size // 2
            y = top_left[1] + i * cell_size + cell_size // 2
            print(f"Кликаю по клетке: ({i}, {j}) -> координаты ({x},{y})")
            pyautogui.moveTo(x, y)
            pyautogui.click()
            clicked_cells.add((i,j))
            time.sleep(0.1)

        step += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
