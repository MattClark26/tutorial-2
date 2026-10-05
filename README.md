# Panel 2: Labour Market Signal

A Python dashboard that tracks US labor market trends, recession indicators, and data revision patterns using FRED data.

## Overview

* **Sahm Rule:** Calculates the 3-month moving average of unemployment minus its 12-month minimum. Flags when it hits the 0.50 percentage point threshold and compares it against FRED's `SAHMREALTIME`series.
* **Jobless Claims:** Plots the 4-week moving average of initial claims and flags sharp jumps off 52-week lows.
* **Monthly Payrolls:** Tracks net monthly changes in nonfarm employment.
* **Data Revisions (ALFRED):** Compares initial payroll releases against current revised numbers to spot significant downward revisions.
* **Recession Scorecard:** Summarises current indicator readings and highlights trigger statuses.
