#!/usr/bin/env python3
"""
Atmospheric conditions of a session, from the flight log and from one weather archive.

The script reads an ArduPilot log (.bin), takes from it the coordinates and
the absolute GPS time, fetches for that place and time the data from the ERA5
reanalysis (Open-Meteo Archive API), computes the air density and prints a
ready block in the session-card format.

People supply only the two values that are not in the log and that a weather
model cannot measure over the field: the wind speed from the GM816 anemometer
and the illuminance from the GM1010 lux meter.

    python3 session_weather.py log_8_2026-8-21-19-56-38.bin \
        --wind "1-2 m/s" --lux "58 lx at start -> 21 lx at end" \
        --card ../../sessions/session-cards/S-05_2026-08-21_filter-verification.md --append

Requires: pymavlink. The rest is the standard library.

--- Why ERA5 ------------------------------------------------------------------

The condition set by the project is: one source for all sessions, including
those already flown. ERA5 is the ECMWF reanalysis: the same model and the same
assimilation procedure for every date since 1940, so an August session and a
November session are comparable. A "live" weather service does not give this,
because it changes model and resolution over time.

The price of this choice: ERA5 enters the archive with a delay of about five
days. The script will not build a block for a session flown yesterday and says
so explicitly. It does not substitute data from another source, because that
would destroy comparability.

--- What the script does NOT take from the log ------------------------------

Temperature. The fields BARO.Temp and BARO.GndTemp are the temperature inside
the controller housing, not the air: in the log of 18 August BARO.Temp is
39.3 degC at an air temperature of the order of 20 degC. The barometer heats
itself and measures its own board. The ERA5 temperature enters the air density,
and eventually the reading from the GM816 anemometer, which has its own sensor.

Pressure, however, is taken from the aircraft (BARO.Press), because it is a
measurement made at the same place and time as the flight. ERA5 serves here as
a check: a discrepancy greater than 2 hPa means that something is wrong with
one or the other.
"""
import argparse
import datetime
import json
import math
import os
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

from pymavlink import mavutil

# --- constants --------------------------------------------------------------

GPS_EPOCH = datetime.datetime(1980, 1, 6, tzinfo=datetime.timezone.utc)
LEAP_SECONDS = 18                 # as of 2026; GPS-UTC


def polish_zone():
    """Civil time in Poland. Autumn sessions fall after the clock change,
    so the hours must not be converted with a fixed +2 offset."""
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo('Europe/Warsaw')
    except Exception:
        return None


def local(moment_utc):
    zone = polish_zone()
    if zone is not None:
        return moment_utc.astimezone(zone)
    # fallback: EU rule, last Sunday of March and October, 01:00 UTC
    year = moment_utc.year

    def last_sunday(month):
        d = datetime.datetime(year, month, 31, 1, tzinfo=datetime.timezone.utc)
        while d.month != month:
            d -= datetime.timedelta(days=1)
        return d - datetime.timedelta(days=(d.weekday() + 1) % 7)

    summer = last_sunday(3) <= moment_utc < last_sunday(10)
    return moment_utc.astimezone(
        datetime.timezone(datetime.timedelta(hours=2 if summer else 1)))

EV_ARM, EV_DISARM = 10, 11

R_DRY = 287.058        # gas constant of dry air [J/(kg*K)]
R_VAPOUR = 461.495     # gas constant of water vapour [J/(kg*K)]
DENSITY_ISA = 1.225    # 15 degC, 1013.25 hPa, dry air [kg/m3]

ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive'
VARIABLES = ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
             'surface_pressure', 'pressure_msl', 'cloud_cover', 'precipitation',
             'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m',
             'shortwave_radiation']
ERA5_DELAY = 5         # days; declared by the provider

SECTION_HEADING = '## Atmospheric conditions'
SECTION_HEADING_PL = '## Warunki atmosferyczne'   # heading used in cards before 20 Sep 2026


# --- helpers ----------------------------------------------------------------

def fmt(x, places=1):
    """Number with a decimal point, or a dash when there is no value."""
    if x is None:
        return 'n/a'
    return f'{x:.{places}f}'


def utc_time(gwk, gms):
    """GPS week and milliseconds to UTC time."""
    return (GPS_EPOCH + datetime.timedelta(weeks=gwk, milliseconds=gms)
            - datetime.timedelta(seconds=LEAP_SECONDS))


def vapour_pressure(temp_c, humidity_pct):
    """Partial pressure of water vapour [Pa]. Buck's formula over water."""
    if temp_c is None or humidity_pct is None:
        return None
    saturation = 611.21 * math.exp((18.678 - temp_c / 234.5)
                                   * (temp_c / (257.14 + temp_c)))
    return saturation * humidity_pct / 100.0


def air_density(pressure_pa, temp_c, humidity_pct):
    """Density of moist air [kg/m3], Dalton's law."""
    if pressure_pa is None or temp_c is None:
        return None
    kelvin = temp_c + 273.15
    vapour = vapour_pressure(temp_c, humidity_pct) or 0.0
    dry = pressure_pa - vapour
    return dry / (R_DRY * kelvin) + vapour / (R_VAPOUR * kelvin)


def compass_point(degrees):
    if degrees is None:
        return None
    rose = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return rose[int((degrees % 360) / 22.5 + 0.5) % 16]


# --- log --------------------------------------------------------------------

def read_log(path):
    """Extracts from the log the session window, the position and the onboard pressure."""
    m = mavutil.mavlink_connection(path)
    events, gps, baro = [], [], {}
    t_first = t_last = None

    while True:
        try:
            msg = m.recv_match(blocking=False)
        except Exception:
            continue
        if msg is None:
            break
        t = getattr(msg, 'TimeUS', None)
        if t is None:
            continue
        ts, typ = t / 1e6, msg.get_type()
        if t_first is None:
            t_first = ts
        t_last = ts

        if typ == 'EV' and msg.Id in (EV_ARM, EV_DISARM):
            events.append((ts, msg.Id))
        elif typ == 'GPS' and getattr(msg, 'Status', 0) >= 3:
            gps.append((ts, msg.Lat, msg.Lng, msg.Alt, msg.GWk, msg.GMS))
        elif typ == 'BARO':
            i = getattr(msg, 'I', 0)
            baro.setdefault(i, []).append((ts, msg.Press))

    if not gps:
        raise SystemExit('The log contains no GPS position with a 3D fix. '
                         'Without coordinates and absolute time the script '
                         'has nothing to look up in the archive.')

    arms = [t for t, i in events if i == EV_ARM]
    disarms = [t for t, i in events if i == EV_DISARM]
    if arms and disarms and max(disarms) > min(arms):
        start_log, end_log = min(arms), max(disarms)
        window_source = f'{len(arms)} armings in the log'
    else:
        start_log, end_log = t_first, t_last
        window_source = 'no arming events, the whole record was taken'

    # absolute time: the GPS sample nearest to the start and end of the window
    def absolute(ts_log):
        p = min(gps, key=lambda g: abs(g[0] - ts_log))
        return utc_time(p[4], p[5]) + datetime.timedelta(seconds=ts_log - p[0])

    in_window = [g for g in gps if start_log <= g[0] <= end_log] or gps

    pressures = []
    for i in sorted(baro):
        samples = [p for ts, p in baro[i] if start_log <= ts <= end_log]
        if samples:
            pressures.append((i, statistics.median(samples), len(samples)))

    return {
        'file': os.path.basename(path),
        'lat': statistics.median([g[1] for g in in_window]),
        'lon': statistics.median([g[2] for g in in_window]),
        'alt_gnss': statistics.median([g[3] for g in in_window]),
        'start': absolute(start_log),
        'end': absolute(end_log),
        'start_log': start_log,
        'end_log': end_log,
        'window_source': window_source,
        'pressures': pressures,
        'satellites': None,
    }


# --- weather archive --------------------------------------------------------

def fetch_era5(lat, lon, day):
    """One query to the archive. Returns (data, url)."""
    since = day - datetime.timedelta(days=1)   # the day before, for the precipitation sum
    query = {
        'latitude': f'{lat:.4f}',
        'longitude': f'{lon:.4f}',
        'start_date': since.isoformat(),
        'end_date': day.isoformat(),
        'hourly': ','.join(VARIABLES),
        'wind_speed_unit': 'ms',
        'timezone': 'UTC',
        'models': 'era5',
    }
    url = ARCHIVE + '?' + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={'User-Agent': 'Ariadne/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8')), url
    except urllib.error.HTTPError as e:
        raise SystemExit(f'The archive answered with error {e.code}: {e.reason}\n'
                         f'URL: {url}')
    except urllib.error.URLError as e:
        raise SystemExit(f'No connection to the archive: {e.reason}')


def values_at(data, moment_utc, hours_back=6):
    """Linear interpolation between full hours + precipitation sum backwards."""
    hours = data['hourly']['time']
    stamps = [datetime.datetime.fromisoformat(t).replace(
        tzinfo=datetime.timezone.utc) for t in hours]

    if moment_utc < stamps[0] or moment_utc > stamps[-1]:
        return None, None

    i = max(j for j, t in enumerate(stamps) if t <= moment_utc)
    j = min(i + 1, len(stamps) - 1)
    span = (stamps[j] - stamps[i]).total_seconds() or 1
    weight = (moment_utc - stamps[i]).total_seconds() / span

    result = {}
    for name in VARIABLES:
        series = data['hourly'].get(name) or []
        if len(series) <= j:
            result[name] = None
            continue
        a, b = series[i], series[j]
        if a is None:
            result[name] = None
        elif b is None or name == 'precipitation':
            result[name] = a
        elif name == 'wind_direction_10m':
            # angles are averaged as vectors, otherwise 350 and 10 deg give 180
            x = (1 - weight) * math.cos(math.radians(a)) + weight * math.cos(math.radians(b))
            y = (1 - weight) * math.sin(math.radians(a)) + weight * math.sin(math.radians(b))
            result[name] = math.degrees(math.atan2(y, x)) % 360
        else:
            result[name] = a + (b - a) * weight

    precip = data['hourly'].get('precipitation') or []
    window = [precip[k] for k in range(max(0, i - hours_back + 1), i + 1)
              if k < len(precip) and precip[k] is not None]
    result['precip_back'] = sum(window) if window else None
    result['hours_back'] = hours_back
    return result, stamps[i]


# --- block for the card -----------------------------------------------------

def distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance [km], haversine formula."""
    R = 6371.0
    f1, f2 = math.radians(lat1), math.radians(lat2)
    df, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def build_block(log, weather, data, url, wind_reading, lux_reading, grid_hour):
    start = local(log['start'])
    end = local(log['end'])
    duration = (log['end'] - log['start']).total_seconds() / 60

    temp = weather.get('temperature_2m')
    hum = weather.get('relative_humidity_2m')

    # the leading barometer is instance 0, the one ArduPilot uses by default;
    # the others are shown alongside, because the discrepancy between them is information too
    pressure_onboard = next((p for i, p, _ in log['pressures'] if i == 0), None)
    if pressure_onboard is None and log['pressures']:
        pressure_onboard = log['pressures'][0][1]
    pressure_era5 = weather.get('surface_pressure')
    pressure_era5_pa = pressure_era5 * 100 if pressure_era5 is not None else None

    density = air_density(pressure_onboard or pressure_era5_pa, temp, hum)
    deviation = (density / DENSITY_ISA - 1) * 100 if density else None

    discrepancy = None
    if pressure_onboard is not None and pressure_era5 is not None:
        discrepancy = pressure_onboard / 100 - pressure_era5

    direction = weather.get('wind_direction_10m')
    W = []
    W.append(SECTION_HEADING)
    W.append('')
    W.append(f'*Generated by the script `analysis/scripts/session_weather.py` '
             f'from the log `{log["file"]}`.*')
    W.append('')
    W.append('| | |')
    W.append('|---|---|')
    W.append(f'| Session window (local time) | {start:%Y-%m-%d %H:%M:%S} -> '
             f'{end:%H:%M:%S} ({fmt(duration)} min) |')
    W.append(f'| Flying site (median GNSS position from the log) | '
             f'{fmt(log["lat"], 6)} N / {fmt(log["lon"], 6)} E |')
    grid_lat, grid_lon = data.get('latitude'), data.get('longitude')
    if grid_lat is not None and grid_lon is not None:
        d = distance_km(log['lat'], log['lon'], grid_lat, grid_lon)
        W.append(f'| ERA5 grid point | {fmt(grid_lat, 4)} N / '
                 f'{fmt(grid_lon, 4)} E, {fmt(data.get("elevation"), 0)} m a.s.l., '
                 f'{fmt(d)} km from the flying site |')
    W.append('')
    W.append('**Measured on site**')
    W.append('')
    W.append('| | |')
    W.append('|---|---|')
    W.append(f'| Wind (GM816 anemometer) | **{wind_reading}** |')
    W.append(f'| Illuminance (GM1010 lux meter) | **{lux_reading}** |')
    if pressure_onboard is not None:
        instances = ', '.join(f'BARO{i}: {fmt(p/100, 2)} hPa ({n} samples)'
                              for i, p, n in log['pressures'])
        W.append(f'| Pressure, onboard barometer BARO0 (median over the flight window) | '
                 f'**{fmt(pressure_onboard/100, 2)} hPa** |')
        W.append(f'| All barometers | {instances} |')
    W.append('')
    W.append('**From the ERA5 reanalysis**')
    W.append('')
    W.append('| | |')
    W.append('|---|---|')
    W.append(f'| Air temperature (2 m) | {fmt(temp)} °C |')
    W.append(f'| Dew point | {fmt(weather.get("dew_point_2m"))} °C |')
    W.append(f'| Relative humidity | {fmt(hum, 0)} % |')
    W.append(f'| Cloud cover | {fmt(weather.get("cloud_cover"), 0)} % |')
    W.append(f'| Shortwave radiation | '
             f'{fmt(weather.get("shortwave_radiation"), 0)} W/m² |')
    W.append(f'| Precipitation in the session hour | {fmt(weather.get("precipitation"), 1)} mm |')
    W.append(f'| Precipitation in the preceding {weather.get("hours_back")} h | '
             f'{fmt(weather.get("precip_back"), 1)} mm |')
    W.append(f'| Modelled wind at 10 m | {fmt(weather.get("wind_speed_10m"))} m/s, '
             f'gusts {fmt(weather.get("wind_gusts_10m"))} m/s |')
    W.append(f'| Wind direction | {fmt(direction, 0)}° ({compass_point(direction)}) |')
    W.append(f'| Surface pressure | {fmt(pressure_era5, 2)} hPa |')
    W.append(f'| Pressure reduced to sea level | '
             f'{fmt(weather.get("pressure_msl"), 2)} hPa |')
    if discrepancy is not None:
        W.append(f'| Discrepancy: onboard barometer minus ERA5 | {fmt(discrepancy, 2)} hPa |')
    W.append('')
    W.append('**Air density**')
    W.append('')
    W.append('| | |')
    W.append('|---|---|')
    W.append(f'| Density in session conditions | **{fmt(density, 3)} kg/m³** |')
    W.append(f'| ISA reference (15 °C, 1013.25 hPa) | {fmt(DENSITY_ISA, 3)} kg/m³ |')
    W.append(f'| Deviation from ISA | {fmt(deviation)} % |')
    W.append('')
    W.append(f'Computed from the '
             f'{"onboard" if pressure_onboard is not None else "ERA5"} pressure, '
             f'the ERA5 temperature and humidity, with the moist-air formula '
             f'(Dalton\'s law, saturation pressure after Buck).')
    W.append('')
    W.append('**Note for comparisons between sessions.** The thrust needed to hover '
             'varies inversely with air density. Density rises by about 7% '
             'on cooling from 25 to 5 °C, which gives about 3.5% '
             'difference in `MOT_THST_HOVER`, the same as the differences '
             'currently examined in tuning. When comparing August sessions '
             'with autumn ones, the density deviation must be subtracted before '
             'a change is attributed to tuning.')
    W.append('')
    W.append('**Source of the model data.** ERA5 (ECMWF reanalysis) through the '
             'Open-Meteo Archive API. Values interpolated linearly between '
             f'full hours; nearest grid hour: '
             f'{local(grid_hour):%Y-%m-%d %H:%M} civil time. '
             'The ERA5 grid resolution is about 25 km, so the data describe '
             'the synoptic situation over the area, not the conditions at the take-off point. '
             'The wind speed binding for the rejection criteria of protocol §8 '
             'comes from the anemometer, not from the model.')
    W.append('')
    W.append(f'Query: `{url}`')
    W.append('')
    return '\n'.join(W)


# --- main path --------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        description='Atmospheric-conditions block for the session card, '
                    'from the ArduPilot log and the ERA5 reanalysis.')
    p.add_argument('log', help='.bin file')
    p.add_argument('--wind', default='[TO BE FILLED IN: GM816 anemometer]',
                   help='anemometer reading, e.g. "1-2 m/s"')
    p.add_argument('--lux', default='[TO BE FILLED IN: GM1010 lux meter]',
                   help='lux meter reading, e.g. "58 lx -> 21 lx"')
    p.add_argument('--card', help='session card to which the block is appended')
    p.add_argument('--append', action='store_true',
                   help='actually append to the card (without it, preview only)')
    p.add_argument('--archive', metavar='DIRECTORY',
                   help='save the raw API response as JSON, for inspection '
                        'and for reproducing the result offline')
    p.add_argument('--hours-back', type=int, default=6,
                   help='how many hours back to sum precipitation (default 6)')
    a = p.parse_args()

    log = read_log(a.log)
    day = log['start'].date()

    days_ago = (datetime.datetime.now(datetime.timezone.utc).date() - day).days
    if days_ago < ERA5_DELAY:
        available = day + datetime.timedelta(days=ERA5_DELAY)
        print(f'The session of {day.isoformat()} is {days_ago} days old. '
              f'ERA5 enters the archive with a delay of about '
              f'{ERA5_DELAY} days, so the data may not be there yet; '
              f'the safe date is {available.isoformat()}.\n'
              f'Trying anyway; if the values come back empty, run '
              f'again in a few days.\n', file=sys.stderr)

    data, url = fetch_era5(log['lat'], log['lon'], day)

    middle = log['start'] + (log['end'] - log['start']) / 2
    weather, grid_hour = values_at(data, middle, a.hours_back)

    if weather is None or all(weather.get(z) is None for z in VARIABLES):
        available = day + datetime.timedelta(days=ERA5_DELAY)
        raise SystemExit(
            f'The archive answered, but there are no values yet for '
            f'{day.isoformat()}. This is the normal ERA5 delay. Retry after '
            f'{available.isoformat()}. The card remains untouched.')

    if a.archive:
        os.makedirs(a.archive, exist_ok=True)
        target = os.path.join(a.archive,
                              os.path.splitext(log['file'])[0] + '_era5.json')
        with open(target, 'w', encoding='utf-8') as f:
            json.dump({'query': url, 'response': data}, f,
                      ensure_ascii=False, indent=1)
        print(f'Raw response saved: {target}', file=sys.stderr)

    block = build_block(log, weather, data, url, a.wind, a.lux, grid_hour)

    if a.card and a.append:
        with open(a.card, 'r', encoding='utf-8') as f:
            content = f.read()
        if SECTION_HEADING in content or SECTION_HEADING_PL in content:
            raise SystemExit(
                f'{a.card} already has an atmospheric-conditions section. '
                f'The script does not overwrite what someone may have corrected by hand; '
                f'remove the old section or append the block yourself.')
        with open(a.card, 'a', encoding='utf-8') as f:
            f.write('\n---\n\n' + block)
        print(f'Appended to {a.card}', file=sys.stderr)
    else:
        print(block)
        if a.card:
            print('\n[preview: add --append to write to the card]',
                  file=sys.stderr)


if __name__ == '__main__':
    main()
