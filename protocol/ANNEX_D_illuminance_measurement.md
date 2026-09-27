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

where `h` is the elevation of the sun above the horizon. A reading exceeding this value is wrong regardless of the weather.

## 6. Verification of the readings from sessions S-02 to S-06

Sun elevation computed for 50.914 N / 19.0865 E, absolute time reconstructed from the GPS week and milliseconds in the logs.

| Session | Log | Local time | Sun elevation | Upper limit | Reading | Assessment |
|---|---|---|---|---|---|---|
| S-02 18 Aug | 5 | 18:46 | 10.2° | 19 400 lx | 1 330 lx | possible |
| S-03 19 Aug | 6 | 19:29 | 3.3° | 6 400 lx | 355 lx | possible |
| S-04 20 Aug | 7 | 16:50 | 27.8° | 51 400 lx | 2 450 lx | possible |
| S-05 21 Aug | 8 | 19:52 | −0.8° | approx. 230 lx | 58 → 21 lx | possible |
| **S-06 22 Aug** | **9** | **16:01** | **34.3°** | **62 100 lx** | **"over 7000 lx"** | **inconsistent** |

**S-06.** The session card gives the weather as: *after rain, clear sky, full sun*. At a sun elevation of 34.3° and a clear sky, the illuminance on a horizontal plane is about 62 000 lx. A reading of 7 000 lx would correspond to dense overcast. A reading of 7000 on the **×10 range gives 70 000 lx**, i.e. 13% above the model, within its accuracy.

Conclusion: S-06 is **70 000 lx**.

**S-02 to S-05.** The readings lie below the upper limit, so they are possible under overcast. The cards of these sessions **contain no description of the sky**, so the readings can be neither confirmed nor refuted. They remain as recorded, with a note about the unknown multiplier and the unknown sensor orientation.

## 7. Range covered by the axis

After the correction of S-06 the axis covers **21 to 70 000 lx**, i.e. three and a half orders of magnitude.
