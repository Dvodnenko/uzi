from typing import List, Tuple, Dict


def parse_cli_args(
        argv: List[str]
) -> Tuple[List[str], Dict[str, str], List[str]]:
    args = []
    kwargs = {}
    flags = []
    i = 0

    while i < len(argv):
        token = argv[i]

        if token.startswith("--") and "=" in token:
            key, value = token[2:].split("=", 1)
            kwargs[key] = value

        elif token.startswith("--"):
            key = token[2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                kwargs[key] = argv[i + 1]
                i += 1
            else:
                flags.append(key)

        elif token.startswith("-") and len(token) > 1:
            for ch in token[1:]:
                flags.append(ch)

        else:
            args.append(token)

        i += 1

    return args, kwargs, flags
