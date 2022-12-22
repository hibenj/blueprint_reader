import re

network_name = []

with open('i99t/b06/b06.bench', 'r') as reader:
    line = reader.readline()
    # print(reader.readline)
    # while line != '':  # The EOF char is an empty string
    #     if not(line[0] == "#"):
    #        print(line, end='')
            
    #     line = reader.readline()
    
    full_text = reader.readlines()

    network_name = re.split('\.|/', str(reader.name))

with open('i99t_blueprints/b06.txt', 'w') as writer:
    # Alternatively you could use
    # writer.writelines(reversed(dog_breeds))
    
    writer.write("template <typename Ntk>\n")
    writer.write("mockturtle::names_view<Ntk> {}()\n".format(network_name[2]))
    writer.write("{\n")
    writer.write("    mockturtle::names_view<Ntk> ntk{};\n")

    # Write the dog breeds to the file in reversed order
    register_storage = []
    bridge_storage = []
    output_storage = []
    gate_string_storage = []
    placed_gates_storage = []
    required_gates_storage = []
    place_this_gate = []
    bridge_counter = 1

    for new_line in full_text:
        if not(new_line[0] == "#"):
            new_line = new_line.replace(' ', '')
            res = re.split('=|\)|\(|,', new_line)

            if("INPUT" in new_line):
                # writer.write(new_line)
                
                #split the string to get the name of the INPUT
                #INPUT name = res[1]

                #write the corresponding blueprint line
                # e.g. const auto a = ntk.create_pi("a");

                writer.write("    const auto {} = ntk.create_pi(\"{}\");".format(res[1], res[1]))
                placed_gates_storage.append(res[1])

                writer.write("\n")
            elif("OUTPUT" in new_line):

                #write the corresponding blueprint line
                # e.g. ntk.create_po(m, "f");
                # e.g. const auto bridge_out_neg_1 = ntk.create_not(OUTP_REG);
                if("REG" in res[1]):
                    Bridge_Appendix = []
                    Bridge_Appendix.append("    const auto bridge_out_neg_{} = ntk.create_not({});\n".format(bridge_counter, res[1]))
                    Bridge_Appendix.append("    const auto bridge_out_{} = ntk.create_not(bridge_out_neg_{});\n".format(bridge_counter, bridge_counter))

                    bridge_storage.append(Bridge_Appendix)
                    output_storage.append("    ntk.create_po(bridge_out_{}, \"{}\");\n".format(bridge_counter, res[1]))
                    bridge_counter += 1
                else:
                    output_storage.append("    ntk.create_po({}, \"{}\");\n".format(res[1], res[1]))

            elif("REG" in res[0]):

                #write the corresponding blueprint line for RO
                # e.g. const auto r1_o = ntk.create_ro();
                writer.write("    const auto {} = ntk.create_ro();\n".format(res[0]))
                placed_gates_storage.append(res[0])


                #safe the corresponding blueprint line for RI and write later
                # e.g. ntk.create_ri(xo1);
                ri_creator = "    ntk.create_ri({});\n".format(res[2])
                register_storage.append(ri_creator)

            elif(len(res) == 4):
                if("NOT" in res[1]):
                    #res[2] is input

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    # writer.write("    const auto {} = ntk.create_not({});\n".format(res[0], res[2]))
                    Appendix = []
                    Appendix.append("    const auto {} = ntk.create_not({});\n".format(res[0], res[2]))

                    gate_string_storage.append(Appendix)

                    required_gates_storage.append([res[2]])
                    place_this_gate.append(res[0])
            
            elif(len(res) == 5):
                if("NAND" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h);\n".format(res[0], res[0]))

                    gate_string_storage.append(Appendix)

                elif("AND" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {} = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))

                    gate_string_storage.append(Appendix)
                
                elif("NOR" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h);\n".format(res[0], res[0]))

                    gate_string_storage.append(Appendix)

                elif("OR" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {} = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))

                    gate_string_storage.append(Appendix)

                required_gates_storage.append([res[2], res[3]])

                place_this_gate.append(res[0])

            elif(len(res) == 6):
                if("NAND" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_and({}_h1, {});\n".format(res[0], res[0], res[4]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h2);\n".format(res[0], res[0]))

                    gate_string_storage.append(Appendix)

                elif("AND" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {} = ntk.create_and({}_h1, {});\n".format(res[0], res[0], res[4]))

                    gate_string_storage.append(Appendix)
                
                elif("NOR" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_or({}_h1, {});\n".format(res[0], res[0], res[4]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h2);\n".format(res[0], res[0]))

                    gate_string_storage.append(Appendix)

                elif("OR" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {} = ntk.create_or({}_h1, {});\n".format(res[0], res[0], res[4]))

                    gate_string_storage.append(Appendix)
                
                required_gates_storage.append([res[2], res[3], res[4]])

                place_this_gate.append(res[0])

            elif(len(res) == 7):
                if("NAND" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_and({}, {});\n".format(res[0], res[4], res[5]))
                    Appendix.append("    const auto {}_h3 = ntk.create_and({}_h1, {}_h2);\n".format(res[0], res[0], res[0]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h3);\n".format(res[0], res[0]))

                    gate_string_storage.append(Appendix)

                elif("AND" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_and({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_and({}, {});\n".format(res[0], res[4], res[5]))
                    Appendix.append("    const auto {} = ntk.create_and({}_h1, {}_h2);\n".format(res[0], res[0], res[0]))

                    gate_string_storage.append(Appendix)
                
                elif("NOR" in res[1]):
                    #res[2] and res[3] are the two inputs

                    #write the corresponding blueprint line for RO
                    # e.g. const auto f = ntk.create_and(a, n);
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_or({}, {});\n".format(res[0], res[4], res[5]))
                    Appendix.append("    const auto {}_h3 = ntk.create_or({}_h1, {}_h2);\n".format(res[0], res[0], res[0]))
                    Appendix.append("    const auto {} = ntk.create_not({}_h3);\n".format(res[0], res[0]))
                    gate_string_storage.append(Appendix)

                elif("OR" in res[1]):
                    Appendix = []
                    Appendix.append("    const auto {}_h1 = ntk.create_or({}, {});\n".format(res[0], res[2], res[3]))
                    Appendix.append("    const auto {}_h2 = ntk.create_or({}, {});\n".format(res[0], res[4], res[5]))
                    Appendix.append("    const auto {} = ntk.create_or({}_h1, {}_h2);\n".format(res[0], res[0], res[0]))

                    gate_string_storage.append(Appendix)

                required_gates_storage.append([res[2], res[3], res[4], res[5]])

                place_this_gate.append(res[0])

            else:
                print(res)
    
    go_ahead = False
    i = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while(go_ahead == False):
        go_ahead = True
        iterator = 0
        for write in required_gates_storage:
            # print(write)
            place = True
            if not (place_this_gate[iterator] in placed_gates_storage):
                for current_gate in write:
                    if not(current_gate in placed_gates_storage):
                        place = False
                        go_ahead = False
                        # print("NOT PLACED" + current_gate)
                if(place):
                    placed_gates_storage.append(place_this_gate[iterator])
                    for g in gate_string_storage[iterator]:
                        writer.write(g)
                    # writer.write(gate_string_storage[iterator])
                    # print(iterator)
            iterator +=1
            # print(iterator)

    writer.write("\n")

    for bridge in bridge_storage:
        for b in bridge:
            writer.write(b)

    writer.write("\n")

    for po in output_storage:
        writer.write(po)
    
    writer.write("\n")

    for ri in register_storage:
        writer.write(ri)

    writer.write("\n")
    writer.write("    return ntk;\n")

    writer.write("}")