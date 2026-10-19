"""
Authentic NASA Earthdata SMAP-L4 Granule Downloader
Downloads genuine SPL4SMGP H5 granules from NASA Earthdata Cloud using authenticated credentials.
"""

import os
import sys
import pathlib
import earthaccess

def download_seasonal_granules(dest_dir="data/nasa_real_granules"):
    out_path = pathlib.Path(dest_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    print("[NASA Earthdata] Logging in with netrc credentials...")
    auth = earthaccess.login(strategy="netrc")
    if not auth.authenticated:
        raise RuntimeError("Failed to authenticate with NASA Earthdata using .netrc")
    print(f"[NASA Earthdata] Successfully authenticated as: {auth.username}")
    
    # 5 seasonal dates representing the hydrological cycle
    dates = [
        ("2024-05-01", "2024-05-02"),  # Pre-monsoon dry season
        ("2024-05-20", "2024-05-21"),  # Peak summer
        ("2024-07-20", "2024-07-21"),  # Peak monsoon wet season
        ("2024-08-10", "2024-08-11"),  # Late monsoon wet season
        ("2024-10-05", "2024-10-06"),  # Post-monsoon drying
    ]
    
    downloaded_files = []
    for start, end in dates:
        print(f"\n[NASA Earthdata] Searching SPL4SMGP for {start} to {end}...")
        results = earthaccess.search_data(
            short_name="SPL4SMGP",
            temporal=(start, end),
            count=1
        )
        if not results:
            print(f"[Warning] No granules found for {start}")
            continue
        
        granule = results[0]
        granule_id = granule['umm']['GranuleUR']
        target_file = out_path / granule_id
        
        if target_file.exists() and target_file.stat().st_size > 10 * 1024 * 1024:
            print(f"[Cache] Already downloaded: {target_file.name} ({target_file.stat().st_size / (1024*1024):.1f} MB)")
            downloaded_files.append(target_file)
            continue
            
        print(f"[Download] Downloading authentic granule: {granule_id}...")
        files = earthaccess.download([granule], str(out_path))
        for f in files:
            p = pathlib.Path(f)
            if p.suffix == ".h5":
                downloaded_files.append(p)
                print(f"[Success] Downloaded {p.name} ({p.stat().st_size / (1024*1024):.1f} MB)")
                
    print(f"\n[Complete] Total authentic NASA SMAP granules ready: {len(downloaded_files)}")
    return downloaded_files

if __name__ == "__main__":
    download_seasonal_granules()
