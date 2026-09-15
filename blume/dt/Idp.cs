// idp: divide-and-conquer attack on double columnar transposition (after Lasry, Kopal & Wacker 2014).
// Stage 1: anneal key2 alone. Score = IDP: undo key2, cut the intermediate text into w1 columns (read order unknown,
//          start offsets uncertain because of unequal column lengths), and for each column take the best partner
//          column whose row-aligned letter pairs score well as Spanish bigrams.
// Stage 2: for the best key2 candidates, solve key1 as a single columnar transposition with quadgrams.
// Build: csc.exe /o+ /out:idp.exe Idp.cs
// Usage: idp.exe plant PLAINFILE OFFSET LEN W1 W2 RESTARTS ITERS THREADS SEED
//        idp.exe solve CTFILE W1MIN W1MAX W2MIN W2MAX RESTARTS ITERS THREADS SEED
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

static class Idp
{
    static float[] Q4; static float[] B2;

    static void Load()
    {
        var bytes = File.ReadAllBytes(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "q4_es.bin"));
        Q4 = new float[bytes.Length / 4]; Buffer.BlockCopy(bytes, 0, Q4, 0, bytes.Length);
        // bigram log-probs derived from the quadgram table by marginalising
        var cnt = new double[676];
        for (int c = 0; c < Q4.Length; c++) { double p = Math.Pow(10, Q4[c]); cnt[c / 676] += p; }
        double tot = cnt.Sum(); B2 = new float[676];
        for (int i = 0; i < 676; i++) B2[i] = (float)Math.Log10(Math.Max(cnt[i] / tot, 1e-7));
    }

    static void ColMap(int n, int[] order, int w, int[] map)
    {
        int rows = n / w, rem = n % w, pos = 0;
        for (int k = 0; k < w; k++) { int c = order[k]; int L = rows + (c < rem ? 1 : 0); for (int r = 0; r < L; r++) map[r * w + c] = pos++; }
    }

    static int[] RandPerm(int w, Random rnd) { var p = Enumerable.Range(0, w).ToArray(); for (int i = w - 1; i > 0; i--) { int j = rnd.Next(i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; } return p; }

    static void Mutate(int[] src, int[] dst, int w, Random rnd)
    {
        Array.Copy(src, dst, w); int r = rnd.Next(100);
        if (r < 45) { int a = rnd.Next(w), b = rnd.Next(w); int t = dst[a]; dst[a] = dst[b]; dst[b] = t; }
        else if (r < 80)
        {
            int a = rnd.Next(w), len = 1 + rnd.Next(Math.Max(1, w / 2)); if (a + len > w) len = w - a;
            var rest = new List<int>(); for (int i = 0; i < w; i++) if (i < a || i >= a + len) rest.Add(src[i]);
            var blk = new int[len]; Array.Copy(src, a, blk, 0, len); rest.InsertRange(rnd.Next(rest.Count + 1), blk); rest.CopyTo(dst);
        }
        else { int a = rnd.Next(w), b = rnd.Next(w); if (a > b) { int t = a; a = b; b = t; } Array.Reverse(dst, a, b - a + 1); }
    }

    // IDP of intermediate text I for first-key width w1
    static double IdpScore(int[] I, int n, int w1, double[] pbuf)
    {
        int rows = n / w1, rem = n % w1;
        double total = 0;
        for (int k1 = 0; k1 < w1; k1++)
        {
            double e1 = (double)k1 * rem / w1; int lo1 = Math.Max(0, k1 - (w1 - rem)), hi1 = Math.Min(k1, rem);
            int a1 = Math.Max(lo1, (int)Math.Round(e1) - 2), b1 = Math.Min(hi1, (int)Math.Round(e1) + 2);
            double best = double.NegativeInfinity;
            for (int k2 = 0; k2 < w1; k2++)
            {
                if (k2 == k1) continue;
                double e2 = (double)k2 * rem / w1; int lo2 = Math.Max(0, k2 - (w1 - rem)), hi2 = Math.Min(k2, rem);
                int a2 = Math.Max(lo2, (int)Math.Round(e2) - 2), b2 = Math.Min(hi2, (int)Math.Round(e2) + 2);
                for (int u1 = a1; u1 <= b1; u1++)
                {
                    int s1 = k1 * rows + u1;
                    for (int u2 = a2; u2 <= b2; u2++)
                    {
                        int s2 = k2 * rows + u2; double s = 0;
                        for (int r = 0; r < rows; r++) s += B2[I[s1 + r] * 26 + I[s2 + r]];
                        if (s > best) best = s;
                    }
                }
            }
            total += best;
        }
        return total / (w1 * rows);
    }

    static double Q4Score(int[] t, int n)
    {
        int code = t[0] * 17576 + t[1] * 676 + t[2] * 26 + t[3]; double s = Q4[code];
        for (int i = 4; i < n; i++) { code = (code % 17576) * 26 + t[i]; s += Q4[code]; }
        return s / (n - 3);
    }

    class Cand { public double Score; public int[] K2; public int W1, W2; }

    static Cand AnnealK2(int[] ct, int n, int w1, int w2, long iters, Random rnd)
    {
        int[] map = new int[n], I = new int[n]; double[] pb = new double[1];
        int[] o = RandPerm(w2, rnd), c = new int[w2];
        Func<int[], double> f = k => { ColMap(n, k, w2, map); for (int i = 0; i < n; i++) I[i] = ct[map[i]]; return IdpScore(I, n, w1, pb); };
        double cur = f(o); var best = new Cand { Score = cur, K2 = (int[])o.Clone(), W1 = w1, W2 = w2 };
        double T0 = 0.05, T1 = 0.001;
        for (long it = 0; it < iters; it++)
        {
            double T = T0 * Math.Pow(T1 / T0, (double)it / iters);
            Mutate(o, c, w2, rnd); double v = f(c);
            if (v >= cur || rnd.NextDouble() < Math.Exp((v - cur) / T)) { cur = v; var t = o; o = c; c = t; if (cur > best.Score) { best.Score = cur; best.K2 = (int[])o.Clone(); } }
        }
        return best;
    }

    static Tuple<double, int[]> SolveK1(int[] I, int n, int w1, long iters, Random rnd)
    {
        int[] map = new int[n], P = new int[n];
        int[] o = RandPerm(w1, rnd), c = new int[w1];
        Func<int[], double> f = k => { ColMap(n, k, w1, map); for (int i = 0; i < n; i++) P[i] = I[map[i]]; return Q4Score(P, n); };
        double cur = f(o); double bestS = cur; int[] bestK = (int[])o.Clone();
        double T0 = 0.04, T1 = 0.0008;
        for (long it = 0; it < iters; it++)
        {
            double T = T0 * Math.Pow(T1 / T0, (double)it / iters);
            Mutate(o, c, w1, rnd); double v = f(c);
            if (v >= cur || rnd.NextDouble() < Math.Exp((v - cur) / T)) { cur = v; var t = o; o = c; c = t; if (cur > bestS) { bestS = cur; bestK = (int[])o.Clone(); } }
        }
        return Tuple.Create(bestS, bestK);
    }

    static int[] Encrypt(int[] pt, int n, int[] o, int w) { int[] map = new int[n]; ColMap(n, o, w, map); int[] ct = new int[n]; for (int i = 0; i < n; i++) ct[map[i]] = pt[i]; return ct; }
    static int[] Undo(int[] ct, int n, int[] o, int w) { int[] map = new int[n]; ColMap(n, o, w, map); int[] I = new int[n]; for (int i = 0; i < n; i++) I[i] = ct[map[i]]; return I; }
    static int[] ToInts(string s) { return s.ToLower().Where(ch => ch >= 'a' && ch <= 'z').Select(ch => ch - 'a').ToArray(); }
    static string Str(int[] a, int len) { var sb = new StringBuilder(); for (int i = 0; i < Math.Min(len, a.Length); i++) sb.Append((char)('a' + a[i])); return sb.ToString(); }

    static void Run(int[] ct, int[] pt, int w1min, int w1max, int w2min, int w2max, int restarts, long iters, int threads, int seed)
    {
        int n = ct.Length;
        var jobs = new List<Tuple<int, int, int>>();
        for (int a = w1min; a <= w1max; a++) for (int b = w2min; b <= w2max; b++) for (int r = 0; r < restarts; r++) jobs.Add(Tuple.Create(a, b, r));
        var cands = new List<Cand>(); object lk = new object();
        Parallel.ForEach(jobs, new ParallelOptions { MaxDegreeOfParallelism = threads }, j =>
        {
            var res = AnnealK2(ct, n, j.Item1, j.Item2, iters, new Random(seed * 7919 + j.Item1 * 101 + j.Item2 * 13 + j.Item3));
            lock (lk) cands.Add(res);
        });
        var top = cands.OrderByDescending(c => c.Score).Take(Math.Max(threads, 12)).ToList();
        var finals = new List<Tuple<double, Cand, int[]>>();
        Parallel.ForEach(top, new ParallelOptions { MaxDegreeOfParallelism = threads }, c =>
        {
            var I = Undo(ct, n, c.K2, c.W2);
            Tuple<double, int[]> best = null;
            for (int r = 0; r < 4; r++) { var s = SolveK1(I, n, c.W1, 3000000, new Random(seed + r * 17 + c.K2[0])); if (best == null || s.Item1 > best.Item1) best = s; }
            lock (lk) finals.Add(Tuple.Create(best.Item1, c, best.Item2));
        });
        foreach (var f in finals.OrderByDescending(x => x.Item1).Take(8))
        {
            var I = Undo(ct, n, f.Item2.K2, f.Item2.W2); var P = Undo(I, n, f.Item3, f.Item2.W1);
            string acc = ""; if (pt != null) { int ok = 0; for (int i = 0; i < n; i++) if (P[i] == pt[i]) ok++; acc = " right " + ok + "/" + n; }
            Console.WriteLine("{0}/{1} idp {2:F4} q4 {3:F3}{4}  {5}", f.Item2.W1, f.Item2.W2, f.Item2.Score, f.Item1, acc, Str(P, 70));
        }
    }

    static void Main(string[] a)
    {
        Load(); var sw = System.Diagnostics.Stopwatch.StartNew();
        if (a[0] == "plant")
        {
            var text = ToInts(File.ReadAllText(a[1])); int off = int.Parse(a[2]), len = int.Parse(a[3]), w1 = int.Parse(a[4]), w2 = int.Parse(a[5]);
            int seed = int.Parse(a[9]); var rnd = new Random(seed); var pt = text.Skip(off).Take(len).ToArray();
            var k1 = RandPerm(w1, rnd); var k2 = RandPerm(w2, rnd);
            var ct = Encrypt(Encrypt(pt, len, k1, w1), len, k2, w2);
            var trueI = Undo(ct, len, k2, w2);
            Console.WriteLine("true key2 idp {0:F4}; random key2 idp {1:F4}", IdpScore(trueI, len, w1, null), IdpScore(Undo(ct, len, RandPerm(w2, rnd), w2), len, w1, null));
            Run(ct, pt, w1, w1, w2, w2, int.Parse(a[6]), long.Parse(a[7]), int.Parse(a[8]), seed);
        }
        else
        {
            var ct = ToInts(File.ReadAllText(a[1]));
            Run(ct, null, int.Parse(a[2]), int.Parse(a[3]), int.Parse(a[4]), int.Parse(a[5]), int.Parse(a[6]), long.Parse(a[7]), int.Parse(a[8]), int.Parse(a[9]));
        }
        Console.WriteLine("elapsed {0:F1}s", sw.Elapsed.TotalSeconds);
    }
}
