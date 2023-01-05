import re

network_name = []

file_name = "max"
folder_name = "EPFL"

with open('{}/{}.v'.format(folder_name, file_name), 'r') as reader:
    line = reader.readline()
    # print(reader.readline)
    # while line != '':  # The EOF char is an empty string
    #     if not(line[0] == "#"):
    #        print(line, end='')
            
    #     line = reader.readline()
    
    full_text = reader.readlines()

    network_name = re.split('\.|/', str(reader.name))

with open('{}_blueprints/{}.txt'.format(folder_name, file_name), 'w') as writer:
    # Alternatively you could use
    # writer.writelines(reversed(dog_breeds))
    
    writer.write("template <typename Ntk>\n")
    writer.write("mockturtle::names_view<Ntk> {}_{}()\n".format(folder_name, network_name[1]))
    writer.write("{\n")
    writer.write("    mockturtle::names_view<Ntk> ntk{};\n")

    # Write the dog breeds to the file in reversed order
    output_storage = []
    output_name_storage = []
    gate_string_storage = []
    placed_gates_storage = []
    required_gates_storage = []
    place_this_gate = []
    inv_output_storage = []
    inputs = []

    one_line = ""
    last_sign_flag = False
    process_flag = False

    inverted_lines = []
    for new_line in full_text:
        new_line = new_line.lower()
        new_line = new_line.replace(';', '')
        new_line = new_line.replace(',', '')
        res = new_line.split()
        r_it = 0
        for r in res:
            if r[-1] == "_":
                res[r_it] = res[r_it][:-1]
            r_it += 1
        # print(res)
        if(len(res)==6):
            check = ""
            check = res[3].replace('~', '')
            if(check[0] == "\\"):
                    check = check.replace('\\', '')
            if(check[0].isdigit()):
                check =  "x" + check

            if("~" in res[3] and not (check in inverted_lines)):
                res[3] = res[3].replace('~', '')
                if(res[3][0] == "\\"):
                    res[3] = res[3].replace('\\', '')
                if(res[3][0].isdigit()):
                    res[3] =  "x" + res[3]
                inverted_lines.append(res[3])

            check = res[5].replace('~', '')
            if(check[0] == "\\"):
                    check = check.replace('\\', '')
            if(check[0].isdigit()):
                check =  "x" + check

            if("~" in res[5] and not (check in inverted_lines)):
                res[5] = res[5].replace('~', '')
                if(res[5][0] == "\\"):
                    res[5] = res[5].replace('\\', '')
                if(res[5][0].isdigit()):
                    res[5] =  "x" + res[5]
                inverted_lines.append(res[5])
    # print(inverted_lines)

    place_0_const = False
    place_1_const = False

    for new_line in full_text:
        new_line = new_line.lower()
        res = new_line.split()
        if "1'b0" in new_line:
            place_0_const = True
        if "1'b1" in new_line:
            place_1_const = True


    for new_line in full_text:
        new_line = new_line.lower()
        inv_one_sign = ""
        inv_two_sign = ""
        
        if(len(new_line)>3):
            if(new_line[-2] != ";"):
                if(one_line == ""):
                    one_line = new_line
                else:
                    one_line = (one_line + new_line)
                last_sign_flag = True
            
            elif(last_sign_flag == True):
                one_line = (one_line + new_line)
                #new_line = one_line.replace('\n', '')
                new_line = one_line
                # print(res)
                last_sign_flag = False
                process_flag = True
                one_line = ""
            else:
                process_flag = True

            if(process_flag == True):
                new_line = new_line.replace(';', '')
                new_line = new_line.replace(',', '')
                res = new_line.split()
                r_it = 0
                for r in res:
                    if r[-1] == "_":
                        res[r_it] = res[r_it][:-1]
                    r_it += 1

                if(len(res) == 6):
                    if("~" in res[3]):
                        inv_one_sign = "n"
                        res[3] = res[3].replace('~', '')
                        if(res[3][0] == "\\"):
                            res[3] = res[3].replace('\\', '')
                        if(res[3][0].isdigit()):
                            res[3] =  "x" + res[3]
                        if(res[3] in inverted_lines):
                            writer.write("    const auto n{} = ntk.create_not({});\n".format(res[3], res[3]))
                            inverted_lines.remove(res[3])
                    if("~" in res[5]):
                        inv_two_sign = "n"
                        res[5] = res[5].replace('~', '')
                        if(res[5][0] == "\\"):
                            res[5] = res[5].replace('\\', '')
                        if(res[5][0].isdigit()):
                            res[5] =  "x" + res[5]
                        if(res[5] in inverted_lines):
                            writer.write("    const auto n{} = ntk.create_not({});\n".format(res[5], res[5]))
                            inverted_lines.remove(res[5])

                if(len(res) == 0):
                    pass
                elif(res[0] == "wire"):
                    pass
                elif(res[0] == "module"):
                    pass
                elif(res[0] == "endmodule"):
                    pass
                elif(line[0]=="//"):
                    pass
                
                elif(res[0] == "input"):
                    inputs = res
                    if(place_0_const == True):
                        writer.write("    const auto const0 = ntk.create_pi(\"const0\");\n")
                        place_0_const = False
                    if(place_1_const == True):
                        writer.write("    const auto const1 = ntk.create_pi(\"const1\");\n")
                        place_1_const = False

                    for input in res:
                        if(input != "input"):
                            if(input[0] == "\\"):
                                input = input.replace('\\', '')
                            if(input[0].isdigit()):
                                input =  "x" + input
                            writer.write("    const auto {} = ntk.create_pi(\"{}\");\n".format(input, input))
                            placed_gates_storage.append(input)
                            
                
                elif(res[0] == "output"):
                    for output in res:
                        if(output != "output"):
                            if(output[0] == "\\"):
                                output = output.replace('\\', '')
                            if(output[0].isdigit()):
                                output =  "x" + output
                            output_storage.append("    ntk.create_po({}, \"{}\");\n".format(output, output))
                
                elif(3 <len(res)<6):
                    if("~" in res[3]):
                        res[3] = res[3][1:]
                        if(res[1][0] == "\\"):
                            res[1] = res[1].replace('\\', '')
                        
                        if(res[1][0].isdigit()):
                            res[1] =  "x" + res[1]
                        
                        if(res[3][0] == "\\"):
                            res[3] = res[3].replace('\\', '')
                        
                        if(res[3][0].isdigit()):
                            res[3] =  "x" + res[3]
                        writer.write("    const auto {} = ntk.create_not({});\n".format(res[1], res[3]))
                    else:
                        if(res[1][0] == "\\"):
                            res[1] = res[1].replace('\\', '')
                        
                        if(res[1][0].isdigit()):
                            res[1] =  "x" + res[1]
                        
                        if(res[3][0] == "\\"):
                            res[3] = res[3].replace('\\', '')
                        
                        if(res[3][0].isdigit()):
                            res[3] =  "x" + res[3]
                        for o in output_storage:
                            string = res[1] + ","
                            if string in o:
                                output_storage.remove(o)
                        if (res[3] =="x1'b0"):
                            inv_output_storage.append("    const auto nconst0 = ntk.create_not(const0);\n")
                            inv_output_storage.append("    const auto nnconst0 = ntk.create_not(nconst0);\n")
                            output_storage.append("    ntk.create_po(nnconst0, \"{}\");\n".format(res[1]))
                            print(res)
                        elif (res[3] =="x1'b1"):
                            inv_output_storage.append("    const auto nconst1 = ntk.create_not(const1);\n")
                            inv_output_storage.append("    const auto nnconst1 = ntk.create_not(nconst1);\n")
                            output_storage.append("    ntk.create_po(nnconst1, \"{}\");\n".format(res[1]))
                            print(res)
                        else:
                            if res[3][1:] in inputs:
                                print(res)
                                inv_output_storage.append("    const auto n{} = ntk.create_not({});\n".format(res[1], res[3]))
                                inv_output_storage.append("    const auto nn{} = ntk.create_not(n{});\n".format(res[1], res[1]))
                                output_storage.append("    ntk.create_po(nn{}, \"{}\");\n".format(res[1], res[1]))
                            else:
                                output_storage.append("    ntk.create_po({}, \"{}\");\n".format(res[3], res[1]))
                        
                elif(len(res)<4):
                    print(res)   

                elif(res[4] == "&"):
                    if(res[1][0] == "\\"):
                        res[1] = res[1].replace('\\', '')
                    if(res[1][0].isdigit()):
                        res[1] =  "x" + res[1]
                    if(res[3][0] == "\\"):
                        res[3] = res[3].replace('\\', '')
                    if(res[3][0].isdigit()):
                        res[3] =  "x" + res[3]
                    if(res[5][0] == "\\"):
                        res[5] = res[5].replace('\\', '')
                    if(res[5][0].isdigit()):
                        res[5] =  "x" + res[5]
                    writer.write("    const auto {} = ntk.create_and({}{}, {}{});\n".format(res[1], inv_one_sign, res[3], inv_two_sign ,res[5]))

                elif(res[4] == "|"):
                    if(res[1][0] == "\\"):
                        res[1] = res[1].replace('\\', '')
                    if(res[1][0].isdigit()):
                        res[1] =  "x" + res[1]
                    if(res[3][0] == "\\"):
                        res[3] = res[3].replace('\\', '')
                    if(res[3][0].isdigit()):
                        res[3] =  "x" + res[3]
                    if(res[5][0] == "\\"):
                        res[5] = res[5].replace('\\', '')
                    if(res[5][0].isdigit()):
                        res[5] =  "x" + res[5]
                    writer.write("    const auto {} = ntk.create_or({}, {});\n".format(res[1], res[3], res[5]))

                elif(res[4] == "^"):
                    if(res[1][0] == "\\"):
                        res[1] = res[1].replace('\\', '')
                    if(res[1][0].isdigit()):
                        res[1] =  "x" + res[1]
                    if(res[3][0] == "\\"):
                        res[3] = res[3].replace('\\', '')
                    if(res[3][0].isdigit()):
                        res[3] =  "x" + res[3]
                    if(res[5][0] == "\\"):
                        res[5] = res[5].replace('\\', '')
                    if(res[5][0].isdigit()):
                        res[5] =  "x" + res[5]
                    writer.write("    const auto n{} = ntk.create_not({});\n".format(res[3], res[3]))
                    writer.write("    const auto n{} = ntk.create_not({});\n".format(res[5], res[5]))
                    writer.write("    const auto {}_h = ntk.create_and({}, n{});\n".format(res[3], res[3], res[5]))
                    writer.write("    const auto {}_h = ntk.create_and(n{}, {});\n".format(res[5], res[3], res[5]))
                    writer.write("    const auto {} = ntk.create_or({}_h, {}_h);\n".format(res[1], res[3], res[5]))
                
                process_flag = False

    writer.write("\n")

    for inv_po in inv_output_storage:
        writer.write(inv_po)

    for po in output_storage:
        writer.write(po)
    

    writer.write("\n")
    writer.write("    return ntk;\n")

    writer.write("}")