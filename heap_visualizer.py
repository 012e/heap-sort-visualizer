from pathlib import Path

history = []


def export_swap(a: list[int], index: int) -> str:
    if index >= len(a):
        return ""
    result = ""

    if index == 0 or index == len(a) - 1:
        result += f"{a[index]}: {{ style.stroke: red }}\n"

    child1 = 2 * index + 1
    child2 = 2 * index + 2
    if child1 < len(a):
        result += f"{a[index]} -> {a[child1]}\n"
        result += export_swap(a, child1)
    if child2 < len(a):
        result += f"{a[index]} -> {a[child2]}\n"
        result += export_swap(a, child2)
    return result


def format(parent: int, child: int, diff: list[int]) -> str:
    if child in diff:
        return f"""{parent} -- {child}: {{
    style: {{
        stroke: red;
        animated: true
    }}
}}\n"""
    return f"{parent} -> {child}\n"


def export(a: list[int], index: int, diff: list[int]) -> str:
    if index >= len(a):
        return ""
    result = ""
    child1 = 2 * index + 1
    child2 = 2 * index + 2
    if child1 < len(a):
        result += format(a[index], a[child1], diff)
        result += export(a, child1, diff)
    if child2 < len(a):
        result += format(a[index], a[child2], diff)
        result += export(a, child2, diff)
    return result


def heapify(a: list[int], n: int, i: int):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and a[l] > a[largest]:
        largest = l
    if r < n and a[r] > a[largest]:
        largest = r
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        heapify(a, n, largest)


def write_file(name: str, content: str):
    with open(name, "w") as f:
        f.write(content)


def heapSort(a: list[int], n: int, i: int):
    n = len(a)
    count = 1
    history.append(a.copy())
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)

    history.append(a.copy())
    for i in range(n - 1, 0, -1):
        history.append((a[: i + 1]).copy())
        a[i], a[0] = a[0], a[i]
        history.append((a[: i + 1]).copy())
        history.append((a[:i]).copy())
        heapify(a, i, 0)
        count += 1
        history.append((a[:i]).copy())


def get_modified_elements(a: list[int], b: list[int]) -> list[int]:
    result = []
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            result.append(a[i])
    return result


OUTPUT_DIR = "./output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
heapSort([4, 1, 3, 2, 16, 9, 10, 14, 8, 7], 10, 0)
with open(f"{OUTPUT_DIR}/heap00.d2", "w") as f:
    f.write(export(history[0], 0, []))

for i in range(1, len(history)):
    diff = get_modified_elements(history[i - 1], history[i])
    # print("current: ", history[i])
    # print("diff:", diff)
    with open(f"{OUTPUT_DIR}/heap{i:02d}.d2", "w") as f:
        if len(diff) == 2 and sorted(diff) == sorted([history[i][0], history[i][-1]]):
            f.write(export_swap(history[i], 0))
        else:
            f.write(export(history[i], 0, diff))
