#!/usr/bin/env python
"""For running Swytcher without installing anything"""
import sys

import swytcher.cli

if __name__ == "__main__":
    try:
        swytcher.cli.main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nExiting...\n")
