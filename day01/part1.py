

def main():
    digits = {
        str(k): k for k in range(10)
    }

    with open('input.txt') as f:
        lines = list(f)

    lines = [
        [digits[c] for c in line if c in digits]
        for line in lines
    ]
    total = sum(line[0] * 10 + line[-1] for line in lines)
    print(total)


if __name__ == '__main__':
    main()
