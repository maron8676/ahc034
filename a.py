import sys
from collections import defaultdict, deque
from sys import stdin

readline = stdin.readline


def li():
    return list(map(int, readline().split()))


N = int(input())
grid = []
for _ in range(N):
    grid.append(li())
grid_org = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        grid_org[i][j] = grid[i][j]

move_list = [(-1, 0), (0, 1), (1, 0), (0, -1)]
move_dict = {
    (1, 0): "D",
    (-1, 0): "U",
    (0, 1): "R",
    (0, -1): "L"
}


# 0,0 -> 0,1, ..., 0,N-1, 1,N-1
def get_next_targets(progress):
    res = []
    for i in range(N):
        if i % 2 == 0:
            for j in range(N):
                if not progress[i][j]:
                    res.append((i, j))
                    if len(res) >= 2:
                        return res
        else:
            for j in range(N - 1, -1, -1):
                if not progress[i][j]:
                    res.append((i, j))
                    if len(res) >= 2:
                        return res

    return res


track = (0, 0)
track_v = 0
progress = [[False] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        progress[i][j] = grid[i][j] == 0
ans_nearest = []
cost_nearest = 0

# １マスずつやる方針
state = sum(map(sum, progress))
while state < N ** 2:
    # print(state, track, track_v, cost_nearest, file=sys.stderr)
    # 次に0にしたいマス
    target = get_next_targets(progress)

    diff = grid[target[0][0]][target[0][1]]
    if diff < 0:
        # targetが足りない場合　近場の終わっていない場所から必要な土を取ってくる
        if abs(diff) <= track_v:
            # すでに必要な量を持っていたら、置いて終わり
            # target[0]まで移動
            if target[0][0] - track[0] > 0:
                move = "D"
            else:
                move = "U"
            for _ in range(abs(target[0][0] - track[0])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            if target[0][1] - track[1] > 0:
                move = "R"
            else:
                move = "L"
            for _ in range(abs(target[0][1] - track[1])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            track = target[0]

            # 土を置く
            ans_nearest.append(f"-{abs(diff)}")
            grid[track[0]][track[1]] += abs(diff)
            track_v -= abs(diff)
            cost_nearest += abs(diff)
        else:
            # 近場を探す いったんtarget[1]ということにする
            # 土を取るためにtarget[1]へ移動
            if target[1][0] - track[0] > 0:
                move = "D"
            else:
                move = "U"
            for _ in range(abs(target[1][0] - track[0])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            if target[1][1] - track[1] > 0:
                move = "R"
            else:
                move = "L"
            for _ in range(abs(target[1][1] - track[1])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            track = target[1]

            # 土を取る
            v = abs(diff) - track_v
            ans_nearest.append(f"+{v}")
            grid[track[0]][track[1]] -= v
            track_v += v
            cost_nearest += v

            # target[0]まで移動
            if target[0][0] - track[0] > 0:
                move = "D"
            else:
                move = "U"
            for _ in range(abs(target[0][0] - track[0])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            if target[0][1] - track[1] > 0:
                move = "R"
            else:
                move = "L"
            for _ in range(abs(target[0][1] - track[1])):
                ans_nearest.append(move)
                cost_nearest += track_v + 100
            track = target[0]

            # 土を置く
            ans_nearest.append(f"-{abs(diff)}")
            grid[track[0]][track[1]] += abs(diff)
            track_v -= abs(diff)
            cost_nearest += abs(diff)
    else:
        # target[0]が余分の場合　余分な量を全て回収
        # target[0]まで移動
        if target[0][0] - track[0] > 0:
            move = "D"
        else:
            move = "U"
        for _ in range(abs(target[0][0] - track[0])):
            ans_nearest.append(move)
            cost_nearest += track_v + 100
        if target[0][1] - track[1] > 0:
            move = "R"
        else:
            move = "L"
        for _ in range(abs(target[0][1] - track[1])):
            ans_nearest.append(move)
            cost_nearest += track_v + 100
        track = target[0]

        # 土を取る
        ans_nearest.append(f"+{diff}")
        grid[track[0]][track[1]] -= diff
        track_v += diff
        cost_nearest += diff

    # 状態更新
    for i in range(N):
        for j in range(N):
            progress[i][j] = grid[i][j] == 0
    state = sum(map(sum, progress))

# ある程度持ってから配る方針
# upper_limitを超えるまで取りにいく
# lower_limitを下回るまで配りにいく
# またupper_limitを超えるまで取りにいく
upper_limit = 200
lower_limit = 100

for i in range(N):
    for j in range(N):
        grid[i][j] = grid_org[i][j]
track = [0, 0]
track_v = 0
progress = [[False] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        progress[i][j] = grid[i][j] == 0
ans_stack = []
cost_stack = 0
mode = "pick"

state = sum(map(sum, progress))


def move_to_target(track, target):
    global move, grid, cost_stack, track_v, v, d

    if target[0] - track[0] > 0:
        move = "D"
        v = 1
    else:
        move = "U"
        v = -1
    for _ in range(abs(target[0] - track[0])):
        ans_stack.append(move)
        cost_stack += track_v + 100
        track[0] += v
        # 経路上で置ける分は置く
        if grid[track[0]][track[1]] < 0:
            d = min(track_v, abs(grid[track[0]][track[1]]))
            if d > 0:
                ans_stack.append(f"-{d}")
                grid[track[0]][track[1]] += d
                track_v -= d
                cost_stack += d
    if target[1] - track[1] > 0:
        move = "R"
        v = 1
    else:
        move = "L"
        v = -1
    for _ in range(abs(target[1] - track[1])):
        ans_stack.append(move)
        cost_stack += track_v + 100
        track[1] += v
        # 経路上で置ける分は置く
        if grid[track[0]][track[1]] < 0:
            d = min(track_v, abs(grid[track[0]][track[1]]))
            if d > 0:
                ans_stack.append(f"-{d}")
                grid[track[0]][track[1]] += d
                track_v -= d
                cost_stack += d


while state < N ** 2:
    # print(state, track, track_v, cost_stack, file=sys.stderr)

    # 0より高い・低い場所
    high_set = set()
    low_set = set()
    for i in range(N):
        for j in range(N):
            if grid[i][j] > 0:
                high_set.add((i, j))
            if grid[i][j] < 0:
                low_set.add((i, j))
    if len(high_set) == 0:
        mode = "put"

    if mode == "pick":
        # 取る場所を探して最短の移動列を生成
        # 同じ距離にある場合は、先に見つけた方
        target = None
        min_dis = 2 * N
        for high in high_set:
            dis = abs(high[0] - track[0]) + abs(high[1] - track[1])
            if dis < min_dis:
                min_dis = dis
                target = high

        # 縦移動と横移動は固定にする　→　DPなどで置けるマス数か量が最大になるようにしたい
        # 移動する
        # 経路で、置いた方がよい場所があれば取る
        # 先に縦を合わせる
        move_to_target(track, target)

        # 取る
        d = grid[target[0]][target[1]]
        ans_stack.append(f"+{d}")
        grid[track[0]][track[1]] -= d
        track_v += d
        cost_stack += d

        if track_v > upper_limit:
            mode = "put"
    else:
        # 配る
        # 配る場所を探して最短の移動列を生成
        target = None
        min_dis = 2 * N
        for low in low_set:
            dis = abs(low[0] - track[0]) + abs(low[1] - track[1])
            if dis < min_dis:
                min_dis = dis
                target = low

        # 縦移動と横移動は固定にする　→　DPなどで取れるマス数か量が最大になるようにしたい
        # 移動する
        # 経路で、取った方がよい場所があれば取る
        # 先に縦を合わせる
        if target[0] - track[0] > 0:
            move = "D"
            v = 1
        else:
            move = "U"
            v = -1
        for _ in range(abs(target[0] - track[0])):
            ans_stack.append(move)
            cost_stack += track_v + 100
            track[0] += v
            # 経路上で取れる分は取る
            if grid[track[0]][track[1]] > 0:
                d = grid[track[0]][track[1]]
                ans_stack.append(f"+{d}")
                grid[track[0]][track[1]] -= d
                track_v += d
                cost_stack += d

        if target[1] - track[1] > 0:
            move = "R"
            v = 1
        else:
            move = "L"
            v = -1
        for _ in range(abs(target[1] - track[1])):
            ans_stack.append(move)
            cost_stack += track_v + 100
            track[1] += v
            # 経路上で取れる分は取る
            if grid[track[0]][track[1]] > 0:
                d = grid[track[0]][track[1]]
                ans_stack.append(f"+{d}")
                grid[track[0]][track[1]] -= d
                track_v += d
                cost_stack += d

        # 置く
        d = min(track_v, abs(grid[target[0]][target[1]]))
        ans_stack.append(f"-{d}")
        grid[track[0]][track[1]] += d
        track_v -= d
        cost_stack += d

        if track_v < lower_limit:
            mode = "pick"

    # 状態更新
    for i in range(N):
        for j in range(N):
            progress[i][j] = grid[i][j] == 0
    state = sum(map(sum, progress))

if cost_nearest < cost_stack:
    for ope in ans_nearest:
        print(ope)
else:
    for ope in ans_stack:
        print(ope)

print(cost_nearest, cost_stack, file=sys.stderr)
