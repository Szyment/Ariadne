import sys, numpy as np, datetime
from pymavlink import mavutil
f, out = sys.argv[1], sys.argv[2]
m = mavutil.mavlink_connection(f)
D = {k: [] for k in ['RFND', 'ATT', 'POS', 'GPS', 'MODE', 'XKF1']}
off = None
def gps_unix(wk, ms): return (datetime.datetime(1980,1,6,tzinfo=datetime.timezone.utc) + datetime.timedelta(weeks=wk, milliseconds=ms) - datetime.timedelta(seconds=18)).timestamp()
while True:
    r = m.recv_match(type=list(D), blocking=False)
    if r is None: break
    t = r.TimeUS / 1e6; tp = r.get_type()
    if tp == 'GPS':
        if r.Status >= 3 and r.GWk > 0:
            if off is None: off = gps_unix(r.GWk, r.GMS) - t
            D['GPS'].append((t, r.Lat, r.Lng, r.Alt, r.Spd, r.GCrs, r.NSats, r.HDop))
    elif tp == 'RFND': D['RFND'].append((t, r.Dist, getattr(r, 'Stat', 0)))
    elif tp == 'ATT': D['ATT'].append((t, r.Roll, r.Pitch, r.Yaw))
    elif tp == 'POS': D['POS'].append((t, r.Lat, r.Lng, r.Alt))
    elif tp == 'MODE': D['MODE'].append((t, r.ModeNum))
    elif tp == 'XKF1' and r.C == 0: D['XKF1'].append((t, r.PN, r.PE, r.PD, r.VN, r.VE, r.Yaw))
np.savez(out, off=off, **{k: np.array(v, float) for k, v in D.items()})
print(f.split('/')[-1], 'unix offset', off, {k: len(v) for k, v in D.items()})
