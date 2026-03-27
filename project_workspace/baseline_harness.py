import atheris
import sys

# 1. YOU MUST INSTRUMENT BEFORE IMPORTING THE TARGET
with atheris.instrument_imports():
    import python_target 

def TestOneInput(data):
    try:
        python_target.process_request(data)
    except Exception:
        pass

def main():
    # Standard Atheris setup
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()