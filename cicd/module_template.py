"""Python module template."""


def hello_world(*arg, **kvarg):
    print("Hello World")
    if arg or kvarg:
        print(f"  - Arguments as inputs: {arg}")
        print(f"  - Key-Value arguments: {kvarg}")
    return True
