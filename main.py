#!/usr/bin/env python
"""For running Swytcher without installing anything"""
import swytcher.cli

if __name__ == "__main__":
    try:
        swytcher.cli.main()
    except KeyboardInterrupt:
        print("\nExiting...\n")
