import sys
from tokenizer import Tokenizer
from parser_1 import Parser
from translator import Translator
from interpreter import Interpreter
from postprocessing import unite, set_com_reg, make_jumps, modify_jump_var, replace_register, delete_temp_register

def show_help():
    print('simple pascal interpret for version 1.0')


def main(in_file, out_file):
    '''
    if len(sys.argv) == 1:
        show_help()
        return
    text = open(sys.argv[1], 'r').read()
    '''

    ''''''
    '''
    text = open(in_file, 'r').read()
    f = open("temp1.txt", 'w')
    f.write("mm3\n\n")
    f.write("[config]\n")
    lines = []
    lines = lines=text.split('\n')
    for i in range(len(lines)):
        f.write(";"+lines[i]+"\n")
    f.write("\n\n[code]\n")
    f.close()
    '''
    with open(in_file, 'r') as fp:
        for len_text, line in enumerate(fp):
            pass

    text = open(in_file, 'r').read()
    
    min_memory = len_text*10
    f = open("temp1.txt", 'w')
    f.write("mm3\n\n")
    f.write("[config]\n\n")
    f.write("\n\n[code]\n")
    f.close()
    
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    
    
    temp_memory_arr = parser.for_memory
    temp_functions_list = parser.functions_list
    #print(parser.for_memory)
    tokenizer = Tokenizer(text)
    parser = Parser(tokenizer)
    translator = Translator(parser, min_memory)

    translator.memory_arr = temp_memory_arr
    translator.functions_list = temp_functions_list

    print(translator.memory_arr)
    translator.translate()
    translator.file.close()
    
    unite("temp_function.txt", "temp1.txt", "temp2.txt")
    set_com_reg("temp2.txt", "temp3.txt")
    make_jumps("temp3.txt", "temp4.txt")
    modify_jump_var("temp4.txt", "temp5.txt")
    replace_register("temp5.txt", "temp6.txt")
    delete_temp_register("temp6.txt", out_file)
    #print(translator.EQUALDICT)
    


if __name__ == "__main__":
    main()
