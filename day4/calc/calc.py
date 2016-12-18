import re


def calc(formula):
    formula = re.sub(' ', '', formula)
    formula_ret = 0
    match_brackets = re.search('\([^()]+\)', formula)
    if match_brackets:
        calc_result = calc(match_brackets.group().strip("(,)"))
        formula = formula.replace(match_brackets.group(), str(calc_result))
        return calc(formula)
    else:
        while re.findall("[*/]", formula):
            formula = formula.replace('--', '+').replace('++', '+').replace('-+', '-').replace('+-', '-')
            get_formula = re.search("[.\d]+[*/]+[-]?[.\d]+", formula)
            if get_formula:
                get_formula_str = get_formula.group()
                if get_formula_str.count("*"):
                    formula_list = get_formula_str.split("*")
                    ret = float(formula_list[0]) * float(formula_list[1])
                else:
                    formula_list = get_formula_str.split("/")
                    ret = float(formula_list[0]) / float(formula_list[1])
                formula = formula.replace(get_formula_str, str(ret)).replace('--', '+').replace('++', '+')
        formula = re.findall('[-]?[.\d]+', formula)
        for num in formula:
            formula_ret += float(num)
    return formula_ret
calc_str = input('>>>')
# calc_str = '1-2*((60-30+(-40-5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
formula_result = calc(calc_str)
print(formula_result)
