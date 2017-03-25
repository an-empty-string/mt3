import collections

def parse_expr(e):
    stack = collections.deque()
    result = []
    word = ""
    for c in e:

        if c in "( \n\r)" and word != "":
            print(word)
            if word.isnumeric():
                word = int(word)
            stack.append(word)
            word = ""

        if c == "(":
            stack.append(c)
        elif c == ")":
            current_expr = collections.deque()
            while True:
                current_value = stack.pop()
                if current_value == '(':
                    break
                else:
                    current_expr.appendleft(current_value)
            stack.append(list(current_expr))
        elif c in " \r\n":
            pass
        else:
            word += c

    return stack.pop()
