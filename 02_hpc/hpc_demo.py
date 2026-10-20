import argparse, math, time
from multiprocessing import Pool, cpu_count

def compute(bounds):
    start, end = bounds
    total = 0.0
    for i in range(start, end):
        x = i / 1000
        total += math.sqrt(x + 1) * math.sin(x)
    return total

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=80000)
    parser.add_argument("--workers", type=int, default=min(4, cpu_count()))
    args = parser.parse_args()
    if args.n < 1 or args.workers < 1:
        parser.error("--n dan --workers harus lebih besar dari nol")

    start = time.perf_counter()
    serial = compute((0, args.n))
    serial_time = time.perf_counter() - start

    step = (args.n + args.workers - 1) // args.workers
    tasks = [(i, min(i + step, args.n)) for i in range(0, args.n, step)]
    start = time.perf_counter()
    with Pool(args.workers) as pool:
        parallel = sum(pool.map(compute, tasks))
    parallel_time = time.perf_counter() - start

    print("=== SERIAL VS PARALEL ===")
    print(f"Iterasi: {args.n:,} | Worker: {args.workers}")
    print(f"Waktu serial : {serial_time:.4f} detik")
    print(f"Waktu paralel: {parallel_time:.4f} detik")
    print(f"Speedup      : {serial_time / parallel_time:.2f}x")
    print("Hasil konsisten:", math.isclose(serial, parallel, rel_tol=1e-9))
    print("Overhead proses dapat membuat paralel lebih lambat untuk tugas kecil.")

if __name__ == "__main__":
    main()
