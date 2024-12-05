
import sympy as sp
import itertools
import qiskit.quantum_info as qi
import typing

def CounterXYZ(pauli_string_list):
    XY_tuple = [(stabilizer.count('-'),stabilizer.count('X'),stabilizer.count('Y'),stabilizer.count('Z')) for stabilizer in pauli_string_list]
    count_dict = {}
# Counting elements
    for element in XY_tuple:
        if element in count_dict:
            count_dict[element] += 1
        else:
            count_dict[element] = 1
    #print(count_dict)
    return count_dict

def generator2stabilizer(generator_set, to_label=True):

    G_qi = [qi.Pauli(G) for G in generator_set]
    n_qubit = G_qi[0].num_qubits
    S_qi = []
    for n_ele in range(len(G_qi)+1):
        for subset in itertools.combinations(G_qi, n_ele):
            stabilizer = qi.Pauli('I'*n_qubit)
            for element in subset:
                stabilizer = stabilizer @ element
            S_qi.append(stabilizer)



    return [S.to_label() for S in S_qi] if to_label else S_qi

def get_poly_from_code(generator_set, logical_operator):

    X_L, Z_L = qi.Pauli(logical_operator['X']), qi.Pauli(logical_operator['Z'])
    Y_L = 1j * Z_L @ X_L

    S_qi = generator2stabilizer(generator_set=generator_set, to_label=False)
    stabilizer_set = [S.to_label() for S in S_qi] 
    dict_p_suc = CounterXYZ(stabilizer_set)

    logical_X_qi = [S @ X_L for S in S_qi]
    logical_X_set = [ele.to_label() for ele in logical_X_qi]
    dict_X = CounterXYZ(logical_X_set)

    logical_Z_qi = [S @ Z_L for S in S_qi]
    logical_Z_set = [ele.to_label() for ele in logical_Z_qi]
    dict_Z = CounterXYZ(logical_Z_set)

    logical_Y_qi = [S @ Y_L for S in S_qi]
    logical_Y_set = [ele.to_label() for ele in logical_Y_qi]
    dict_Y = CounterXYZ(logical_Y_set)

    poly_dicts = {'p': dict_p_suc, 'X': dict_X, 'Y': dict_Y, 'Z': dict_Z}

    return poly_dicts

def poly_dicts_to_sympy(poly_dicts, y_value=None):
    x = sp.Symbol('x', real=True)
    y = sp.Symbol('y', real=True)
    z = sp.Symbol('z', real=True)

    def dict_to_sympy(poly_dict):
        poly_sp = 0
        for ele in poly_dict:
            coef = poly_dict[ele]
            poly_sp += (-1)**ele[0] * x**ele[1] * y**ele[2] * z**ele[3] * coef
        return poly_sp
    
    p_poly = dict_to_sympy(poly_dicts['p'])
    X_poly = dict_to_sympy(poly_dicts['X'])
    Y_poly = dict_to_sympy(poly_dicts['Y'])
    Z_poly = dict_to_sympy(poly_dicts['Z'])

    if y_value is None:
        return p_poly, X_poly/p_poly, Y_poly/p_poly, Z_poly/p_poly
    else:
        return p_poly.subs(y, y_value), (X_poly/p_poly).subs(y, y_value), (Y_poly/p_poly).subs(y, y_value), (Z_poly/p_poly). subs(y, y_value)
    



def get_stabilizer_code(code_name: str) -> typing.Tuple[list[str], typing.Union[dict, list[dict]]]:

    if code_name == '15_RM':
        generator_set = [
                        'ZIZIZIZIZIZIZIZ',
                        'IZZIIZZIIZZIIZZ',
                        'IIIZZZZIIIIZZZZ',
                        'IIIIIIIZZZZZZZZ',
                        'IIZIIIZIIIZIIIZ',
                        'IIIIZIZIIIIIZIZ',
                        'IIIIIZZIIIIIIZZ',
                        'IIIIIIIIIZZIIZZ',
                        'IIIIIIIIIIIZZZZ',
                        'IIIIIIIIZIZIZIZ',
                        'XIXIXIXIXIXIXIX',
                        'IXXIIXXIIXXIIXX',
                        'IIIXXXXIIIIXXXX',
                        'IIIIIIIXXXXXXXX']
        logical_operator = {'Z': 'ZZZZZZZZZZZZZZZ', 'X': 'XXXXXXXXXXXXXXX'}
    
    elif code_name == '7_Steane':
        generator_set = ['XXXXIII', 'XXIIXXI', 'XIXIXIX', 'ZZZZIII', 'ZZIIZZI', 'ZIZIZIZ']
        logical_operator = {'Z':'ZZZZZZZ','X':'XXXXXXX'}

    
    elif code_name == '5_1_3':
        generator_set = ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']
        logical_operator = {'Z':'ZZZZZ','X':'XXXXX'}

    elif code_name == '12_2_4':
        generator_set = ['IZIZZZIIZZII',
                        'ZIIIIZZZZIZI',
                        'IIZZIIIZIZZZ',
                        'ZZIZIZIIIIZZ',
                        'IIZIZIZZZZII',
                        'XXXIIIXXXIII',
                        'IIXXXIIIXXXI',
                        'XIIIXXXIIIXX',
                        'XXXXXXIIIIII',
                        'IIIIIIXXXXXX']
        logical_operator = [{"X": "IIIIXXIXIIIX", "Z": "IIZZIIZIIIIZ"}, {"X": "IIIIIXIXXIXI", "Z": "IZIZIIZIIIZI"}]
    
    elif code_name == '3a':
        generator_set = ['XZI', 'ZXX']
        logical_operator = {'Z':'IIX','X':'IZZ'}
    elif code_name == '3a_y':
        generator_set = ['ZYI', 'YZZ']
        logical_operator = {'Z': 'IZY', 'X': 'IIX'}
    elif code_name == '4a':
        generator_set = ['XZII', 'ZXZX', 'IZXI']
        logical_operator = {'Z':'IIIX','X':'IZIZ'}


    elif code_name == '6a':
        generator_set =  ['YYZZII', 'ZIXZZI', 'IZZXZI', 'XZIZXZ', 'XZZIZX']
        logical_operator = {'Z':'XZZIII','X':'ZZIIZZ'}

    elif code_name == '14_2_2':
        generator_set = [
            'XIXIXIXXIXIXIX',
            'IXXIIXXIXXIIXX',
            'IIIXXXXIIIXXXX',
            'IZZZZIIIIIIIII',
            'ZIZZIZIIIIIIII',
            'ZZIZIIZIIIIIII',
            'ZZIIIIIZZIIIII',
            'ZIZIIIIZIZIIII',
            'ZIIZIIIZIIZIII',
            'IZZIIIIIIIZZII',
            'IIZZIIIZIIIIZI',
            'IZIZIIIZIIIIIZ'
        ]

        logical_operator = [{'X': 'XXXXXXXIIIIIII', 'Z': 'ZZZZZZZIIIIIII'}, {'X': 'IIIIIIIXXXXXXX', 'Z': 'IIIIIIIZZZZZZZ'}]

    else:
        raise ValueError("the input code name has not been implemented.")
    return (generator_set, logical_operator)