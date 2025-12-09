import ftplib
import sys
from pathlib import Path

# ==============================
#  CONFIG - EDIT THESE
# ==============================
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"

# Remote path where DZB_Loadout_1.json lives on your host
REMOTE_PATH = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus/custom/DZB_Loadout_1.json"

# Local folder on the Pi where your loadouts live
LOCAL_DIR = Path("/home/d3nd4n/dayz_loadouts")


def upload_loadout(mode: str) -> None:
    """Upload weekday or weekend loadout JSON to the server."""
    if mode == "weekday":
        local_file = LOCAL_DIR / "loadout_weekday.json"
    elif mode == "weekend":
        local_file = LOCAL_DIR / "loadout_weekend.json"
    else:
        raise SystemExit("Mode must be 'weekday' or 'weekend'")

    if not local_file.exists():
        raise SystemExit(f"Local loadout not found: {local_file}")

    print(f"[LOADOUT {mode.upper()}] Connecting to FTP {FTP_HOST}...")
    with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        # Split remote path into dir + filename
        remote_dir = str(Path(REMOTE_PATH).parent).replace('\\', '/')
        remote_name = Path(REMOTE_PATH).name

        ftp.cwd(remote_dir)

        with open(local_file, "rb") as f:
            print(f"[LOADOUT {mode.upper()}] Uploading {local_file.name} -> {remote_name}")
            ftp.storbinary(f"STOR {remote_name}", f)

    print(f"[LOADOUT {mode.upper()}] Upload complete.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 set_loadout.py weekday|weekend")
        raise SystemExit(1)

    upload_loadout(sys.argv[1])
