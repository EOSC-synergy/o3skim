"""Python module template."""


def hello_world(*arg, **kvarg):
    print("Hello World")
    if arg or kvarg:
        print(f"  - Arguments as Inputs: {arg}")
        print(f"  - Arguments as KeyVal: {kvarg}")
    return True
