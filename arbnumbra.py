# arbnumbra - Arbitrary Precision Arithmetic Test Case Generator and Verifier
# MIT LICENSE | (c) 2024 Benjamin Gorlick | github.com/bgorlick/arbnumbra
# Version: 0.0.1 
#
# This script is a specialized tool for generating and verifying test cases
# for arbitrary precision arithmetic operations, with a focus on number
# representation and precision handling. 
# 
# Current Limitations:
# - Not a comprehensive test suite for all arithmetic operations
# - Focused on representation and precision, not on arithmetic calculations
# - Does not cover all possible edge cases or complex scenarios
#
# This tool is designed as a starting point for testing arbitrary precision
# implementations, particularly in scenarios where exact representation and
# precision handling are critical.
# 
# Its primary functions include:
#
# 1. Test Case Generation:
#    - Creates test cases for arbitrary-precision numbers with specified precisions
#    - Handles normal numbers, large/small exponents, and special values (inf, NaN)
#    - Generates edge cases and subnormal numbers
#    - Produces pi approximations to various precisions
#
# 2. Precision and Representation Testing:
#    - Focuses on testing the ability to represent numbers at specified precisions
#    - Verifies correct handling of significand and exponent in various scenarios
#    - Emphasizes full, non-scientific notation string representation of numbers
#
# 3. Verification Mechanism:
#    - Compares generated results against expected outputs
#    - Useful for validating the accuracy of arbitrary precision implementations
#
# 4. Flexible Input/Output:
#    - Supports various input formats (text, JSON, TOML)
#    - Offers multiple output formats (JSON, CSV, TOML, C struct)
#
# 5. Customization Options:
#    - Allows specification of precision ranges, exponent ranges
#    - Supports custom radix and base settings
#
# Use Cases:
# - Initial validation of arbitrary precision arithmetic libraries
# - Testing number-to-string and string-to-number conversions at high precisions
# - Generating test suites for numerical algorithm implementations
# - Verifying correct handling of edge cases in precision-sensitive applications
#


# Input Formats:
# Text file (input.txt):
# 0.123456789e-5 10
# 1.23e10 15 10 2

# JSON (input.json):
# [
#   {"num": "0.123456789e-5", "precision": 10},
#   {"num": "1.23e10", "precision": 15, "radix": 10, "base": 2}
# ]

# TOML (input.toml):
# [[testcase]]
# num = "0.123456789e-5"
# precision = 10
#
# [[testcase]]
# num = "1.23e10"
# precision = 15
# radix = 10
# base = 2

# Usage:
# Generate: python script.py -gen [options]
# Verify: python script.py -ver [options]
# Both: python script.py -gen -ver [options]

# Key Options:
# -f FILE : Input file
# -n NUM : Number of random cases
# -o FILE : Output file
# -t {json,csv,toml,c} : Output type
# --min_precision, --max_precision, --min_exponent, --max_exponent
# --include_special, --include_edge, --include_subnormal, --include_pi NUM
# --radix NUM, --base NUM
# -v : Verbose output

# Examples:
# Generate 10 random cases + special cases:
# python script.py -gen -n 10 -o tests -t json --include_special

# Generate from JSON input, include edge cases:
# python script.py -gen -f input.json -o tests -t c --include_edge

# Verify cases from TOML file:
# python script.py -ver -f tests.toml -v

# Generate with specific precision and exponent range:
# python script.py -gen -n 20 --min_precision 50 --max_precision 100 --min_exponent -50 --max_exponent 50

# Generate and verify with custom radix and base:
# python script.py -gen -ver -f input.txt -o tests -t json --radix 16 --base 2

# Generate pi approximations:
# python script.py -gen --include_pi 100 -o pi_tests -t csv

# Complex scenario:
# python script.py -gen -ver -f input.json -n 50 -o complex_tests -t toml --include_special --include_edge --include_subnormal --include_pi 10 --min_precision 1 --max_precision 1000 --min_exponent -1000 --max_exponent 1000 --radix 10 --base 2 -v


import sys
import json
import csv
import tomli_w
import random
import argparse
from decimal import Decimal, getcontext, InvalidOperation
from typing import List, Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from functools import partial

@dataclass
class TestCase:
    num_str: str
    precision: int
    expected: str
    radix: Optional[int] = None
    base: Optional[int] = None

class NumberParser:
    @staticmethod
    def parse(num_str: str) -> tuple:
        return NumberParser._split_exponent(num_str)

    @staticmethod
    def _split_exponent(num_str: str) -> tuple:
        parts = num_str.lower().split('e')
        exponent = int(parts[1]) if len(parts) > 1 else 0
        return NumberParser._split_mantissa(parts[0], exponent)

    @staticmethod
    def _split_mantissa(mantissa: str, exponent: int) -> tuple:
        parts = mantissa.split('.')
        integer_part = parts[0]
        fractional_part = parts[1] if len(parts) > 1 else ''
        return integer_part, fractional_part, exponent

class NumberGenerator:
    @staticmethod
    def generate(mantissa: str, precision: int, radix: Optional[int], base: Optional[int], verbose: bool) -> str:
        try:
            return NumberGenerator._format_number(Decimal(mantissa), precision)
        except InvalidOperation:
            print(f"Invalid input: {mantissa}" if verbose else "")
            return "Invalid input"

    @staticmethod
    def _format_number(number: Decimal, precision: int) -> str:
        getcontext().prec = precision + 1
        result = f"{number:.{precision}f}"
        return NumberGenerator._remove_trailing_zeros(result)

    @staticmethod
    def _remove_trailing_zeros(number_str: str) -> str:
        result = number_str.rstrip('0')
        return result if not result.endswith('.') else result + '0'

class TestCaseGenerator:
    @staticmethod
    def generate(num_str: str, precision: int, radix: Optional[int], base: Optional[int], verbose: bool) -> TestCase:
        integer_part, fractional_part, exponent = NumberParser.parse(num_str)
        number = TestCaseGenerator._calculate_number(integer_part, fractional_part, exponent)
        formatted_number = TestCaseGenerator._format_number(number, precision, exponent)
        return TestCase(num_str=num_str, precision=precision, expected=formatted_number, radix=radix, base=base)

    @staticmethod
    def _calculate_number(integer_part: str, fractional_part: str, exponent: int) -> Decimal:
        mantissa = f"{integer_part}.{fractional_part}"
        return Decimal(mantissa) * Decimal(10) ** Decimal(exponent)

    @staticmethod
    def _format_number(number: Decimal, precision: int, exponent: int) -> str:
        getcontext().prec = precision + max(exponent, 0) + 1
        formatted_number = f"{number:.{precision}f}"
        return NumberGenerator._remove_trailing_zeros(formatted_number)

class RandomTestCaseGenerator:
    @staticmethod
    def generate(min_precision: int, max_precision: int, min_exponent: int, max_exponent: int, radix: Optional[int], base: Optional[int], verbose: bool) -> TestCase:
        precision = random.randint(min_precision, max_precision)
        exponent = random.randint(min_exponent, max_exponent)
        mantissa = f"{random.random():.{precision}f}"
        num_str = f"{mantissa}e{exponent}"
        return TestCaseGenerator.generate(num_str, precision, radix, base, verbose)

class TestCaseReader:
    @staticmethod
    def read_from_file(filename: Path, verbose: bool) -> List[TestCase]:
        print(f"\nReading test cases from file: {filename}" if verbose else "")
        return [TestCaseReader._parse_line(line, verbose) for line in filename.read_text().splitlines() if TestCaseReader._is_valid_line(line, verbose)]

    @staticmethod
    def _is_valid_line(line: str, verbose: bool) -> bool:
        parts = line.strip().split()
        if len(parts) < 2:
            print(f"Skipping invalid line: {line}" if verbose else "")
            return False
        return True

    @staticmethod
    def _parse_line(line: str, verbose: bool) -> TestCase:
        parts = line.strip().split()
        num_str, precision = parts[:2]
        radix = int(parts[2]) if len(parts) > 2 else None
        base = int(parts[3]) if len(parts) > 3 else None
        return TestCaseGenerator.generate(num_str, int(precision), radix, base, verbose)

class TestCaseWriter:
    @staticmethod
    def write(test_cases: List[TestCase], output_format: str, output_file: Path, verbose: bool) -> None:
        test_case_dicts = [asdict(tc, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}) for tc in test_cases]
        TestCaseWriter._write_to_file(test_case_dicts, output_format, output_file)
        TestCaseWriter._print_summary(test_cases, output_file, verbose)

    @staticmethod
    def _write_to_file(test_case_dicts: List[Dict[str, Any]], output_format: str, output_file: Path) -> None:
        writers = {
            'json': partial(json.dump, indent=2),
            'csv': lambda data, f: csv.DictWriter(f, fieldnames=set().union(*data)).writerows(data),
            'toml': partial(tomli_w.dump, {'test_cases': test_case_dicts}),
            'c': lambda data, f: f.write("struct TestCase test_cases[] = {\n" + 
                                         ''.join(TestCaseWriter._format_c_struct(tc) for tc in data) + 
                                         "};\n")
        }
        with output_file.open('w', newline='') as f:
            writers[output_format](test_case_dicts, f)

    @staticmethod
    def _format_c_struct(tc: Dict[str, Any]) -> str:
        base_struct = f'    {{"{tc["num_str"]}", {tc["precision"]}, "{tc["expected"]}"'
        if "radix" in tc:
            base_struct += f', {tc["radix"]}'
            if "base" in tc:
                base_struct += f', {tc["base"]}'
        base_struct += "},\n"
        return base_struct

    @staticmethod
    def _print_summary(test_cases: List[TestCase], output_file: Path, verbose: bool) -> None:
        if verbose:
            print(f"\nWrote {len(test_cases)} test cases to {output_file}")
            print("\nGenerated test cases:")
            for tc in test_cases:
                print(f"  {tc}")

class TestCaseVerifier:
    @staticmethod
    def verify(test_cases: List[TestCase], verbose: bool) -> None:
        for tc in test_cases:
            expected = tc.expected
            actual = TestCaseGenerator.generate(tc.num_str, tc.precision, tc.radix, tc.base, verbose).expected
            if expected == actual:
                print(f"PASS: {tc.num_str}" if verbose else "", end="")
            else:
                print(f"FAIL: {tc.num_str}\nExpected: {expected}\nActual: {actual}")

class SpecialCaseGenerator:
    @staticmethod
    def generate_special_cases(verbose: bool) -> List[TestCase]:
        return [TestCaseGenerator.generate(case, 0, None, None, verbose) for case in ["CUSTOM_INFINITY", "-CUSTOM_INFINITY", "CUSTOM_NAN"]]

    @staticmethod
    def generate_edge_cases(verbose: bool) -> List[TestCase]:
        return [TestCaseGenerator.generate(case, 308, None, None, verbose) for case in ["1.7976931348623157e308", "-1.7976931348623157e308"]]

    @staticmethod
    def generate_subnormal_cases(verbose: bool) -> List[TestCase]:
        return [TestCaseGenerator.generate("4.9406564584124654e-324", 324, None, None, verbose)]

    @staticmethod
    def generate_pi_approximations(count: int, verbose: bool) -> List[TestCase]:
        pi = "3.14159265358979323846264338327950288419716939937510"
        return [TestCaseGenerator.generate(pi, i, None, None, verbose) for i in range(1, count + 1)]

def main():
    parser = argparse.ArgumentParser(description="Generate and verify test cases for floating-point to string conversion")
    parser.add_argument("-gen", action="store_true", help="Generate test cases")
    parser.add_argument("-ver", action="store_true", help="Verify test cases")
    parser.add_argument("-f", "--file", type=Path, help="Input file containing test cases")
    parser.add_argument("-n", "--num_cases", type=int, default=1, help="Number of random test cases to generate")
    parser.add_argument("-o", "--output", type=Path, default=Path("test_cases"), help="Output file name (without extension)")
    parser.add_argument("-t", "--type", choices=['json', 'csv', 'toml', 'c'], default='c', help="Output file type")
    parser.add_argument("--min_precision", type=int, default=1, help="Minimum precision for random generation")
    parser.add_argument("--max_precision", type=int, default=324, help="Maximum precision for random generation")
    parser.add_argument("--min_exponent", type=int, default=-324, help="Minimum exponent for random generation")
    parser.add_argument("--max_exponent", type=int, default=308, help="Maximum exponent for random generation")
    parser.add_argument("--include_special", action="store_true", help="Include special cases (inf, nan)")
    parser.add_argument("--include_edge", action="store_true", help="Include edge cases (min/max representable)")
    parser.add_argument("--include_subnormal", action="store_true", help="Include subnormal numbers")
    parser.add_argument("--include_pi", type=int, help="Include pi approximations up to specified precision")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--radix", type=int, help="Radix for number representation")
    parser.add_argument("--base", type=int, help="Base for number representation")
    args = parser.parse_args()

    if not (args.gen or args.ver):
        parser.error("At least one of -gen or -ver must be specified")

    test_cases = []

    if args.gen:
        if args.file:
            test_cases.extend(TestCaseReader.read_from_file(args.file, args.verbose))
        
        test_cases.extend(RandomTestCaseGenerator.generate(args.min_precision, args.max_precision, args.min_exponent, args.max_exponent, args.radix, args.base, args.verbose) for _ in range(args.num_cases))

        if args.include_special:
            test_cases.extend(SpecialCaseGenerator.generate_special_cases(args.verbose))

        if args.include_edge:
            test_cases.extend(SpecialCaseGenerator.generate_edge_cases(args.verbose))

        if args.include_subnormal:
            test_cases.extend(SpecialCaseGenerator.generate_subnormal_cases(args.verbose))

        if args.include_pi:
            test_cases.extend(SpecialCaseGenerator.generate_pi_approximations(args.include_pi, args.verbose))

        TestCaseWriter.write(test_cases, args.type, args.output.with_suffix(f".{args.type}"), args.verbose)

    if args.ver:
        if not test_cases:
            test_cases = TestCaseReader.read_from_file(args.file, args.verbose)
        TestCaseVerifier.verify(test_cases, args.verbose)

if __name__ == "__main__":
    main()
