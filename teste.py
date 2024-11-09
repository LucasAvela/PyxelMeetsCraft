matriz = [
    [None, "44", "44"],
    [None, "44", "44"],
    [None, None, None]
]

matrizes = {
    "t1": {"m": [
        ["44", "44"],
        ["44", "44"]
        ]},
}

matriz_non_none = [[elem for elem in row if elem is not None] for row in matriz]

for key, m in matrizes.items():
    for i, x in enumerate(m['m']):
        for j, y in enumerate(x):
            if m['m'][i][j] == matriz_non_none[i][j]:
                print('ok', i, j)
            else:
                print("ops")
                break
    else:
        print('tudo ok')
