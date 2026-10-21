def save_history(history):
    with open("history.txt", "w", encoding="utf-8") as file:
        for item in history:
            file.write(item + "\n")

    print("履歴を保存しました") # 履歴保存

def load_history():
    history = []

    try:
        with open("history.txt", "r", encoding="utf-8") as file:
            for line in file:
                history.append(line.strip())

    except FileNotFoundError:
        pass

    return history # 履歴読み込み


def tokenize(expression):
    tokens = []
    number = ""

    for char in expression:
        if char.isdigit() or char == ".":
            number += char

        else:
            if number:
                tokens.append(number)
                number = ""

            if char in "+-*/^%()":
                tokens.append(char)
            elif char.isspace():
                continue
            else:
                raise ValueError("不正な文字です")
            
    if number:
        tokens.append(number)

    # ここから追加
    result = []

    for token in tokens:
        if token not in "+-*/^%()":
            result.append(float(token))
        else:
            result.append(token)

    return result


def parse_operator(tokens, index):
    token = tokens[index]

    if token in "+-*/^%":
        return token, index + 1

    raise ValueError("演算子が必要です")

def evaluate_simple(left, operator, right):
    if operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return left * right
    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("0で割ることはできません")
        return left / right
    elif operator == "%":
        if right == 0:
            raise ZeroDivisionError("0で割ることはできません")
        return left % right
    elif operator == "^":
        return left ** right

    raise ValueError("不正な演算子です")


def parse_add_sub(tokens, index):
    result, index = parse_mul_div_mod(tokens, index)

    while index < len(tokens):
        if tokens[index] not in "+-":
            break

        operator, index = parse_operator(tokens, index)
        right, index = parse_mul_div_mod(tokens, index)

        result = evaluate_simple(result, operator, right)

    return result, index

def parse_mul_div_mod(tokens, index):
    result, index = parse_power(tokens, index)

    while index < len(tokens):
        if tokens[index] not in "*/%":
            break

        operator, index = parse_operator(tokens, index)
        right, index = parse_power(tokens, index)

        result = evaluate_simple(result, operator, right)

    return result, index

def parse_power(tokens, index):
    negative = False

    if tokens[index] == "-":
        negative = True
        index += 1

    result, index = parse_primary(tokens, index)

    if index < len(tokens) and tokens[index] == "^":
        operator, index = parse_operator(tokens, index)
        right, index = parse_power(tokens, index)

        result = evaluate_simple(result, operator, right)

    if negative:
        result = -result

    return result, index

def parse_primary(tokens, index):
    if tokens[index] == "+":
        return parse_primary(tokens, index + 1)
    
    if tokens[index] == "-":
        result, index = parse_primary(tokens, index + 1)
        return -result, index
    
    if isinstance(tokens[index], float):
        return tokens[index], index + 1

    if tokens[index] == "(":
        result, index = parse_add_sub(tokens, index + 1)

        if index >= len(tokens) or tokens[index] != ")":
            raise ValueError("括弧の対応が正しくありません")

        return result, index + 1

    raise ValueError("数値または括弧が必要です")


def evaluate_expression(expression):
    tokens = tokenize(expression)

    if not tokens:
        raise ValueError("式が空です")

    result, index = parse_add_sub(tokens, 0)

    if index != len(tokens):
        raise ValueError("式を最後まで読み取れません")

    return result


def show_history(history):
    if not history:
        print("履歴はありません")
    else:
        print("--- 計算履歴 ---")

        for i, item in enumerate(history, 1):
            print(str(i) + ". " + item) # 履歴を参照

def clear_history(history):
    history.clear()
    print("履歴を削除しました") # 履歴を削除

def use_history(history, number):
    try:
        number = int(number)

        if number < 1 or number > len(history):
            print("履歴番号が無効です")
            return None

        history_item = history[number - 1]
        parts = history_item.split("=")
        result = float(parts[1])
        print("履歴" + str(number) + "を使用:", result)

        return result

    except ValueError:
        print("履歴番号が無効です")
        return None # 履歴を使用
