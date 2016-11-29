#!/usr/bin/env python
'''
   Evaluate a boolean expression given a dictionary of values.
       evaluate_boolean_expression(s, the_dict):
       Where: s is the expression (e.g., "goal1 and (goal2 or goal3)"
              the_dict is a dictionary of boolean values, e.g., the_dict['goal1'] = True.
       See test cases in __main__
'''
str_to_token = {'True':True,
                'False':False,
                'and':lambda left, right: left and right,
                'or':lambda left, right: left or right,
                '(':'(',
                ')':')'}

empty_res = True


def create_token_lst(s, str_to_token=str_to_token):
    """create token list:
    'True or False' -> [True, lambda..., False]"""
    s = s.replace('(', ' ( ')
    s = s.replace(')', ' ) ')

    return [str_to_token[it] for it in s.split()]


def find(lst, what, start=0):
    return [i for i,it in enumerate(lst) if it == what and i >= start]


def parens(token_lst):
    """returns:
        (bool)parens_exist, left_paren_pos, right_paren_pos
    """
    left_lst = find(token_lst, '(')

    if not left_lst:
        return False, -1, -1

    left = left_lst[-1]

    #can not occur earlier, hence there are args and op.
    right = find(token_lst, ')', left + 4)[0]

    return True, left, right


def bool_eval(token_lst):
    """token_lst has length 3 and format: [left_arg, operator, right_arg]
    operator(left_arg, right_arg) is returned"""
    return token_lst[1](token_lst[0], token_lst[2])


def formatted_bool_eval(token_lst, empty_res=empty_res):
    """eval a formatted (i.e. of the form 'ToFa(ToF)') string"""
    if not token_lst:
        return empty_res

    if len(token_lst) == 1:
        return token_lst[0]

    has_parens, l_paren, r_paren = parens(token_lst)

    if not has_parens:
        return bool_eval(token_lst)

    token_lst[l_paren:r_paren + 1] = [bool_eval(token_lst[l_paren+1:r_paren])]

    return formatted_bool_eval(token_lst, bool_eval)


def nested_bool_eval(s):
    """The actual 'eval' routine,
    if 's' is empty, 'True' is returned,
    otherwise 's' is evaluated according to parentheses nesting.
    The format assumed:
        [1] 'LEFT OPERATOR RIGHT',
        where LEFT and RIGHT are either:
                True or False or '(' [1] ')' (subexpression in parentheses)
    """
    return formatted_bool_eval(create_token_lst(s))

def evaluate_boolean_expression(s, the_dict):
    left = s.count('(')
    right = s.count(')')
    if left != right:
        print 'ERROR unbalanced parens'
        exit(1)
    
    for item in the_dict:
        if item in s:
            value = '%r' % the_dict[item]
            s = s.replace(item, value)

    tokens = ['(',')','and','AND','or','OR','True','False'] 
    remains = s
    for t in tokens:
        remains = remains.replace(t,'')
    if len(remains.strip()) > 0:
        print('ERROR: unknown token: %s' % remains)
        exit(1)
    
    return nested_bool_eval(s) 

if __name__ == "__main__":
    t_dict = {}
    t_dict['goal1'] = True
    t_dict['goal2'] = False
    t_dict['goal3'] = True
    t_dict['goal4'] = True

    t_string = 'goal1 and (goal2 or goal3) and goal4'
    print('%s evaluates to %r' % (t_string,  evaluate_boolean_expression(t_string, t_dict)))

    t_string = 'goal1 or ((goal2 or goal3) and goal4)'
    print('%s evaluates to %r' % (t_string,  evaluate_boolean_expression(t_string, t_dict)))

    t_string = 'goal1 and (goal2 or goal3) or goal7'
    print evaluate_boolean_expression(t_string, t_dict)
