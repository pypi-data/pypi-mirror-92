# Introduction
A library provides pylint checkers.  

# Install

```bash
pip install usachev_pylint_checkers
```

# Get started
```bash
pylint --load-plugins=usachev.checkers src >> report.txt
```

# Checkers

## forbidden-print-statement
The checker looks usage of print statement and provides warning if it finds.

# Release notes
## 0.1
1. Added forbidden-print-statement checker
