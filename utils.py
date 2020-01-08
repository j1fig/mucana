import string


def camel_to_kebab(name):
    tokens = []
    token_index = 0

    for l in name:
        if l in string.ascii_uppercase:
            tokens.append('')
            token_index += 1
        tokens[token_index-1] += l.lower()
    return '-'.join(tokens)


def kebab_to_display(name):
    tokens = name.split('-')
    return ' '.join(t.capitalize() for t in tokens)
