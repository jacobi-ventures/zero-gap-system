
# 🧾 CHANGELOG — Zero Gap System Tool

A modular, real-time, IBKR-connected options strategy scanner for strangles and credit spreads.

---

## [v1.7.1] — 2025-05-14
### Added
- IBKR execution module (`ibkr.py`)
- Live combo ticket builder using `ib_insync`
- `send_combo_order` with dry-run + real trade capability

---

## [v1.7.0] — 2025-05-13
### Added
- Modular project structure (main.py, filters.py, strategy.py, ui.py)
- Strategy box UI and credit/strangle rendering
- Recommend + Reset filters
- Styled layout with tooltips for each slider

---

## [v1.6.3] — 2025-05-13
### Improved
- Added helper text next to each filter slider
- Rebuilt color-coded styled trade boxes
- "Send Strategy to IBKR (Simulated)" button
- Filter logic debugged and stable

---

## [v1.6.2] — 2025-05-13
### Fixed
- Bug in deprecated rerun method
- Explained and logged recommended filter criteria

---

## [v1.6.1] — 2025-05-13
### Restored
- Version history panel
- Color-coded strategy boxes
- "Reset Filters", "Recommend Filters", and export buttons

---

## [v1.6.0] and Earlier
- Built initial Streamlit app with simulated trade logic
- Integrated Tradier API live options chain
- Created combo ranking system (R/R + strangle skew)
