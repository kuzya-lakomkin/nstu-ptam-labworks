from lab1.temp_parser.buffer_input import readbuff

def foo(a, b):
    try:
        return a ** b
    except TypeError:
        raise TypeError("WAIT NIGGA!!!!")
    
if __name__ == "__main__":
    try:
        foo("aaa", "sad")
    except TypeError:
        print("LOL")

    print(-.111)

    s = "a"

    while s[-1] != '\n':
        s += str(readbuff())
        print(s)
    
    print(s)