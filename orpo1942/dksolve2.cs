// Doppelkasten solver v2: staged scoring (unigram -> bigram -> quadgram) to widen the basin of the double encipherment.
// Build: csc -o+ -platform:x64 -out:dksolve2.exe dksolve2.cs
// Usage: dksolve2 <cipherfile> <L> <restarts> <seed> <rounds> <dir R|L> <stages> [initA initB kick]
//   stages: comma list of order:iters:T0 , e.g. 1:300000:2,2:1000000:2,4:2000000:1   (order 1,2,4; T scaled per letter)
// cipherfile: "label<TAB>CIPHERTEXT" lines; all lines share one key; '#' lines ignored.
using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic;

class DK2
{
    const string AL = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    static float[] Q1, Q2, Q4;
    static int[][] cx, lay;
    static int rounds = 2, totalLen;
    static bool left = false;   // in-line (same row) case: cipher = letter to the LEFT (NSA/NI) instead of right (OKW 1941)

    static float[] Load(string f) { var raw = File.ReadAllBytes(f); var q = new float[raw.Length / 4]; Buffer.BlockCopy(raw, 0, q, 0, raw.Length); return q; }

    static int[] Layout(int n, int L)
    {
        var o = new List<int>(); int k = 0;
        while (n - k >= 2 * L) { for (int i = 0; i < L; i++) { o.Add(k + i); o.Add(k + L + i); } k += 2 * L; }
        int h = (n - k) / 2;
        for (int i = 0; i < h; i++) { o.Add(k + i); o.Add(k + h + i); }
        return o.ToArray();
    }

    static void Decrypt(int[] A, int[] B, int[] pA, int[] pB, int[][] buf)
    {
        cA = A; cB = B; cpA = pA; cpB = pB;
        int dl = left ? 1 : 4;  // decrypt shift: inverse of encrypt shift (+1 right => -1 == +4)
        for (int m = 0; m < cx.Length; m++)
        {
            var c = cx[m]; var ly = lay[m]; var p = buf[m];
            for (int k = 0; k < c.Length; k += 2)
            {
                int a = c[k], b = c[k + 1];
                for (int r = 0; r < rounds; r++)
                {
                    int pb = pB[a], pa = pA[b];
                    int rb = pb / 5, cb = pb % 5, ra = pa / 5, ca = pa % 5;
                    if (rb == ra) { a = A[ra * 5 + (ca + dl) % 5]; b = B[rb * 5 + (cb + dl) % 5]; }
                    else { a = A[rb * 5 + ca]; b = B[ra * 5 + cb]; }
                }
                p[ly[k]] = a; p[ly[k + 1]] = b;
            }
        }
    }

    [ThreadStatic] static int[] cA, cB, cpA, cpB;  // current key for order-0 score (per thread)
    static double[] F1 = new double[25];
    static double RowCol(int[] A, int[] B, int[] pA, int[] pB)
    {
        // product-form approximation of the unigram likelihood: log FA(row)+log GA(col) for p1 in A, log FB(row)+log GB(col) for p2 in B
        double[] FA = new double[5], GA = new double[5], FB = new double[5], GB = new double[5];
        for (int i = 0; i < 25; i++) { FA[i / 5] += F1[A[i]]; GA[i % 5] += F1[A[i]]; FB[i / 5] += F1[B[i]]; GB[i % 5] += F1[B[i]]; }
        for (int i = 0; i < 5; i++) { FA[i] = Math.Log(FA[i]); GA[i] = Math.Log(GA[i]); FB[i] = Math.Log(FB[i]); GB[i] = Math.Log(GB[i]); }
        double s = 0; int dl = left ? 1 : 4;
        for (int m = 0; m < cx.Length; m++)
        {
            var c = cx[m];
            for (int k = 0; k < c.Length; k += 2)
            {
                int pb = pB[c[k]], pa = pA[c[k + 1]];
                int rb = pb / 5, cb = pb % 5, ra = pa / 5, ca = pa % 5, v1, v2;
                if (rb == ra) { v1 = A[ra * 5 + (ca + dl) % 5]; v2 = B[rb * 5 + (cb + dl) % 5]; }
                else { v1 = A[rb * 5 + ca]; v2 = B[ra * 5 + cb]; }
                int q1 = pB[v1], q2 = pA[v2];
                s += FA[q1 / 5] + GB[q1 % 5] + GA[q2 % 5] + FB[q2 / 5];
            }
        }
        return s;
    }

    static double Score(int[][] buf, int order)
    {
        if (order == 0) return RowCol(cA, cB, cpA, cpB);
        double s = 0;
        foreach (var p in buf)
        {
            int n = p.Length;
            if (order == 1) for (int i = 0; i < n; i++) s += Q1[p[i]];
            else if (order == 2) for (int i = 0; i + 1 < n; i++) s += Q2[p[i] * 25 + p[i + 1]];
            else for (int i = 0; i + 3 < n; i++) s += Q4[((p[i] * 25 + p[i + 1]) * 25 + p[i + 2]) * 25 + p[i + 3]];
        }
        return s;
    }

    static void Pos(int[] X, int[] p) { for (int i = 0; i < 25; i++) p[X[i]] = i; }
    static void Shuffle(int[] x, Random R) { for (int i = x.Length - 1; i > 0; i--) { int j = R.Next(i + 1); int t = x[i]; x[i] = x[j]; x[j] = t; } }

    public static bool TauFix = Environment.GetEnvironmentVariable("DK_TAUFIX") == "1";
    static void Mutate(int[] A, int[] B, Random R)
    {
        if (TauFix) { int x = R.Next(25), y = R.Next(25); Apply(A, B, 2, x, y); return; }
        int[] X = R.Next(2) == 0 ? A : B;
        int t = R.Next(100);
        if (t < 80) { int i = R.Next(25), j = R.Next(25); int z = X[i]; X[i] = X[j]; X[j] = z; }
        else if (t < 88) { int r1 = R.Next(5), r2 = R.Next(5); for (int c = 0; c < 5; c++) { int z = X[r1 * 5 + c]; X[r1 * 5 + c] = X[r2 * 5 + c]; X[r2 * 5 + c] = z; } }
        else if (t < 96) { int c1 = R.Next(5), c2 = R.Next(5); for (int r = 0; r < 5; r++) { int z = X[r * 5 + c1]; X[r * 5 + c1] = X[r * 5 + c2]; X[r * 5 + c2] = z; } }
        else { int i = R.Next(25), j = R.Next(25), k = R.Next(25); int z = X[i]; X[i] = X[j]; X[j] = X[k]; X[k] = z; }
    }

    public static bool Relabel = Environment.GetEnvironmentVariable("DK_RELABEL") == "1";
    // move w: 0 swap cells i,j of A; 1 swap cells i,j of B; 2 swap letters i,j in both boxes (keeps sigma). Self-inverse.
    static void Apply(int[] A, int[] B, int w, int i, int j)
    {
        if (w == 0) { int z = A[i]; A[i] = A[j]; A[j] = z; }
        else if (w == 1) { int z = B[i]; B[i] = B[j]; B[j] = z; }
        else
        {
            for (int q = 0; q < 25; q++) { if (A[q] == i) A[q] = j; else if (A[q] == j) A[q] = i; if (B[q] == i) B[q] = j; else if (B[q] == j) B[q] = i; }
        }
    }
    // steepest ascent over all single-cell swaps within A or B until no improvement
    static double Steep(int[] A, int[] B, int order, int[][] buf)
    {
        int[] pA = new int[25], pB = new int[25];
        Pos(A, pA); Pos(B, pB); Decrypt(A, B, pA, pB, buf); double cur = Score(buf, order);
        while (true)
        {
            double bs = cur; int bw = -1, bi = 0, bj = 0;
            for (int w = (TauFix ? 2 : 0); w < (Relabel || TauFix ? 3 : 2); w++)
            {
                for (int i = 0; i < 25; i++) for (int j = i + 1; j < 25; j++)
                {
                    Apply(A, B, w, i, j);
                    Pos(A, pA); Pos(B, pB); Decrypt(A, B, pA, pB, buf); double s = Score(buf, order);
                    Apply(A, B, w, i, j);
                    if (s > bs + 1e-9) { bs = s; bw = w; bi = i; bj = j; }
                }
            }
            if (bw < 0) return cur;
            Apply(A, B, bw, bi, bj); cur = bs;
        }
    }

    static string Str(int[] x) { return new string(x.Select(i => AL[i]).ToArray()); }

    static void Main(string[] args)
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        Q1 = Load(Path.Combine(dir, "q1.bin")); for (int i = 0; i < 25; i++) F1[i] = Math.Pow(10, Q1[i]); Q2 = Load(Path.Combine(dir, "q2.bin")); Q4 = Load(Path.Combine(dir, "q4.bin"));
        var lines = File.ReadAllLines(args[0]).Where(l => l.Trim().Length > 0 && !l.StartsWith("#")).ToArray();
        int L = int.Parse(args[1]), restarts = int.Parse(args[2]), seed = int.Parse(args[3]);
        rounds = int.Parse(args[4]); left = args[5] == "L";
        var stages = args[6].Split(',').Select(s => s.Split(':')).Select(a => Tuple.Create(a[0].StartsWith("S") ? -1 - int.Parse(a[0].Substring(1)) : a[0].StartsWith("P") ? 100 + int.Parse(a[0].Substring(1)) : int.Parse(a[0]), long.Parse(a[1]), double.Parse(a[2]))).ToArray();
        string initA = args.Length > 9 ? args[7] : null, initB = args.Length > 9 ? args[8] : null;
        int kick = args.Length > 9 ? int.Parse(args[9]) : 0;
        var labels = new string[lines.Length];
        cx = new int[lines.Length][]; lay = new int[lines.Length][];
        for (int m = 0; m < lines.Length; m++)
        {
            var parts = lines[m].Split('\t'); labels[m] = parts[0];
            var t = parts[parts.Length - 1].Trim().ToUpper().Replace("J", "I").Replace(".", "X");
            cx[m] = t.Where(ch => AL.IndexOf(ch) >= 0).Select(ch => AL.IndexOf(ch)).ToArray();
            if (cx[m].Length % 2 == 1) cx[m] = cx[m].Take(cx[m].Length - 1).ToArray();
            lay[m] = Layout(cx[m].Length, L); totalLen += cx[m].Length;
        }
        double gBest = double.NegativeInfinity; object lk = new object();
        Parallel.For(0, restarts, new ParallelOptions { MaxDegreeOfParallelism = 22 }, rs =>
        {
            var R = new Random(seed * 100003 + rs * 7919);
            int[] A = Enumerable.Range(0, 25).ToArray(), B = Enumerable.Range(0, 25).ToArray();
            Shuffle(A, R); Shuffle(B, R);
            if (initA != null)
            {
                A = initA.Select(ch => AL.IndexOf(ch)).ToArray(); B = initB.Select(ch => AL.IndexOf(ch)).ToArray();
                if (TauFix && kick < 0) { int[] perm = Enumerable.Range(0, 25).ToArray(); Shuffle(perm, R); for (int q = 0; q < 25; q++) { A[q] = perm[A[q]]; B[q] = perm[B[q]]; } }
                else for (int q = 0; q < kick; q++) { int[] X = R.Next(2) == 0 ? A : B; int i = R.Next(25), j = R.Next(25); int z = X[i]; X[i] = X[j]; X[j] = z; }
            }
            int[] pA = new int[25], pB = new int[25], nA = new int[25], nB = new int[25];
            var buf = cx.Select(c => new int[c.Length]).ToArray();
            double best = 0; var sb = new System.Text.StringBuilder();
            foreach (var st in stages)
            {
                if (st.Item1 < 0)
                {
                    int ord = -1 - st.Item1; int cycles = (int)st.Item2; int ksz = (int)st.Item3;
                    double sc = Steep(A, B, ord, buf); int[] kA = (int[])A.Clone(), kB = (int[])B.Clone(); double ks = sc;
                    for (int cy = 0; cy < cycles; cy++)
                    {
                        int[] tA = (int[])kA.Clone(), tB = (int[])kB.Clone();
                        for (int q = 0; q < ksz; q++) { int[] X = R.Next(2) == 0 ? tA : tB; int i = R.Next(25), j = R.Next(25); int z = X[i]; X[i] = X[j]; X[j] = z; }
                        double s2 = Steep(tA, tB, ord, buf);
                        if (s2 > ks) { ks = s2; kA = tA; kB = tB; }
                    }
                    Array.Copy(kA, A, 25); Array.Copy(kB, B, 25);
                    sb.AppendFormat(" S{0}={1:F3}", ord, ks / totalLen);
                    continue;
                }
                if (st.Item1 >= 100)
                {
                    int ordp = st.Item1 - 100; long sweeps = st.Item2; double Thi = st.Item3 * totalLen / 100.0, Tlo = Thi / 60.0;
                    int NR = 24;
                    var RA = new int[NR][]; var RB = new int[NR][]; var RS = new double[NR]; var TT = new double[NR];
                    for (int q = 0; q < NR; q++)
                    {
                        RA[q] = (int[])A.Clone(); RB[q] = (int[])B.Clone();
                        if (q > 0) { Shuffle(RA[q], R); Shuffle(RB[q], R); }
                        TT[q] = Tlo * Math.Pow(Thi / Tlo, (double)q / (NR - 1));
                        Pos(RA[q], pA); Pos(RB[q], pB); Decrypt(RA[q], RB[q], pA, pB, buf); RS[q] = Score(buf, ordp);
                    }
                    double pbest = RS.Max(); int[] pbA = (int[])RA[Array.IndexOf(RS, pbest)].Clone(), pbB = (int[])RB[Array.IndexOf(RS, pbest)].Clone();
                    for (long sw = 0; sw < sweeps; sw++)
                    {
                        for (int q = 0; q < NR; q++)
                        {
                            for (int mv = 0; mv < 50; mv++)
                            {
                                Array.Copy(RA[q], nA, 25); Array.Copy(RB[q], nB, 25);
                                Mutate(nA, nB, R);
                                Pos(nA, pA); Pos(nB, pB); Decrypt(nA, nB, pA, pB, buf);
                                double sc2 = Score(buf, ordp);
                                if (sc2 >= RS[q] || R.NextDouble() < Math.Exp((sc2 - RS[q]) / TT[q]))
                                {
                                    Array.Copy(nA, RA[q], 25); Array.Copy(nB, RB[q], 25); RS[q] = sc2;
                                    if (sc2 > pbest) { pbest = sc2; Array.Copy(nA, pbA, 25); Array.Copy(nB, pbB, 25); }
                                }
                            }
                        }
                        for (int q = 0; q + 1 < NR; q++)
                        {
                            double d = (RS[q + 1] - RS[q]) * (1 / TT[q] - 1 / TT[q + 1]);
                            if (d >= 0 || R.NextDouble() < Math.Exp(d))
                            { var ta = RA[q]; RA[q] = RA[q + 1]; RA[q + 1] = ta; var tb = RB[q]; RB[q] = RB[q + 1]; RB[q + 1] = tb; var ts = RS[q]; RS[q] = RS[q + 1]; RS[q + 1] = ts; }
                        }
                    }
                    Array.Copy(pbA, A, 25); Array.Copy(pbB, B, 25);
                    sb.AppendFormat(" P{0}={1:F3}", ordp, pbest / totalLen);
                    continue;
                }
                int order = st.Item1; long iters = st.Item2; double T0 = st.Item3 * totalLen / 100.0;
                Pos(A, pA); Pos(B, pB); Decrypt(A, B, pA, pB, buf);
                double cur = Score(buf, order); best = cur;
                int[] bA = (int[])A.Clone(), bB = (int[])B.Clone();
                for (long it = 0; it < iters; it++)
                {
                    double T = T0 * (1.0 - (double)it / iters) + 1e-4;
                    Array.Copy(A, nA, 25); Array.Copy(B, nB, 25);
                    Mutate(nA, nB, R);
                    Pos(nA, pA); Pos(nB, pB); Decrypt(nA, nB, pA, pB, buf);
                    double s = Score(buf, order);
                    if (s >= cur || R.NextDouble() < Math.Exp((s - cur) / T))
                    {
                        Array.Copy(nA, A, 25); Array.Copy(nB, B, 25); cur = s;
                        if (s > best) { best = s; Array.Copy(A, bA, 25); Array.Copy(B, bB, 25); }
                    }
                }
                Array.Copy(bA, A, 25); Array.Copy(bB, B, 25);
                sb.AppendFormat(" s{0}={1:F3}", order, best / totalLen);
            }
            Pos(A, pA); Pos(B, pB); Decrypt(A, B, pA, pB, buf);
            double q4 = Score(buf, 4);
            lock (lk)
            {
                bool nb = q4 > gBest; if (nb) gBest = q4;
                Console.WriteLine("R{0} q4 {1:F1} per {2:F3} A={3} B={4}{5}{6}", rs, q4, q4 / totalLen, Str(A), Str(B), sb, nb ? " *" : "");
                if (nb) for (int m = 0; m < cx.Length; m++) Console.WriteLine("   {0}: {1}", labels[m], new string(buf[m].Select(i => AL[i]).ToArray()));
                Console.Out.Flush();
            }
        });
    }
}
