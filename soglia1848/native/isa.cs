using System; using System.IO; using System.Linq; using System.Collections.Generic;
class I { static bool inj=true; static int[] owner;
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
      owner=new int[cand.Length]; for(int i=0;i<owner.Length;i++) owner[i]=-1;
      for(int i=0;i<ntypes;i++) if(fixedv[i]>=0){ m[i]=fixedv[i]; owner[m[i]]=i; }
      for(int i=0;i<ntypes;i++) if(fixedv[i]<0){ int c; do{ c=rnd.Next(cand.Length);}while(owner[c]>=0); m[i]=c; owner[c]=i; }
      double cur=Score(m), best=cur; int[] bm=(int[])m.Clone();
      for(long it=0;it<iters;it++){
        double T=T0*Math.Pow(T1/T0,(double)it/iters);
        int k=rnd.Next(ntypes); if(fixedv[k]>=0) continue;
        int old=m[k],k2=-1,old2=0;
        double u=rnd.NextDouble();
        if(u<0.6){ int c= rnd.NextDouble()<pl ? rnd.Next(nletters) : rnd.Next(cand.Length);
          if(c==old) continue;
          int o=owner[c];
          if(o>=0){ if(fixedv[o]>=0) continue; k2=o; old2=m[o]; m[o]=old; owner[old]=o; } else owner[old]=-1;
          m[k]=c; owner[c]=k; }
        else { k2=rnd.Next(ntypes); if(k2==k||fixedv[k2]>=0) continue; old2=m[k2]; m[k]=old2; m[k2]=old; owner[old2]=k; owner[old]=k2; }
        double nw=Score(m);
        if(nw>=cur || rnd.NextDouble()<Math.Exp((nw-cur)/T)){ cur=nw; if(cur>best){best=cur; Array.Copy(m,bm,ntypes);} }
        else { owner[m[k]]=-1; if(k2>=0) owner[m[k2]]=-1; m[k]=old; owner[old]=k; if(k2>=0){ m[k2]=old2; owner[old2]=k2; } }
      }
      outw.WriteLine(best.ToString("F2")+"\t"+string.Join(" ",bm)); outw.Flush();
    }
    outw.Close();
  }
}
