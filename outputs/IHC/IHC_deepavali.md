# [IHC] Deepavali month: Actual vs Predicted

Deepavali months are read from ./src/events/event_ranges/deepavali.csv. [2024-10, 2025-10] fall inside the eval period 2024-04 to 2026-03, and 2026-11, 2027-10 inside the predict period 2026-04 to 2028-03.

**Best model:** Holt-Winters exponential smoothing
- A positive difference means the model over-predicted.
- A negative difference means the model under-predicted.

## Deepavali months in the eval + predict period

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 28.77 | -15.13 | -34.47% |
| 2025-10 | 38.30 | 30.43 | -7.87 | -20.54% |
| 2026-11 | -- | 15.68 | -- | -- |
| 2027-10 | -- | 38.35 | -- | -- |
