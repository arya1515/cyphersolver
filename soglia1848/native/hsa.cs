using System; using System.IO; using System.Linq; using System.Collections.Generic;
class H {
  static float[] LP;
  static int[] seq; static int ntypes;
  static double Score(int[] m){
    double t=0; int h=0; // h = last 4 chars packed base 27
    for(int i=0;i<seq.Length;i++){
      int k=seq[i]; int c= k<0?0:m[k]; if(c<0) continue;
      int idx=h*27+c; t+=LP[idx]; h=idx%531441;
    }
    t+=LP[h*27];
    return t;
  }
  static void Main(string[] a){
    // args: lm.bin seq.txt seed iters restarts T0 T1 out allowed
    byte[] b=File.ReadAllBytes(a[0]); LP=new float[b.Length/4]; Buffer.BlockCopy(b,0,LP,0,b.Length);
    var lines=File.ReadAllLines(a[1]);
    ntypes=int.Parse(lines[0]); seq=lines[1].Split(' ').Select(int.Parse).ToArray();
    int[] fixedv=lines.Length>2 && lines[2].Length>0 ? lines[2].Split(' ').Select(int.Parse).ToArray() : Enumerable.Repeat(0,ntypes).ToArray();
    int seed=int.Parse(a[2]); long iters=long.Parse(a[3]); int R=int.Parse(a[4]);
    double T0=double.Parse(a[5]),T1=double.Parse(a[6]);
    string allowedS=a.Length>8?a[8]:"abcdefghilmnopqrstuvz";
    int[] allowed=allowedS.Select(ch=>ch-'a'+1).ToArray();
    var rnd=new Random(seed);
    var outw=new StreamWriter(a[7]);
    double gbest=-1e18;
    for(int r=0;r<R;r++){
      int[] m=new int[ntypes];
      for(int i=0;i<ntypes;i++) m[i]= fixedv[i]!=0? fixedv[i] : allowed[rnd.Next(allowed.Length)];
      double cur=Score(m), best=cur; int[] bm=(int[])m.Clone();
      for(long it=0;it<iters;it++){
        double T=T0*Math.Pow(T1/T0,(double)it/iters);
        int k=rnd.Next(ntypes); if(fixedv[k]!=0) continue;
        int old=m[k],k2=-1,old2=0;
        if(rnd.NextDouble()<0.8) m[k]=allowed[rnd.Next(allowed.Length)];
        else { k2=rnd.Next(ntypes); if(fixedv[k2]!=0) continue; old2=m[k2]; m[k]=old2; m[k2]=old; }
        double nw=Score(m);
        if(nw>=cur || rnd.NextDouble()<Math.Exp((nw-cur)/T)){ cur=nw; if(cur>best){best=cur; Array.Copy(m,bm,ntypes);} }
        else { m[k]=old; if(k2>=0) m[k2]=old2; }
      }
      outw.WriteLine(best.ToString("F2")+"\t"+string.Join(" ",bm)); outw.Flush();
      if(best>gbest) gbest=best;
    }
    outw.Close();
  }
}
