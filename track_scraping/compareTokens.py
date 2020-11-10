def compareTokens(one, two):
    mismatch = False
    # string manipulations
    one = one.lower().replace("(", "").replace(")", "").replace("-", ' ').replace(" extended", "").replace(" extended mix", "").replace(" original mix", "")
    two = two.lower().replace("(", "").replace(")", "").replace("-", ' ').replace(" extended", "").replace(" extended mix", "").replace(" original mix", "")

    # test one
    tokens = two.split(' ')
    comparisonTokens = one.split(' ')
    difference = 0
    for index, var in enumerate(tokens):
        if var.lower() not in one.lower() and (var.lower() != "remix" and var.lower() != "mix") or ("remix" not in one.lower() and "mix" not in one.lower()) and ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
            # compare index of token lists character by character
            if len(tokens) > index and len(comparisonTokens) > index:
                common = 0
                length = min(len(tokens[index]), len(comparisonTokens[index]))
                for i in range(length):
                    if tokens[index][i] != comparisonTokens[index][i]: break
                    common += 1
                difference += len(var) - common
            else: difference += len(var)

    if difference/len(one) > 0.15:
        mismatch = True
        return mismatch
    # test two
    tokens = one.split(' ')
    comparisonTokens = two.split(' ')
    difference = 0
    for index, var in enumerate(tokens):
        if var.lower() not in two.lower() and (var.lower() != "remix" and var.lower() != "mix") or ("remix" not in two.lower() and "mix" not in two.lower()) and ('extended' not in var.lower() and 'original' not in var.lower() and var.lower() != 'mix'):
            # compare index of token lists character by character
            if len(tokens) > index and len(comparisonTokens) > index:
                common = 0
                length = min(len(tokens[index]), len(comparisonTokens[index]))
                for i in range(length):
                    if tokens[index][i] != comparisonTokens[index][i]:break
                    common+=1
                difference += len(var) - common
            else: difference += len(var)
    if difference / len(one) > 0.15: mismatch = True
    return mismatch