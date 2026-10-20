"""暴力对拍：验证"块 = 环，绕一圈只掉一次"的判据。

暴力法：k 可排序 <=> 对每个块，存在某个旋转量使该块等于 sorted(nums) 的对应块。
优化法：块内环形下降点（断点）恰好 1 个，且从断点切开后的序列 == 对应目标块。
"""
import random
from itertools import product


def divisors(n):
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def brute(nums):
    """暴力：逐块枚举所有旋转。"""
    n = len(nums)
    s = sorted(nums)
    total = 0
    for k in divisors(n):
        ok = True
        for st in range(0, n, k):
            block = nums[st:st + k]
            target = s[st:st + k]
            hit = False
            for t in range(k):
                if block[t:] + block[:t] == target:
                    hit = True
                    break
            if not hit:
                ok = False
                break
        if ok:
            total += k
    return total


def fast(nums):
    """优化：数断点 + 切开比对。"""
    n = len(nums)
    s = sorted(nums)
    total = 0
    for k in divisors(n):
        ok = True
        for st in range(0, n, k):
            brk = -1
            for i in range(k):
                if nums[st + i] > nums[st + (i + 1) % k]:
                    if brk != -1:
                        ok = False
                        break
                    brk = i
            if not ok:
                break
            off = 0 if brk == -1 else brk + 1
            for i in range(k):
                if nums[st + (off + i) % k] != s[st + i]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            total += k
    return total


def main():
    # 1. 题面三例
    assert brute([3, 1, 2]) == 3, brute([3, 1, 2])
    assert brute([7, 6, 5]) == 0
    assert brute([5, 8]) == 3
    print("题面样例: OK")

    # 2. 课文里用到的每一组数
    for a in ([2, 1, 4, 3], [3, 1, 4, 2], [1, 2, 1], [1, 2, 1, 2], [3, 4, 1, 2]):
        print(f"  nums={a} -> k 的和 = {brute(a)}")
        assert brute(a) == fast(a)

    # 3. 穷举小规模全组合
    cnt = 0
    for n in range(1, 7):
        for combo in product(range(1, 4), repeat=n):
            arr = list(combo)
            b, f = brute(arr), fast(arr)
            assert b == f, (arr, b, f)
            cnt += 1
    print(f"穷举 value in [1,3], n<=6: {cnt} 组 OK")

    # 4. 随机对拍（含大量重复值）
    random.seed(20261020)
    for it in range(4000):
        n = random.randint(1, 30)
        hi = random.choice([2, 3, 5, n])
        arr = [random.randint(1, hi) for _ in range(n)]
        b, f = brute(arr), fast(arr)
        assert b == f, (arr, b, f)
    print("随机对拍 4000 组: OK")

    # 5. 破坏性测试：把"断点恰好 1 个"改成"至多 1 个"必须被检出
    def broken(nums):
        n = len(nums)
        s = sorted(nums)
        total = 0
        for k in divisors(n):
            ok = True
            for st in range(0, n, k):
                brk = -1
                for i in range(k):
                    if nums[st + i] > nums[st + (i + 1) % k]:
                        if brk != -1:
                            ok = False
                            break
                        brk = i
                if not ok:
                    break
                off = 0 if brk == -1 else brk + 1
                for i in range(k):
                    if nums[st + (off + i) % k] != s[st + i]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                total += k
        return total

    def broken2(nums):
        """故意破坏：忽略目标块比对，只看断点个数（会误判）。"""
        n = len(nums)
        total = 0
        for k in divisors(n):
            ok = True
            for st in range(0, n, k):
                brk = -1
                for i in range(k):
                    if nums[st + i] > nums[st + (i + 1) % k]:
                        if brk != -1:
                            ok = False
                            break
                        brk = i
                if not ok:
                    break
            if ok:
                total += k
        return total

    diff = 0
    for it in range(2000):
        n = random.randint(2, 12)
        arr = [random.randint(1, 4) for _ in range(n)]
        if broken2(arr) != brute(arr):
            diff += 1
    print(f"破坏性测试（去掉目标块比对）误判组数: {diff}（>0 说明该步骤不可省）")
    assert diff > 0


if __name__ == "__main__":
    main()
    print("\n全部通过")
