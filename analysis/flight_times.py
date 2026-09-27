import sys, os, datetime
from pymavlink import mavutil
# GPS: GWk = GPS week, GMS = ms within the week. GPS epoch 1980-01-06, 18 leap seconds (since 2017)
GPS_EPOCH = datetime.datetime(1980,1,6, tzinfo=datetime.timezone.utc)
LEAP = 18
TZ = datetime.timezone(datetime.timedelta(hours=2))  # Europe/Warsaw, CEST

def utc(gwk, gms):
    return GPS_EPOCH + datetime.timedelta(weeks=gwk, milliseconds=gms) - datetime.timedelta(seconds=LEAP)

for path in sys.argv[1:]:
    m = mavutil.mavlink_connection(path)
    anchor = None      # (TimeUS_s, datetime)
    arms, disarms = [], []
    while True:
        try: msg = m.recv_match(blocking=False)
        except Exception: continue
        if msg is None: break
        t = getattr(msg,'TimeUS',None)
        if t is None: continue
        ts = t/1e6; ty = msg.get_type()
        if ty=='GPS' and anchor is None:
            gwk = getattr(msg,'GWk',0); gms = getattr(msg,'GMS',0)
            if gwk and gwk > 2000:
                anchor = (ts, utc(gwk,gms))
        elif ty=='EV' and msg.Id==10: arms.append(ts)
        elif ty=='EV' and msg.Id==11: disarms.append(ts)
    print(f"### {os.path.basename(path)}")
    if anchor is None:
        print("   no GPS time in the log\n"); continue
    t_ref, dt_ref = anchor
    def wall(ts): return (dt_ref + datetime.timedelta(seconds=ts-t_ref)).astimezone(TZ)
    print(f"   file name suggests: {os.path.basename(path).split('_',2)[2].replace('.bin','')}")
    for i,a in enumerate(arms,1):
        b = next((x for x in disarms if x>a), None)
        if b is None: continue
        print(f"   flight {i}: {wall(a).strftime('%H:%M:%S')} -> {wall(b).strftime('%H:%M:%S')}  ({b-a:.0f} s)")
    print(f"   session (whole record): {wall(min(arms) if arms else t_ref).strftime('%H:%M')} ... {wall(max(disarms) if disarms else t_ref).strftime('%H:%M')}\n")
