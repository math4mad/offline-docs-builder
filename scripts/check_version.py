# scripts/check_version.py
import requests
import sys

def get_latest_pypi_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    resp = requests.get(url)
    return resp.json()['info']['version']

if __name__ == "__main__":
    package = sys.argv[1]
    print(get_latest_pypi_version(package))