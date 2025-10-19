import random, time
from statistics import median
from cyk import cyk_parse
from ll1 import parse as ll1_parse

def make_valid(k:int) -> str:
    return " + ".join(["id"]*k)

def make_invalid(k:int) -> str:
    s = make_valid(k)
    pos = random.randrange(len(s))
    return s[:pos] + "+" + s[pos:]  # induce '++' o '+' al final

def timeit(func, cases, rounds=3):
    times=[]
    for _ in range(rounds):
        t0=time.perf_counter()
        for s in cases:
            func(s.split())
        times.append(time.perf_counter()-t0)
    return min(times), median(times)

def main():
    random.seed(0)
    sizes = [5, 10, 20, 40, 80]   # moderado
    print("n_ids;cases;cyk_min;cyk_med;ll1_min;ll1_med")
    for n in sizes:
        valid = [make_valid(n) for _ in range(20)]
        invalid = [make_invalid(n) for _ in range(20)]
        batch = valid + invalid
        cmin, cmed = timeit(cyk_parse, batch)
        lmin, lmed = timeit(ll1_parse, batch)
        print(f"{n};{len(batch)};{cmin:.6f};{cmed:.6f};{lmin:.6f};{lmed:.6f}")

if __name__=="__main__":
    main()

