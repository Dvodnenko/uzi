def afk_parser(argv: list[str]) -> tuple:
    """
    Parses argv and returns `args` (positional),
    `kwargs` & `flags` (the ones that starts with dash)
    """

    args = []
    flags = []
    kwargs = {}
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

    return args, flags, kwargs


def sql_parser(argv: list[str]) -> dict:

    filters = {}
    i = 0

    while i < len(argv):
        token = argv[i]

        if token.startswith("--") and "=" in token:
            key, value = token[2:].split("=", 1)
            if filters.get(key):
                filters[key].append(value)
            else:
                filters[key] = [value]

        elif token.startswith("--"):
            key = token[2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                if filters.get(key):
                    filters[key].append(argv[i + 1])
                else:
                    filters[key] = [argv[i + 1]]
                i += 1

        i += 1
    
    return filters
