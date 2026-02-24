import os

def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        raw = f.read(4)
        if raw.startswith(b'\xff\xfe\x00\x00') or raw.startswith(b'\xff\xfe'):
            return 'utf-16'
        elif raw.startswith(b'\xfe\xff\x00\x00') or raw.startswith(b'\xfe\xff'):
            return 'utf-16'
        elif raw.startswith(b'\xef\xbb\xbf'):
            return 'utf-8-sig'
        else:
            return 'utf-8'


def process_file(input_file: str, output_file: str, chars_to_replace: str) -> None:
    encoding = detect_encoding(input_file)
    buffer = []
    chunk_size = 4096
    fin, fout = None, None

    try:
        fin = open(input_file, 'r', encoding=encoding, errors='replace')
    except FileNotFoundError:
        print(f"[Fatal] file '{input_file}' was not found.")
        return
    except PermissionError:
        print(f"[Fatal] no permission to '{input_file}'.")
        return
    
    try:
        fout = open(output_file, 'w', encoding='utf-8')
    except FileNotFoundError:
        print(f"[Fatal] file '{output_file}' was not found.")
        fin.close()
        return
    except PermissionError:
        print(f"[Fatal] no permission to '{output_file}'.")
        fin.close()
        return

    while True:
        chunk = fin.read(chunk_size)
        if not chunk:
            break
            
        for c in chunk:
            if c in chars_to_replace:
                buffer.append(' ')
            else:
                buffer.append(c)
            
        fout.write(''.join(buffer))
        buffer.clear()


if __name__ == "__main__":
    input_file = ''
    print("enter the input file path: ", end=' ')
    while True:
        input_file = input()
        if (len(input_file) != 0):
            break
        print('please, enter the file path.')
    
    output_file = ''
    print("enter the output file path: ", end=' ')
    while True:
        output_file = input()
        if (len(output_file) != 0):
            break
        print('please, enter the file path.')

    chars_to_replace = set(input("enter the symbols to replace: "))

    process_file(input_file, output_file, chars_to_replace)
    print("Process finished.")
