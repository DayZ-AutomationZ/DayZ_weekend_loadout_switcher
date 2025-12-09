# DayZ Weekend Loadout Switcher (DZBTools)

This package lets you automatically swap a **DZBTools** loadout JSON on your DayZ server for weekends (e.g. fun / meme / raid weekend spawn gear) and switch back to a normal weekday loadout using a small Python script and cron on your Raspberry Pi (or any Linux box).

---

## 1. What this does

- You keep **two DZB loadout JSON files**:
  - `loadout_weekday.json` – your normal spawn loadout  
  - `loadout_weekend.json` – your special weekend loadout (e.g. beer + rotten meat theme :) )
- The Pi script uploads the chosen JSON to your server as:
  - `dayzstandalone/mpmissions/dayzOffline.chernarusplus/custom/DZB_Loadout_1.json`
- You use **DZBTools** to generate the JSONs and configure your loadout in `cfgGameplay.json`:
  ```json
  "spawnGearPresetFiles": ["custom/DZB_Loadout_1.json"]
  Search for 

  "PlayerData": {
  "disablePersonalLight": false,
  "spawnGearPresetFiles": [] <-- empty by default


  "PlayerData": {
  "disablePersonalLight": false,
  "spawnGearPresetFiles": ["custom/DZB_Loadout_1.json"] <-- add the loadout

  ```

You then schedule cron like:

- **Friday 18:00** → weekend loadout  
- **Sunday 23:59** → weekday loadout

(Adjust times to match your restart schedule.)

---

## 2. Folder structure (on the Pi)

Recommended path:

```bash
/home/PIusername/dayz_loadouts/
├── loadout_weekday.json
├── loadout_weekend.json
└── set_loadout.py
```

This repo already matches that structure. You can rename the folder if you want, but then update paths in cron.

---

## 3. Configure your DayZ server (DZBTools integration)

1. Go to **`cfgGameplay.json`** on your server:

   ```text
   dayzstandalone
   └── mpmissions
       └── dayzOffline.chernarusplus
           └── cfgGameplay.json
   ```

2. In the `PlayerData` section, make sure its set:

   ```json
   "PlayerData": {
       ...
       "spawnGearPresetFiles": ["custom/DZB_Loadout_1.json"],
       ...
   }
   ```

3. Make sure this file actually exists on the server (the Python script in this package will handle uploading).

4. Use https://loadouts.dzbtools.com/ to **design your loadouts** and export them as JSON:
   - Save your weekday JSON as `loadout_weekday.json`
   - Save your weekend JSON as `loadout_weekend.json`

This package already includes example JSON configs; overwrite them with your own from DZBTools if you want something different.

---

## 4. Configure FTP credentials in `set_loadout.py`

Open `set_loadout.py` and set:

```python
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"

REMOTE_PATH = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus/custom/DZB_Loadout_1.json"
```

- On Nitrado this is usually correct, but double-check the path via your FTP client (FileZilla, WinSCP, etc.).
- Keep the filename `DZB_Loadout_1.json` so it matches `cfgGameplay.json`.

---

## 5. Test from your Pi

On your Pi (or Linux box):

```bash
cd /home/PIusername/dayz_loadouts

# Test weekday upload
python3 set_loadout.py weekday

# Test weekend upload
python3 set_loadout.py weekend
```

If everything is correct, you should see something like:

```text
[LOADOUT WEEKDAY] Connecting to FTP...
[LOADOUT WEEKDAY] Uploading loadout_weekday.json -> DZB_Loadout_1.json
[LOADOUT WEEKDAY] Upload complete.
```

Restart your DayZ server and verify that new spawns have the expected gear.

---

## 6. Cron setup for automatic switching

Edit crontab on your Pi:

```bash
crontab -e
```

Add something like:

```cron
# --- WEEKEND LOADOUT ON (FRIDAY 18:00) ---
0 18 * * 5 python3 /home/PIusername/dayz_loadouts/set_loadout.py weekend

# --- WEEKEND LOADOUT OFF (SUNDAY 23:59 -> back to weekday) ---
59 23 * * 0 python3 /home/PIusername/dayz_loadouts/set_loadout.py weekday
```

Explanation:

- `* * 5` = Friday (day-of-week 5)
- `* * 0` = Sunday (day-of-week 0)
- Adjust times to match your **raid schedule** and **server restarts**.  
  You want the upload to happen **before** the restart that activates the new loadout.
  Make sure your PI has the exact same timezone settings as your server or you need to adjust it.
  the server this is made for restarts 18:00 so at 18:00 a new file is uploaded which is loaded on restart at 18:06 on friday.
  On sunday the server restarts at 0:06 so file is also uploaded before restart.
  Make sure it is set correct at least a couple of minutes before restart.
  

If your server restarts at 00:06, you could e.g.:

- Friday 17:55 → `weekend`
- Sunday 23:55 → `weekday`

---

## 7. Example: weekday & weekend loadouts

This package includes two **example** DZB JSON loadouts derived from your configs:

- `loadout_weekday.json` – more basic survival start
- `loadout_weekend.json` – baseball bat + knife + cat food fun spawn

You can edit them directly or overwrite with exports from DZBTools.

---

## 8. Safety tips

- Always keep a **backup** of your original `DZB_Loadout_1.json` before automating.
- Test the script manually before relying on cron.
- If anything goes wrong, just re-upload your backup loadout JSON and restart the server.

---

## 9. Quick start TL;DR

1. Put this folder on your Pi: `/home/Piusername/dayz_loadouts`
2. Edit `set_loadout.py` FTP credentials.
3. Configure `cfgGameplay.json` to use `custom/DZB_Loadout_1.json`.
4. Test: `python3 set_loadout.py weekend` and restart server → check new spawn.
5. Add cron entries to auto-switch Friday / Sunday.

Enjoy your **weekend meme loadout** on your server.
