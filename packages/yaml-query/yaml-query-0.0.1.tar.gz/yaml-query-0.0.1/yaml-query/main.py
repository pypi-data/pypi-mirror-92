import os
import sys

import yaml


def fatal(msg, exit_code=1):
    sys.stderr.write("error: " + msg + "\n")
    sys.exit(exit_code)


def parse_args():
    argv = sys.argv[1:]

    if len(argv) == 1:
        return argv[0], None
    elif len(argv) == 2:
        return argv[0], argv[1]

    pretty_argv = "', '".join(argv)
    fatal(f"expected at most 2 arguments, got:\n'{pretty_argv}'")


def validate_filepath(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return
    fatal(f"invalid filepath: '{filepath}'")


def walk_yaml_data(yamlpath, yamldata):
    obj = yamldata

    for segment in yamlpath.split():
        if "[" in segment:
            segment, idx = segment.split("[")
            idx = int(idx[:-1])
            try:
                obj = obj[segment][idx]
            except KeyError:
                fatal(f"key '{segment}' does not exist")
            except IndexError:
                fatal(f"index '{segment}[{idx}]' out of bounds")
        else:
            try:
                obj = obj[segment]
            except KeyError:
                fatal(f"key '{segment}' does not exist")

    return obj


if __name__ == "__main__":
    yamlpath, filepath = parse_args()
    yamldata = None

    if filepath is not None:
        validate_filepath(filepath)
        with open(filepath) as f:
            try:
                yamldata = yaml.safe_load(f)
            except yaml.scanner.ScannerError:
                fatal("invalid yaml input")
    else:
        try:
            yamldata = yaml.safe_load(sys.stdin)
        except yaml.scanner.ScannerError:
            fatal("invalid yaml input")

    output_obj = walk_yaml_data(yamlpath, yamldata)
    yaml.dump(output_obj, sys.stdout)
    sys.stdout.close()
