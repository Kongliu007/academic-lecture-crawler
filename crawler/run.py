#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pku.physics.crawl import fetch_pku_physics
from thu.physics.crawl import fetch_thu_physics

def main():
    print("=== Academic Lecture Crawler ===\n")

    print("Fetching Peking University Physics Lectures...")
    fetch_pku_physics()
    print()

    print("Fetching Tsinghua University Physics Lectures...")
    fetch_thu_physics()
    print()

    print("All lectures fetched and saved successfully!")

if __name__ == "__main__":
    main()
