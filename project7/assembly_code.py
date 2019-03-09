# -*- coding: utf-8 -*- 

"""
Dictionaries and functions that map virtual-machine commands to assembly-code snippets. 
"""


symbol_table = {
    'local': 'LCL', 
    'constant': 'constant',
    'argument': 'ARG', 
    'this': 'THIS', 
    'that': 'THAT', 
    'temp': 'R5',
    'pointer': 'R3'
}

math_table = {
    'add': 'D+M',
    'sub': 'M-D',
    'neg': '-M',
    'eq': 'EQ',
    'gt': 'GT',
    'lt': 'LT',
    'and': '&',
    'or': '|',
    'not': '!'    
}

def pop_cmd(segment, index, static=False):
    """
    Accepts memory segment and memory segment index,
    and returns assembly code for pop command.
    """
    
    code = ''''''
    
    if static:
        code += '''@{segment}.{index}
        D=A    
        '''.format(segment=segment, index=index)
    
    else: 
        code += '''@{index}
        D=A
        @{segment}
        '''.format(index=index, segment=segment)
        
        if segment == 'R3' or segment == 'R5':
            code += '''D=D+A
            '''  

        else:
            code += '''D=D+M
            '''         
        
    code += '''@R13
    M=D
    @SP
    M=M-1
    A=M
    D=M
    @R13
    A=M
    M=D
    '''
    
    return code.replace(' ','')
    
def push_cmd(segment, index, static=False):
    """
    Accepts memory segment and memory segment index,
    and returns assembly code for push command.    
    """
    
    code = ''''''
    
    if static:
        code += '''@{segment}.{index}
        D=M
        '''.format(segment=segment, index=index) 
    
    else:     
        code += '''@{index}
        D=A
        '''.format(index=index)
        
        if segment != 'constant':        
            code += '''@{segment}
            '''.format(segment=segment)  
            
            if segment == 'R3' or segment == 'R5':
                code += '''A=D+A
                D=M
                '''        
    
            else:
                code += '''A=D+M
                D=M
                ''' 
    
    code += '''@SP
    A=M
    M=D
    @SP
    M=M+1
    '''

    return code.replace(' ','')

def math_cmd(command):
    """
    Accepts math command string and returns assembly code for math operation, 
    and returns assembly code:
    - command = D+M, M-D or -M
    - command string = add, sub or neg
    """
    
    if command == '-M':
        code = '''@SP
        A=M-1
        M=-M
        '''    
    else:
        code = '''@SP
        M=M-1
        A=M
        D=M
        A=A-1
        M={command}
        '''.format(command=command)
    
    return code.replace(' ','')    
    
def compare_cmd(command, jump):
    """
    Accepts two string arguments and returns assembly code for comparison operation, 
    and returns assembly code:
    - command = EQ, GT or LT
    - command string = eq, gt or lt
    - jump label includes incremented number each time a jump is used by CodeWriter instance    
    """
    
    code = '''@SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=M-D
    M=-1
    @{jump}
    D;J{command}
    @SP
    A=M-1
    M=0
    ({jump})
    '''.format(command=command,   
               jump=jump)
               
    return code.replace(' ','')
    
def logic_cmd(command):
    """
    Accepts logic command string and returns assembly code for logical operation, 
    and returns assembly code:
    - command = &, |, !
    - command string = and, or, not 
    """
    
    if command == '!':
        code = '''@SP
        A=M-1
        M=!M
        '''    
    else:
        code = '''@SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D{command}M
        '''.format(command=command)
    
    return code.replace(' ','')  