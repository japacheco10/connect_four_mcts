# example_script.py
import sys

print("Script name:", sys.argv[0])
for i, arg in enumerate(sys.argv[1:]):
    print(f"Argument {i+1}: {arg}")
