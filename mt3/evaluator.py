import copy
import inspect
import pprint
from . import lisp

def fold(env, f, x):
    x = copy.copy(x)
    e = lambda k: evaluate(k, env)
    while len(x) > 1:
        x.insert(0, e([f, x.pop(0), x.pop(0)]))
    return x[0]

def lookup(env, pairs, key, default=None):
    for k, v in pairs:
        if evaluate(k, env) == key:
            return evaluate(v, env)
    return evaluate(default, env)

def forever(env, f):
    while True:
        evaluate(f, env)

default_env = {
    '+': lambda env, x, y: x + y,
    '-': lambda env, x, y: x - y,
    '*': lambda env, x, y: x * y,
    '/': lambda env, x, y: x // y,
    '%': lambda env, x, y: x % y,
    'eq': lambda env, x, y: x == y,
    'gt': lambda env, x, y: x > y,
    'lt': lambda env, x, y: x < y,
    'and': lambda env, x, y: x and y,

    'set': lambda env, x, y: env.update({x: y}),
    'run': lambda env, *_: _[-1],
    'map': lambda env, f, x: [evaluate([f, i], env) for i in x],
    'rep': lambda env, x, n: [x for _ in range(n)],
    'fold': fold,
    'lookup': lookup,
    'showenv': lambda env: pprint.pprint(env),
    'out': lambda env, x: pprint.pprint(x),
    'forever': forever,
    'if': lambda env, cond, t, f: evaluate(t, env) if cond else evaluate(f, env),
    '!': lambda env, l, i: l[i],
    ':': lambda env, *_: list(_),
    'last': lambda env, l: l[-1]
}

def evaluate(code, env=default_env):
    if isinstance(code, (str, int)):
        if code in env:
            return env[code]
        return code

    if inspect.isfunction(code):
        return code

    f = code[0]
    if f == "'":
        # indicates that we don't want to evaluate
        return code[1:]

    if not isinstance(f, list) and f in env:
        f = env[f]

    args = [evaluate(i, env) for i in code[1:]]

    if isinstance(f, list):
        if not isinstance(f[0], list) and f[0] in env:
            new_env = copy.copy(env)
            new_stuff = {f"#{n}": evaluate(code[n], env) for n in range(1, len(code))}
            new_env.update(new_stuff)
            return evaluate(f, new_env)
        return code
    elif inspect.isfunction(f):
        return f(env, *args)
    else:
        return code

def run_file(fn, env):
    with open(fn) as f:
        return evaluate(lisp.parse_expr(f.read()), env)
