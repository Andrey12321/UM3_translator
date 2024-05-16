from astnodes import AST, BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, \
    Param, VarDecl, Type, ProcedureDecl, ProcedureCall, Boolean, Condition, Then, Else, FunctionDecl, FunctionCall, \
    WhileLoop, Continue, Break
from errors import SyntaxError, ErrorCode
from tokenizer import Tokenizer, Token
from tokens import TokenType
from typing import List
import sys

class Parser(object):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()


        '''
        '''

        self.for_memory = []
        self.functions_list = []

        '''
        '''

        '''
        '''

        '''
        self.file = open(sys.argv[2], 'a')
        self.EQUALDICT = {"0":"0000"}
        self.counter = 0
        self.STRDICT = []
        self.Funcnames = []
        self.Funcvariables = {}
        self.Functionarguments = {}
        self.Functionjump = {}
        self.close = []
        self.Globalvariables = {}
        '''

        '''
        '''

    def error(self, error_code, token):
        raise SyntaxError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type: TokenType):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def program(self) -> Program:
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        programe_name = var_node.name  # value hold the variable's name
        self.eat(TokenType.SEMI)
        block = self.block()
        self.eat(TokenType.DOT)
        return Program(programe_name, block)

    def block(self) -> Block:
        """block : declarations compound_statement"""
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self) -> List[AST]:
        """
        declarations : (VAR (variable_declaration SEMI)+)? procedure_declaration*
        """
        declarations = []

        if self.current_token.type is TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type is TokenType.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI)

        while self.current_token.type is TokenType.PROCEDURE:
            proc_decl = self.procedure_declaration()
            declarations.append(proc_decl)

        while self.current_token.type is TokenType.FUNCTION:
            func_decl = self.function_declaration()
            declarations.append(func_decl)

        return declarations

    def procedure_declaration(self) -> ProcedureDecl:
        """procedure_declaration :
            PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI
        """
        self.eat(TokenType.PROCEDURE)
        proc_token = self.current_token
        self.eat(TokenType.ID)
        params = []

        if self.current_token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            params = self.formal_parameter_list()
            self.eat(TokenType.RPAREN)

        self.eat(TokenType.SEMI)
        block_node = self.block()
        proc_decl = ProcedureDecl(
            token=proc_token,
            params=params,
            block=block_node)
        self.eat(TokenType.SEMI)
        return proc_decl

    def function_declaration(self) -> FunctionDecl:
        """function_declaration :
            FUNCTION ID (LPAREN formal_parameter_list RPAREN)? COLON type_spec SEMI block SEMI
        """
        self.eat(TokenType.FUNCTION)
        func_token = self.current_token
        self.eat(TokenType.ID)
        params = []

        if self.current_token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            params = self.formal_parameter_list()
            self.eat(TokenType.RPAREN)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        self.eat(TokenType.SEMI)
        block_node = self.block()
        self.eat(TokenType.SEMI)
        func_decl = FunctionDecl(
            token=func_token,
            params=params,
            block=block_node,
            return_type=type_node
        )
        self.for_memory.append(str(func_token.value))
        self.functions_list.append(str(func_token.value))
        return func_decl

    def formal_parameter_list(self) -> List[Param]:
        """ formal_parameter_list : formal_parameters
                              | formal_parameters SEMI formal_parameter_list
        """
        if self.current_token.type is not TokenType.ID:
            return []

        params = self.formal_parameters()
        while self.current_token.type is TokenType.SEMI:
            self.eat(TokenType.SEMI)
            params.extend(self.formal_parameters())

        return params

    def formal_parameters(self) -> List[Param]:
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        return [Param(var_node=var_node, type_node=type_node) for var_node in var_nodes]

    def variable_declaration(self) -> List[VarDecl]:
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)
        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()

        '''
        '''
        for var_node in var_nodes:
            if not(str(var_node.name) in self.for_memory):
                self.for_memory.append(str(var_node.name))
                '''
                print ("\n\n",var_node.name,"\n")
                print(self.for_memory,"\n\n")
                '''
        '''
        '''
        
        '''
        '''
        '''
        for var_node in var_nodes:
            if not(str(var_node.name) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(var_node.name)] = '%04d' % self.counter
        '''
        '''
        '''


        return [VarDecl(var_node=var_node, type_node=type_node) for var_node in var_nodes]

    def type_spec(self) -> Type:
        """type_spec : INTEGER
                     | REAL
                     | BOOLEAN
        """
        token = self.current_token
        if token.type in (TokenType.INTEGER, TokenType.REAL, TokenType.BOOLEAN):
            self.eat(token.type)
            return Type(token)
        self.error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

    def compound_statement(self) -> Compound:
        """compound_statement: BEGIN statement_list END"""
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)
        root = Compound()
        for node in nodes:
            root.childrens.append(node)
        return root

    def statement_list(self) -> List[AST]:
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        if self.current_token.type is not TokenType.SEMI:
            return results
        self.eat(TokenType.SEMI)
        results.extend(self.statement_list())
        return results

    def statement(self) -> AST:
        """
        statement : compound_statement
                  | proccall_statement
                  | condition_statement
                  | while_statement
                  | assignment_statement
                  | break
                  | continue
                  | empty
        """
        if self.current_token.type is TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type is TokenType.ID and self.tokenizer.current_char is '(':
            node = self.proccall_statement()
        elif self.current_token.type is TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type is TokenType.IF:
            node = self.condition_statement()
        elif self.current_token.type is TokenType.WHILE:
            node = self.while_statement()
        elif self.current_token.type is TokenType.CONTINUE:
            node = self.continue_statement()
        elif self.current_token.type is TokenType.BREAK:
            node = self.break_statement()
        else:
            node = self.empty()
        return node

    def condition_statement(self) -> Condition:
        """
        condition_statement : IF expr THEN (ELSE)?
        """
        token = self.current_token
        self.eat(TokenType.IF)
        condition_node = self.expr()
        then_node = self.then()
        else_node = None
        if self.current_token.type is TokenType.ELSE:
            else_node = self._else()
        return Condition(
            token=token,
            condition_node=condition_node,
            then_node=then_node,
            else_node=else_node
        )

    def then(self) -> Then:
        """
        THEN statement
        """
        token = self.current_token
        self.eat(TokenType.THEN)
        child = self.statement()
        return Then(token=token, child=child)

    def _else(self) -> Else:
        """
        ELSE statement
        """
        token = self.current_token
        self.eat(TokenType.ELSE)
        child = self.statement()
        return Else(token=token, child=child)

    def while_statement(self) -> WhileLoop:
        """
        while_statement : WHILE expr DO statement
        """
        token = self.current_token
        self.eat(TokenType.WHILE)
        condition_node = self.expr()
        self.eat(TokenType.DO)
        body_node = self.statement()
        return WhileLoop(token=token, condition_node=condition_node, body_node=body_node)

    def continue_statement(self) -> Continue:
        token = self.current_token
        self.eat(TokenType.CONTINUE)
        return Continue(token)

    def break_statement(self) -> Break:
        token = self.current_token
        self.eat(TokenType.BREAK)
        return Break(token)

    def assignment_statement(self) -> Assign:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        op = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()

        '''
        '''

        '''
        if (right.token.type is TokenType.INTEGER_CONST or right.token.type is TokenType.REAL_CONST or
            right.token.type is TokenType.INTEGER or right.token.type is TokenType.REAL):
            #self.file.write("ZZZ\n")
            if not(str(left.name) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(left.name)] = '%04d' % self.counter
            if not(str(right.value)) in self.EQUALDICT:
                self.counter = self.counter + 1
                self.EQUALDICT[str(right.value)] = '%04d' % self.counter
            string = ("01 " + self.EQUALDICT[str(right.value)] +
            " " + self.EQUALDICT[str(0)] + " " + self.EQUALDICT[str(left.name)] +
            "; " + str(left.name) + " = " + str(right.value) + "\n")
            if not(string in self.STRDICT): 
                self.STRDICT.append(string)
                self.file.write (string)
        
        if op is TokenType.PLUS:
            if not(str(left.name) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(left.name)] = '%04d' % self.counter
            if not(str(self.visit(node.right)) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(self.visit(node.right))] = '%04d' % self.counter
            if not(str(left.name + self.visit(node.right)) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(left.name + self.visit(node.right))] = '%04d' % self.counter
            string = ("01 " + self.EQUALDICT[str(left.name)] + " " +
            self.EQUALDICT[str(self.visit(node.right))] + " " +
            self.EQUALDICT[str(left.name + self.visit(node.right))] +
            "; " + str(left.name + self.visit(node.right)) + " = " +
            str(left.name) + " + " + (str(self.visit(node.right))) + "\n")
            if not(string in self.STRDICT): 
                self.STRDICT.append(string)
                self.file.write (string)
        ''' 


        '''
        '''


        return Assign(left=left, op=op, right=right)

    def proccall_statement(self) -> ProcedureCall:
        """proccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN"""
        procc_token = self.current_token
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        if self.current_token.type is TokenType.RPAREN:
            self.eat(TokenType.RPAREN)
            return ProcedureCall(procc_token.value, [], procc_token)
        else:
            actual_params = [self.expr()]
            while self.current_token.type is TokenType.COMMA:
                self.eat(TokenType.COMMA)
                actual_params.append(self.expr())

            self.eat(TokenType.RPAREN)
            return ProcedureCall(
                proc_name=procc_token.value,
                actual_params=actual_params,
                token=procc_token
            )

    def funccall_statement(self) -> FunctionCall:
        """funccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN"""
        funccall_token = self.current_token
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        if self.current_token.type is TokenType.RPAREN:
            self.eat(TokenType.RPAREN)
            return FunctionCall(
                func_name=funccall_token.value,
                actual_params=[],
                token=funccall_token
            )
        else:
            actual_params = [self.expr()]
            while self.current_token.type is TokenType.COMMA:
                self.eat(TokenType.COMMA)
                actual_params.append(self.expr())

            self.eat(TokenType.RPAREN)
            return FunctionCall(
                func_name=funccall_token.value,
                actual_params=actual_params,
                token=funccall_token)

    def variable(self) -> Var:
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self) -> AST:
        """An empty production"""
        return NoOp()
    """
    def check_repeat(self) -> AST:
        token = self.current_token
        '''
        if token.type is TokenType.PLUS:
            #self.eat(TokenType.PLUS)
            
            #return UnaryOp(op=token, factor=self.first_priority())
            return UnaryOp(op=token, factor=self.first_priority())
            
        elif token.type is TokenType.MINUS:
            
            #self.eat(TokenType.MINUS)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.NOT:
            
            #self.eat(TokenType.NOT)
            return UnaryOp(op=token, factor=self.first_priority())
        '''
        
        if token.type is TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)

        elif token.type is TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)

        elif token.type is TokenType.TRUE:
            
            self.eat(TokenType.TRUE)
            return Boolean(token)

        elif token.type is TokenType.FALSE:
            
            self.eat(TokenType.FALSE)
            return Boolean(token)

        elif token.type is TokenType.LPAREN:
            
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        elif token.type is TokenType.ID and self.tokenizer.current_char is '(':
            
            return self.funccall_statement()

        elif token.type in (TokenType.PLUS,
                            TokenType.MINUS,
                            TokenType.NOT):
            return "repeat first"

        else:
            return self.variable()
    
    def first_priority(self) -> AST:

        
        """
    '''
        factor: PLUS  factor
              | MINUS factor
              | NOT factor
              | INTEGER_CONST
              | REAL_CONST
              | TRUE
              | FALSE
              | LPAREN expr RPAREN
              | variable
              | funccall
    '''
    """
        '''
        token = self.current_token
        left = self.first_priority()
        '''
        if self.current_token.type in (TokenType.MUL,
                         TokenType.INTEGER_DIV,
                         TokenType.FLOAT_DIV,
                         TokenType.MOD):
            return "repeat second"
        token = self.current_token
        left = self.check_repeat()
        result = left

        

        while self.current_token.type in (TokenType.PLUS,
                                        TokenType.MINUS,
                                        TokenType.NOT,
                                        #TokenType.INTEGER_CONST,
                                        #TokenType.REAL_CONST,
                                        #TokenType.TRUE,
                                        #TokenType.FALSE,
                                        #TokenType.LPAREN,
                                        ##TokenType.RPAREN
                                        #TokenType.ID,
                                        #TokenType.VAR
                                         ):
            token = self.current_token
            #left = self.check_repeat()
            if token.type is TokenType.PLUS:
                
                if self.check_repeat() == "repeat first":
                    
                    self.eat(token.type)
                    #result = UnaryOp(op=token, factor=self.first_priority())
                    result = BinOp(left=left, op=token, right=self.third_priority())
                else:
                    #left = self.check_repeat()
                    self.eat(token.type)
                    result = UnaryOp(op=token, factor=self.check_repeat())
                    #result = BinOp(left=left, op=token, right=self.check_repeat())
                '''
                self.eat(TokenType.PLUS) 
                return UnaryOp(op=token, factor=self.first_priority())
                '''
                
            elif token.type is TokenType.MINUS:
                if self.check_repeat() == "repeat first":
                    
                    self.eat(token.type)
                    #result = UnaryOp(op=token, factor=self.first_priority())
                    result = BinOp(left=left, op=token, right=self.third_priority())
                else:
                    #left = self.check_repeat()
                    self.eat(token.type)
                    result = UnaryOp(op=token, factor=self.check_repeat())
                    #result = BinOp(left=left, op=token, right=self.check_repeat())
                '''
                self.eat(TokenType.MINUS)
                return UnaryOp(op=token, factor=self.first_priority())
                '''
            elif token.type is TokenType.NOT:
                if self.check_repeat() == "repeat first":
                    
                    self.eat(token.type)
                    #result = UnaryOp(op=token, factor=self.first_priority())
                    result = BinOp(left=left, op=token, right=self.third_priority())
                else:
                    #left = self.check_repeat()
                    self.eat(token.type)
                    result = UnaryOp(op=token, factor=self.check_repeat())
                    #result = BinOp(left=left, op=token, right=self.check_repeat())
                '''
                self.eat(TokenType.NOT)
                return UnaryOp(op=token, factor=self.first_priority())
                '''
            elif token.type is TokenType.INTEGER_CONST:
                #print("\n\n\n", "1", '\n\n\n')
                '''
                '''
                if not(str(token.value) in self.for_memory):
                    self.for_memory.append(str(token.value))
                '''
                '''
                self.eat(TokenType.INTEGER_CONST)
                result = Num(token)
                #return Num(token)

            elif token.type is TokenType.REAL_CONST:
                
                '''
                '''
                if not(str(token.value) in self.for_memory):
                    self.for_memory.append(str(token.value))
                '''
                '''
                self.eat(TokenType.REAL_CONST)
                return Num(token)

            elif token.type is TokenType.TRUE:
                
                self.eat(TokenType.TRUE)
                return Boolean(token)

            elif token.type is TokenType.FALSE:
                
                self.eat(TokenType.FALSE)
                return Boolean(token)

            elif token.type is TokenType.LPAREN:
                
                self.eat(TokenType.LPAREN)
                node = self.expr()
                self.eat(TokenType.RPAREN)
                return node

            elif token.type is TokenType.ID and self.tokenizer.current_char is '(':
                
                return self.funccall_statement()

            else:
                return self.variable()
        return result
    """

    def first_priority(self) -> AST:
        """
        factor: PLUS  factor
              | MINUS factor
              | NOT factor
              | INTEGER_CONST
              | REAL_CONST
              | TRUE
              | FALSE
              | LPAREN expr RPAREN
              | variable
              | funccall
        """
        '''
        if self.current_token.type in (TokenType.MUL,
                         TokenType.INTEGER_DIV,
                         TokenType.FLOAT_DIV,
                         TokenType.MOD):
            return "repeat second"
        '''
        token = self.current_token
        if token.type is TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(op=token, factor=self.first_priority())

        elif token.type is TokenType.INTEGER_CONST:
            if not(str(token.value) in self.for_memory):
                self.for_memory.append(str(token.value))
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)

        elif token.type is TokenType.REAL_CONST:
            if not(str(token.value) in self.for_memory):
                self.for_memory.append(str(token.value))
            self.eat(TokenType.REAL_CONST)
            return Num(token)

        elif token.type is TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(token)

        elif token.type is TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(token)

        elif token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        elif token.type is TokenType.ID and self.tokenizer.current_char is '(':
            return self.funccall_statement()

        else:
            return self.variable()

    def second_priority(self) -> AST:
        """term : factor ((MUL | DIV | MOD) factor)*"""
        '''
        if self.current_token.type in (TokenType.PLUS,
                                          TokenType.MINUS):
            return "repeat second"
        '''
        left = self.first_priority()
        result = left
        
        
        while self.current_token.type in (TokenType.MUL,
                                          TokenType.INTEGER_DIV,
                                          TokenType.FLOAT_DIV,
                                          TokenType.MOD):

            #if self.first_priority() == "repeat second":
                #left = self.first_priority()
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.second_priority())
            '''
            else:
                #left = self.first_priority()
                token = self.current_token
                self.eat(token.type)
                result = BinOp(left=left, op=token, right=self.first_priority())
            '''

            '''
            print("left", str(result.left.value))
            print (str(token.type))
            print("right", str(result.right.value))
            result.left.value = result.left.value * result.right.value
            print("left", str(result.left.value))
            print (str(token.type))
            print("right", str(result.right.value))
            '''
        
            
            #print("\n\n\n", "VVVV", '\n\n\n')
        #result.left.value = result.left.value // result.right.value
        #print("\n\n\n", "2", '\n\n\n')
        
        #print ("conted : ",result.value)
        return result

    def third_priority(self) -> AST:
        """simple_expr: term((PLUS | MINUS) term)*"""
        '''
        left = self.second_priority()
        result = left

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.second_priority())
        #print("\n\n\n", "3", '\n\n\n')
        '''
        left = self.second_priority()
        result = left
        
        while self.current_token.type in (TokenType.PLUS,
                                          TokenType.MINUS):

            #if self.second_priority() == "repeat third":
                #left = self.first_priority()
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.third_priority())
            

        return result

    def fourth_priority(self) -> AST:
        """
        GREATER| GREATER_EQUALS| LESS| LESS_EQUALS
        """
        left = self.third_priority()
        result = left

        while self.current_token.type in (TokenType.GREATER,
                                          TokenType.GREATER_EQUALS,
                                          TokenType.LESS,
                                          TokenType.LESS_EQUALS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.third_priority())
        #print("\n\n\n", "4", '\n\n\n')
        return result

    def fifth_priority(self) -> AST:
        """
        EQUALS|NOT_EQUALS
        """
        left = self.fourth_priority()
        result = left

        while self.current_token.type in (TokenType.EQUALS, TokenType.NOT_EQUALS):
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.fourth_priority())
        #print("\n\n\n", "5", '\n\n\n')
        return result

    def sixth_priority(self) -> AST:
        """
        AND
        """
        left = self.fifth_priority()
        result = left

        while self.current_token.type is TokenType.AND:
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.fifth_priority())
        #print("\n\n\n", "6", '\n\n\n')
        return result

    def seventh_priority(self) -> AST:
        """
        OR
        """
        left = self.sixth_priority()
        result = left

        while self.current_token.type is TokenType.OR:
            token = self.current_token
            self.eat(token.type)
            result = BinOp(left=left, op=token, right=self.sixth_priority())
        #print("\n\n\n", "7", '\n\n\n')
        return result

    def expr(self) -> AST:
        
        token = self.current_token

        '''
        '''
        '''
        if (token.type is TokenType.INTEGER_CONST or token.type is TokenType.REAL_CONST or
            token.type is TokenType.INTEGER or token.type is TokenType.REAL):
            if not(str(token.value) in self.EQUALDICT):
                self.counter = self.counter + 1
                self.EQUALDICT[str(token.value)] = '%04d' % self.counter
        '''
        '''
        '''

        '''
        '''
        '''
        '''
        #print("\n\n\n", "expr", '\n\n\n')
        return self.seventh_priority()

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
