# Apiary Operating System — v1.2 Data Integrity Release

## Main purpose
This release addresses possible data loss from earlier releases by adding:

- Data Integrity tab
- Baseline colony/nuc validation
- Missing colony detection
- One-click restore of baseline entities
- Stronger bootstrap: it adds missing baseline records without overwriting existing records
- Full expected colony/nuc baseline included in code
- System audit when missing records are restored

## Important
Earlier releases sometimes seeded a smaller colony list. If your database was created from one of those releases, some hives/nucs may not appear. This release does **not** delete your existing data. It checks for missing baseline records and lets you restore them.

## First time with this release

1. Extract ZIP.
2. Double-click `Install_AOS.bat` if needed.
3. Double-click `Run_AOS.bat`.
4. Open the **Data Integrity** tab.
5. Click **Run Integrity Check**.
6. If records are missing, click **Restore Missing Baseline Entities**.

## Normal use
Double-click `Run_AOS.bat`.
