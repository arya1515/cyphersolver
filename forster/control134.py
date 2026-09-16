"""The control the goal asked for by name: six matched French controls of 134 letters (the tracker's wrong count)
under the final word-edge model of solve2.py, to show what that length does; then the real 207 as reference."""
import solve2, key
for n in (134, 207):
    hits = 0
    for seed in range(6):
        cg, tk, pt = solve2.make_control(100+seed, n_letters=n)
        sc, k = solve2.anneal(cg, restarts=8)
        a = solve2.acc(cg, k, tk); hits += a > 0.95
        print(f'{n}-letter CONTROL {seed}: found {sc:.1f} truth {solve2.score(solve2.enc(" "+pt+" ")):.1f} letters right {a:.3f} | {solve2.render(cg,k)[:70]}', flush=True)
    print(f'== {n} letters: {hits}/6 controls read', flush=True)
