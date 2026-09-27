#!/usr/bin/env python3
"""Cuts A->B->A runs out of an ArduPilot log (.bin) into CSV, one file per run.

Run window: from the message 'Using EKF Source Set 2' to 'Using EKF Source Set 1'
(the GNSS-denied phase), with a margin of --margin seconds on both sides (default 25 s,
to capture the 20 s reference hover before and a moment after). The master .bin stays untouched.

Usage:
  python3 cut_runs.py LOG.bin --names calibration,E1-001,E1-002 --cell LUX1-SURF1-ALT3-VEL15 --date 20260912 --out analysis/data/E1
Successive SRC2 windows longer than 20 s receive successive names from --names.
Columns: t_log[s], phase (before/flow_only/after), EKF position (POS), GNSS (GPS, GPA), OF, RFND, CTUN, ATT, XKF3/XKF4/XKF5 (innovations, including flow FIX/FIY, own error estimate eVel/ePos), VIBE, RCIN ch7, mode.
v0.2 (12 Sep, evening): added GPA.HAcc/SAcc, XKF3.IVN/IVE, XKF4.TS, XKF5.FIX/FIY/AFI/HAGL/RI/eVel/ePos, VIBE.VibeX/Y/Z.
"""
import sys, csv, argparse, bisect, os
from pymavlink import mavutil
ap=argparse.ArgumentParser(); ap.add_argument('log'); ap.add_argument('--names',required=True); ap.add_argument('--cell',required=True)
ap.add_argument('--date',required=True); ap.add_argument('--out',default='.'); ap.add_argument('--margin',type=float,default=25.0); ap.add_argument('--min-window',type=float,default=20.0)
a=ap.parse_args(); names=a.names.split(',')
m=mavutil.mavlink_connection(a.log)
S={k:[] for k in ['POS','GPS','GPA','OF','RFND','CTUN','ATT','XKF3','XKF4','XKF5','VIBE','RCIN','MODE']}; MSG=[]
while True:
    x=m.recv_match(type=list(S)+['MSG'])
    if x is None: break
    k=x.get_type(); t=x.TimeUS/1e6
    if k=='MSG': MSG.append((t,x.Message)); continue
    if k=='GPS' and getattr(x,'I',0)!=0: continue
    if k in ('XKF3','XKF4','XKF5') and getattr(x,'C',0)!=0: continue
    if k=='GPA' and getattr(x,'I',0)!=0: continue
    if k=='VIBE' and getattr(x,'IMU',0)!=0: continue
    S[k].append((t,x))
src=[(t,2 if 'Set 2' in s else 1) for t,s in MSG if 'EKF Source Set' in s]
win=[]; cur=None
for t,v in src:
    if v==2 and cur is None: cur=t
    elif v==1 and cur is not None:
        if t-cur>=a.min_window: win.append((cur,t))
        cur=None
if len(win)!=len(names): sys.exit(f"{len(win)} windows, {len(names)} names: check the input")
ts={k:[t for t,_ in v] for k,v in S.items()}
def near(k,t):
    i=bisect.bisect_left(ts[k],t); i=min(max(i-1,0),len(S[k])-1); return S[k][i][1] if S[k] else None
os.makedirs(a.out,exist_ok=True)
for (t0,t1),name in zip(win,names):
    tag=name if name.startswith('E1') else 'KAL'
    fn=os.path.join(a.out,f"ARIADNE_{tag.replace('E1-','E1_')}_{a.date}_{a.cell}.csv") if tag!='KAL' else os.path.join(a.out,f"ARIADNE_KAL_{a.date}_{os.path.basename(a.log).split('_')[1]}.csv")
    rows=[]
    for t,p in S['POS']:
        if t0-a.margin<=t<=t1+a.margin:
            g=near('GPS',t); o=near('OF',t); r=near('RFND',t); c=near('CTUN',t); at=near('ATT',t); k4=near('XKF4',t); k3=near('XKF3',t); k5=near('XKF5',t); ga=near('GPA',t); vb=near('VIBE',t); rc=near('RCIN',t); md=near('MODE',t)
            phase='before' if t<t0 else ('flow_only' if t<=t1 else 'after')
            rows.append([round(t,3),phase,round(t-t0,3),p.Lat,p.Lng,round(p.Alt,3),
                g.Lat,g.Lng,g.NSats,g.HDop,round(g.Spd,3),
                o.Qual,round(o.flowX,4),round(o.flowY,4),round(o.bodyX,4),round(o.bodyY,4),
                round(r.Dist,3),round(c.Alt,3),round(at.Roll,2),round(at.Pitch,2),round(at.Yaw,2),
                round(k4.SV,3),round(k4.SP,3),round(k4.SH,3),round(k4.SM,3),k4.SS if hasattr(k4,'SS') else '',
                getattr(rc,'C7',''),md.Mode,
                round(ga.HAcc,2),round(ga.SAcc,2),round(k3.IVN,3),round(k3.IVE,3),k4.TS if hasattr(k4,'TS') else '',
                k5.FIX,k5.FIY,k5.AFI,round(k5.HAGL,2),round(k5.RI,3),round(k5.eVel,4),round(k5.ePos,4),
                round(vb.VibeX,2),round(vb.VibeY,2),round(vb.VibeZ,2)])
    with open(fn,'w',newline='') as f:
        w=csv.writer(f); w.writerow(['t_log_s','phase','t_since_src2_s','ekf_lat','ekf_lon','ekf_alt','gps_lat','gps_lon','gps_nsats','gps_hdop','gps_spd','of_qual','of_flowX','of_flowY','of_bodyX','of_bodyY','rfnd_dist','ctun_alt','roll','pitch','yaw','xkf4_SV','xkf4_SP','xkf4_SH','xkf4_SM','xkf4_SS','rc7','mode','gpa_hacc','gpa_sacc','xkf3_IVN','xkf3_IVE','xkf4_TS','xkf5_FIX','xkf5_FIY','xkf5_AFI','xkf5_HAGL','xkf5_RI','xkf5_eVel','xkf5_ePos','vibe_x','vibe_y','vibe_z']); w.writerows(rows)
    print(f"{name}: window {t0:.1f}-{t1:.1f} s, {len(rows)} rows -> {fn}")
