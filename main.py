import subprocess
import sys

def run_format():
    try:
        result = subprocess.run(
            ["python3", "src/format.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running format.py:")
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

def get_output():
    try:
        result = subprocess.run(
            ["python3", "src/run2.py"],
            stdin=sys.stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running run2.py:")
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

def get_output3():
    try:
        result = subprocess.run(
            ["python3", "src/run3.py"],
            stdin=sys.stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running run3.py:")
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

def main():
    format_output = run_format()
    sys.stdout.write(format_output)
    output = None
    try:
        a = int(sys.argv[1])
    except (IndexError, ValueError):
        a = 2 # default 2-model
    if a == 2:
        output = get_output()
        sys.stdout.write(output)
    elif a == 3:
        output = get_output3()
        sys.stdout.write(output)

if __name__ == "__main__":
    main()