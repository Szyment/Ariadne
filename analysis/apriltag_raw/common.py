import numpy as np, cv2, csv, datetime
FX, CX, CY, K1 = 1258.0, 648.0, 486.0, -0.2986
KM = np.array([[FX, 0, CX], [0, FX, CY], [0, 0, 1.]]); DM = np.array([K1, 0, 0, 0, 0])
def unix(hms): return datetime.datetime(2026, 11, 1, *hms, tzinfo=datetime.timezone(datetime.timedelta(hours=1))).timestamp()
SESS = {'s065': ('s065.csv', unix((12, 16, 29)), 'log63', 12.5), 's066': ('s066.csv', unix((12, 52, 21)), 'log64', 3.15)}
def ne(lat, lon, lat0=50.9186533, lon0=19.0812728):
    R = 6371008.8
    return np.radians(lat - lat0) * R, np.radians(lon - lon0) * R * np.cos(np.radians(lat0))
def load(name):
    csvp, t0, lg, dt = SESS[name]
    R = list(csv.DictReader(open(csvp)))
    fr = np.array([int(r['frame']) for r in R]); ids = np.array([int(r['id']) for r in R])
    C = np.array([[float(r[f'{k}{i}']) for i in range(4) for k in 'xy'] for r in R]).reshape(-1, 4, 2)
    U = cv2.undistortPoints(C.reshape(-1, 1, 2), KM, DM).reshape(-1, 4, 2)   # normalised, undistorted
    L = np.load(lg + '.npz'); off = float(L['off'])
    t = t0 + fr / 30.0 + dt
    g = lambda arr, col: np.interp(t, arr[:, 0] + off, arr[:, col])
    rf = L['RFND']; A = L['ATT']; P = L['POS']
    # yaw unwrap before interpolation
    yaw = np.degrees(np.unwrap(np.radians(A[:, 3]))); Ay = A.copy(); Ay[:, 3] = yaw
    d = dict(t=t, fr=fr, id=ids, C=C, U=U, uc=U.mean(1), h=g(rf, 1), roll=g(A, 1), pitch=g(A, 2), yaw=g(Ay, 3) % 360)
    n, e = ne(P[:, 1], P[:, 2]); Pn = np.c_[P[:, 0], n, e]
    d['N'] = g(Pn, 1); d['E'] = g(Pn, 2)
    G = L['GPS']; d['spd'] = g(G, 4); d['crs'] = g(G, 5)
    d['mode'] = np.interp(t, L['MODE'][:, 0] + off, L['MODE'][:, 1], left=np.nan)  # approximate (step)
    return d
