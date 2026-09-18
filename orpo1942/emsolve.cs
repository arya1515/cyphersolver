// Hard-EM ciphertext-only attack on the double Doppelkasten.
// State: key K=(A,B) and a plaintext guess P. Score = w*quadgram(P) + sum_pairs kp(K; p_k, c_k), where kp is the
// meet-in-the-middle agreement between E_K(p) and D_K(c) (row/col of both intermediates, +2 when exact).
// Alternate: K-step = annealing of kp given P (smooth, like known plaintext); P-step = ICM over pairs, all 625 options.
// Build: csc -o+ -platform:x64 -out:emsolve.exe emsolve.cs
// Usage: emsolve <cipherfile> <L> <restarts> <seed> <rounds_em> <kiters> <w> [dir R|L]
using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic;

class EM
{
    const string AL = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    static float[] Q4;
    static int[][] cx, lay, posOf;   // per message: cipher letters; layout (plain position of each cipher letter)
    static int nPairs; static int[] pm, pk;  // flattened pair -> (message, pair index)
    static bool left = false;

    static float[] Load(string f) { var raw = File.ReadAllBytes(f); var q = new float[raw.Length / 4]; Buffer.BlockCopy(raw, 0, q, 0, raw.Length); return q; }
    static int[] Layout(int n, int L)
    {
        var o = new List<int>(); int k = 0;
        while (n - k >= 2 * L) { for (int i = 0; i < L; i++) { o.Add(k + i); o.Add(k + L + i); } k += 2 * L; }
        int h = (n - k) / 2; for (int i = 0; i < h; i++) { o.Add(k + i); o.Add(k + h + i); }
        return o.ToArray();
    }
    static void Pos(int[] X, int[] p) { for (int i = 0; i < 25; i++) p[X[i]] = i; }
    static void Shuffle(int[] x, Random R) { for (int i = x.Length - 1; i > 0; i--) { int j = R.Next(i + 1); int t = x[i]; x[i] = x[j]; x[j] = t; } }

    static void Enc(int[] A, int[] B, int[] pA, int[] pB, int x1, int x2, out int y1, out int y2)
    {
        int ra = pA[x1] / 5, ca = pA[x1] % 5, rb = pB[x2] / 5, cb = pB[x2] % 5; int sh = left ? 4 : 1;
        if (ra == rb) { y1 = B[ra * 5 + (cb + sh) % 5]; y2 = A[ra * 5 + (ca + sh) % 5]; } else { y1 = B[ra * 5 + cb]; y2 = A[rb * 5 + ca]; }
    }
    static void Dec(int[] A, int[] B, int[] pA, int[] pB, int x1, int x2, out int y1, out int y2)
    {
        int rb = pB[x1] / 5, cb = pB[x1] % 5, ra = pA[x2] / 5, ca = pA[x2] % 5; int sh = left ? 1 : 4;
        if (rb == ra) { y1 = A[ra * 5 + (ca + sh) % 5]; y2 = B[rb * 5 + (cb + sh) % 5]; } else { y1 = A[rb * 5 + ca]; y2 = B[ra * 5 + cb]; }
    }
    static int Agree(int[] pA, int[] pB, int f1, int f2, int b1, int b2)
    {
        int qa = pA[f1], qb = pA[b1], ra = pB[f2], rb = pB[b2];
        int s = (qa / 5 == qb / 5 ? 1 : 0) + (qa % 5 == qb % 5 ? 1 : 0) + (ra / 5 == rb / 5 ? 1 : 0) + (ra % 5 == rb % 5 ? 1 : 0);
        if (f1 == b1 && f2 == b2) s += 2;
        return s;
    }
    // kp total for key given plaintext P
    static int KP(int[] A, int[] B, int[] pA, int[] pB, int[][] P)
    {
        int s = 0;
        for (int m = 0; m < cx.Length; m++)
        {
            var c = cx[m]; var ly = lay[m]; var p = P[m];
            for (int k = 0; k < c.Length; k += 2)
            {
                int f1, f2, b1, b2;
                Enc(A, B, pA, pB, p[ly[k]], p[ly[k + 1]], out f1, out f2);
                Dec(A, B, pA, pB, c[k], c[k + 1], out b1, out b2);
                s += Agree(pA, pB, f1, f2, b1, b2);
            }
        }
        return s;
    }
    static double LMat(int[] p, int i)   // sum of quadgram windows containing position i
    {
        double s = 0; int n = p.Length;
        for (int st = Math.Max(0, i - 3); st <= i && st + 3 < n; st++) s += Q4[((p[st] * 25 + p[st + 1]) * 25 + p[st + 2]) * 25 + p[st + 3]];
        return s;
    }
    static double LM(int[][] P) { double s = 0; foreach (var p in P) for (int i = 0; i + 3 < p.Length; i++) s += Q4[((p[i] * 25 + p[i + 1]) * 25 + p[i + 2]) * 25 + p[i + 3]]; return s; }

    static void Main(string[] args)
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        Q4 = Load(Path.Combine(dir, "q4.bin"));
        var lines = File.ReadAllLines(args[0]).Where(l => l.Trim().Length > 0 && !l.StartsWith("#")).ToArray();
        int L = int.Parse(args[1]), restarts = int.Parse(args[2]), seed = int.Parse(args[3]), emRounds = int.Parse(args[4]);
        long kiters = long.Parse(args[5]); double w = double.Parse(args[6]); left = args.Length > 7 && args[7] == "L";
        cx = new int[lines.Length][]; lay = new int[lines.Length][]; int total = 0;
        for (int m = 0; m < lines.Length; m++)
        {
            var t = lines[m].Split('\t').Last().Trim().ToUpper().Replace("J", "I").Replace(".", "X");
            cx[m] = t.Where(ch => AL.IndexOf(ch) >= 0).Select(ch => AL.IndexOf(ch)).ToArray();
            if (cx[m].Length % 2 == 1) cx[m] = cx[m].Take(cx[m].Length - 1).ToArray();
            lay[m] = Layout(cx[m].Length, L); total += cx[m].Length;
        }
        object lk = new object();
        Parallel.For(0, restarts, new ParallelOptions { MaxDegreeOfParallelism = 22 }, rs =>
        {
            var R = new Random(seed * 1009 + rs * 7);
            int[] A = Enumerable.Range(0, 25).ToArray(), B = Enumerable.Range(0, 25).ToArray(); Shuffle(A, R); Shuffle(B, R);
            int[] pA = new int[25], pB = new int[25]; Pos(A, pA); Pos(B, pB);
            // initial plaintext: current decryption
            var P = cx.Select(c => new int[c.Length]).ToArray();
            DecryptAll(A, B, pA, pB, P);
            int[] tA = new int[25], tB = new int[25];
            double bestFull = double.NegativeInfinity; string bestKey = "";
            for (int em = 0; em < emRounds; em++)
            {
                // K-step: anneal kp given P
                int cur = KP(A, B, pA, pB, P);
                for (long it = 0; it < kiters; it++)
                {
                    double T = 2.0 * (1.0 - (double)it / kiters) + 0.05;
                    int[] X = R.Next(2) == 0 ? A : B; int mt = R.Next(100), i = R.Next(25), j = R.Next(25);
                    if (mt >= 80) { i = R.Next(5); j = R.Next(5); }
                    Move(X, mt, i, j); Pos(A, pA); Pos(B, pB);
                    int s = KP(A, B, pA, pB, P);
                    if (s >= cur || R.NextDouble() < Math.Exp((s - cur) / T)) cur = s;
                    else { Move(X, mt, i, j); Pos(A, pA); Pos(B, pB); }
                }
                // P-step: ICM over pairs
                for (int m = 0; m < cx.Length; m++)
                {
                    var c = cx[m]; var ly = lay[m]; var p = P[m];
                    for (int k = 0; k < c.Length; k += 2)
                    {
                        int b1, b2; Dec(A, B, pA, pB, c[k], c[k + 1], out b1, out b2);
                        int i1 = ly[k], i2 = ly[k + 1];
                        double[] lt = new double[25], lb = new double[25];
                        int o1 = p[i1], o2 = p[i2];
                        for (int x = 0; x < 25; x++) { p[i1] = x; lt[x] = LMat(p, i1); } p[i1] = o1;
                        for (int x = 0; x < 25; x++) { p[i2] = x; lb[x] = LMat(p, i2); } p[i2] = o2;
                        double bs = double.NegativeInfinity; int bx = o1, by = o2;
                        for (int x = 0; x < 25; x++) for (int y = 0; y < 25; y++)
                        {
                            int f1, f2; Enc(A, B, pA, pB, x, y, out f1, out f2);
                            double sc = w * (lt[x] + lb[y]) + Agree(pA, pB, f1, f2, b1, b2);
                            if (sc > bs) { bs = sc; bx = x; by = y; }
                        }
                        p[i1] = bx; p[i2] = by;
                    }
                }
                // monitor: full decryption quadgram
                var D = cx.Select(q => new int[q.Length]).ToArray(); DecryptAll(A, B, pA, pB, D);
                double full = LM(D) / total;
                if (full > bestFull) { bestFull = full; bestKey = new string(A.Select(q => AL[q]).ToArray()) + " " + new string(B.Select(q => AL[q]).ToArray()); }
            }
            lock (lk) { Console.WriteLine("R{0} bestfull {1:F3} key {2} lmP {3:F3}", rs, bestFull, bestKey, LM(P) / total); Console.Out.Flush(); }
        });
    }
    static void DecryptAll(int[] A, int[] B, int[] pA, int[] pB, int[][] P)
    {
        for (int m = 0; m < cx.Length; m++)
        {
            var c = cx[m]; var ly = lay[m];
            for (int k = 0; k < c.Length; k += 2)
            {
                int a = c[k], b = c[k + 1], y1, y2;
                Dec(A, B, pA, pB, a, b, out y1, out y2); Dec(A, B, pA, pB, y1, y2, out a, out b);
                P[m][ly[k]] = a; P[m][ly[k + 1]] = b;
            }
        }
    }
    static void Move(int[] X, int mt, int i, int j)
    {
        if (mt < 80) { int z = X[i]; X[i] = X[j]; X[j] = z; }
        else if (mt < 90) { for (int c = 0; c < 5; c++) { int z = X[i * 5 + c]; X[i * 5 + c] = X[j * 5 + c]; X[j * 5 + c] = z; } }
        else { for (int r = 0; r < 5; r++) { int z = X[r * 5 + i]; X[r * 5 + i] = X[r * 5 + j]; X[r * 5 + j] = z; } }
    }
}
