# Run card: template

*Annex B of the E1–E3 protocol. One card per measurement run. Filled in in the field, before the flight and immediately after it, not from memory in the evening.*

**Rule:** the card is filled in before the result is looked at. The rejection criteria of protocol §8 are applied on the basis of the data on conditions, not on the result.

---

| Field | Value |
|---|---|
| Run number | |
| Phase (E1 / E2 / E3) | |
| Date and time | |
| Matrix cell (LUX / SURF / ALT / VEL) | |
| Illuminance [lx], median of 3 readings | |
| Wind before the run: AVG / MAX [m/s], 60 s measurement | |
| Wind after the run: AVG / MAX [m/s], 60 s measurement | |
| Wind direction (45° sector it blows from; "variable" when below 1 m/s) | |
| Wind relative to the run axis: head / cross / tail | |
| Wind measurement height [m] | 2.0 |
| Surface, verbal description | |
| Surface condition: dry / damp / wet | |
| Cloud cover: clear / cloudy / heavy | |
| Surface photo (file name) | |
| Battery number | |
| Take-off voltage [V] | |
| Take-off mass [g] | |
| Pack temperature: before take-off / after landing [°C] | |
| Surface temperature [°C] | |
| Number of satellites / PDOP | |
| Time of switch to SRC2 [log s] | |
| Time of switch back to SRC1 [log s] | |
| Log file name | |
| Run accepted / rejected | |
| Reason for rejection | |
| Pilot's remarks | |

---

## Log file naming (protocol §9.1)

```
ARIADNE_E{phase}_{run_number}_{date}_{cell}.bin
```

Example: `ARIADNE_E2_047_20261012_LUX2-SURF1-ALT2-VEL0.bin`

## Rejection criteria (protocol §8)

A run is rejected if **before the result is looked at** any of the following is found:

- PDOP above 2.0 or number of satellites below 10
- wind above 5 m/s in the run window; the larger of the two AVG values decides, from the measurement at a height of 2.0 m (Annex C §7)
- pilot intervention for reasons other than drift (obstacle, bystander)
- a hardware fault detected
- incomplete record
- a change of illuminance during the run of more than 30 percent

Rejections are recorded together with the reason. The number of rejections and their distribution over the matrix cells go into the paper, because systematic rejection in one cell is information in itself.

## Why we record the surface condition

The campaign runs from October to mid-November. In this period low illuminance and a wet surface occur together, because both result from cloud cover. If the dark cells are flown only on cloudy days and the bright ones on sunny days, illuminance becomes entangled with surface condition and their effects cannot be separated.

Wet asphalt at dusk is not dark asphalt but a mirror-like surface, and that is an entirely different condition for the optical-flow sensor. The surface condition must be recorded at every run and enter the analysis as a covariate, not as part of the cell label.

## Temperature measurement with the infrared thermometer

The measurement is made with the Axiomet AX-7510 infrared thermometer (range −20…550 °C, accuracy ±2 °C, resolution 0.1 °C, adjustable emissivity 0.1–1, distance-to-spot ratio 12:1).

**Set the emissivity to 0.95 and do not change it between runs.** The infrared thermometer does not measure temperature but radiation, and converts it into temperature at the assumed emissivity. Changing the setting during the campaign invalidates comparisons between runs.

**Battery.** Stick a piece of matt black tape on the pack's shrink wrap (ordinary black PVC insulating tape for wires is enough, as long as it is matt, not glossy) and always measure at the same spot, perpendicularly, from a distance of about 15 cm (spot about 1.3 cm). Reason: the heat-shrink sleeve is glossy, and a glossy surface reflects the radiation of the surroundings and lowers the reading by as much as ten or more degrees. The tape gives a repeatable emissivity close to 0.95.

**Sticker size.** At least 3×3 cm. At a distance of 15 cm the measurement spot is about 1.3 cm; if it extends even partly beyond the tape, the reading is a mixture of two surfaces of different emissivity and ceases to be repeatable.

**Emissivity check, once, before the campaign.** Stick on the tape, leave the pack in a room for half an hour so that it equalises with the ambient temperature, measure the air temperature with the thermometer of the GM816 anemometer, then the tape with the infrared thermometer. Both values should be equal. If the infrared thermometer reads low, raise the emissivity; if it reads high, lower it. Record the established value and do not change it until the end of the campaign.

**Surface.** Measure perpendicularly, from about 30 cm, at the take-off point. Grass and damp soil have an emissivity close to 0.95, so the same setting is correct.

**What the infrared thermometer will not replace.** It measures the surface temperature, not the air temperature. The air temperature comes from the GM816 anemometer, and when completed retrospectively, from the ERA5 reanalysis (`analysis/session_weather.py`). Pointing the infrared thermometer at the air or the sky gives a reading of the sky, not of the surroundings.

**Purpose of this measurement.** The pack temperature affects its internal resistance, and through it the voltage under load and the available flight time. The campaign runs in the cold months, so a pack taken out of a warm car and a pack chilled for an hour in the field behave differently. Without a temperature record, the difference in run range looks like battery wear.

## Wind measurement

Full procedure: `protocol/ANNEX_C_wind_measurement.md`. In brief:

- a fixed measurement point, the same throughout the campaign, at least 10 m from the aircraft and away from obstacles;
- height 2.0 m, arm extended in front, the person measuring faces the wind;
- the measurement lasts 60 s; the anemometer is **switched on at its start** and switched off at the end, because this defines the averaging window regardless of how the manufacturer implemented the AVG mode;
- read AVG, MAX and CU; AVG and MAX go into the card;
- measure before arming and after landing, never with the propellers running;
- read the direction from the ribbon on the stake, not by turning the anemometer; record the 45° sector as the one the wind blows **from**, and the class relative to the run axis (head / cross / tail);
- below 1 m/s the ribbon drops and there is no direction; enter "variable", do not guess.

Readings below 1 m/s are recorded as "below 1 m/s". The vane impeller has a start-up speed and at the lower end of the range it does not measure, it only indicates.

After the session the direction is checked independently with the script `analysis/wind_from_log.py`, which calculates it from the aircraft tilt in hover.

## Altitude limit

In GNSS-denied runs a ceiling of **6 m** applies, resulting from `RNGFND1_MAX`. With `EK3_SRC2_POSXY = 0` the aircraft will not climb above the rangefinder's range.
