#!/usr/bin/python3

#  -*- python -*-

import re
import sys 

global MAX_SPACE
# creating global variables to use throughout our code. 
# Maximum addressable memory space of a 20-bit address
MAX_SPACE = 1048576
# creating global variables to use throughout our code. 
# The variable below refers to the maximum range that base addressing can reach
global MAX_BASE_RANGE
MAX_BASE_RANGE = 4095
# creating global variables to use throughout our code. 
# The variable below refers to the maximum range that PC addressing can reach
global MAX_PC_RANGE
MAX_PC_RANGE = 2047
# creating global variables to use throughout our code. 
# The variable below refers to the base format 
global BASE_FORMAT
BASE_FORMAT = 16384
# creating global variables to use throughout our code. 
# The variable below refers to the PC format
global PC_FORMAT
PC_FORMAT = 8192
# creating global variables to use throughout our code. 
# The variable below refers to the maximum numerical value, 2^16
global MAX_VALUE
MAX_VALUE = 65536
# creating global variables to use throughout our code. 
# Saving the ASCII value for H so that it can be globally accessed for emmitting H records
global H
H = "48"
# creating global variables to use throughout our code. 
# Saving the ASCII value for E so that it can be globally accessed for emmitting E records
global E
E = "45"
# creating global variables to use throughout our code. 
# Saving the ASCII value for T so that it can be globally accessed for emmitting T records
global T
T = "54"

# creating global variables to use throughout our code. 
# Creating a table to store all the opcodes for every mnemonic available.
# This is a direct "copy-paste" from the handout and other resources provided by Professor.
opCodes = {'ADD': {'Code': 24.0, 'Type': 3.0, 'Args': 0},
 'ADDF': {'Code': 88.0, 'Type': 3.0, 'Args': 0},
 'ADDR': {'Code': 144.0, 'Type': 2.0, 'Args': 0},
 'AND': {'Code': 64.0, 'Type': 3.0, 'Args': 0},
 'CLEAR': {'Code': 180.0, 'Type': 2.0, 'Args': 1},
 'COMP': {'Code': 40.0, 'Type': 3.0, 'Args': 0},
 'COMPF': {'Code': 136.0, 'Type': 3.0, 'Args': 0},
 'COMPR': {'Code': 160.0, 'Type': 2.0, 'Args': 0},
 'DIV': {'Code': 36.0, 'Type': 3.0, 'Args': 0},
 'DIVF': {'Code': 100.0, 'Type': 3.0, 'Args': 0},
 'DIVR': {'Code': 156.0, 'Type': 2.0, 'Args': 0},
 'FIX': {'Code': 196.0, 'Type': 1.0, 'Args': 0},
 'FLOAT': {'Code': 192.0, 'Type': 1.0, 'Args': 0},
 'HIO': {'Code': 244.0, 'Type': 1.0, 'Args': 0},
 'J': {'Code': 60.0, 'Type': 3.0, 'Args': 0},
 'JEQ': {'Code': 48.0, 'Type': 3.0, 'Args': 0},
 'JGT': {'Code': 52.0, 'Type': 3.0, 'Args': 0},
 'JLT': {'Code': 56.0, 'Type': 3.0, 'Args': 0},
 'JSUB': {'Code': 72.0, 'Type': 3.0, 'Args': 0},
 'LDA': {'Code': 0.0, 'Type': 3.0, 'Args': 0},
 'LDB': {'Code': 104.0, 'Type': 3.0, 'Args': 0},
 'LDCH': {'Code': 80.0, 'Type': 3.0, 'Args': 0},
 'LDF': {'Code': 112.0, 'Type': 3.0, 'Args': 0},
 'LDL': {'Code': 8.0, 'Type': 3.0, 'Args': 0},
 'LDS': {'Code': 108.0, 'Type': 3.0, 'Args': 0},
 'LDT': {'Code': 116.0, 'Type': 3.0, 'Args': 0},
 'LDX': {'Code': 4.0, 'Type': 3.0, 'Args': 0},
 'LPS': {'Code': 208.0, 'Type': 3.0, 'Args': 0},
 'MUL': {'Code': 32.0, 'Type': 3.0, 'Args': 0},
 'MULF': {'Code': 96.0, 'Type': 3.0, 'Args': 0},
 'MULR': {'Code': 152.0, 'Type': 2.0, 'Args': 0},
 'NORM': {'Code': 200.0, 'Type': 1.0, 'Args': 0},
 'OR': {'Code': 68.0, 'Type': 3.0, 'Args': 0},
 'RD': {'Code': 216.0, 'Type': 3.0, 'Args': 0},
 'RMO': {'Code': 172.0, 'Type': 2.0, 'Args': 0},
 'RSUB': {'Code': 76.0, 'Type': 3.0, 'Args': 1},
 'SHIFTL': {'Code': 164.0, 'Type': 2.0, 'Args': 2},
 'SHIFTR': {'Code': 168.0, 'Type': 2.0, 'Args': 2},
 'SIO': {'Code': 240.0, 'Type': 1.0, 'Args': 0},
 'SSK': {'Code': 236.0, 'Type': 3.0, 'Args': 0},
 'STA': {'Code': 12.0, 'Type': 3.0, 'Args': 0},
 'STB': {'Code': 120.0, 'Type': 3.0, 'Args': 0},
 'STCH': {'Code': 84.0, 'Type': 3.0, 'Args': 0},
 'STF': {'Code': 128.0, 'Type': 3.0, 'Args': 0},
 'STI': {'Code': 212.0, 'Type': 3.0, 'Args': 0},
 'STL': {'Code': 20.0, 'Type': 3.0, 'Args': 0},
 'STS': {'Code': 124.0, 'Type': 3.0, 'Args': 0},
 'STSW': {'Code': 232.0, 'Type': 3.0, 'Args': 0},
 'STT': {'Code': 132.0, 'Type': 3.0, 'Args': 0},
 'STX': {'Code': 16.0, 'Type': 3.0, 'Args': 0},
 'SUB': {'Code': 28.0, 'Type': 3.0, 'Args': 0},
 'SUBF': {'Code': 92.0, 'Type': 3.0, 'Args': 0},
 'SUBR': {'Code': 148.0, 'Type': 2.0, 'Args': 0},
 'SVC': {'Code': 176.0, 'Type': 2.0, 'Args': 3},
 'TD': {'Code': 224.0, 'Type': 3.0, 'Args': 0},
 'TIO': {'Code': 248.0, 'Type': 1.0, 'Args': 0},
 'TIX': {'Code': 44.0, 'Type': 3.0, 'Args': 0},
 'TIXR': {'Code': 184.0, 'Type': 2.0, 'Args': 1},
 'WD': {'Code': 220.0, 'Type': 3.0, 'Args': 0},
 'BYTE': {'Code': -1.0, 'Type': -1.0, 'Args': 0},
 'WORD': {'Code': -1.0, 'Type': -1.0, 'Args': 0},
 'RESW': {'Code': -2.0, 'Type': -2.0, 'Args': 1.0},
 'RESB': {'Code': -2.0, 'Type': -2.0, 'Args': 1.0}}
# Registers is a dictionary that consists of all the registers and their associated numerical values
registers = {'A': '0', 'X': '1', 'L': '2', 'PC': '8', 'SW': '9', 'B': '3', 'S': '4', 'T': '5', 'F': '6'}
# Setting up the regular expressions to discern between Type 2 instructions and Type 3 instructions
# Type 2 regular expression is checked for matching in Pass Two of the assembler, where we try to determine whether the instruction is of Type 2
# Type 3 regular expression is checked for matching in Pass Two of the assembler, where we try to determine whether the instruction is of Type 3
type2 = [r"^\s*(?P<reg1>A|X|L|PC|SW|B|S|T|F)\s*,\s*(?P<reg2>A|X|L|PC|SW|B|S|T|F)\s*$", r"^\s*(?P<reg>A|X|L|PC|SW|B|S|T|F)\s*$", r"^\s*(?P<reg>A|X|L|PC|SW|B|S|T|F)\s*,\s*#?(?P<arg>[1-9]|1[0-6])\s*$", r"^\s*#?(?P<arg2>[1-9]|1[0-6])\s*$"]
type3 = [r"^\s*(?P<mode>[@#])?(?P<arg>[0-9]*|[a-z]+[a-z0-9]*)\s*(?P<x>\s*,\s*x)?\s*$", r"^\s*$"]
# An array containing directives that we can use in our later passes to check if detected words are directives
SIC_Directives = [ "START", "END", "BASE", "NOBASE"]
# A class used to create a Line object, for every Line in a file
# The class has a constructor that sets up each object
class Line:
    
    comment = None
    label = None
    mnemonic = None
    number = None
    line_address = None
    orig = None
    args = None
    extended = False
    executable = ""
    base = None
    
    def __init__(self, text, executable, comment, mnemonic, args, label, extended):
        self.orig = text
        self.number = num_line
        self.line_address = line_address
        self.executable = executable
        self.comment = comment
        self.mnemonic = mnemonic
        self.args = args
        self.label = label
        self.extended = extended
        self.base = base

    def display(self):

        if self._mnemonic:
            print("mnemonic =", self._mnemonic, end = ', ')
        if self._label:
            print("label =", self._label, end = ', ')
        if self._comment:
            print("comment =", self._comment, end = ', ')
        if self._extended:
            print("extended =", self._extended, end = ', ')
        print()
        print("       ", self._source)


class ObjectCode:
# The __init__ method takes a filename as an argument and opens it in binary write mode. 
# It also initializes the _program_name instance variable to None.
    def __init__(self, filename):
        try:
            self._file = open(filename, "wb")
            self._program_name = None
        except Exception as e:
            error("File open error:", e)
# The write method writes the specified bytes to the file opened in the __init__ method.
    def write(self, bytes):
        self._file.write(bytes)
# The emitHrecord method emits the Header Record (H record) for the object code file. 
# It calculates the program name, start address, and program length and returns the 
# H record as a string.
    def emitHrecord(self):
        Hrecord = 0
        # name_of_program = (program_name + "      ")[:6]
        name_of_program = ((program_name or "") + "      ")[:6]
        program_name_hex = ""
        for letter in name_of_program:
            program_name_hex += convert_to_hex(ord(letter), 2)
        Hrecord = H + program_name_hex
        Hrecord += convert_to_hex(start_address, 6)
        Hrecord += convert_to_hex(line_address - start_address, 6)
        return Hrecord
# The emitTrecord method emits the Text Records (T record) for the object code file. 
# It takes two arguments: bytesArray which is an array of bytes representing the assembled code, 
# and locArray which is an array of integers representing the location of each byte in memory. 
# It uses these arrays to create one or more T records and returns them as a string.
    def emitErecord(self):
        return E + convert_to_hex(begin, 6)
# The emitErecord method emits the End Record (E record) for the object code file. 
# It takes no arguments and returns the E record as a string.
    def emitTrecord(self, bytesArray, locArray):
        T_records = []
        text_records = ""
        text_record_start = None
        text_record_bytes = ""
        for i in range(len(bytesArray)):
            b = bytesArray[i]
            l = locArray[i]
            if not b:
                if text_record_start is not None:
                    text_record_length = len(text_record_bytes) // 2
                    text_records = text_records + text_record_start + convert_to_hex(text_record_length, 2) + text_record_bytes
                    # reset the text_record_start and text_record_bytes to empty strings.
                    text_record_start = None
                    text_record_bytes = ""
            
            elif text_record_start is None:
                text_record_start = T + convert_to_hex(l, 6)

            if len(text_record_bytes) + len(b) <= 128:
                text_record_bytes += b

            elif len(text_record_bytes) + len(b) > 128:
                text_record_length = len(text_record_bytes) // 2
                text_records = text_records + text_record_start + convert_to_hex(64, 2) + (text_record_bytes + b)[:128]
                text_record_start = T + convert_to_hex(l + (128 - len(text_record_bytes)) // 2, 6)
                text_record_bytes = b[128 - len(text_record_bytes):]

            else:
                text_record_length = len(text_record_bytes) // 2
                text_records += "{}{}{}".format(text_record_start, convert_to_hex(text_record_length, 2), text_record_bytes)
                text_record_start = None
                text_record_bytes = ""
            
        if text_record_bytes:
            text_record_length = len(text_record_bytes) // 2
            text_records += "{}{}{}".format(text_record_start, convert_to_hex(text_record_length, 2), text_record_bytes)
            
        return text_records
# The emitSIC method is the main method of the ObjectCode class. It takes two arguments: bytesArray and locArray, and 
# returns a string that represents the entire object code file. It does this by calling the emitHrecord, emitTrecord, 
# and emitErecord methods and concatenating the resulting strings together.
    def emitSIC(self, bytesArray, locArray):
        records = self.emitHrecord() + self.emitTrecord(bytesArray, locArray) + self.emitErecord()
        return records
# This is a Python function called parseAsmLine that takes a single argument text, which is a string representing an assembly language code line. 
# The function uses regular expressions to extract various pieces of information from the input text.
# The function first initializes several variables to None, an empty string, or False. 
# It then uses the re module to match the input text against various regular expressions.
# The first regular expression is used to check if the line is a comment or empty line. 
# If it is, the function sets the comment variable to the matched comment text, and leaves the other variables as None, an empty string, or False.
# If the line is not a comment or empty line, the function extracts the label (if any), mnemonic, arguments, 
# and extended flag (if present) using another regular expression. The extracted information is then assigned to 
# the label, mnemonic, args, and extended variables, respectively.
# Finally, the function creates and returns a Line object with the extracted information, as well as the original text, 
# the non-comment/non-empty executable part of the text, and the comment part of the text.
def parseAsmLine(text):
    comment = None
    label = None
    mnemonic = None
    args = None
    extended = False
    executable = ""

    match = re.match(r"(^\s*\.\s*(?P<comment>.*)?)|(^\s*$)", text[:40], re.IGNORECASE)
    if match:
        executable = ""
        comment = match.group("comment")
    else:
        executable = text[:40].rstrip()
        completeparse = re.match(r"(^\s*((?P<label>[a-z_][a-z0-9_]*):)?\s*(?P<extended>\+)?(?P<mnemonic>[a-z_]+)\s+(?P<args>.*)?)", text[:40].upper(), re.IGNORECASE)
        comment = text[40:]

        if completeparse:  # check if there was a match
            mnemonic = completeparse.group("mnemonic")
            args = completeparse.group("args").rstrip()   
            label = completeparse.group("label")
            if completeparse.group("extended") == "+":
                extended = True
    return Line(text, executable, comment, mnemonic, args, label, extended)
# CITE: Professor Bailey
# DESC: This code was provided in class to produce customizable errors.
def error(*args):
    print(*args, file = sys.stderr)
    sys.exit(1)        

def REParser(info):
    if isNumber(info.args):
        if int(info.args) >= 2**15:
            raise Exception(f'cant fit in byte line {info.number}: {info.code}')
        else:
            return 1
        
    else:
        match = re.match(r"^\s*(x'(?P<hex>[0-9a-f]*)')|(^\s*c'(?P<string>.*)')", info.args, re.IGNORECASE)
        if match:
            if match.group("hex") != None:
                int(match.group("hex"), base=16)
                return int(len(match.group("hex"))/2) + (len(match.group("hex")) % 2)
            if match.group("string") != None:
                return len(match.group("string"))      
        else:
            sys.exit(1)
# Pass One of the assembler performs the initial parsing of the input source code and generates the symbol table, 
# which maps each symbol to its corresponding memory location.
def passOne(filename): 
# GLOBALS:
    # the name of the program
    global program_name
    program_name = None
    # the starting address
    global start_address
    start_address = 0
    # the line number
    global num_line 
    num_line = 0
    # the address of the line
    global line_address
    line_address = 0
    # address when we begin reading
    global begin
    begin = 0

    global base
    base = None
# VARIABLES:
    file_contents = []
    
    SYMTAB = {}
    
    file =  open(filename, "r")
    
    first_line = 0
    
    started = 0 ### THIS MAYBE WE CAN GET RID OF (RN IT DOESN'T REALLY DO ANYTHING)
    
    while True:
        
        info = file.readline().expandtabs(8)
        info = parseAsmLine(info)
        
        LocCTR = 0
        
        if info.executable != "":
            
            if info.label != None:
                if info.label in SYMTAB.keys():
                    error("Repeated label: ", info.label+".")
                else:
                    SYMTAB[info.label] = line_address
            
            
            if info.mnemonic == "START" and started == False:
                if isNumber(info.args) and int(info.args, base=16) < MAX_SPACE:
                    line_address = int(info.args, base=16)
                    SYMTAB = {x: line_address for x in SYMTAB}
                    started = True
                    if info.label == None:
                        program_name = ""
                    else:
                        program_name = info.label
                    start_address = int(info.args, base=16)
                else:
                    error("Invalid start on line", str(info.number)+":",info.executable)          

            elif info.mnemonic == "START" and started == True:
                error("Program repeats a start on line", str(info.number)+":",info.executable)

            elif info.mnemonic == "BYTE":
                charTemp = 0
                hexTemp = 0
                if isNumber(info.args):
                    if int(info.args) >= 2**15:
                        error("Error: Exceeds allowed characters for byte line ", str(info.number)+":",info.executable)          
                    else:  
                        LocCTR = 1
                else:
                    match = re.match(r"^\s*(x'(?P<X>[0-9a-f]*)')", info.args, re.IGNORECASE)
                    if match:
                        hexTemp = 1
                        if match.group("X") is not None:
                            int(match.group("X"), base=16)
                            LocCTR = int(len(match.group("X"))/2) + (len(match.group("X")) % 2)
                    match = re.match(r"^\s*(c'(?P<C>.*)')", info.args, re.IGNORECASE)
                    if match:
                        charTemp = 1
                        if match.group("C") is not None:
                            LocCTR = len(match.group("C"))
                    if charTemp == 0 and hexTemp == 0:
                        error("Error: Improper decleration of byte directive. Error is on line", str(info.number)+":",info.executable)
                
            elif info.mnemonic == "WORD":
                LocCTR = 3
                
            elif info.mnemonic == "RESW":
                if isNumber(info.args):
                    LocCTR = 3 * int(info.args)
                else:
                    error("Error: invalid arguments given on line", str(info.number)+":",info.executable)

            elif info.mnemonic == "RESB":
                if isNumber(info.args):
                    LocCTR = int(info.args)
                else:
                    error("Error: invalid arguments given on line", str(info.number)+":",info.executable)
            
            
            elif info.mnemonic == "BASE":
                base = info.args
                
            elif info.mnemonic == "NOBASE": # keep in mind
                if info.args == None:
                    base = None
                else:
                    error("Directive NOBASE should take no arguments. Error on line", str(info.number)+":",info.executable)

            elif info.mnemonic == "END":
                file_contents.append(info)
                return SYMTAB, file_contents

            elif info.mnemonic not in opCodes.keys():
                error("Error: mnemonic given is nonexistent. Error is on line", str(info.number)+":",info.executable)  

            else:
                LocCTR = opCodes[info.mnemonic]["Type"]
                
                if first_line == False:
                    begin = info.line_address
                    first_line = True

            if info.extended:
                if opCodes[info.mnemonic]["Type"] == 3:
                    LocCTR = 4
                else:
                    error("Error:"+info.mnemonic+" can't be extended. Error is on line", str(info.number)+":",info.executable)
                        
            line_address += LocCTR
            line_address = line_address % MAX_SPACE
        num_line += 1
        file_contents.append(info)
### ============================================= END OF PASS ONE ========================================================

def displacement_value(info, target, SYMTAB, file_contents):
    displacement_val = 0
    if not info.extended:
        if info.base is not None:
            displacement = (target - convert_to_int(info.base, SYMTAB, info))
            if  0 <= displacement:
                if displacement <= MAX_BASE_RANGE:
                    displacement_val = BASE_FORMAT + displacement
                    return displacement_val
        temp_val = file_contents.index(info) + 1
        displacement = (target - file_contents[temp_val].line_address)
        if 0 <= displacement:
            if displacement <= MAX_PC_RANGE:
                displacement_val = PC_FORMAT + displacement
                return displacement_val

        elif -(MAX_PC_RANGE+1) <= displacement:
            if displacement < 0:
                displacement_val = PC_FORMAT + make_2s_comp(displacement, 12 + (info.extended*8))
                return displacement_val
        else:
            error("A Type 4 instruction needed to reach address at line {info.number}: {info.executable}")
    else:
        displacement = target
        displacement_val = (info.extended * MAX_SPACE) + displacement
        return displacement_val
    
    
def machine_code_generator(opCode, info, target, SYMTAB, file_contents):
    machine_code = 0
    if info.base is not None:
        displacement = (target - convert_to_int(info.base, SYMTAB, info))
        if  0 <= displacement:
            if displacement <= MAX_BASE_RANGE:
                machine_code = ((opCode + 3) * MAX_VALUE) + BASE_FORMAT + displacement
                return machine_code

    displacement = (target - file_contents[file_contents.index(info) + 1].line_address)
    if 0 <= displacement:
        if displacement <= MAX_PC_RANGE:
            machine_code = ((opCode + 3) * MAX_VALUE) + PC_FORMAT + displacement
            return machine_code

    elif -(MAX_PC_RANGE+1) <= displacement:
        if displacement < 0:
            machine_code = ((opCode + 3) * MAX_VALUE) + PC_FORMAT + make_2s_comp(displacement, 12 + (info.extended*8))
            return machine_code

    displacement = target
    if displacement < (MAX_VALUE/2): 
        machine_code = (opCode * MAX_VALUE) + displacement
        return machine_code
    else:
        error("A Type 4 instruction needed to reach address at line {info.number}: {info.executable}")

def make_2s_comp(number, digits):
    if int(number) < 0:
        number = 2 ** digits + int(number)
    return number

def byte_generator(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
# CITE: Professor Bailey
# DESC: Code provided by Professor during class.
def chopNdice(value, size):
    result = []

    while size > 0:
        result.insert(0, value & 0xFF)
        value >>= 8
        size -= 1
    return result

# Pass Two of the assembler
# This code, in a general sense, determines what type of instruction is in each line, as well as
# what type of addressing is needed for this instruction.
def passTwo(SYMTAB, file_contents):
        
    bytesArray = []
    locArray = []
    targetAddress = 0
    for info in file_contents:
        if info.mnemonic is not None and info.mnemonic not in SIC_Directives:
            line_content = ""
            #Code = opCodes[info.mnemonic]["Code"]
            if opCodes[info.mnemonic]["Type"] == 1:
                if len(info.args) != 0:
                    error("Error: Given arguments for type 1 instruction are invalid. Error is on line", str(info.number))  
                else:
                    line_content = hex(int(opCodes[info.mnemonic]["Code"]))[2:]
            elif opCodes[info.mnemonic]["Type"] == 2:
                line_content += type2case(SYMTAB, file_contents, line_content, info, registers)
            elif opCodes[info.mnemonic]["Type"] == 3: 
                args = int(opCodes[info.mnemonic]["Args"])
                checkType3 = re.match(type3[args], info.args, re.IGNORECASE)
                if checkType3:
                    if args == 1:
                        line_content = line_content + hex(int(opCodes[info.mnemonic]["Code"]) + 3)[2:] 
                        line_content = line_content + "0000"
                        if info.extended:
                            line_content = line_content + "00"
                    else:
                        if checkType3.group("mode") == None:
                            targetAddress = convert_to_int(checkType3.group("arg"), SYMTAB, info)
                            if info.extended is False:
                                disp = machine_code_generator(opCodes[info.mnemonic]["Code"], info, targetAddress, SYMTAB, file_contents)
                                factor = (MAX_VALUE/2) * (checkType3.group("x") != None)
                                line_content += convert_to_hex(int(disp) + factor, 6)
                            else:
                                line_content += convert_to_hex(opCodes[info.mnemonic]["Code"] + 3, 2)
                                factor = 2 ** 23
                                factor = factor * (checkType3.group("x") != None)
                                factor += displacement_value(info, targetAddress, SYMTAB, file_contents)
                                line_content += convert_to_hex(factor, 6)
            #indirect:
                        elif checkType3.group("mode") == "@" and checkType3.group("x") == None:
                            # line_content, targetAddress = indirect_mode(info, SYMTAB, file_contents, line_content, targetAddress)
                            line_content += convert_to_hex(opCodes[info.mnemonic]["Code"] + 2, 2)
                            targetAddress = convert_to_int(checkType3.group("arg"), SYMTAB, info)
                            if info.extended:
                                temp_length = 6
                            else:
                                temp_length = 4
                            line_content += convert_to_hex(displacement_value(info, targetAddress, SYMTAB, file_contents), temp_length)
                            # return line_content, targetAddress
            #immediate:
                        elif checkType3.group("mode") == "#" and checkType3.group("x") == None:
                            # line_content, targetAddress = immediate_mode(info, SYMTAB, file_contents, line_content, targetAddress)
                            line_content += convert_to_hex(opCodes[info.mnemonic]["Code"] + 1, 2)
                            targetAddress = convert_to_int(checkType3.group("arg"), SYMTAB, info)
                            if info.extended:
                                temp_length = 6
                            else:
                                temp_length = 4
                            line_content += convert_to_hex(displacement_value(info, targetAddress, SYMTAB, file_contents), temp_length)
                            # return line_content, targetAddress
                        else:
                            error("Error: Addressing mode is invalid on line"+str(info.number)+":",info.executable)
                else:
                    error("Error: Arguments are invalid on line"+str(info.number)+":",info.executable)
                    
            elif opCodes[info.mnemonic]["Type"] == -1:
                if info.mnemonic == "WORD":
                    if int(info.args) < 0:
                        line_content = convert_to_hex(make_2s_comp(info.args, 24), 6)
                    else:
                        line_content = convert_to_hex(info.args, 6)
                else:
                    checkDirective = re.match(r"^\s*(x'(?P<X>[0-9a-f]*)')", info.args, re.IGNORECASE)
                    temp_hex_val = 0
                    temp_str_val = 0 
                    if checkDirective:
                        temp_hex_val = 1
                        if checkDirective.group("X") != None:
                            line_content += convert_to_hex(int(checkDirective.group("X"), base=16), len(checkDirective.group("X")) + (len(checkDirective.group("X")) % 2))
                    checkDirective = re.match(r"^\s*(c'(?P<C>.*)')", info.args, re.IGNORECASE)
                    if checkDirective:
                        temp_str_val = 1
                        if checkDirective.group("C") != None:
                            for letter in checkDirective.group("C") :
                                line_content = line_content + hex(ord(letter))[2:]
                    if temp_hex_val == 0 and temp_str_val == 0:
                        val = int(info.args)
                        if 0 <= val < 256: 
                            line_content = convert_to_hex(info.args, 2)
                        elif 0 > val >= -256:
                            line_content = convert_to_hex(make_2s_comp(info.args, 8), 2)
                
            bytesArray.append(line_content)
            locArray.append(info.line_address)
                
    return bytesArray, locArray
### ============================================== END OF PASS TWO =========================================================
# Indirect Addressing helper function
def indirect_mode(info, SYMTAB, file_contents, line_content, targetAddress):
    line_content += convert_to_hex(opCodes[info.mnemonic]["Code"] + 2, 2)
    targetAddress = convert_to_int(checkType3.group("arg"), SYMTAB, info)
    if info.extended:
        temp_length = 6
    else:
        temp_length = 4
    line_content += convert_to_hex(displacement_value(info, targetAddress, SYMTAB, file_contents), temp_length)
    return line_content, targetAddress
# Immediate Addressing helper function
def immediate_mode(info, SYMTAB, file_contents, line_content, targetAddress):
    line_content += convert_to_hex(opCodes[info.mnemonic]["Code"] + 1, 2)
    targetAddress = convert_to_int(checkType3.group("arg"), SYMTAB, info)
    if info.extended:
        temp_length = 6
    else:
        temp_length = 4
    line_content += convert_to_hex(displacement_value(info, targetAddress, SYMTAB, file_contents), temp_length)
    return line_content, targetAddress
# Code that is executed if the instruction is a Type 2 instruction 
def type2case(SYMTAB, file_contents, line_content, info, registers):
    temp_arg = int(opCodes[info.mnemonic]["Args"])
    match = re.match(type2[temp_arg], info.args, re.IGNORECASE)
    temp_val = opCodes[info.mnemonic]["Code"]
    casted_temp = int(temp_val)
    hex_casted = hex(casted_temp)
    spliced_hex = hex_casted[2:]
    if match:
        if temp_arg == 0:
            line_content = line_content + spliced_hex + registers[match.group("reg1")] + registers[match.group("reg2")]
        
        elif temp_arg == 1:
            line_content = line_content + spliced_hex + registers[match.group("reg")] + "0"

        elif temp_arg == 2:
            line_content = line_content + spliced_hex + registers[match.group("reg")] + hex(int(match.group("arg")) - 1)[2:]

        else:
            line_content = line_content + spliced_hex + hex(int(match.group("arg2")))[2:] + "0"
    else:
        error("Invalid argument given on line"+ info.number+ " Error in code: ")
    return line_content

def convert_to_int(val, SYMTAB, info):
    try:
        return int(val)
    except ValueError:
        try:
            return int(SYMTAB[val])
        except KeyError:
            error(val+" is not a label at line "+str(info.number)+":",info.executable)

def convert_to_hex(i, length):
    return format(int(i), f'0{length}x')

def isNumber(num):
    try:
        int(num)
        return True
    except:
        return False

def main():
    filename = sys.argv[1]
    objectFile = sys.argv[2]
  
    SYMTAB, file_contents = passOne(filename)

    bytesArray, locArray = passTwo(SYMTAB, file_contents)

    objcode = ObjectCode(sys.argv[2])
    Assembled_Code = byte_generator(objcode.emitSIC(bytesArray, locArray))

    file = open(objectFile, "wb")
    for i in range(len(Assembled_Code)): 
        # to_bytes = byte size 1, and "little" for little-endian order
        file.write(int(Assembled_Code[i], base = 16).to_bytes(1, "little"))
         
main()