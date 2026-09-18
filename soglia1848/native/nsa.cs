using System; using System.IO; using System.Linq; using System.Collections.Generic;
class N {
  static float[] LP; static int[] seq; static int ntypes; static int[][] cand; static double lam;
  static double Score(int[] m){
    double t=0; int h=0; int n=0;
    for(int i=0;i<seq.Length;i++){
      int k=seq[i];
      if(k<0){ int idx=h*27; t+=LP[idx]; h=idx%531441; n++; continue; }
      int[] s=cand[m[k]];
      for(int j=0;j<s.Length;j++){ int idx=h*27+s[j]; t+=LP[idx]; h=idx%531441; n++; }
    }
    t+=LP[h*27];
    return t+lam*n;
  }
  static void Main(string[] a){
    // args: lm.bin seq.txt cand.txt seed iters restarts T0 T1 lam out pletter
    byte[] b=File.ReadAllBytes(a[0]); LP=new float[b.Length/4]; Buffer.BlockCopy(b,0,LP,0,b.Length);
    var lines=File.ReadAllLines(a[1]);
    ntypes=int.Parse(lines[0]); seq=lines[1].Split(' ').Select(int.Parse).ToArray();
    int[] fixedv=lines.Length>2 && lines[2].Trim().Length>0 ? lines[2].Split(' ').Select(int.Parse).ToArray() : Enumerable.Repeat(-1,ntypes).ToArray();
    var cl=File.ReadAllLines(a[2]).Where(x=>x.Length>0).ToArray();
    cand=cl.Select(x=>x.Select(ch=>ch-'a'+1).ToArray()).ToArray();
    int nletters=cl.Count(x=>x.Length==1);
    int seed=int.Parse(a[3]); long iters=long.Parse(a[4]); int R=int.Parse(a[5]);
    double T0=double.Parse(a[6]),T1=double.Parse(a[7]); lam=double.Parse(a[8]);
    double pl=double.Parse(a[10]);
    var rnd=new Random(seed); var outw=new StreamWriter(a[9]);
    for(int r=0;r<R;r++){
      int[] m=new int[ntypes];
      for(int i=0;i<ntypes;i++) m[i]= fixedv[i]>=0? fixedv[i] : rnd.Next(nletters);
      double cur=Score(m), best=cur; int[] bm=(int[])m.Clone();
      for(long it=0;it<iters;it++){
        double T=T0*Math.Pow(T1/T0,(double)it/iters);
        int k=rnd.Next(ntypes); if(fixedv[k]>=0) continue;
        int old=m[k],k2=-1,old2=0;
        double u=rnd.NextDouble();
        if(u<0.6) m[k]= rnd.NextDouble()<pl ? rnd.Next(nletters) : rnd.Next(cand.Length);
        else { k2=rnd.Next(ntypes); if(fixedv[k2]>=0) continue; old2=m[k2]; m[k]=old2; m[k2]=old; }
        double nw=Score(m);
        if(nw>=cur || rnd.NextDouble()<Math.Exp((nw-cur)/T)){ cur=nw; if(cur>best){best=cur; Array.Copy(m,bm,ntypes);} }
        else { m[k]=old; if(k2>=0) m[k2]=old2; }
      }
      outw.WriteLine(best.ToString("F2")+"\t"+string.Join(" ",bm)); outw.Flush();
    }
    outw.Close();
  }
}
