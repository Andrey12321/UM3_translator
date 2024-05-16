from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, Program, \
    Block, VarDecl, ProcedureDecl, ProcedureCall, Boolean, Condition, Then, Else, FunctionDecl, FunctionCall, WhileLoop, \
    Continue, Break, AST
from callstack import CallStack, Frame, FrameType
from parser_1 import Parser
from semantic_analyzer import SemanticAnalyzer
from tokens import TokenType
from visitor import Visitor
from errors import RuntimeError, ErrorCode, ContinueError, BreakError

import sys


class Translator(Visitor):
    """
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree
    """

    def __init__(self, parser: Parser, min_memory):
        self.parser = parser
        self.analyzer = SemanticAnalyzer()
        self.callstack = CallStack()
        
        '''
        '''
        
        self.file = open("temp1.txt", 'a')
        self.memory_counter = min_memory + 1
        self.memory_arr = []
        self.functions_list = []

        self.MEMORYDICT = {
            "0": f"{min_memory:04x}",
            "-1": f"{(min_memory + 1):04x}"
        }  
        print(self.MEMORYDICT)
        self.temp_memory_counter = 0x8fff
        self.TEMPMEMORYDICT = {}

        self.command_register  = 0

        self.functions_param_dict = {}
        self.used_function_arr = []
        self.function_memory_counter = 0x3fff

        self.jump_counter = 0
        self.else_counter = 0
        self.while_arr = []
        self.if_arr = []
        self.else_stack = []
        self.JUMPDICT = {}
        self.STRDICT = []
        self.Funcnames = []
        self.Funcvariables = {}
        self.Functionarguments = {}
        self.Functionjump = {}
        self.close = []
        self.Globalvariables = {}
        

        '''
        '''


    def error(self, error_code: ErrorCode, token):
        raise RuntimeError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def log(self, msg):
        '''
        print(msg)
        '''

    def visit_binop(self, node: BinOp):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        left = node.left
        right = node.right
        # todo type checker
        if node.op.type is TokenType.PLUS:
            '''
            '''
            '''
            #левая переменная?
            isinstance(left,Var)
            not(isinstance(left,Var))
            #правая переменная?
            isinstance(right,Var)
            not(isinstance(right,Var))
            #левая в TEMPMEMORYDICT?
            str(left_val) in self.TEMPMEMORYDICT
            not(str(left_val) in self.TEMPMEMORYDICT)
            #правая в TEMPMEMORYDICT?
            str(right_val) in self.TEMPMEMORYDICT
            not(str(right_val) in self.TEMPMEMORYDICT)
            '''
            #if and and and :

            #левая переменная? #правая переменная? #левая в TEMPMEMORYDICT? #левая в TEMPMEMORYDICT?
            
            self.temp_memory_counter += 1
            self.command_register += 1
            
            

            if (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and not(str(right_val) in self.TEMPMEMORYDICT)):
                
                string = ("01 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["  
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    str(left_val) + " + " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                
                #----
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and str(right_val) in self.TEMPMEMORYDICT):
                
                string = ("01 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["  
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    str(left_val) + " + [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                

                #---+
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and not(str(right_val) in self.TEMPMEMORYDICT)):
                
                string = ("01 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] := [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] + " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                
                #--+-
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and str(right_val) in self.TEMPMEMORYDICT):
                
                string = ("01 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] := [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] + [" + 
                    self.TEMPMEMORYDICT[(str(right_val))] + "] " + "|| " + '%04d' % self.command_register + "\n")
                
                #--++
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                not(str(left_val) in self.TEMPMEMORYDICT)):
                string = ("01 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    (str(left_val)) + " + " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-+--
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                str(left_val) in self.TEMPMEMORYDICT):
                string = ("01 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["  
                    + format(self.temp_memory_counter, '04x') + "] := [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] + " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-++-   
            
            
            elif (isinstance(left,Var) and not(isinstance(right,Var))
                   and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("01 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["  
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    (str(node.left.name)) + " + " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #+---

            elif (isinstance(left,Var) and not(isinstance(right,Var)) 
                   and str(right_val) in self.TEMPMEMORYDICT):
                string = ("01 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    (str(node.left.name)) + " + [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #+--+
            
            
            elif (isinstance(left,Var) and isinstance(right,Var)):
                string = ("01 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] := " +
                    (str(node.left.name)) + " + " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #++--
            
            else:
                print("\n\n\n ERRRRRRRRRORRRRRRR  \n\n\n")
                string ="ERRROR in Plus\n"
            
            

            self.TEMPMEMORYDICT[str(left_val + right_val)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)

            return left_val + right_val
        
        elif node.op.type is TokenType.MINUS:


            self.temp_memory_counter += 1

            self.command_register += 1

            if (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("02 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " - " + 
                    str(right_val) + " " + "|| " + '%04d' % self.command_register + "\n")
                #----
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("02 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " - [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #---+
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("02 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] - " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #--+-
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and str(right_val) in self.TEMPMEMORYDICT):
                string = ("02 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] - [" + 
                    self.TEMPMEMORYDICT[(str(right_val))] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #--++
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                not(str(left_val) in self.TEMPMEMORYDICT)):
                string = ("02 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(left_val)) + " - " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-+--
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                str(left_val) in self.TEMPMEMORYDICT):
                string = ("02 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] - " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-++-   
            
            
            elif (isinstance(left,Var) and not(isinstance(right,Var))
                   and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("02 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " - " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #+---

            elif (isinstance(left,Var) and not(isinstance(right,Var)) 
                  and str(right_val) in self.TEMPMEMORYDICT):
                string = ("02 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " - [" +
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #+--+
            
            
            elif (isinstance(left,Var) and isinstance(right,Var)):
                string = ("02 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " - " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #++--
            
            else:
                print("\n\n\n ERRRRRRRRRORRRRRRR \n\n\n")
                string = "ERRROR in MINUS\n"

            self.TEMPMEMORYDICT[str(left_val - right_val)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)

            return left_val - right_val
        
        elif node.op.type is TokenType.MUL:

            self.temp_memory_counter += 1
            self.command_register += 1

            if (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("03 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " * " + 
                    str(right_val) + " " + "|| " + '%04d' % self.command_register + "\n")
                #----
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("03 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " * [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #---+
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("03 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] * " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #--+-
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and str(right_val) in self.TEMPMEMORYDICT):
                string = ("03 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] * [" + 
                    self.TEMPMEMORYDICT[(str(right_val))] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #--++
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                not(str(left_val) in self.TEMPMEMORYDICT)):
                string = ("03 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(left_val)) + " * " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-+--
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                str(left_val) in self.TEMPMEMORYDICT):
                string = ("03 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] * " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-++-   
            
            
            elif (isinstance(left,Var) and not(isinstance(right,Var)) 
                   and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("03 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " * " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #+---

            elif (isinstance(left,Var) and not(isinstance(right,Var)) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("03 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " * [" +
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #+--+
            
            
            elif (isinstance(left,Var) and isinstance(right,Var)):
                string = ("03 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " * " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #++--
            
            else:
                print("\n\n\n ERRRRRRRRRORRRRRRR \n\n\n")
                string = "ERRROR in MUL\n"
            


            self.TEMPMEMORYDICT[str(left_val * right_val)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)

            return left_val * right_val
        
        elif node.op.type is TokenType.INTEGER_DIV:
            '''
         !!!!
         Если выполняется операция деления, в оперативную память записываются
         два результата: частное  в ячейку c адресом A3, остаток  в следующую
         ячейку, по адресу (A3+1) mod 16^4
         !!!!
            '''

            self.temp_memory_counter += 1
            self.command_register += 1

            if (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " div " + 
                    str(right_val) + " " + "|| " + '%04d' % self.command_register + "\n")
                #----
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    str(left_val) + " div [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #---+
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] div " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #--+-
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] div [" + 
                    self.TEMPMEMORYDICT[(str(right_val))] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #--++
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                not(str(left_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(left_val)) + " div " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-+--
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                str(left_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] div " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-++-   
            
            
            elif (isinstance(left,Var) and not(isinstance(right,Var)) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " div " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #+---

            elif (isinstance(left,Var) and not(isinstance(right,Var)) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " div [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #+--+
            
            
            elif (isinstance(left,Var) and isinstance(right,Var)):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter, '04x') + "] = " +
                    (str(node.left.name)) + " div " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #++--
            
            else:
                print("\n\n\n ERRRRRRRRRORRRRRRR \n\n\n")
                string = "ERRROR in INTEGER DIV\n"

            self.TEMPMEMORYDICT[str(left_val // right_val)] = format(self.temp_memory_counter, '04x')

            #увеличивавем еще тк записываем в следущую ячейку памяти mod от деления
            self.temp_memory_counter += 1
            self.TEMPMEMORYDICT[str(left_val % right_val)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)
            
            return left_val // right_val
        
        elif node.op.type is TokenType.FLOAT_DIV:
            #????????? тут мб нельзя сделать
            '''
            '''
            '''
            if not(str(left_val) in self.MEMORYDICT):
                self.memory_counter = self.memory_counter + 1
                self.MEMORYDICT[str(left_val)] = '%04d' % self.memory_counter
            if not(str(right_val) in self.MEMORYDICT):
                self.memory_counter = self.memory_counter + 1
                self.MEMORYDICT[str(right_val)] = '%04d' % self.memory_counter
            if not(str(left_val / right_val) in self.MEMORYDICT):
                self.memory_counter = self.memory_counter + 1
                self.MEMORYDICT[str(left_val / right_val)] = '%04d' % self.memory_counter
            string = ("04 " + self.MEMORYDICT[str(left_val)] +
            " " + self.MEMORYDICT[str(right_val)] + " " +
            self.MEMORYDICT[str(left_val / right_val)] +
            "; " + str(left_val / right_val) + " = " +
            str(left_val) + " / " + (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
            if not(string in self.STRDICT): 
                self.STRDICT.append(string)
                self.file.write (string)
            '''
            '''
            '''
            self.temp_memory_counter += 1
            self.command_register += 1
            self.TEMPMEMORYDICT[str(left_val / right_val)] = format(self.temp_memory_counter, '04x')
            string = "float div\n"
            self.file.write (string)

            return left_val / right_val
        
        elif node.op.type is TokenType.MOD:
            '''
         !!!!
         Если выполняется операция деления, в оперативную память записываются
         два результата: частное  в ячейку c адресом A3, остаток  в следующую
         ячейку, по адресу (A3+1) mod 16^4
         !!!!
            '''

            self.temp_memory_counter += 1
            self.command_register += 1

            if (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    str(left_val) + " mod " + 
                    str(right_val) + " " + "|| " + '%04d' % self.command_register + "\n")
                #----
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                not(str(left_val) in self.TEMPMEMORYDICT) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    str(left_val) + " mod [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #---+
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] mod " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #--+-
            
            elif (not(isinstance(left,Var)) and not(isinstance(right,Var)) and 
                str(left_val) in self.TEMPMEMORYDICT and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] mod [" + 
                    self.TEMPMEMORYDICT[(str(right_val))] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #--++
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                not(str(left_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    (str(left_val)) + " mod " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-+--
            
            elif (not(isinstance(left,Var)) and isinstance(right,Var) and 
                str(left_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.TEMPMEMORYDICT[str(left_val)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = [" +
                    self.TEMPMEMORYDICT[str(left_val)] + "] mod " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #-++-   
            
            
            elif (isinstance(left,Var) and not(isinstance(right,Var)) and not(str(right_val) in self.TEMPMEMORYDICT)):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    (str(node.left.name)) + " mod " + 
                    (str(right_val)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #+---

            elif (isinstance(left,Var) and not(isinstance(right,Var)) and str(right_val) in self.TEMPMEMORYDICT):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.TEMPMEMORYDICT[str(right_val)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" 
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    (str(node.left.name)) + " mod [" + 
                    self.TEMPMEMORYDICT[str(right_val)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                #+--+
            
            
            elif (isinstance(left,Var) and isinstance(right,Var)):
                string = ("04 " + 
                    self.MEMORYDICT[str(node.left.name)] + " " +
                    self.MEMORYDICT[str(node.right.name)] + " "
                    + format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "["
                    + format(self.temp_memory_counter + 1, '04x') + "] = " +
                    (str(node.left.name)) + " mod " + 
                    (str(node.right.name)) + " " + "|| " + '%04d' % self.command_register + "\n")
                #++--
            
            else:
                print("\n\n\n ERRRRRRRRRORRRRRRR \n\n\n")
                string = "ERRROR in MOD\n"

            self.TEMPMEMORYDICT[str(left_val // right_val)] = format(self.temp_memory_counter, '04x')

            #увеличивавем еще тк записываем в следущую ячейку памяти mod от деления
            self.temp_memory_counter += 1
            self.TEMPMEMORYDICT[str(left_val % right_val)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)
            return left_val % right_val
        

        elif node.op.type is TokenType.AND:
            return left_val and right_val
        elif node.op.type is TokenType.OR:
            return left_val or right_val
        elif node.op.type is TokenType.EQUALS:
            return left_val == right_val
        elif node.op.type is TokenType.NOT_EQUALS:
            return left_val != right_val
        elif node.op.type is TokenType.GREATER:
            return left_val > right_val
        elif node.op.type is TokenType.GREATER_EQUALS:
            return left_val >= right_val
        elif node.op.type is TokenType.LESS:
            return left_val < right_val
        elif node.op.type is TokenType.LESS_EQUALS:
            return left_val <= right_val

    def visit_num(self, node: Num):
        if str(node.value) not in self.MEMORYDICT:
            self.memory_counter = self.memory_counter + 1
            self.MEMORYDICT[str(node.value)] = format(self.memory_counter, '04x')
        return node.value

    def visit_boolean(self, node: Boolean):
        return node.value

    def visit_unaryop(self, node: UnaryOp):
        if node.op.type is TokenType.PLUS:
            return +self.visit(node.factor)
        
        if node.op.type is TokenType.MINUS:
            self.temp_memory_counter += 1
            self.command_register += 1
            factor = node.factor
            factor_value = self.visit(node.factor)


            if not(isinstance(factor,Var)) and not(str(factor_value) in self.TEMPMEMORYDICT):
                #умножаем на минус 1
                string = ("03 " + 
                    self.MEMORYDICT[str(factor_value)] + " " + 
                    self.MEMORYDICT[str(-1)] + " " + 
                    format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" + 
                    format(self.temp_memory_counter, '04x') + "] := -" +
                    str(factor_value) + " " + "|| " + '%04d' % self.command_register + "\n")
            elif not(isinstance(factor,Var)) and str(factor_value) in self.TEMPMEMORYDICT:
                string = ("03 " + 
                    self.TEMPMEMORYDICT[str(factor_value)] + " " + 
                    self.MEMORYDICT[str(-1)] + " " + 
                    format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" + 
                    format(self.temp_memory_counter, '04x') + "] := - [" +
                    self.TEMPMEMORYDICT[str(factor_value)] + "] " + "|| " + '%04d' % self.command_register + "\n")
            elif isinstance(factor,Var):
                string = ("03 " + 
                    self.MEMORYDICT[str(factor.name)] + " " + 
                    self.MEMORYDICT[str(-1)] + " " + 
                    format(self.temp_memory_counter, '04x') + "; " + '%04d' % self.command_register + " || " + "[" + 
                    format(self.temp_memory_counter, '04x') + "] := -" +
                    str(factor.name) + " " + "|| " + '%04d' % self.command_register + "\n")
            else:
                print("\n\n\n UNARY_MINUS ERROR \n\n\n")
                string = "\n\n\n UNARY_MINUS ERROR \n\n\n"


            self.TEMPMEMORYDICT[str(-factor_value)] = format(self.temp_memory_counter, '04x')

            self.file.write (string)

            return -factor_value
        if node.op.type is TokenType.NOT:
            return not self.visit(node.factor)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_var(self, node: Var):
        current_frame: Frame = self.callstack.peek()
        # get value by variable's name
        val = current_frame.get_value(node.name)
        

        return val

    def visit_assign(self, node: Assign):

        '''
        '''
        
        var_name = node.left.name  # get variable's name
        left = node.left
        right = node.right
        var_value = self.visit(node.right)
        current_frame: Frame = self.callstack.peek()

        self.command_register += 1

        if isinstance(right,FunctionCall):
            
            string = ("00 " + 
                self.MEMORYDICT[str(node.right.func_name)] + " " + 
                "ffff" + " " + 
                self.MEMORYDICT[str(node.left.name)] + "; " + '%04d' % self.command_register + " || " + 
                str(node.left.name) + " := " +
                node.right.func_name + " " + "|| " + '%04d' % self.command_register + "\n")
        elif not(isinstance(right,Var)) and not(str(var_value) in self.TEMPMEMORYDICT):
            string = ("00 " + 
                self.MEMORYDICT[str(var_value)] + " " + 
                "ffff" + " " + 
                self.MEMORYDICT[str(node.left.name)] +"; " + '%04d' % self.command_register + " || " + 
                str(node.left.name) + " := " +
                str(var_value) + " " + "|| " + '%04d' % self.command_register + "\n")
        elif not(isinstance(right,Var)) and str(var_value) in self.TEMPMEMORYDICT:
            string = ("00 " + 
                self.TEMPMEMORYDICT[str(var_value)] + " " + 
                "ffff" + " " + 
                self.MEMORYDICT[str(node.left.name)] + "; " + '%04d' % self.command_register + " || " + 
                str(node.left.name) + " := [" + 
                self.TEMPMEMORYDICT[str(var_value)] + "] " + "|| " + '%04d' % self.command_register + "\n")
        elif isinstance(right,Var):
            string = ("00 " + 
                self.MEMORYDICT[str(node.right.name)] + " " + 
                "ffff" + " " + 
                self.MEMORYDICT[str(node.left.name)] + "; " + '%04d' % self.command_register + " || " + 
                str(node.left.name) + " := " +
                node.right.name + " " + "|| " + '%04d' % self.command_register + "\n")
        
        else:
            print("\n\n\n ASSIGN ERROR \n\n\n")
            string = "\n\n\n ASSIGN ERROR \n\n\n"

        self.TEMPMEMORYDICT = {}

        self.file.write (string)
        
        if current_frame.type is FrameType.FUNCTION and current_frame.name == var_name:
            current_frame.return_val = var_value
        else:
            current_frame.set_value(var_name, var_value)

    def visit_program(self, node: Program):
        program_name = node.name

        self.log(f'ENTER: PROGRAM {program_name}')

        frame = Frame(name=program_name, type=FrameType.PROGRAM)

        self.callstack.push(frame)
        self.visit(node.block)

        self.log(str(self.callstack))

        self.callstack.pop()
        self.log(f'LEAVE: PROGRAM {program_name}')

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_vardecl(self, node: VarDecl):
        var_name = node.var_node.name

        self.memory_counter = self.memory_counter + 1
        self.MEMORYDICT[str(var_name)] = format(self.memory_counter, '04x')

        current_frame: Frame = self.callstack.peek()
        current_frame.define(var_name)

    def visit_procdecl(self, node: ProcedureDecl):
        
        self.memory_counter = self.memory_counter + 1
        self.MEMORYDICT[str(node.token.value)] = format(self.memory_counter, '04x')

        proc_name = node.token.value
        current_frame: Frame = self.callstack.peek()
        current_frame.define(proc_name)
        current_frame.set_value(proc_name, node)

    def visit_proccall(self, node: ProcedureCall):
        proc_name = node.proc_name
        current_frame = self.callstack.peek()
        proc_node: ProcedureDecl = current_frame.get_value(proc_name)

        self.log(f'ENTER: PROCEDURE {proc_name}')

        # get actual params values
        actual_param_values = [self.visit(actual_param)
                               for actual_param in node.actual_params]

        proc_frame = Frame(name=proc_name, type=FrameType.PROCEDURE)

        self.callstack.push(proc_frame)
        current_frame: Frame = self.callstack.peek()

        # map actual params to formal params
        for (formal_param, actual_param_value) in zip(proc_node.params, actual_param_values):
            current_frame.define(formal_param.var_node.name)
            current_frame.set_value(formal_param.var_node.name, actual_param_value)

        self.visit(proc_node.block)
        self.log(str(self.callstack))

        self.callstack.pop()
        self.log(f'LEAVE: PROCEDURE {proc_name}')

    def visit_funcdecl(self, node: FunctionDecl):
        self.memory_counter = self.memory_counter + 1
        
        self.MEMORYDICT[str(node.token.value)] = format(self.memory_counter, '04x')
        func_name = node.token.value

        current_frame: Frame = self.callstack.peek()
        current_frame.define(func_name)
        current_frame.set_value(func_name, node)


        

    def visit_funccall(self, node: FunctionCall):

        current_frame = self.callstack.peek()
        func_name = node.func_name
        func_node: FunctionDecl = current_frame.get_value(func_name)

        self.log(f'ENTER: FUNCTION {func_name}')
        func_frame = Frame(name=func_name, type=FrameType.FUNCTION)
        self.callstack.push(func_frame)
        current_frame: Frame = self.callstack.peek()

        


        # get actual params values to formal params
        actual_param_values = [self.visit(actual_param)
                               for actual_param in node.actual_params]

        for (formal_param, actual_param_value) in zip(func_node.params, actual_param_values):
            current_frame.define(formal_param.var_node.name)
            current_frame.set_value(formal_param.var_node.name, actual_param_value)

        '''
        '''
        if str(func_name) not in self.used_function_arr :
            now_function_dict = {}
            for formal_param in func_node.params:
                self.temp_memory_counter += 1
                now_function_dict[str(formal_param.var_node.name)] = format(self.temp_memory_counter, '04x')
        
            self.functions_param_dict[str(func_name)] = now_function_dict

        now_function_dict = self.functions_param_dict[str(func_name)]

        for (formal_param, actual_param, actual_param_value) in zip(func_node.params, node.actual_params, actual_param_values):
            self.command_register += 1
            if isinstance(actual_param, Var):
                string = ("00 " + 
                self.MEMORYDICT[str(actual_param.name)] + " " + 
                "ffff" + " " + 
                now_function_dict[str(formal_param.var_node.name)] + "; " + '%04d' % self.command_register + " || " + "[" + 
                now_function_dict[str(formal_param.var_node.name)] + "] := " +
                actual_param.name + " " + "|| " + '%04d' % self.command_register + "\n")
            else:
                string = ("00 " + 
                self.MEMORYDICT[str(actual_param_value)] + " " + 
                "ffff" + " " + 
                now_function_dict[str(formal_param.var_node.name)] + "; " + '%04d' % self.command_register + " || " + "[" + 
                now_function_dict[str(formal_param.var_node.name)] + "] := " +
                str(actual_param_value) + " " + "|| " + '%04d' % self.command_register + "\n")
            self.file.write(string)

        self.command_register += 1
        jump_to = self.command_register + 2
        print('%04d' % self.command_register)
        print('%04d' % jump_to)
        string = "00 jump ffff " + '%04d' % jump_to + "; " + '%04d' % self.command_register + " || " + "variable jump = " + '%04d' % jump_to + " || " + '%04d' % self.command_register + "\n"
        self.file.write(string)

        self.command_register += 1
        string = "_call_func_" + str(func_name) + " " + "80 ffff ffff ????" + "; " + '%04d' % self.command_register + " || " + "call function " + str(func_name) + " || " + '%04d' % self.command_register + "\n"
        self.file.write(string)
        
        '''
        '''

        '''
        '''
        flag = 0
        if str(func_name) not in self.used_function_arr :
            print(self.used_function_arr)
            flag = 1

            self.file.close()
            self.file = open("temp_function.txt", 'a')

            main_memory_dict = self.MEMORYDICT
            self.MEMORYDICT = {}

            temp_command_register = self.command_register
            self.command_register = 0

            string = '_function_' + str(func_name) + " "
            self.file.write(string)
            self.used_function_arr.append(str(func_name))

            for elem in main_memory_dict:
                if elem.isdigit():
                    self.MEMORYDICT[elem] = main_memory_dict[elem]
                if elem in self.functions_list:
                    self.MEMORYDICT[elem] = main_memory_dict[elem]
            
            for param in func_node.params:
                #print(str(param.var_node.name))
                self.function_memory_counter += 1
                self.MEMORYDICT[str(param.var_node.name)] = format(self.function_memory_counter, '04x')

            self.MEMORYDICT[str(func_name)] = main_memory_dict[str(func_name)]

            now_function_dict = self.functions_param_dict[str(func_name)]
            
            for (formal_param, actual_param, actual_param_value) in zip(func_node.params, node.actual_params, actual_param_values):
                self.command_register += 1
                if isinstance(actual_param, Var):
                    string = ("00 " + 
                    main_memory_dict[str(actual_param.name)] + " " + 
                    "ffff" + " " + 
                    now_function_dict[str(formal_param.var_node.name)] + "; " + '%04d' % self.command_register + " || " + 
                    str(formal_param.var_node.name) + " := [" +
                    now_function_dict[str(formal_param.var_node.name)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                else:
                    string = ("00 " + 
                    main_memory_dict[str(actual_param_value)] + " " + 
                    "ffff" + " " + 
                    now_function_dict[str(formal_param.var_node.name)] + "; " + '%04d' % self.command_register + " || " + 
                    str(formal_param.var_node.name) + " := [" +
                    now_function_dict[str(formal_param.var_node.name)] + "] " + "|| " + '%04d' % self.command_register + "\n")
                self.file.write(string)

            
            #print(actual_param_values)
            #print(func_node.params)
            
            #print(self.MEMORYDICT)

            



        '''
        '''
        if flag == 0:
            now_file = self.file.name
            self.file.close()
            self.file = open("bracket.txt", 'a')

        self.visit(func_node.block)
        self.log(str(self.callstack))
        self.log(f'LEAVE: FUNCTION {func_name}')

        if flag == 0:
            self.file.close()
            self.file = open(now_file, 'a')


        '''
        '''
        if flag == 1:
            self.command_register += 1
            string = "80 ffff ffff jump; " + '%04d' % self.command_register + " || " + "return " + "|| " + '%04d' % self.command_register + "\n"
            self.file.write(string)
            self.file.write("\n")
            self.file.close()
            self.file = open("temp1.txt", 'a')
            self.MEMORYDICT = main_memory_dict
            self.command_register = temp_command_register



        '''
        '''

        return_val = current_frame.return_val
        self.callstack.pop()
        if return_val is None:
            self.error(error_code=ErrorCode.MISSING_RETURN, token=node.token)
        return return_val

    def visit_condition(self, node: Condition):

        '''
        string = ""
        if node.condition_node.op.value == "=":
            string = "81 "
        elif node.condition_node.op.value == "<>":
            string = "82 "
        elif node.condition_node.op.value == "<":
            string = "83 "
        elif node.condition_node.op.value == "<=":
            string = "84 "
        elif node.condition_node.op.value == ">=":
            string = "85 "
        elif node.condition_node.op.value == ">":
            string = "86 "


        if not(str(node.condition_node.left.token.value) in self.MEMORYDICT):
            self.memory_counter = self.memory_counter + 1
            self.MEMORYDICT[str(node.condition_node.left.token.value)] = '%04d' % self.memory_counter
        if not(str(node.condition_node.right.token.value) in self.MEMORYDICT):
            self.memory_counter = self.memory_counter + 1
            self.MEMORYDICT[str(node.condition_node.right.token.value)] = '%04d' % self.memory_counter
        string += (self.MEMORYDICT[str(node.condition_node.left.token.value)] + " " + 
                   self.MEMORYDICT[str(node.condition_node.right.token.value)] + " " +
                   " КУДА Я ПРЫГНУ?!!!!!?!?!?!?!? " + "; " + "if " +
                   str(node.condition_node.left.token.value) + " " + node.condition_node.op.value + " " + 
                   str(node.condition_node.right.token.value) + " then goto " + " КУДА Я ПРЫГНУ " + " " + "|| " + '%04d' % self.command_register + "\n")
        
        #if not(string in self.STRDICT): 
        self.STRDICT.append(string)
        self.file.write (string)
        '''

        '''
        '''
        self.command_register += 1
        self.jump_counter += 1
        self.if_arr.append(self.jump_counter)

        string = "_jump_if_false_condition_" + str(self.if_arr[-1]) + " "

        if node.condition_node.op.value == "=":
            string += "82 "
            cond = "<>"
        elif node.condition_node.op.value == "<>":
            string += "81 "
            cond = "="
        elif node.condition_node.op.value == "<":
            string += "84 "
            cond = ">="
        elif node.condition_node.op.value == "<=":
            string += "86 "
            cond = ">"
        elif node.condition_node.op.value == ">=":
            string += "83 "
            cond = "<"
        elif node.condition_node.op.value == ">":
            string += "85 "
            cond = "<="

        if isinstance (node.condition_node.left, Var) and not (isinstance(node.condition_node.right,Var)):
            self.visit(node.condition_node.right)
            string += (self.MEMORYDICT[str(node.condition_node.left.name)] + " " + self.MEMORYDICT[str(node.condition_node.right.value)] +
            " ????; " + '%04d' % self.command_register + " || " 
            + "goto if " + str(node.condition_node.left.name) + " " + cond + " " + str(node.condition_node.right.value) + "|| " + 
            '%04d' % self.command_register + "\n")
        elif not(isinstance (node.condition_node.left, Var)) and (isinstance(node.condition_node.right,Var)):
            self.visit(node.condition_node.left)
            string += (self.MEMORYDICT[str(node.condition_node.left.value)] + " " + self.MEMORYDICT[str(node.condition_node.right.name)] +
            " ????; " + '%04d' % self.command_register + " || " 
            + "goto if " + str(node.condition_node.left.value) + " " + cond + " " + str(node.condition_node.right.name) + "|| " + 
            '%04d' % self.command_register + "\n")
        elif isinstance (node.condition_node.left, Var) and isinstance(node.condition_node.right,Var):
            string += (self.MEMORYDICT[str(node.condition_node.left.name)] + " " + self.MEMORYDICT[str(node.condition_node.right.name)] +
            " ????; " + '%04d' % self.command_register + " || " 
            + "goto if " + str(node.condition_node.left.name) + " " + cond + " " + str(node.condition_node.right.name) + "|| " + 
            '%04d' % self.command_register + "\n")
        else:
            self.visit(node.condition_node.left)
            self.visit(node.condition_node.right)
            string += (self.MEMORYDICT[str(node.condition_node.left.value)] + " " + self.MEMORYDICT[str(node.condition_node.right.value)] +
            " ????; " + '%04d' % self.command_register + " || " 
            + "goto if " + str(node.condition_node.left.value) + " " + cond + " " + str(node.condition_node.right.value) + "|| " + 
            '%04d' % self.command_register + "\n")

        self.file.write(string)
        if node.else_node is None:
            self.visit(node.then_node)
            string = "_arrive_after_false_condition_" + str(self.if_arr.pop()) + " "
            self.file.write(string)
        else:
            self.visit(node.then_node)
            self.else_counter += 1
            self.else_stack.append(self.else_counter)
            self.command_register += 1
            string = ("_jump_before_else_" + str(self.else_counter) + " 80 ffff ffff ???? ; " +
                    '%04d' % self.command_register + " || " + "visited if, not using else || " + '%04d' % self.command_register + "\n")
            self.file.write(string)
            string = "_arrive_after_false_condition_" + str(self.if_arr.pop()) + " "
            self.file.write(string)
            self.visit(node.else_node)
            string = "_arrive_after_else_" + str(self.else_stack.pop()) + " "
            self.file.write(string)


        

        '''
        '''

        '''
        if self.visit(node.condition_node):
            self.visit(node.then_node)
        elif node.else_node is not None:
            self.visit(node.else_node)
        '''
            
    def visit_then(self, node: Then):
        self.visit(node.child)

    def visit_else(self, node: Else):
        self.visit(node.child)

    def visit_while(self, node: WhileLoop):
        '''
        '''
        self.jump_counter += 1
        self.command_register += 1
        self.while_arr.append(self.jump_counter)
        string = "_jump_if_false_while_" + str(self.while_arr[-1]) + " "

        if node.conditon_node.op.value == "=":
            string += "82 "
        elif node.conditon_node.op.value == "<>":
            string += "81 "
        elif node.conditon_node.op.value == "<":
            string += "84 "
        elif node.conditon_node.op.value == "<=":
            string += "86 "
        elif node.conditon_node.op.value == ">=":
            string += "83 "
        elif node.conditon_node.op.value == ">":
            string += "85 "
        
        if isinstance (node.conditon_node.left, Var) and not (isinstance(node.conditon_node.right,Var)):
            if str(node.conditon_node.right.value) not in self.MEMORYDICT:
                self.memory_counter += 1
                self.MEMORYDICT[str(node.conditon_node.right.value)] = f"{self.memory_counter:04x}"    
            string += (self.MEMORYDICT[str(node.conditon_node.left.name)] + " " + self.MEMORYDICT[str(node.conditon_node.right.value)] +
                " ????; " + '%04d' % self.command_register + " || "
                "while" + " " + "|| " + '%04d' % self.command_register + "\n")   
        elif not(isinstance (node.conditon_node.left, Var)) and (isinstance(node.conditon_node.right,Var)):
            if str(node.conditon_node.left.value) not in self.MEMORYDICT:
                self.memory_counter += 1
                self.MEMORYDICT[str(node.conditon_node.left.value)] = f"{self.memory_counter:04x}"  
            string += (self.MEMORYDICT[str(node.conditon_node.left.value)] + " " + self.MEMORYDICT[str(node.conditon_node.right.name)] +
                " ????; " + '%04d' % self.command_register + " || "
                "while" + " " + "|| " + '%04d' % self.command_register + "\n")
        elif isinstance (node.conditon_node.left, Var) and isinstance(node.conditon_node.right,Var):
            string += (self.MEMORYDICT[str(node.conditon_node.left.name)] + " " + self.MEMORYDICT[str(node.conditon_node.right.name)] +
                " ????; " + '%04d' % self.command_register + " || "
                "while" + " " + "|| " + '%04d' % self.command_register + "\n")
        else:
            if str(node.conditon_node.right.value) not in self.MEMORYDICT:
                self.memory_counter += 1
                self.MEMORYDICT[str(node.conditon_node.right.value)] = f"{self.memory_counter:04x}" 
            if str(node.conditon_node.left.value) not in self.MEMORYDICT:
                self.memory_counter += 1
                self.MEMORYDICT[str(node.conditon_node.left.value)] = f"{self.memory_counter:04x}"
            string += (self.MEMORYDICT[str(node.conditon_node.left.value)] + " " + self.MEMORYDICT[str(node.conditon_node.right.value)] +
                " ????; " + '%04d' % self.command_register + " || "
                "while" + " " + "|| " + '%04d' % self.command_register + "\n")

        self.file.write(string)

        
        
        
        '''  
        while self.visit(node.conditon_node) is True:
            try:
                self.visit(node.body_node)
            except ContinueError:
                #вернуться в начало
                continue
            except BreakError:
                #завершить цикл
                break
        '''

        "BREAK AND CONTINUE!!!"
        
        self.visit(node.body_node)

        self.command_register += 1
        string = ("_repeat_while_" + str(self.while_arr[-1]) + " " + "80 ffff ffff ????; " + 
        '%04d' % self.command_register + " || " + "go to start while " + "|| " + '%04d' % self.command_register + "\n")
        self.file.write(string)
        string = "_arrive_after_false_while_" + str(self.while_arr.pop()) + " "
        self.file.write(string)
        
        '''
        '''

    def visit_continue(self, node: Continue):
        raise ContinueError()

    def visit_break(self, node: Break):
        pass

    def translate(self):
        '''
        for elem in self.memory_arr:
            if not elem in self.MEMORYDICT:
                self.memory_counter = self.memory_counter + 1
                self.MEMORYDICT[elem] = format(self.memory_counter, '04x')
        '''
        
        clear = open("temp_function.txt", 'w')
        clear.close()
        ast = self.parser.parse()
        self.analyzer.visit(ast)
        self.visit(ast)
        self.command_register += 1
        string = "99 ffff ffff ffff; " + '%04d' % self.command_register + " || finish " + "|| " + '%04d' % self.command_register + "\n"
        self.file.write(string)
        self.file.write("-------\n")
        for elem in self.MEMORYDICT:
            string = elem + " : " + self.MEMORYDICT[elem] + "\n"
            self.file.write(string)
        print(self.MEMORYDICT)
        self.file.close()
