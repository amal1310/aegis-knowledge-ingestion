# Evaluation Question Answers

1. **Before HPU startup:** fluid level NORMAL; IV-21 OPEN; emergency stop RESET; maintenance access panel CLOSED/not removed.
2. **Current pressure:** 200 bar for software revision 3.2 and later. The supplied configuration is firmware 3.2.1.
3. **A17:** hydraulic pressure below 150 bar. Causes: IV-21 closed/partially closed, low fluid, invalid pressure-sensor signal.
4. **PS-04 vs PS-04A:** No. PS-04A supersedes PS-04 from software 3.2 and is not form-fit-function interchangeable.
5. **Change document:** ECN-1042.
6. **Direct controller connections:** PS-04A and IV-21 in the hydraulic schematic.
7. **A17 >10 s:** execute Shutdown Procedure 4.7.
8. **Reset restriction:** do not reset PLC-03 above 50 bar; pressure must be below 50 bar.
9. **Before 3.2:** 180 bar; ECN-1042 changed the sensor to PS-04A and setpoint to 200 bar.
10. **Below 150 bar alarm:** A17.
11. **IV-21 location:** Hydraulic Module.
12. **Training-only content:** Auxiliary Reservoir is introduced as a Line 4/5-specific detail not covered in the standard Operator Manual; no new alarm is introduced.
13. **Diagnostics tag:** P.S.04-A; maps to PS-04A.
14. **3.2 effective date:** 2025-09-30; PS-04→PS-04A and 180→200 bar changed alongside it.
15. **Configuration key:** `sensor_ps04a_threshold_bar=200` corresponds to the 200-bar normal HPU discharge pressure setpoint in the Operator Manual.
16. **Scope of 200 bar:** software 3.2+; not all historical units. ECN-1042 also notes units manufactured after 2024.
17. **PS-04 vs PS-40:** No. PS-40 is a separate coolant-loop sensor in Skid B.
18. **Pre-3.2 pressure:** 180 bar.
19. **PS-04A max continuous temperature:** not stated in supplied package.
20. **Voltage-sensor calibration interval:** not stated; supplied calibration record says no interval is specified and the applicable maintenance schedule is not included.
21. **ECN-1058 approver:** not stated.
22. **IV-21 MTBF:** not stated.
23. **3-phase 400 V compatibility:** cannot be determined from supplied package.
