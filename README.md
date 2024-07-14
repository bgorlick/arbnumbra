# arbnumbra

Arbitrary Precision Arithmetic Test Case Generator and Verifier

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://semver.org)

## Overview

arbnumbra is a tool for generating, experimenting with, and verifying test cases for arbitrary precision arithmetic operations. It can be easily adapted to the variety of syntax needs of arbitrary precision arithmetic libraries.

I created this as a quick test suite for assertion checks while developing my own custom arbitrary precision arithmetic library. It proved so useful that I decided to share it, hoping others might find similar benefit in their projects.

## Features

- **Test Case Generation**: Creates diverse test cases for arbitrary-precision numbers with specified precisions.
- **Precision and Representation Testing**: Focuses on testing the ability to represent numbers at specified precisions.
- **Verification Mechanism**: Compares generated results against expected outputs.
- **Flexible Input/Output**: Supports various input formats (text, JSON, TOML) and output formats (JSON, CSV, TOML, C struct).
- **Customization Options**: Allows specification of precision ranges, exponent ranges, radix, and base settings.

## Installation

```bash
git clone https://github.com/bgorlick/arbnumbra.git
cd arbnumbra
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python arbnumbra.py -gen [options]  # Generate test cases
python arbnumbra.py -ver [options]  # Verify test cases
python arbnumbra.py -gen -ver [options]  # Generate and verify
```

### Key Options

- `-f FILE`: Input file
- `-n NUM`: Number of random cases
- `-o FILE`: Output file
- `-t {json,csv,toml,c}`: Output type
- `--min_precision`, `--max_precision`, `--min_exponent`, `--max_exponent`
- `--include_special`, `--include_edge`, `--include_subnormal`, `--include_pi NUM`
- `--radix NUM`, `--base NUM`
- `-v`: Verbose output

### Examples

Generate 10 random cases + special cases:
```bash
python arbnumbra.py -gen -n 10 -o tests -t json --include_special
```

Generate from JSON input, include edge cases:
```bash
python arbnumbra.py -gen -f input.json -o tests -t c --include_edge
```

Verify cases from TOML file:
```bash
python arbnumbra.py -ver -f tests.toml -v
```

Generate with specific precision and exponent range:
```bash
python arbnumbra.py -gen -n 20 --min_precision 50 --max_precision 100 --min_exponent -50 --max_exponent 50
```

Generate and verify with custom radix and base:
```bash
python arbnumbra.py -gen -ver -f input.txt -o tests -t json --radix 16 --base 2
```

Generate pi approximations:
```bash
python arbnumbra.py -gen --include_pi 100 -o pi_tests -t csv
```

Complex scenario:
```bash
python arbnumbra.py -gen -ver -f input.json -n 50 -o complex_tests -t toml --include_special --include_edge --include_subnormal --include_pi 10 --min_precision 1 --max_precision 1000 --min_exponent -1000 --max_exponent 1000 --radix 10 --base 2 -v
```

## Input Formats

### Text File (input.txt)
```
0.123456789e-5 10
1.23e10 15 10 2
```

### JSON (input.json)
```json
[
  {"num": "0.123456789e-5", "precision": 10},
  {"num": "1.23e10", "precision": 15, "radix": 10, "base": 2}
]
```

### TOML (input.toml)
```toml
[[testcase]]
num = "0.123456789e-5"
precision = 10

[[testcase]]
num = "1.23e10"
precision = 15
radix = 10
base = 2
```

## Example Input Files

The `examples/` directory contains sample input files in different formats:

- `examples/input.txt`: Text file format
- `examples/input.json`: JSON format
- `examples/input.toml`: TOML format

You can use these files to test the tool or as templates for your own input files.

### Using Example Files

Generate test cases from the example JSON file:
```bash
python arbnumbra.py -gen -f examples/input.json -o output -t json
```

Verify test cases using the example TOML file:
```bash
python arbnumbra.py -ver -f examples/input.toml -v
```

## Project Structure

```
arbnumbra/
│
├── arbnumbra.py
├── README.md
├── LICENSE
├── requirements.txt
│
└── examples/
    ├── input.txt
    ├── input.json
    └── input.toml
```

## Use Cases

- Initial validation of arbitrary precision arithmetic libraries
- Testing number-to-string and string-to-number conversions at high precisions
- Generating test suites for numerical algorithm implementations
- Verifying correct handling of edge cases in precision-sensitive applications

## Limitations

- Not a comprehensive test suite for all arithmetic operations
- Focused on representation and precision, not on arithmetic calculations
- Does not cover all possible edge cases or complex scenarios

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

(c) 2024 Benjamin Gorlick

## Acknowledgements

- This tool is designed as a starting point for testing arbitrary precision implementations, particularly in scenarios where exact representation and precision handling are critical.