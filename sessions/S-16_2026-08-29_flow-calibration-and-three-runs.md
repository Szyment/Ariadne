# S-16: 29 Aug 2026, afternoon, flow calibration and three Dryf3 runs at 3.0 m

Logs: `log_26_2026-8-29-17-07-02.bin` (calibration) · `log_27_2026-8-29-17-13-34.bin` (run 1) · `log_28_2026-8-29-17-21-54.bin` (runs 2 and 3, two take-off–landing cycles without disarming)

Onboard camera recordings: `movies/kam0_20260829_164514.mp4` / `kam1_20260829_164514.mp4`: calibration and run 1; `movies/kam0_20260829_171358.mp4` / `kam1_20260829_171358.mp4`: runs 2 and 3 (assignment from viewing the content). Do not use absolute times from mtime for these files: the first segments after power-up close before the clock correction from GNSS, on the fake-hwclock clock set back in time; mtime becomes reliable only once the RTC battery is fitted.

## Conditions

| | |
|---|---|
| Wind | 2–2.5 m/s, from 294° |
| Surface | field, the same as in the previous sessions |
| Plan | `S-15_Drift3.plan`, take-off 50.9139779/19.0864497, turn point 40 m on azimuth 114°, altitude **3.0 m** |

First session at 3.0 m; altitude lowered from 3.5 m by the decision after S-15, the same for all runs. Leg reversed (`--z-wiatrem`): outbound downwind, return upwind.

## Finding 1: flow calibration collected data but refused to write

The built-in calibration (`RC8_OPTION` = 158, LOITER at about 5 m, rocking to 100% on both axes) computed candidates and did not apply them:

```
FlowCal: no better scalar x:1.106 (fit:0.165 > orig)
FlowCal: no better scalar y:1.082 (fit:0.160 > orig)
```

`FLOW_FXSCALER/FYSCALER` remained 0, confirmed in the PARM of log 28. The candidates say: the flow underestimates by about 10.6% in the X axis and about 8.2% in the Y axis, but the fit with the correction came out worse than without it, so the autopilot did not accept the result. The convergence of three independent estimates (the calibrator's candidates, the fit from the S-15 hovers (X axis about 13% underestimate with a weak R²) and the distance deficit in the runs) indicates that the underestimate is real; its magnitude remains unresolved. Repeat the calibration in calmer air.

## Finding 2: the leg asymmetry is systematic: 4 runs out of 4

| Run | Outbound (downwind) | Return (upwind) | Whole | Final drift |
|---|---|---|---|---|
| S-15 morning, 3.5 m, wind 3.5 | 0.907 | 0.942 | 0.935 | 2.91 m |
| P1 (log 27) | 0.806 | 0.928 | 0.878 | 8.67 m |
| P2 (log 28) | 0.845 | 0.950 | 0.901 | 5.65 m |
| P3 (log 28) | 0.847 | 0.991 | 0.924 | 6.98 m |

The downwind half is always worse, the downwind final drift 2–5× larger. A global flow scale does not explain this: a constant underestimate of about 10% would give both halves at about 0.90, while upwind reaches 0.991. A mechanism dependent on the direction relative to the wind; an open item, material directly for RQ1.

GNSS distance of the outbound half in P1: 52.5 m on a 40 m leg; the aircraft navigating by its own estimate overshot the turn point by about 25%, exactly as much as the estimate was short (0.806). The estimate deficit translates one to one into overshoot on the ground.

## Finding 3: the 3.0 m altitude removed the switching threshold problem

`RFND` in the runs: medians 2.63–3.05 m, maximum **3.37 m**; margin to the 4.2 m threshold at least 0.8 m. In the morning at 3.5 m and a 3.5 m/s wind the threshold was being crossed (4.7% of samples). `OF.Qual` = 255 in all runs.

## Finding 4: altitude reference drift above the criterion, several times below Dryf2

`CTUN.Alt` on the ground after the flight: P1 **+0.50 m**, log 28 (two runs, three take-off–landing cycles) **−0.60 m**; above the 0.3 m criterion of `S-15_Dryf3_README`, against 1.72–2.00 m on `Dryf2`. `TOfs`: 0.19→−0.32 (P1), 0.52→1.06 (log 28). More cycles and longer time on the rangefinder source give a larger drift. To be observed; in the morning a single run fitted within the criterion (−0.16 m).

## Beyond the runs

- SE kill switch used for real at the end of the day: `RPi: SE detected, hold 3 s` in log 28 (408.6 s).
- Return to set 1 again before the switch to LOITER (as in S-15); in P2 even 0.8 s before reaching the end point, so the GNSS-denied phase was cut short by a fraction of the return half. No harm to the data (phase boundaries are taken from the messages, not from the plan), but the procedure prescribes the reverse order.
- In log 27 after landing `PreArm: Battery 1 below minimum arming voltage`: pack exhausted, replaced before log 28.

## To do

- [ ] Repeat the flow calibration in a wind < 2 m/s; if it refuses to write again, consider manual `FLOW_FXSCALER` ≈ 106, `FLOW_FYSCALER` ≈ 82 and validation with a single run
- [ ] Explain the mechanism of the downwind/upwind asymmetry (candidates: estimator behaviour under wind push, coupling of tilt with flow)
- [ ] Keep to the order of procedure steps 7–8 (LOITER before the source switch)

Photos and screenshots: `build-log/photos/2026-08-29/`.
