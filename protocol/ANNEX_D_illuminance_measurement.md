# Annex D: illuminance measurement

*Established 23 Aug 2026. In force from session S-08. Instrument: Benetech GM1010 lux meter.*

---

## 1. Convention

Sensor **horizontal, window facing up**, at a height of about 1 m, in an open space, outside the shadow of the operator and the drone.

The operator stands **facing the sun** and holds the instrument at arm's length in front of them. The shadow then falls behind the operator.

The quantity measured is the illuminance on a horizontal plane. Illuminance is not measured perpendicular to the sun's rays or with the sensor facing down.

## 2. Recording

**Four items** are entered in the session card, never the product alone:

```
reading × range multiplier = result, sensor orientation, time
6000 × 10 = 60 000 lx, horizontal facing up, 12:50
```

Recording only the result makes it impossible to correct a misread multiplier later.

## 3. Frequency

A reading at the start and at the end of every cell. Protocol §8 rejects a run when the illuminance changes by more than 30%, so a single reading per session does not allow this criterion to be applied.

## 4. Additional measurement: light reflected from the surface

Sensor facing down, at a height of 1 m above the surface, operator out of the path of the rays. This is the quantity the PMW3901 sees.

Entered as a **separate item**, described as reflected light. It does not replace the measurement of §1.

## 5. Independent check

The ERA5 reanalysis via `analysis/session_weather.py` gives the surface solar radiation in W/m². The luminous efficacy of daylight is about 120 lm/W.

Upper limit for a clear sky:

```
E [lx] ≈ 110 000 · sin(h)
```

where `h` is the elevation of the sun above the horizon. This is horizontal illuminance; the GM1010 dome pointed at the sky in direct sun reads 1.5–3 times more (§8), so the limit applies to the sensor horizontal, not to the campaign readings taken towards the sky.

## 6. Verification of the readings from sessions S-02 to S-06

Sun elevation computed for 50.914 N / 19.0865 E, absolute time reconstructed from the GPS week and milliseconds in the logs. Readings converted from foot-candles (§8) on 4 Oct 2026.

| Session | Log | Local time | Sun elevation | Upper limit | Reading (fc) | Illuminance (lx) | Assessment |
|---|---|---|---|---|---|---|---|
| S-02 18 Aug | 5 | 18:46 | 10.2° | 19 400 lx | 1330 | 14 300 | possible |
| S-03 19 Aug | 6 | 19:29 | 3.3° | 6 400 lx | 355 | 3 820 | possible |
| S-04 20 Aug | 7 | 16:50 | 27.8° | 51 400 lx | 2450 | 26 400 | possible |
| S-05 21 Aug | 8 | 19:52 | −0.8° | approx. 230 lx | 58 → 21 | 624 → 226 | the first reading (19:48, sun about +0.1°) is above the model for 19:52; borderline |
| S-06 22 Aug | 9 | 16:01 | 34.3° | 62 100 lx | 7000 | 75 300 | 21 % above the model; within the combined uncertainty of a class-B meter and the model |

**S-06.** The session card gives the weather as: *after rain, clear sky, full sun*. The correction of 23 Aug ("7000 on the ×10 range = 70 000 lx") is withdrawn: the display 7000 is below the X10 threshold of 9999 (§8), so the reading was 7000 fc, i.e. 75 300 lx; the excess over the horizontal model is the dome in direct sun.

**S-02 to S-05.** The readings lie below or at the upper limit, so they are possible. The cards of these sessions **contain no description of the sky**, so the readings can be neither confirmed nor refuted. They remain as recorded, with a note about the unknown sensor orientation.

## 7. Range covered by the axis

The axis covers **226 to 75 300 lx** in August and, with the E1 campaign, **16 lx (dusk, image quality 0) to about 90 000 lx**: three and a half orders of magnitude.

## 8. Unit and range of the GM1010 readings (4 and 11 Oct 2026)

The GM1010 was in foot-candle mode (LCD indicator **FC**) on every photographed reading of the campaign, 23 Aug to 11 Oct 2026. All readings before 4 Oct were recorded as lux. Conversion applied throughout the repository: **1 fc = 10.764 lx**, checked on the instrument from 15 lx to 87 klx (1.4 fc ↔ 15.7 lx; 906.2 fc ↔ 9756 lx; 1962 fc ↔ 21 130 lx; 2729 fc ↔ 29 500 lx; 7716 fc ↔ 84 650 lx; 8048 fc ↔ 84 700 lx; pairs taken seconds apart, FC and Lux mode).

Display ranges: below 1000 fc one decimal (906.2); 1000–9999 four digits; above 9999 the **X10** indicator and the display divided by 10, in both modes (Lux: 2114 X10 = 21 140 lx; FC: 2144 X10 = 21 440 fc). The X10 readings of the campaign (23 Aug 2150, 3000, 6000; 26 Aug 1537, 2777; 28 Aug 1404; 13 Sep 1979, 2055, 1774, 1549) are therefore display × 10 fc and are converted like all others.

With the dome in direct sun the instrument reads 1.5–3 times the horizontal illuminance (11 Oct, sun at 30°: 87 klx against about 55 klx horizontal; 23 Aug, sun at 50°: 231 klx against 85 klx; the dome collects the direct beam almost independently of the sun's angle). Readings are instrument values with the sensor pointed at the sky, comparable within the campaign; they are not horizontal illuminance and are not compared with models or the literature. Readings above 200 klx exceed the instrument's specified range (26 Aug 299 klx perpendicular to the sun; 23 Aug 646 klx aimed at the sun).

Rules:

- The meter stays in FC mode. The session card records the display value, the indicators (FC, X10) and the illuminance in lux. Cell codes, INDEX, README and protocol thresholds are in lux.
- Readings with direct sun on the dome are marked as such in the card.
- The "× 10 range" corrections of 23 Aug (S-07) stand; their withdrawal of 4 Oct is itself withdrawn (the X10 indicator on IMG_9575 is lit).
