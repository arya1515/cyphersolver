// Known-plaintext solver for the double Doppelkasten: meet-in-the-middle with coordinate-level partial credit.
// For each known pair (p1,p2)->(c1,c2): V_fwd = E(p) and V_bwd = D(c) must agree (same boxes both passes).
// Score = sum over pairs of [row/col agreement of v1 in A, v2 in B] (+ bonus for exact letter agreement).
// Build: csc -o+ -platform:x64 -out:kpsolve.exe kpsolve.cs
// Usage: kpsolve <pairsfile: lines "p1p2 c1c2"> <restarts> <iters> <seed> <dir R|L> [T0]
using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

class KP
{
    const string AL = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    static int[] P1, P2, C1, C2; static int n; static bool left = false;

    static void Enc(int[] A, int[] B, int[] pA, int[] pB, int x1, int x2, out int y1, out int y2)
    {
        int ra = pA[x1] / 5, ca = pA[x1] % 5, rb = pB[x2] / 5, cb = pB[x2] % 5;
        int sh = left ? 4 : 1;
        if (ra == rb) { y1 = B[ra * 5 + (cb + sh) % 5]; y2 = A[ra * 5 + (ca + sh) % 5]; }
        else { y1 = B[ra * 5 + cb]; y2 = A[rb * 5 + ca]; }
    }
    static void Dec(int[] A, int[] B, int[] pA, int[] pB, int x1, int x2, out int y1, out int y2)
    {
        int rb = pB[x1] / 5, cb = pB[x1] % 5, ra = pA[x2] / 5, ca = pA[x2] % 5;
        int sh = left ? 1 : 4;
        if (rb == ra) { y1 = A[ra * 5 + (ca + sh) % 5]; y2 = B[rb * 5 + (cb + sh) % 5]; }
        else { y1 = A[rb * 5 + ca]; y2 = B[ra * 5 + cb]; }
    }

    static double Score(int[] A, int[] B, int[] pA, int[] pB, out int exact)
    {
        double s = 0; exact = 0;
        for (int k = 0; k < n; k++)
        {
            int f1, f2, b1, b2;
            Enc(A, B, pA, pB, P1[k], P2[k], out f1, out f2);   // intermediate from plaintext
            Dec(A, B, pA, pB, C1[k], C2[k], out b1, out b2);   // intermediate from ciphertext
            // v1 is looked up in A in pass 2, v2 in B: compare their cells
            int qa = pA[f1], qb = pA[b1], ra = pB[f2], rb = pB[b2];
            s += (qa / 5 == qb / 5 ? 1 : 0) + (qa % 5 == qb % 5 ? 1 : 0) + (ra / 5 == rb / 5 ? 1 : 0) + (ra % 5 == rb % 5 ? 1 : 0);
            if (f1 == b1 && f2 == b2) { exact++; s += 2; }
        }
        return s;
    }

    // self-inverse moves: cell swap (mt<80), row swap (80-89), column swap (90-99)
    static void Move(int[] X, int mt, int i, int j)
    {
        if (mt < 80) { int z = X[i]; X[i] = X[j]; X[j] = z; }
        else if (mt < 90) { for (int c = 0; c < 5; c++) { int z = X[i * 5 + c]; X[i * 5 + c] = X[j * 5 + c]; X[j * 5 + c] = z; } }
        else { for (int r = 0; r < 5; r++) { int z = X[r * 5 + i]; X[r * 5 + i] = X[r * 5 + j]; X[r * 5 + j] = z; } }
    }
    static void Pos(int[] X, int[] p) { for (int i = 0; i < 25; i++) p[X[i]] = i; }
    static void Shuffle(int[] x, Random R) { for (int i = x.Length - 1; i > 0; i--) { int j = R.Next(i + 1); int t = x[i]; x[i] = x[j]; x[j] = t; } }

    static void Main(string[] args)
    {
        var lines = File.ReadAllLines(args[0]).Where(l => l.Trim().Length > 0 && !l.StartsWith("#")).ToArray();
        n = lines.Length; P1 = new int[n]; P2 = new int[n]; C1 = new int[n]; C2 = new int[n];
        for (int k = 0; k < n; k++)
        {
            var t = lines[k].Split(' ');
            P1[k] = AL.IndexOf(t[0][0]); P2[k] = AL.IndexOf(t[0][1]); C1[k] = AL.IndexOf(t[1][0]); C2[k] = AL.IndexOf(t[1][1]);
        }
        int restarts = int.Parse(args[1]); long iters = long.Parse(args[2]); int seed = int.Parse(args[3]); left = args[4] == "L";
        double T0 = args.Length > 5 ? double.Parse(args[5]) : 3.0;
        object lk = new object();
        Parallel.For(0, restarts, new ParallelOptions { MaxDegreeOfParallelism = 22 }, rs =>
        {
            var R = new Random(seed * 7777 + rs * 131);
            int[] A = Enumerable.Range(0, 25).ToArray(), B = Enumerable.Range(0, 25).ToArray(); Shuffle(A, R); Shuffle(B, R);
            int[] pA = new int[25], pB = new int[25]; Pos(A, pA); Pos(B, pB);
            int ex; double cur = Score(A, B, pA, pB, out ex), best = cur; int[] bA = (int[])A.Clone(), bB = (int[])B.Clone(); int bex = ex;
            for (long it = 0; it < iters; it++)
            {
                double T = T0 * (1.0 - (double)it / iters) + 0.02;
                int[] X = R.Next(2) == 0 ? A : B; int mt = R.Next(100), i = R.Next(25), j = R.Next(25);
                if (mt >= 80) { i = R.Next(5); j = R.Next(5); }
                Move(X, mt, i, j); Pos(A, pA); Pos(B, pB);
                double s = Score(A, B, pA, pB, out ex);
                if (s >= cur || R.NextDouble() < Math.Exp((s - cur) / T)) { cur = s; if (s > best) { best = s; bex = ex; Array.Copy(A, bA, 25); Array.Copy(B, bB, 25); } }
                else { Move(X, mt, i, j); Pos(A, pA); Pos(B, pB); }
            }
            lock (lk) { Console.WriteLine("R{0} score {1} exact {2}/{3} A={4} B={5}", rs, best, bex, n, new string(bA.Select(q => AL[q]).ToArray()), new string(bB.Select(q => AL[q]).ToArray())); Console.Out.Flush(); }
        });
    }
}
