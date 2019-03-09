# -*- coding: utf-8 -*- 

"""
The VM Translator accepts a single command line parameter, Xxx or Xxx.vm, where either 
Xxx is a directory containing one more .vm files, or Xxx.vm is a file containing VM code.

FROM vm_translator DIRECTORY:
-prompt> python VMTranslator.py Xxx
-prompt> python VMTranslator.py Xxx.vm

FROM VMTranslator DIRECTORY one level up:
-prompt> python -m vm_translator Xxx
-prompt> python -m vm_translator Xxx.vm

The translator then translates the Xxx.vm file, or in case of a directory all .vm files. The result
is always a single assembly-language file named Xxx.asm. 
"""

import os, sys, ntpath 

if os.getcwd().endswith('VMTranslator'):
    from vm_translator import vm_parser
    from vm_translator import code_writer
    
else:
    import vm_parser
    import code_writer
    

def translate_file(file, file_full_path, writer):
    """
    Accepts name of virtual machine code file.
    Returns translation into assembly code, as a string. 
    """
    
    fname = file.replace('.vm', '')
    writer.set_file_name(fname)
    file_parser = vm_parser.Parser(file_full_path)
    
    while file_parser.has_more_commands():
        file_parser.advance()
        command_type = file_parser.command_type()
        args = file_parser.get_args()
        writer.write(command_type, args)
 
def main():
    """
    Checks command argument to see if its a directory of virtual machine code files or just one file.
    Writes translated assembly code to one file, whether working with a directory of vm files or just one file.
    The translated file, with an .asm extension, is saved to the same directory where the vm file/s reside.
    """

    #get directory or file from arg and, if on Windows, convert to back slashes
    to_translate = sys.argv[1].strip()  
    to_translate = os.path.abspath(to_translate) 
    
    #add trailing slash to last directory if it's missing
    if not to_translate.endswith('.vm'):
        to_translate = ntpath.join(to_translate, '')   
    
    #get name to write to name.asm, using either name.vm or name directory 
    path, tail = ntpath.split(to_translate)    
    fname = tail or ntpath.basename(path)
    
    to_write = os.path.join(path, fname.replace('.vm', '') + '.asm')      
    writer = code_writer.CodeWriter(to_write)
    
    if os.path.isdir(to_translate):
        print('Translating .vm files in directory: ' + to_translate)
        
        for root, dirs, files in os.walk(to_translate):
            for file in files:
                if file.endswith('.vm'):
                    file_full_path = os.path.join(root, file)
                    translate_file(file, file_full_path, writer)
        
    else:
        print('Translating file: ' + to_write) 
        translate_file(fname, to_translate, writer)
    
    writer.close()
    print('Translation completed')    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()   