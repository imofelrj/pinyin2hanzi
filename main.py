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
            ["python3", "src/run.py"],
            stdin=sys.stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running run.py:")
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

def main():
    format_output = run_format()
    output = get_output()
    sys.stdout.write(output)

if __name__ == "__main__":
    main()