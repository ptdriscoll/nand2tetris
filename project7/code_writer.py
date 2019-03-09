# -*- coding: utf-8 -*- 

"""
This class translates each VM command into assembly code. 
"""

import os

if os.getcwd().endswith('VMTranslator'):
    from vm_translator import assembly_code as asm
    
else:
    import assembly_code as asm


class CodeWriter:
    """
    Translates VM commands into assembly code.
    """
    
    def __init__(self, full_path):
        """
        Initializes virtual RAM for pointers and base address indices, 
        and, if write_to_file=True, opens output file/stream and prepares to write into it.
        """
        
        self._file_open = open(full_path, 'w')        
        self._file_name = ''
        self._jump_count = 0   
        
        self._dispatch = {
            'C_ARITHMETIC': self.write_arithmetic,
            'C_PUSH': self.write_push_pop,
            'C_POP': self.write_push_pop,
            'C_LABEL': None,
            'C_GOTO': None,
            'C_IF': None,
            'C_FUNCTION': None,
            'C_RETURN': None,
            'C_CALL': None,    
        }
    
    def __str__(self):
        to_print = 'Writing file: ' + self._file_name + '\n' 
        return to_print 
    
    def set_file_name(self, fname):
        """
        Informs code writer that translation of a new VM file has started.
        """
        
        self._file_name = fname 
        self._jump_count = 0
        
    def write_arithmetic(self, command):
        """
        Writes assembly code that is a translation of given arithmetic command.
        """
        
        note = '// ' + self._file_name + ': ' + command + '\n'
       
        if command in ['add', 'sub', 'neg']:
            code = asm.math_cmd(asm.math_table[command])
            
        elif command in ['eq', 'gt', 'lt']:
            self._jump_count += 1
            jump = self._file_name + '$JUMP.' + str(self._jump_count)
            code = asm.compare_cmd(asm.math_table[command], jump)  

        #if command is an and, or, not      
        else:
            code = asm.logic_cmd(asm.math_table[command])     

        self._file_open.write(note + code + '\n')    
        return note + code + '\n'             
        
    def write_push_pop(self, command, segment, index):
        """
        Writes assembly code that is the translation of a given command, 
        where command is either:
        - C_PUSH
        - C_POP        
        """
        
        note = '// ' + self._file_name + ': ' 
        note += command + ' ' + segment + ' ' + index + '\n'
        
        static = False
        
        if segment == 'static':
            symbol = self._file_name 
            static = True            
            
        else:        
            symbol = asm.symbol_table[segment]   
        
        if command == 'pop':           
            code = asm.pop_cmd(symbol, index, static=static)    
        
        #if command == 'push'        
        else:
            code = asm.push_cmd(symbol, index, static=static)    
            
        self._file_open.write(note + code + '\n') 
        return note + code + '\n'  

    def write(self, command_type, args):
        """
        Uses command_type passed from parser to call correct write method 
        through self._dispatch mapping dictionary.                
        """        
  
        self._dispatch[command_type](*args)        
        
    def close(self):
        """
        Closes output file.
        """
        
        self._file_open.close()
    
    
    
    
        
