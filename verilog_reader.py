import re

network_name = []

with open('trindade16/FA.v', 'r') as reader:
    line = reader.readline()
    # print(reader.readline)
    # while line != '':  # The EOF char is an empty string
    #     if not(line[0] == "#"):
    #        print(line, end='')
            
    #     line = reader.readline()
    
    full_text = reader.readlines()

    network_name = re.split('\.|/', str(reader.name))

with open('trindade16_blueprints/FA.txt', 'w') as writer:
    # Alternatively you could use
    # writer.writelines(reversed(dog_breeds))
    
    writer.write("template <typename Ntk>\n")
    writer.write("mockturtle::names_view<Ntk> {}()\n".format(network_name[1]))
    writer.write("{\n")
    writer.write("    mockturtle::names_view<Ntk> ntk{};\n")

    # Write the dog breeds to the file in reversed order
    output_storage = []
    output_name_storage = []
    gate_string_storage = []
    placed_gates_storage = []
    required_gates_storage = []
    place_this_gate = []

    one_line = ""
    last_sign_flag = False
    process_flag = False

    inverted_lines = []
    for new_line in full_text:
        new_line = new_line.replace(';', '')
        new_line = new_line.replace(',', '')
        res = new_line.split()
        if(len(res)==6):
            if("~" in res[3] and not (res[3][1:] in inverted_lines)):
                res[3] = res[3].replace('~', '')
                inverted_lines.append(res[3])
            if("~" in res[5] and not (res[5][1:] in inverted_lines)):
                res[5] = res[5].replace('~', '')
                inverted_lines.append(res[5])

    for new_line in full_text:
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

                if(len(res) == 6):
                    if("~" in res[3]):
                        inv_one_sign = "n"
                        res[3] = res[3].replace('~', '')
                        if(res[3] in inverted_lines):
                            writer.write("    const auto n{} = ntk.create_not({});\n".format(res[3], res[3]))
                            inverted_lines.remove(res[3])
                    if("~" in res[5]):
                        inv_two_sign = "n"
                        res[5] = res[5].replace('~', '')
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
                    for input in res:
                        if(input != "input"):
                            writer.write("    const auto {} = ntk.create_pi(\"{}\");\n".format(input, input))
                            placed_gates_storage.append(input)
                
                elif(res[0] == "output"):
                    for output in res:
                        if(output != "output"):
                            output_storage.append("    ntk.create_po({}, \"{}\");\n".format(output, output))
                
                elif(4 <len(res)<6):
                    if("~" in res[3]):
                        res[3] = res[3][1]
                        writer.write("    const auto {} = ntk.create_not({});\n".format(res[1], res[3]))
                elif(len(res)<4):
                    pass   

                elif(res[4] == "&"):
                    writer.write("    const auto {} = ntk.create_and({}{}, {}{});\n".format(res[1], inv_one_sign, res[3], inv_two_sign ,res[5]))

                elif(res[4] == "|"):
                    writer.write("    const auto {} = ntk.create_or({}, {});\n".format(res[1], res[3], res[5]))

                elif(res[4] == "^"):
                    writer.write("    const auto n{} = ntk.create_not({});\n".format(res[3], res[3]))
                    writer.write("    const auto n{} = ntk.create_not({});\n".format(res[5], res[5]))
                    writer.write("    const auto {}_h = ntk.create_and({}, n{});\n".format(res[3], res[3], res[5]))
                    writer.write("    const auto {}_h = ntk.create_and(n{}, {});\n".format(res[5], res[3], res[5]))
                    writer.write("    const auto {} = ntk.create_or({}_h, {}_h);\n".format(res[1], res[3], res[5]))
                
                process_flag = False

    writer.write("\n")

    for po in output_storage:
        writer.write(po)
    

    writer.write("\n")
    writer.write("    return ntk;\n")

    writer.write("}")