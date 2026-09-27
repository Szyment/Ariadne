import sys, math
from pymavlink import mavutil
def dist(a,b):
    dy=(b[0]-a[0])*111320; dx=(b[1]-a[1])*111320*math.cos(math.radians(a[0])); return math.hypot(dx,dy)
def run(path):
    m=mavutil.mavlink_connection(path)
    POS=[];GPS=[];MSG=[];MODE=[];OF=[];RFND=[];CTUN=[];EV=[];XKF4=[]
    while True:
        x=m.recv_match(type=['POS','GPS','MSG','MODE','OF','RFND','CTUN','EV','XKF4'])
        if x is None: break
        t=x.TimeUS/1e6; k=x.get_type()
        if k=='POS': POS.append((t,x.Lat,x.Lng,x.Alt))
        elif k=='GPS' and getattr(x,'I',0)==0: GPS.append((t,x.Lat,x.Lng,x.NSats,x.HDop,x.Spd))
        elif k=='MSG': MSG.append((t,x.Message))
        elif k=='MODE': MODE.append((t,x.Mode))
        elif k=='OF': OF.append((t,x.Qual))
        elif k=='RFND': RFND.append((t,x.Dist))
        elif k=='CTUN': CTUN.append((t,x.Alt))
        elif k=='EV': EV.append((t,x.Id))
        elif k=='XKF4' and getattr(x,'C',0)==0: XKF4.append((t,x.SS if hasattr(x,'SS') else 0))
    src=[(t,2 if 'Set 2' in s else 1) for t,s in MSG if 'EKF Source Set' in s]
    win=[]; cur=None
    for t,s in src:
        if s==2 and cur is None: cur=t
        elif s==1 and cur is not None: win.append((cur,t)); cur=None
    print(f"### {path.split('/')[-1]}")
    def near(arr,t):
        import bisect
        ts=[a[0] for a in arr]; i=bisect.bisect_left(ts,t); i=min(max(i,0),len(arr)-1); return arr[i]
    for (t0,t1) in win:
        if t1-t0<20: print(f"SRC2 window {t0:.1f}-{t1:.1f} s ({t1-t0:.0f} s): too short, skipped"); continue
        P=[p for p in POS if t0<=p[0]<=t1]; G=[g for g in GPS if t0<=g[0]<=t1]
        # start = position at the beginning of the window
        p0=P[0]; g0=G[0]
        # turn point = maximum distance from the start according to GNSS
        dg=[dist((g0[1],g0[2]),(g[1],g[2])) for g in G]; iturn=max(range(len(G)),key=lambda i:dg[i]); tturn=G[iturn][0]
        def plen(arr,ta,tb):
            s=0; prev=None
            for a in arr:
                if ta<=a[0]<=tb:
                    if prev: s+=dist((prev[1],prev[2]),(a[1],a[2]))
                    prev=a
            return s
        Lg_out=plen(G,t0,tturn); Lg_back=plen(G,tturn,t1); Lp_out=plen(P,t0,tturn); Lp_back=plen(P,tturn,t1)
        def drift_at(dt):
            tt=t0+dt
            if tt>t1: return None
            p=near(P,tt); g=near(G,tt); return dist((p[1],p[2]),(g[1],g[2]))
        d15,d30,d60=drift_at(15),drift_at(30),drift_at(60); pend=near(P,t1); gend=near(G,t1); dend=dist((pend[1],pend[2]),(gend[1],gend[2]))
        q=[o[1] for o in OF if t0<=o[0]<=t1]; r=[x[1] for x in RFND if t0<=x[0]<=t1]
        sats=[g[3] for g in G]; hd=[g[4] for g in G]
        print(f"SRC2 window {t0:.1f}-{t1:.1f} s ({t1-t0:.0f} s); GNSS turn {tturn-t0:.0f} s after the switch, max distance {max(dg):.1f} m")
        print(f"   GNSS path outbound {Lg_out:.1f} m / return {Lg_back:.1f} m; estimator outbound {Lp_out:.1f} / return {Lp_back:.1f}")
        ro=Lp_out/Lg_out if Lg_out else float('nan'); rb=Lp_back/Lg_back if Lg_back else float('nan')
        print(f"   path ratio: outbound {ro:.3f}, return {rb:.3f}, total {(Lp_out+Lp_back)/(Lg_out+Lg_back):.3f}")
        print(f"   estimator drift vs GNSS: 15 s {d15 and f'{d15:.2f}'} m, 30 s {d30 and f'{d30:.2f}'} m, 60 s {d60 and f'{d60:.2f}'} m, end {dend:.2f} m")
        if q: print(f"   OF.Qual min/med {min(q)}/{sorted(q)[len(q)//2]}; RFND med {sorted(r)[len(r)//2]:.2f} max {max(r):.2f} m; sat {min(sats)}-{max(sats)}, HDOP {min(hd):.2f}-{max(hd):.2f}")
    # CTUN.Alt at disarming
    for t,i in EV:
        if i==11:
            c=near(CTUN,t); r=near(RFND,t); print(f"disarm {t:.0f} s: CTUN.Alt {c[1]:.2f} m, RFND {r[1]:.2f} m -> reference drift {c[1]-r[1]:+.2f} m")
    print("modes:", ' -> '.join(f"{t:.0f}s:{md}" for t,md in MODE))
for p in sys.argv[1:]: run(p)
