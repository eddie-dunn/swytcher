#!/usr/bin/env python
"""For running Swytcher without installing anything"""
import swytcher.swytcher

if __name__ == "__main__":
    try:
        swytcher.swytcher.main()
    except KeyboardInterrupt:
        print("\nExiting...\n")
