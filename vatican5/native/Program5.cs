// vsolve (C# 5 for .NET Framework csc.exe): lattice solver for Vatican Challenge Part 5.
// Build: csc.exe /o+ /out:vsolve.exe Program5.cs
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

class Chunk
{
    public int[] D; public bool[] Dot; public int Start, Len;
    public int[][] OptId; public int[][] OptN;
    public double Score = -1e9; public List<int> PathSym; public List<int[]> PathVal; public int[] Letters = new int[32];
    public Chunk(int[] d, bool[] dot, int start, int len)
    {
        D = d; Dot = dot; Start = start; Len = len; OptId = new int[len][]; OptN = new int[len][];
        for (int i = 0; i < len; i++)
        {
            var ids = new List<int>(); var ns = new List<int>(); int p = start + i;
            if (dot[p])
            {
                ids.Add(10 + d[p]); ns.Add(1);
                if (i + 1 < len && !dot[p + 1]) { ids.Add(120 + d[p + 1]); ns.Add(2); }
                if (i + 2 < len && !dot[p + 1] && !dot[p + 2]) { ids.Add(130 + d[p + 1] * 10 + d[p + 2]); ns.Add(3); }
            }
            else
            {
                ids.Add(d[p]); ns.Add(1);
                if (p > start && dot[p - 1]) { ids.Add(230 + d[p]); ns.Add(1); }   // digit right after a dotted digit
                if (i + 1 < len && !dot[p + 1]) { ids.Add(20 + d[p] * 10 + d[p + 1]); ns.Add(2); }
            }
            OptId[i] = ids.ToArray(); OptN[i] = ns.ToArray();
        }
    }
    struct St { public int ctx; public double sc; public int bpPos, bpIdx, sym; public int[] v; }
    St[][] layers; int[] cnt; int cap; int[][] hkey, hval, hstamp; int stamp; const int HS = 1024;
    static readonly int[] EMPTY = new int[0];
    int Find(int layer, int ctx)
    {
        var hk = hkey[layer]; var hs = hstamp[layer]; int slot = (int)(((uint)ctx * 2654435761u) >> 22) & (HS - 1);
        while (hs[slot] == stamp) { if (hk[slot] == ctx) return hval[layer][slot]; slot = (slot + 1) & (HS - 1); }
        return -1;
    }
    void Insert(int layer, int ctx, int idx)
    {
        var hk = hkey[layer]; var hs = hstamp[layer]; int slot = (int)(((uint)ctx * 2654435761u) >> 22) & (HS - 1);
        while (hs[slot] == stamp) slot = (slot + 1) & (HS - 1);
        hs[slot] = stamp; hk[slot] = ctx; hval[layer][slot] = idx;
    }
    public double Viterbi(List<int[]>[] key, float[] lm, int beam, double lambda)
    {
        int L = Program.L, B = L + 1, B3 = B * B * B;
        if (layers == null || cap < beam * 12)
        {
            cap = beam * 12; layers = new St[Len + 1][]; cnt = new int[Len + 1];
            hkey = new int[Len + 1][]; hval = new int[Len + 1][]; hstamp = new int[Len + 1][];
            for (int i = 0; i <= Len; i++) { layers[i] = new St[cap]; hkey[i] = new int[HS]; hval[i] = new int[HS]; hstamp[i] = new int[HS]; }
        }
        stamp++;
        Array.Clear(cnt, 0, Len + 1);
        var s0 = new St(); s0.ctx = ((L * B + L) * B + L) * B + L; s0.sc = 0; s0.bpPos = -1; layers[0][0] = s0; cnt[0] = 1; Insert(0, s0.ctx, 0);
        for (int i = 0; i < Len; i++)
        {
            var Lyr = layers[i]; int n0 = cnt[i]; if (n0 == 0) continue;
            if (n0 > beam)
            {   // partial selection: keep best `beam` (simple selection sort on small arrays)
                for (int a = 0; a < beam; a++) { int m = a; for (int b = a + 1; b < n0; b++) if (Lyr[b].sc > Lyr[m].sc) m = b; var tmp = Lyr[a]; Lyr[a] = Lyr[m]; Lyr[m] = tmp; }
                n0 = beam;
            }
            for (int si = 0; si < n0; si++)
            {
                var st = Lyr[si];
                {   // penalized skip (treat digit as a null) so that a chunk never becomes unparseable
                    var target = layers[i + 1]; int tc = cnt[i + 1]; double sc = st.sc - 15.0; int found = Find(i + 1, st.ctx);
                    if (found < 0) { if (tc < cap) { var ns = new St(); ns.ctx = st.ctx; ns.sc = sc; ns.bpPos = i; ns.bpIdx = si; ns.sym = -1; ns.v = EMPTY; target[tc] = ns; Insert(i + 1, st.ctx, tc); cnt[i + 1] = tc + 1; } }
                    else if (sc > target[found].sc) { var ns = new St(); ns.ctx = st.ctx; ns.sc = sc; ns.bpPos = i; ns.bpIdx = si; ns.sym = -1; ns.v = EMPTY; target[found] = ns; }
                }
                for (int oi = 0; oi < OptId[i].Length; oi++)
                {
                    int id = OptId[i][oi], n = OptN[i][oi];
                    var vals = key[id];
                    if (vals.Count == 0)
                    {
                        if (Program.unk <= 0 || n < 2) continue;
                        var tgt = layers[i + n]; int tcc = cnt[i + n]; double scu = st.sc - Program.unk * n; int fu = Find(i + n, st.ctx);
                        if (fu < 0) { if (tcc < cap) { var nu = new St(); nu.ctx = st.ctx; nu.sc = scu; nu.bpPos = i; nu.bpIdx = si; nu.sym = -2; nu.v = EMPTY; tgt[tcc] = nu; Insert(i + n, st.ctx, tcc); cnt[i + n] = tcc + 1; } }
                        else if (scu > tgt[fu].sc) { var nu = new St(); nu.ctx = st.ctx; nu.sc = scu; nu.bpPos = i; nu.bpIdx = si; nu.sym = -2; nu.v = EMPTY; tgt[fu] = nu; }
                        continue;
                    }
                    var target = layers[i + n]; int tc = cnt[i + n];
                    for (int vi = 0; vi < vals.Count; vi++)
                    {
                        int[] v = vals[vi]; int h = st.ctx; double sc = st.sc;
                        for (int k = 0; k < v.Length; k++) { int c = v[k]; sc += lm[h * L + c] + lambda; h = (h % B3) * B + c; }
                        int found = Find(i + n, h);
                        if (found < 0)
                        {
                            if (tc >= cap) continue;
                            var ns = new St(); ns.ctx = h; ns.sc = sc; ns.bpPos = i; ns.bpIdx = si; ns.sym = id; ns.v = v; target[tc] = ns; Insert(i + n, h, tc); tc++;
                        }
                        else if (sc > target[found].sc)
                        {
                            var ns = new St(); ns.ctx = h; ns.sc = sc; ns.bpPos = i; ns.bpIdx = si; ns.sym = id; ns.v = v; target[found] = ns;
                        }
                    }
                    cnt[i + n] = tc;
                }
            }
        }
        var end = layers[Len]; int ne = cnt[Len];
        Array.Clear(Letters, 0, Letters.Length);
        if (ne == 0) { Score = -12.0 * Len; PathSym = null; PathVal = null; return Score; }
        int bi = 0; for (int k = 1; k < ne; k++) if (end[k].sc > end[bi].sc) bi = k;
        Score = end[bi].sc;
        PathSym = new List<int>(); PathVal = new List<int[]>();
        int pos = Len, idx = bi;
        while (pos > 0)
        {
            var st = layers[pos][idx]; PathSym.Add(st.sym); PathVal.Add(st.v); foreach (var c in st.v) Letters[c]++;
            pos = st.bpPos; idx = st.bpIdx;
        }
        PathSym.Reverse(); PathVal.Reverse();
        if (Program.wcoef > 0 && Program.dict != null)
        {
            var sb = new StringBuilder(); foreach (var v in PathVal) foreach (var c in v) sb.Append(Program.ALPHA[c]);
            string s = sb.ToString(); int n = s.Length; var best = new int[n + 1];
            for (int i = 1; i <= n; i++)
            {
                best[i] = best[i - 1];
                if (s[i - 1] == '_') continue;
                for (int w = Program.wmin; w <= Program.wmax && w <= i; w++)
                {
                    if (s[i - w] == '_') break;
                    if (best[i - w] + w > best[i] && Program.dict.Contains(s.Substring(i - w, w))) best[i] = best[i - w] + w;
                }
            }
            WordCov = best[n]; Score += Program.wcoef * WordCov;
        }
        return Score;
    }
    public int WordCov;
}

static class Program
{
    public static int L = 20; const int NSYM = 240;
    public static string ALPHA = "abcdefghilmnopqrstuz"; static string VOW = "aeiou", CONS = "bcdfghlmnpqrstz";
    static Random rnd; static float[] lm; static List<Chunk> chunks; static List<int>[] symChunks; static int[] symbols;
    static List<int[]>[] key; static long[] letters = new long[32]; static double mu, lambda, codepen; static int beam; static string outPath;
    static double[] expect = { .117, .009, .045, .037, .118, .010, .016, .015, .113, .065, .025, .069, .098, .031, .005, .064, .050, .056, .051, .005, .15 };

    static string SymName(int id)
    {
        if (id < 10) return id.ToString(); if (id < 20) return (id - 10) + "^";
        if (id < 120) return ((id - 20) / 10).ToString() + ((id - 20) % 10);
        if (id < 130) return "^" + (id - 120); if (id < 230) return "^" + ((id - 130) / 10) + ((id - 130) % 10); return "." + (id - 230);
    }
    static bool IsSingle(int id) { return id < 20 || (id >= 120 && id < 130) || id >= 230; }
    static int[] Str(string s) { var a = new int[s.Length]; for (int i = 0; i < s.Length; i++) a[i] = ALPHA.IndexOf(s[i]); return a; }
    static string Val(int[] v) { var sb = new StringBuilder(); foreach (var c in v) sb.Append(ALPHA[c]); return sb.ToString(); }
    static double KL()
    {
        if (mu == 0) return 0; long n = 0; foreach (var x in letters) n += x; if (n == 0) return 0; double kl = 0;
        for (int i = 0; i < L; i++) if (letters[i] > 0) { double p = (double)letters[i] / n; kl += p * Math.Log(p / expect[i]); }
        return -mu * n * kl;
    }
    static double CodePen() { int n = 0; for (int i = 10; i < NSYM; i++) if (key[i].Count > 0) n++; return -codepen * n; }
    static double Total() { double t = 0; foreach (var c in chunks) t += c.Score; return t + KL() + CodePen(); }
    static void RescoreAll()
    {
        Array.Clear(letters, 0, L);
        Parallel.For(0, chunks.Count, new ParallelOptions { MaxDegreeOfParallelism = threads }, ci => { chunks[ci].Viterbi(key, lm, beam, lambda); });
        foreach (var c in chunks) for (int i = 0; i < L; i++) letters[i] += c.Letters[i];
    }
    static int threads = 6; public static double unk = 0; public static double wcoef = 0; public static int wmin = 5, wmax = 14; public static HashSet<string> dict;
    static void Dump(List<int[]>[] k, double score)
    {
        var saved = key; key = k; RescoreAll();
        var sb = new StringBuilder();
        sb.AppendLine("BEST " + score.ToString("F1")); sb.AppendLine("KEY:");
        foreach (var id in symbols) if (key[id].Count > 0)
            sb.AppendLine("  " + SymName(id).PadRight(4) + " = " + string.Join("/", key[id].Select(v => Val(v)).ToArray()));
        sb.AppendLine(); sb.AppendLine("PLAINTEXT:");
        foreach (var c in chunks)
        {
            if (c.PathVal == null) sb.Append(new string('?', c.Len)); else for (int q = 0; q < c.PathVal.Count; q++) { var v = c.PathVal[q]; sb.Append(v.Length == 0 ? (c.PathSym[q] == -2 ? "#" : "*") : Val(v)); }
            sb.Append(" | ");
        }
        File.WriteAllText(outPath, sb.ToString());
        key = saved; RescoreAll();
    }
    static string Opt(Dictionary<string, string> o, string k, string d) { string v; return o.TryGetValue(k, out v) ? v : d; }

    static void Main(string[] args)
    {
        string dir = args.Length > 0 ? args[0] : ".";
        var opt = new Dictionary<string, string>();
        for (int i = 1; i < args.Length; i++) { var kv = args[i].Split(new[] { '=' }, 2); opt[kv[0].TrimStart('-')] = kv.Length > 1 ? kv[1] : "1"; }
        int iters = int.Parse(Opt(opt, "iters", "300000")); int seed = int.Parse(Opt(opt, "seed", "1"));
        double T0 = double.Parse(Opt(opt, "T0", "5")), T1 = double.Parse(Opt(opt, "T1", "0.1"));
        mu = double.Parse(Opt(opt, "mu", "0.5")); lambda = double.Parse(Opt(opt, "lam", "0")); codepen = double.Parse(Opt(opt, "codepen", "20"));
        int chunkLen = int.Parse(Opt(opt, "chunk", "160")); beam = int.Parse(Opt(opt, "beam", "12")); threads = int.Parse(Opt(opt, "threads", "6")); unk = double.Parse(Opt(opt, "unk", "0"));
        wcoef = double.Parse(Opt(opt, "wcoef", "0")); wmin = int.Parse(Opt(opt, "wmin", "5")); int wtop = int.Parse(Opt(opt, "wtop", "5000"));
        if (wcoef > 0)
        {   // it_words.json: [[word,count],...] sorted by count; look in dir then parent
            string wp = File.Exists(Path.Combine(dir, "it_words.json")) ? Path.Combine(dir, "it_words.json") : Path.Combine(dir, "..", "it_words.json");
            dict = new HashSet<string>(); string js = File.ReadAllText(wp);
            var m = System.Text.RegularExpressions.Regex.Matches(js, "\\[\"([a-z_]+)\", ?(\\d+)\\]"); int k = 0;
            foreach (System.Text.RegularExpressions.Match mm in m) { if (k++ >= wtop) break; string wd = mm.Groups[1].Value; if (wd.Length >= wmin && wd.Length <= wmax) dict.Add(wd); }
            Console.WriteLine("dict words: " + dict.Count);
        }
        int maxSet = int.Parse(Opt(opt, "maxset", "3")); bool pairLetters = opt.ContainsKey("pairletters"); bool free = opt.ContainsKey("free");
        outPath = Path.Combine(dir, Opt(opt, "out", "native_result.txt")); string fixSpec = Opt(opt, "fix", "");
        rnd = new Random(seed);
        string lmFile = "lm5.bin";
        if (Opt(opt, "alpha", "") == "sp") { ALPHA = "abcdefghilmnopqrstuz_"; L = 21; CONS = "bcdfghlmnpqrstz_"; lmFile = "lm5sp.bin"; double es = expect.Sum(); for (int i = 0; i < expect.Length; i++) expect[i] /= es; }

        var bytes = File.ReadAllBytes(Path.Combine(dir, lmFile)); lm = new float[bytes.Length / 4]; Buffer.BlockCopy(bytes, 0, lm, 0, bytes.Length);

        chunks = new List<Chunk>();
        foreach (var line in File.ReadAllLines(Path.Combine(dir, "cipher.txt")))
        {
            var toks = line.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries); if (toks.Length == 0) continue;
            var d = toks.Select(t => t[0] - '0').ToArray(); var dot = toks.Select(t => t.EndsWith("^")).ToArray();
            for (int s = 0; s < d.Length; )
            {
                int len = Math.Min(chunkLen, d.Length - s);
                while (s + len < d.Length && (dot[s + len - 1] || dot[s + len - 2])) len++;   // never split a dotted code
                if (len >= 6) chunks.Add(new Chunk(d, dot, s, len));
                s += len;
            }
        }
        symChunks = new List<int>[NSYM]; for (int i = 0; i < NSYM; i++) symChunks[i] = new List<int>();
        var freq = new int[NSYM];
        for (int ci = 0; ci < chunks.Count; ci++) foreach (var ids in chunks[ci].OptId) foreach (var id in ids) { freq[id]++; if (!symChunks[id].Contains(ci)) symChunks[id].Add(ci); }
        symbols = Enumerable.Range(0, NSYM).Where(i => freq[i] > 0 && (!opt.ContainsKey("nopairs") || i < 20 || i >= 230)).ToArray();

        var SYL = new List<int[]>();
        foreach (var c in CONS) foreach (var v in VOW) SYL.Add(Str(c.ToString() + v));
        foreach (var wd in new[] { "qua", "que", "qui", "che", "chi", "gli", "non", "per", "con", "et", "ss", "nt", "st" }) SYL.Add(Str(wd));
        foreach (var wd in Opt(opt, "words", "").Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries)) SYL.Add(Str(wd));
        if (pairLetters) foreach (var ch in ALPHA) for (int k = 0; k < 3; k++) SYL.Add(Str(ch.ToString()));
        bool inject = opt.ContainsKey("inject");
        int[] sylOwner = Enumerable.Repeat(-1, SYL.Count).ToArray(); int[] symSyl = Enumerable.Repeat(-1, NSYM).ToArray();
        var freeSyl = new List<int>(Enumerable.Range(0, SYL.Count));
        Action<int, int> setSyl = delegate(int sym, int syl)
        {   // assign syllable index syl (or -1) to symbol sym, maintaining owner map
            int old = symSyl[sym]; if (old >= 0) { sylOwner[old] = -1; freeSyl.Add(old); }
            symSyl[sym] = syl; key[sym] = new List<int[]>();
            if (syl >= 0) { sylOwner[syl] = sym; freeSyl.Remove(syl); key[sym].Add(SYL[syl]); }
        };

        key = new List<int[]>[NSYM]; for (int i = 0; i < NSYM; i++) key[i] = new List<int[]>();
        // constrained single-digit assignment: vowelDigit[v] in 0..9 (each vowel exactly once); consDigit[c] in -1..9 (at most once)
        int[] vowelIdx = VOW.Select(ch => ALPHA.IndexOf(ch)).ToArray(), consIdx = CONS.Select(ch => ALPHA.IndexOf(ch)).ToArray();
        if (free) { vowelIdx = new int[0]; consIdx = Enumerable.Range(0, L).ToArray(); }
        int NV = vowelIdx.Length, NC = consIdx.Length;
        int nullDigit = int.Parse(Opt(opt, "null", "-1"));
        int[] vowAllowed = Opt(opt, "vowdig", "0123456789").Where(ch => ch - '0' != nullDigit).Select(ch => ch - '0').ToArray();
        int[] consAllowed = Opt(opt, "consdig", "0123456789").Where(ch => ch - '0' != nullDigit).Select(ch => ch - '0').ToArray();
        int[] vowelDigit = new int[NV]; int[] consDigit = new int[NC];
        { var digs = vowAllowed.OrderBy(x => rnd.Next()).ToArray(); for (int v = 0; v < NV; v++) vowelDigit[v] = digs[v % digs.Length]; }
        for (int c = 0; c < NC; c++) consDigit[c] = (free && VOW.IndexOf(ALPHA[consIdx[c]]) >= 0) || rnd.NextDouble() < 0.7 ? consAllowed[rnd.Next(consAllowed.Length)] : -1;
        Action rebuildSingles = delegate()
        {
            for (int d = 0; d < 10; d++) key[d].Clear();
            for (int v = 0; v < NV; v++) key[vowelDigit[v]].Add(new[] { vowelIdx[v] });
            for (int c = 0; c < NC; c++) if (consDigit[c] >= 0) key[consDigit[c]].Add(new[] { consIdx[c] });
        };
        rebuildSingles();
        foreach (var id in symbols)
        {
            if (id < 10 || opt.ContainsKey("noinit")) continue;
            if (rnd.NextDouble() < 0.3)
            {
                if (inject) { if (freeSyl.Count > 0) setSyl(id, freeSyl[rnd.Next(freeSyl.Count)]); }
                else key[id].Add(SYL[rnd.Next(SYL.Count)]);
            }
        }
        var fixedSyms = new HashSet<int>();
        if (nullDigit >= 0)
        {
            key[nullDigit].Clear();
            key[nullDigit].Add(ALPHA.IndexOf('_') >= 0 ? new[] { ALPHA.IndexOf('_') } : new int[0]);
            fixedSyms.Add(nullDigit);
        }
        foreach (var kv in fixSpec.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
        {
            var p = kv.Split('='); int id = -1; for (int i = 0; i < NSYM; i++) if (SymName(i) == p[0]) { id = i; break; }
            if (id < 0) continue; key[id].Clear();
            foreach (var v in p[1].Split(new[] { '/' }, StringSplitOptions.RemoveEmptyEntries)) key[id].Add(Str(v));
            fixedSyms.Add(id);
        }
        RescoreAll();
        double cur = Total(), best = cur;
        var bestKey = key.Select(l => l.ToList()).ToArray();
        Console.WriteLine(chunks.Count + " chunks, " + symbols.Length + " symbols, start " + cur.ToString("F1"));

        var sw = Stopwatch.StartNew();
        int[] singles = symbols.Where(IsSingle).ToArray(), pairs = symbols.Where(i => !IsSingle(i)).ToArray();
        double[] w = symbols.Select(i => Math.Sqrt(freq[i] + 1)).ToArray(); double wsum = w.Sum();
        var savedScore = new double[chunks.Count]; var savedSym = new List<int>[chunks.Count]; var savedVal = new List<int[]>[chunks.Count]; var savedLetters = new int[chunks.Count][];
        int logEvery = Math.Max(1, iters / 40);
        var changedIds = new List<int>(); var changedOld = new List<List<int[]>>();
        // delta of the objective after key[] has been mutated for changedIds (old values in changedOld); saves chunk states for revert
        Func<List<int>, List<List<int[]>>, HashSet<int>, double> scoreChanges = delegate(List<int> ids, List<List<int[]>> olds, HashSet<int> affected)
        {
            foreach (var id in ids) foreach (var ci in symChunks[id]) affected.Add(ci);
            double delta = -KL();
            for (int k = 0; k < ids.Count; k++) if (ids[k] >= 10) { bool wasOn = olds[k].Count > 0, isOn = key[ids[k]].Count > 0; if (wasOn != isOn) delta += isOn ? -codepen : codepen; }
            foreach (var ci in affected)
            {
                var c = chunks[ci]; savedScore[ci] = c.Score; savedSym[ci] = c.PathSym; savedVal[ci] = c.PathVal; savedLetters[ci] = (int[])c.Letters.Clone();
                for (int i = 0; i < L; i++) letters[i] -= c.Letters[i];
            }
            var list = affected.ToArray();
            if (list.Length >= 4) Parallel.For(0, list.Length, new ParallelOptions { MaxDegreeOfParallelism = threads }, k => { chunks[list[k]].Viterbi(key, lm, beam, lambda); });
            else foreach (var ci in list) chunks[ci].Viterbi(key, lm, beam, lambda);
            foreach (var ci in affected)
            {
                var c = chunks[ci]; delta += c.Score - savedScore[ci];
                for (int i = 0; i < L; i++) letters[i] += c.Letters[i];
            }
            return delta + KL();
        };
        Action<HashSet<int>> revertChunks = delegate(HashSet<int> affected)
        {
            foreach (var ci in affected)
            {
                var c = chunks[ci];
                for (int i = 0; i < L; i++) letters[i] -= c.Letters[i];
                c.Score = savedScore[ci]; c.PathSym = savedSym[ci]; c.PathVal = savedVal[ci]; c.Letters = savedLetters[ci];
                for (int i = 0; i < L; i++) letters[i] += c.Letters[i];
            }
        };
        for (int it = 0; it < iters; it++)
        {
            double T = T0 * Math.Pow(T1 / T0, (double)it / iters);
            int s; { double r0 = rnd.NextDouble() * wsum; int i = 0; for (; i < symbols.Length - 1; i++) { r0 -= w[i]; if (r0 <= 0) break; } s = symbols[i]; }
            if (fixedSyms.Contains(s)) continue;
            changedIds.Clear(); changedOld.Clear();
            double r = rnd.NextDouble(); bool skip = false;
            int[] savedVD = null, savedCD = null;
            var injSaved = new List<KeyValuePair<int, int>>();   // (sym, old syl) for inject-mode revert
            if (s < 10)
            {   // structured move on the digit alphabet
                savedVD = (int[])vowelDigit.Clone(); savedCD = (int[])consDigit.Clone();
                var touched = new HashSet<int>();
                if (r < 0.35 && NV > 0)
                {   // move a vowel to another digit (swap if occupied)
                    int v = rnd.Next(NV), d0 = vowelDigit[v], d1 = vowAllowed[rnd.Next(vowAllowed.Length)]; if (d0 == d1) skip = true;
                    else { int v2 = Array.IndexOf(vowelDigit, d1); if (v2 >= 0) vowelDigit[v2] = d0; vowelDigit[v] = d1; touched.Add(d0); touched.Add(d1); }
                }
                else if (free && r < 0.6)
                {   // swap the digits of two letters (or swap all letters of two digits)
                    if (r < 0.5)
                    {
                        int c1 = rnd.Next(NC), c2 = rnd.Next(NC); if (consDigit[c1] == consDigit[c2]) skip = true;
                        else { int t = consDigit[c1]; consDigit[c1] = consDigit[c2]; consDigit[c2] = t; if (consDigit[c1] >= 0) touched.Add(consDigit[c1]); if (consDigit[c2] >= 0) touched.Add(consDigit[c2]); }
                    }
                    else
                    {
                        int d0 = rnd.Next(10), d1 = rnd.Next(10); if (d0 == d1) skip = true;
                        else { for (int k = 0; k < NC; k++) { if (consDigit[k] == d0) consDigit[k] = d1; else if (consDigit[k] == d1) consDigit[k] = d0; } touched.Add(d0); touched.Add(d1); }
                    }
                }
                else
                {   // move a consonant: to another digit, to unused, or from unused
                    int c = rnd.Next(NC), d0 = consDigit[c];
                    bool isVow = VOW.IndexOf(ALPHA[consIdx[c]]) >= 0;
                    int d1 = (!isVow && rnd.NextDouble() < 0.2) ? -1 : consAllowed[rnd.Next(consAllowed.Length)];
                    if (d0 == d1) skip = true;
                    else
                    {
                        int cnt1 = 0; for (int k = 0; k < NC; k++) if (consDigit[k] == d1) cnt1++;
                        if (d1 >= 0 && cnt1 >= maxSet) skip = true;
                        else { consDigit[c] = d1; if (d0 >= 0) touched.Add(d0); if (d1 >= 0) touched.Add(d1); }
                    }
                }
                if (!skip)
                {
                    foreach (var d in touched) { changedIds.Add(d); changedOld.Add(key[d]); key[d] = new List<int[]>(); }
                    for (int v = 0; v < NV; v++) if (touched.Contains(vowelDigit[v])) key[vowelDigit[v]].Add(new[] { vowelIdx[v] });
                    for (int c = 0; c < NC; c++) if (consDigit[c] >= 0 && touched.Contains(consDigit[c])) key[consDigit[c]].Add(new[] { consIdx[c] });
                    if (touched.Count == 0) skip = true;
                }
            }
            else if (inject)
            {   // injective syllable assignment for dotted singles and pairs
                if (symSyl[s] < 0)
                {
                    if (freeSyl.Count == 0) skip = true;
                    else { injSaved.Add(new KeyValuePair<int, int>(s, -1)); changedIds.Add(s); changedOld.Add(key[s]); setSyl(s, freeSyl[rnd.Next(freeSyl.Count)]); }
                }
                else if (r < 0.25) { injSaved.Add(new KeyValuePair<int, int>(s, symSyl[s])); changedIds.Add(s); changedOld.Add(key[s]); setSyl(s, -1); }
                else if (r < 0.55)
                {   // swap syllables with another assigned symbol
                    int t = pairs[rnd.Next(pairs.Length)]; if (t == s || fixedSyms.Contains(t) || symSyl[t] < 0) skip = true;
                    else
                    {
                        int a = symSyl[s], b = symSyl[t];
                        injSaved.Add(new KeyValuePair<int, int>(s, a)); injSaved.Add(new KeyValuePair<int, int>(t, b));
                        changedIds.Add(s); changedOld.Add(key[s]); changedIds.Add(t); changedOld.Add(key[t]);
                        setSyl(s, -1); setSyl(t, a); setSyl(s, b);
                    }
                }
                else if (r < 0.7 && IsSingle(s))
                {   // dotted single may also be a plain letter (not in the injective pool)
                    injSaved.Add(new KeyValuePair<int, int>(s, symSyl[s])); changedIds.Add(s); changedOld.Add(key[s]); setSyl(s, -1); key[s] = new List<int[]> { Str(ALPHA[rnd.Next(L)].ToString()) };
                }
                else
                {
                    if (freeSyl.Count == 0) skip = true;
                    else { injSaved.Add(new KeyValuePair<int, int>(s, symSyl[s])); changedIds.Add(s); changedOld.Add(key[s]); setSyl(s, freeSyl[rnd.Next(freeSyl.Count)]); }
                }
            }
            else if (IsSingle(s))
            {   // dotted single: free value (letter or syllable) or unused
                if (key[s].Count == 0) { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]> { SYL[rnd.Next(SYL.Count)] }; }
                else if (r < 0.3) { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]>(); }
                else { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]> { r < 0.6 ? Str(ALPHA[rnd.Next(L)].ToString()) : SYL[rnd.Next(SYL.Count)] }; }
            }
            else
            {
                if (key[s].Count == 0) { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]> { SYL[rnd.Next(SYL.Count)] }; }
                else if (r < 0.3) { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]>(); }
                else if (r < 0.5)
                {
                    int t = pairs[rnd.Next(pairs.Length)]; if (t == s || fixedSyms.Contains(t) || key[t].Count == 0) skip = true;
                    else { changedIds.Add(t); changedOld.Add(key[t]); changedIds.Add(s); changedOld.Add(key[s]); var tv = key[t]; key[t] = key[s]; key[s] = tv; }
                }
                else { changedIds.Add(s); changedOld.Add(key[s]); key[s] = new List<int[]> { SYL[rnd.Next(SYL.Count)] }; }
            }
            if (skip) { if (savedVD != null) { vowelDigit = savedVD; consDigit = savedCD; } continue; }
            var affected = new HashSet<int>();
            double delta = scoreChanges(changedIds, changedOld, affected);
            if (delta > 0 || rnd.NextDouble() < Math.Exp(delta / T))
            {
                cur += delta;
                if (cur > best) { best = cur; for (int i = 0; i < NSYM; i++) bestKey[i] = key[i].ToList(); }
            }
            else
            {
                for (int k = 0; k < changedIds.Count; k++) key[changedIds[k]] = changedOld[k];
                if (savedVD != null) { vowelDigit = savedVD; consDigit = savedCD; }
                if (injSaved.Count > 0)
                {
                    foreach (var kv in injSaved) setSyl(kv.Key, -1);
                    foreach (var kv in injSaved) if (kv.Value >= 0) setSyl(kv.Key, kv.Value);
                    for (int k = 0; k < changedIds.Count; k++) key[changedIds[k]] = changedOld[k];
                }
                revertChunks(affected);
            }
            if (it % logEvery == 0)
            {
                Console.WriteLine("  it " + it.ToString().PadLeft(8) + " T=" + T.ToString("F2") + " cur=" + cur.ToString("F1").PadLeft(9) + " best=" + best.ToString("F1").PadLeft(9) + " " + sw.Elapsed.TotalSeconds.ToString("F0") + "s");
                Dump(bestKey, best);
            }
        }
        // ---- greedy coordinate sweeps: for each symbol try every candidate value, keep the best ----
        int sweeps = int.Parse(Opt(opt, "sweep", "0"));
        for (int sweep = 0; sweep < sweeps; sweep++)
        {
            double startCur = cur;
            foreach (var s in symbols.OrderByDescending(i => freq[i]).ToArray())
            {
                if (fixedSyms.Contains(s)) continue;
                if (s < 10)
                {   // digit: try each consonant on this digit -> elsewhere, and each consonant elsewhere -> here; each vowel swap onto this digit
                    var cands = new List<Action>();
                    for (int c = 0; c < NC; c++)
                    {
                        int cc = c;
                        if (consDigit[c] == s) { foreach (var d1 in consAllowed) { int dd = d1; if (dd != s) cands.Add(delegate() { consDigit[cc] = dd; }); } cands.Add(delegate() { consDigit[cc] = -1; }); }
                        else if (consAllowed.Contains(s)) cands.Add(delegate() { consDigit[cc] = s; });
                    }
                    for (int v = 0; v < NV; v++) { int vv = v; if (vowelDigit[v] != s && vowAllowed.Contains(s)) cands.Add(delegate() { int d0 = vowelDigit[vv]; int v2 = Array.IndexOf(vowelDigit, s); if (v2 >= 0) vowelDigit[v2] = d0; vowelDigit[vv] = s; }); }
                    foreach (var cand in cands)
                    {
                        var svVD = (int[])vowelDigit.Clone(); var svCD = (int[])consDigit.Clone();
                        cand();
                        bool ok = true; for (int d = 0; d < 10; d++) { int cnt1 = 0; for (int k = 0; k < NC; k++) if (consDigit[k] == d) cnt1++; if (cnt1 > maxSet) ok = false; }
                        if (!ok) { vowelDigit = svVD; consDigit = svCD; continue; }
                        var touched = new HashSet<int>(); for (int d = 0; d < 10; d++) if (!fixedSyms.Contains(d)) touched.Add(d);
                        changedIds.Clear(); changedOld.Clear();
                        foreach (var d in touched) { changedIds.Add(d); changedOld.Add(key[d]); key[d] = new List<int[]>(); }
                        for (int v = 0; v < NV; v++) key[vowelDigit[v]].Add(new[] { vowelIdx[v] });
                        for (int c = 0; c < NC; c++) if (consDigit[c] >= 0) key[consDigit[c]].Add(new[] { consIdx[c] });
                        var affected = new HashSet<int>(); double delta = scoreChanges(changedIds, changedOld, affected);
                        if (delta > 1e-9) { cur += delta; if (cur > best) { best = cur; for (int i = 0; i < NSYM; i++) bestKey[i] = key[i].ToList(); } }
                        else { for (int k = 0; k < changedIds.Count; k++) key[changedIds[k]] = changedOld[k]; vowelDigit = svVD; consDigit = svCD; revertChunks(affected); }
                    }
                }
                else
                {   // pair / dotted symbol: try unused and every free syllable (inject) or every syllable
                    var cands = new List<int>(); cands.Add(-1);
                    if (inject) cands.AddRange(freeSyl); else cands.AddRange(Enumerable.Range(0, SYL.Count));
                    if (IsSingle(s)) for (int c = 0; c < L; c++) cands.Add(-2 - c);   // plain letter
                    foreach (var cand in cands.ToArray())
                    {
                        int oldSyl = symSyl[s]; var oldKey = key[s];
                        if (cand == -1 && key[s].Count == 0) continue;
                        changedIds.Clear(); changedOld.Clear(); changedIds.Add(s); changedOld.Add(key[s]);
                        if (inject) { if (cand >= -1) setSyl(s, cand); else { setSyl(s, -1); key[s] = new List<int[]> { new[] { -2 - cand } }; } }
                        else { key[s] = new List<int[]>(); if (cand >= 0) key[s].Add(SYL[cand]); else if (cand < -1) key[s].Add(new[] { -2 - cand }); }
                        var affected = new HashSet<int>(); double delta = scoreChanges(changedIds, changedOld, affected);
                        if (delta > 1e-9) { cur += delta; if (cur > best) { best = cur; for (int i = 0; i < NSYM; i++) bestKey[i] = key[i].ToList(); } }
                        else
                        {
                            if (inject) { setSyl(s, -1); if (oldSyl >= 0) setSyl(s, oldSyl); }
                            key[s] = oldKey; revertChunks(affected);
                        }
                    }
                }
            }
            Console.WriteLine("  sweep " + sweep + " cur=" + cur.ToString("F1") + " best=" + best.ToString("F1") + " " + sw.Elapsed.TotalSeconds.ToString("F0") + "s");
            Dump(bestKey, best);
            if (cur - startCur < 1e-6) break;
        }
        Dump(bestKey, best);
        var txt = File.ReadAllText(outPath); Console.WriteLine(txt.Substring(0, Math.Min(3000, txt.Length)));
    }
}
