"""Build current modules from separate, documented sources."""
from build_httpdns import main as build_httpdns
from build_ads import main as build_ads

if __name__ == "__main__":
    build_httpdns()
    build_ads()
