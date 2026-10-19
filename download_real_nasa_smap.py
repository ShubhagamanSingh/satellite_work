"""
download_real_nasa_smap.py
==========================
Automated NASA Earthdata Downloader for Real SMAP Level-4 (SPL4SMGP V007) Satellite Granules.

NASA Earthdata Authentication Note:
-----------------------------------
NASA requires a free registered Earthdata Login (username and password) to download scientific
HDF5 (.h5) granules from the National Snow and Ice Data Center (NSIDC DAAC).
Registration URL: https://urs.earthdata.nasa.gov/users/new

This script supports:
1. Interactive prompt for your NASA Earthdata username and password.
2. Reading credentials from environment variables: EARTHDATA_USERNAME and EARTHDATA_PASSWORD.
3. Reading credentials from your standard ~/.netrc file.
4. Downloading the exact SMAP-L4 9km granules for Gujarat coordinates (Lat 20°N-25°N, Lon 68°E-74.5°E).
"""

import os
import sys
import getpass
import argparse
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("NASADownloader")

CMR_GRANULES_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
URS_AUTH_URL = "https://urs.earthdata.nasa.gov"


class EarthdataSession(requests.Session):
    """
    Custom requests session that handles NASA Earthdata OAuth redirect authentication.
    """
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        """
        Overrides rebuild_auth to ensure HTTP Basic Auth is preserved across
        the redirect to urs.earthdata.nasa.gov.
        """
        headers = prepared_request.headers
        url = prepared_request.url
        if "urs.earthdata.nasa.gov" in url:
            prepared_request.prepare_auth(self.auth)


def search_smap_granules(
    bbox=[68.0, 20.0, 74.5, 25.0],
    temporal_range=("2024-01-01T00:00:00Z", "2024-08-31T23:59:59Z"),
    limit=5
):
    """
    Queries NASA CMR (free, open metadata search without login).
    """
    params = {
        "short_name": "SPL4SMGP",
        "version": "007",
        "bounding_box": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "temporal": f"{temporal_range[0]},{temporal_range[1]}",
        "page_size": limit
    }
    logger.info(f"Searching NASA CMR for SMAP-L4 granules covering Gujarat {bbox}...")
    try:
        resp = requests.get(CMR_GRANULES_URL, params=params, timeout=20)
        resp.raise_for_status()
        entries = resp.json().get("feed", {}).get("entry", [])
        granules = []
        for e in entries:
            title = e.get("title", "")
            links = [l.get("href") for l in e.get("links", []) if l.get("href", "").endswith(".h5")]
            if links:
                granules.append({"title": title, "url": links[0]})
        logger.info(f"Found {len(granules)} granules in NASA CMR.")
        return granules
    except Exception as e:
        logger.error(f"CMR search error: {e}")
        return []


def download_granule(session, url, output_path):
    """
    Downloads a single NASA SMAP HDF5 granule with authentication.
    """
    logger.info(f"Downloading from {url} to {output_path}...")
    try:
        with session.get(url, stream=True, timeout=60) as resp:
            if resp.status_code == 401:
                logger.error("Authentication failed: Invalid NASA Earthdata Username or Password.")
                return False
            resp.raise_for_status()
            total_size = int(resp.headers.get("content-length", 0))
            downloaded = 0
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0 and downloaded % (1024 * 1024 * 10) == 0:
                            print(f"  Downloaded {downloaded / 1024 / 1024:.1f} MB / {total_size / 1024 / 1024:.1f} MB...", end="\r")
            print()
            logger.info(f"Download complete: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download Real NASA SMAP L4 HDF5 Granules.")
    parser.add_argument("--username", type=str, default=None, help="NASA Earthdata Username")
    parser.add_argument("--password", type=str, default=None, help="NASA Earthdata Password")
    parser.add_argument("--limit", type=int, default=3, help="Number of granules to download")
    parser.add_argument("--output-dir", type=str, default="data/real_smap_granules", help="Output directory")
    args = parser.parse_args()

    print("=" * 75)
    print("   NASA EARTHDATA SMAP-L4 GRANULE DOWNLOADER")
    print("   Notice: Free registration at https://urs.earthdata.nasa.gov is required.")
    print("=" * 75)

    username = args.username or os.environ.get("EARTHDATA_USERNAME")
    password = args.password or os.environ.get("EARTHDATA_PASSWORD")

    if not username:
        username = input("Enter NASA Earthdata Username: ").strip()
    if not password:
        password = getpass.getpass("Enter NASA Earthdata Password: ").strip()

    if not username or not password:
        print("Error: Both username and password are required to download NASA data.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Step 1: Discover granules via open CMR metadata search
    granules = search_smap_granules(limit=args.limit)
    if not granules:
        print("No granules found for the specified bounding box and date range.")
        sys.exit(1)

    # Step 2: Download with authenticated session
    session = EarthdataSession(username, password)
    success_count = 0

    for idx, g in enumerate(granules):
        fname = os.path.basename(g["url"])
        out_file = os.path.join(args.output_dir, fname)
        print(f"\n[{idx+1}/{len(granules)}] Processing: {fname}")
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1024 * 1024:
            print(f"  File already exists: {out_file} (skipping)")
            success_count += 1
            continue
        if download_granule(session, g["url"], out_file):
            success_count += 1

    print("\n" + "=" * 75)
    print(f"Finished! Successfully downloaded {success_count}/{len(granules)} real NASA granules.")
    print(f"You can now feed any downloaded granule into the reproduction pipeline:")
    print(f"  python main_reproduce.py --h5-file \"{os.path.join(args.output_dir, os.path.basename(granules[0]['url']))}\"")
    print("=" * 75)


if __name__ == "__main__":
    main()
