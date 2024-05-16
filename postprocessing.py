def unite(func_file_name,main_file_name,res):
    func_file = open(func_file_name,"r")
    main_file = open (main_file_name, "r")
    res = open(res, "w")
    main_lines = main_file.readlines()
    func_lines = func_file.readlines()
    main_counter = 0
    main_line = main_lines[main_counter]
    res.write(main_line)
    while main_line != "[code]\n":
        main_counter = main_counter + 1
        main_line = main_lines[main_counter]
        #if main_line != "[code]\n":
        res.write(main_line)
    res.write("\n\n")
    for func_line in func_lines:
        res.write(func_line)
    #temp.write("[code]\n")
    res.write(";/main/\n")
    while main_counter < len(main_lines) - 1:
        main_counter +=1
        main_line = main_lines[main_counter]
        res.write(main_line)
    res.close()

def set_com_reg(temp_file, res):
    temp_file = open(temp_file, "r")
    res = open(res, "w")
    temp_lines = temp_file.readlines()
    lines_counter = 0
    now_line = temp_lines[lines_counter]
    res.write(now_line)
    com_register = 0x0000
    while now_line != "[code]\n":
        lines_counter += 1
        now_line = temp_lines[lines_counter]
        res.write(now_line)

    while lines_counter < len(temp_lines) - 1:
        lines_counter += 1
        now_line = temp_lines[lines_counter]
        if "||" in now_line :
            com_register += 1
            now_line = now_line[:-5]
            now_line += format(com_register, '04x')
            now_line += "\n"
            res.write(now_line)
        else:
             res.write(now_line)


    #new_file.write(format(com_register, '04x'))

    


def make_jumps(temp_file, res):
    temp_file = open(temp_file, "r")
    res = open(res, "w")
    temp_lines = temp_file.readlines()
    _jump_if_false_condition_ = "_jump_if_false_condition_"
    _arrive_after_false_condition_ = "_arrive_after_false_condition_"
    _jump_before_else_ = "_jump_before_else_"
    _arrive_after_else_ ="_arrive_after_else_"
    _repeat_while_ = "_repeat_while_"
    _jump_if_false_while_ = "_jump_if_false_while_"
    _arrive_after_false_while_ = "_arrive_after_false_while_"
    _call_func_ = "_call_func_"
    _function_ = "_function_"
    flag = 1
    while flag == 1:
        flag = 0
        for num in range (len(temp_lines)):
            if _jump_if_false_condition_ in temp_lines[num]:
                index = temp_lines[num].find(_jump_if_false_condition_)
                substring_end = temp_lines[num][index + len(_jump_if_false_condition_):]
                characters_after_substring = substring_end.split()[0]
                found_sting = _arrive_after_false_condition_ + str(characters_after_substring) + " "
                temp_lines[num] = temp_lines[num].replace(_jump_if_false_condition_ + str(characters_after_substring) + " ", "")
                
                for num2 in range (len(temp_lines)):
                    if found_sting in temp_lines[num2]:
                        first_occurrence = temp_lines[num2].find("|| ")
                        if first_occurrence != -1:
                            second_occurrence = temp_lines[num2].find("|| ", first_occurrence + 1)
                        find_com_reg = second_occurrence
                        com_reg = temp_lines[num2][find_com_reg + len("|| "):find_com_reg + len("|| ") + 4]
                        temp_lines[num2] = temp_lines[num2].replace(found_sting, "")
                temp_lines[num] = temp_lines[num].replace("????", com_reg)
                flag = 1

            if _jump_before_else_ in temp_lines[num]:
                index = temp_lines[num].find(_jump_before_else_)
                substring_end = temp_lines[num][index + len(_jump_before_else_):]
                characters_after_substring = substring_end.split()[0]
                found_sting = _arrive_after_else_ + str(characters_after_substring) + " "
                temp_lines[num] = temp_lines[num].replace(_jump_before_else_ + str(characters_after_substring) + " ", "")
                
                for num2 in range (len(temp_lines)):
                    if found_sting in temp_lines[num2]:
                        first_occurrence = temp_lines[num2].find("|| ")
                        if first_occurrence != -1:
                            second_occurrence = temp_lines[num2].find("|| ", first_occurrence + 1)
                        find_com_reg = second_occurrence
                        com_reg = temp_lines[num2][find_com_reg + len("|| "):find_com_reg + len("|| ") + 4]
                        temp_lines[num2] = temp_lines[num2].replace(found_sting, "")
                temp_lines[num] = temp_lines[num].replace("????", com_reg)
                flag = 1

            if _repeat_while_ in temp_lines[num]:
                index = temp_lines[num].find(_repeat_while_)
                substring_end = temp_lines[num][index + len(_repeat_while_):]
                characters_after_substring = substring_end.split()[0]
                found_sting = _jump_if_false_while_ + str(characters_after_substring) + " "
                temp_lines[num] = temp_lines[num].replace(_repeat_while_ + str(characters_after_substring) + " ", "")
                
                for num2 in range (len(temp_lines)):
                    if found_sting in temp_lines[num2]:
                        first_occurrence = temp_lines[num2].find("|| ")
                        if first_occurrence != -1:
                            second_occurrence = temp_lines[num2].find("|| ", first_occurrence + 1)
                        find_com_reg = second_occurrence
                        com_reg = temp_lines[num2][find_com_reg + len("|| "):find_com_reg + len("|| ") + 4]
                temp_lines[num] = temp_lines[num].replace("????", com_reg)
                flag = 1

            if _call_func_ in temp_lines[num]:
                index = temp_lines[num].find(_call_func_)
                substring_end = temp_lines[num][index + len(_call_func_):]
                characters_after_substring = substring_end.split()[0]
                found_sting = _function_ + str(characters_after_substring) + " "
                temp_lines[num] = temp_lines[num].replace(_call_func_ + str(characters_after_substring) + " ", "")
                
                for num2 in range (len(temp_lines)):
                    if found_sting in temp_lines[num2]:
                        first_occurrence = temp_lines[num2].find("|| ")
                        if first_occurrence != -1:
                            second_occurrence = temp_lines[num2].find("|| ", first_occurrence + 1)
                        find_com_reg = second_occurrence
                        com_reg = temp_lines[num2][find_com_reg + len("|| "):find_com_reg + len("|| ") + 4]
                        temp_lines[num2] = temp_lines[num2].replace(found_sting, ";function " + str(characters_after_substring) + "\n")
                temp_lines[num] = temp_lines[num].replace("????", com_reg)
                flag = 1
    flag = 1
    while flag == 1:
        flag = 0
        for num in range (len(temp_lines)):
            if _jump_if_false_while_ in temp_lines[num]:
                index = temp_lines[num].find(_jump_if_false_while_)
                substring_end = temp_lines[num][index + len(_jump_if_false_while_):]
                characters_after_substring = substring_end.split()[0]
                found_sting = _arrive_after_false_while_ + str(characters_after_substring) + " "
                temp_lines[num] = temp_lines[num].replace(_jump_if_false_while_ + str(characters_after_substring) + " ", "")
                
                for num2 in range (len(temp_lines)):
                    if found_sting in temp_lines[num2]:
                        first_occurrence = temp_lines[num2].find("|| ")
                        if first_occurrence != -1:
                            second_occurrence = temp_lines[num2].find("|| ", first_occurrence + 1)
                        find_com_reg = second_occurrence
                        com_reg = temp_lines[num2][find_com_reg + len("|| "):find_com_reg + len("|| ") + 4]
                        temp_lines[num2] = temp_lines[num2].replace(found_sting, "")
                temp_lines[num] = temp_lines[num].replace("????", com_reg)
                flag = 1
    
    for line in temp_lines:
        res.write(line)
    res.close()
    temp_file.close()

                    
def modify_jump_var(in_file, out_file):
    with open(in_file, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line_index, line in enumerate(lines):
        words = line.split()
        if len(words) >= 8 and words[1] == 'jump':
            try:
                word8_index = (line_index + 2) % len(lines)  # Индекс строки + 2
                word8 = int(lines[word8_index].split()[-1], 16)
                print("%04x" % word8)
                words[9] = "%04x" % word8
                words[3] = "%04x" % word8 + ";"
            except (ValueError, IndexError):
                # Если не удается преобразовать в число или выходит за пределы списка строк, оставляем строку без изменений
                pass
        modified_lines.append(' '.join(words) + '\n')

    with open(out_file, 'w') as file:
        file.writelines(modified_lines)


def replace_register(in_file, out_file):
    with open(in_file, 'r') as f_in:
        lines = f_in.readlines()

    with open(out_file, 'w') as f_out:
        for line in lines:
            if line.count("||") >= 2:
                first_pipe_index = line.find("||")
                second_pipe_index = line.find("||", first_pipe_index + 1)
                if second_pipe_index != -1:
                    second_word = line[second_pipe_index + 2:line.find('\n', second_pipe_index)].strip()
                    first_word = line[:first_pipe_index].split()[-1]
                    new_line = line.replace(first_word, second_word, 1)
                    f_out.write(new_line)
                else:
                    f_out.write(line)
            else:
                f_out.write(line)

def delete_temp_register(in_file, out_file):
    with open(in_file, 'r') as input_file:
        with open(out_file, 'w') as output_file:
            inside_code_block = False
            for line in input_file:
                if line.strip() == '[code]':
                    inside_code_block = True
                    output_file.write(line)
                    continue
                elif line.strip() == '-------':
                    inside_code_block = False
                    output_file.write(line)
                    continue
                
                elif len(line.strip()) == 0 or line.strip()[0] == ';':
                    output_file.write(line)
                    continue
                
                if inside_code_block:
                    output_line = line[:-8] + line[-1] if len(line) > 8 else line[-1]
                    output_file.write(output_line)
                else:
                    output_file.write(line)