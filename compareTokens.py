def compareTokens(one, two):
    mismatch = False
    tokens = two.split(' ')
    comparisonTokens = one.split(' ')
    for i in range(len(tokens)):
        if "(" in tokens[i]:
            tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(tokens[i][tokens[i].index("(") + 1:])
        elif ")" in tokens[i]:
            tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(tokens[i][tokens[i].index(")") + 1:])
    difference = 0
    for index, var in enumerate(tokens):
        if var.lower() not in one.lower():
            # edge case: mix and remix are synonymous or original/extended mix is absent in one or another
            if (var.lower() != "remix" and var.lower() != "mix") or ("remix" not in one.lower() and "mix" not in one.lower()) and ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
                # compare index of token lists character by character
                if len(tokens) > index and len(comparisonTokens) > index:
                    common = 0
                    length = min(len(tokens[index]), len(comparisonTokens[index]))
                    for i in range(length):
                        if tokens[index][i] != comparisonTokens[index][i]: break
                        common += 1
                    difference += len(var) - common
                else:
                    difference += len(var)

    if difference/len(one) > 0.15:
        mismatch = True
        return mismatch

    tokens = one.split(' ')
    comparisonTokens = two.split(' ')
    for i in range(len(tokens)):
        if "(" in tokens[i]:tokens[i] = str(tokens[i][0:tokens[i].index("(")]) + str(tokens[i][tokens[i].index("(") + 1:])
        elif ")" in tokens[i]:tokens[i] = str(tokens[i][0:tokens[i].index(")")]) + str(tokens[i][tokens[i].index(")") + 1:])

    difference = 0
    for index, var in enumerate(tokens):
        if var.lower() not in two.lower():
            # edge case: mix and remix are synonymous or original/extended mix is absent in one or another
            if (var.lower() != "remix" and var.lower() != "mix") or ("remix" not in two.lower() and "mix" not in two.lower()) and ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
                # compare index of token lists character by character
                if len(tokens) > index and len(comparisonTokens) > index:
                    common = 0
                    length = min(len(tokens[index]), len(comparisonTokens[index]))
                    for i in range(length):
                        if tokens[index][i] != comparisonTokens[index][i]:break
                        common+=1
                    difference += len(var) - common
                else:
                    difference += len(var)
    if difference / len(one) > 0.15: mismatch = True
    return mismatch