import json
import subprocess
import sys
from pathlib import Path

папка = Path(__file__).parent
примеры = json.loads((папка / "examples.json").read_text(encoding="utf-8"))
while True:
    print("\nВыберите одну мини-систему:")
    for номер, пример in enumerate(примеры, 1):
        print(f"{номер}. {пример['title']}")
    выбор = input(f"Номер от 1 до {len(примеры)} или 0 для выхода: ").strip()
    if выбор == "0":
        break
    if not выбор.isdigit() or not 1 <= int(выбор) <= len(примеры):
        print("Введите номер из списка.")
        continue
    пример = примеры[int(выбор) - 1]
    print("Открываю:", пример["title"])
    print("Если это клуб читателей, учебный код: Club2026!")
    subprocess.run([sys.executable, str(папка / пример["folder"] / "app.py")])
    input("Нажмите Enter, чтобы вернуться к списку...")
