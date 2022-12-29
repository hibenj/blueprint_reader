import re

network_name = []

with open('dot_nws/random_3.dot', 'r') as reader:
    line = reader.readline()
    # print(reader.readline)
    # while line != '':  # The EOF char is an empty string
    #     if not(line[0] == "#"):
    #        print(line, end='')
            
    #     line = reader.readline()
    
    full_text = reader.readlines()

    network_name = re.split('\.|/', str(reader.name))

with open('dot_blueprints/random_3.txt', 'w') as writer:
    # Alternatively you could use
    # writer.writelines(reversed(dog_breeds))
    
    writer.write("template <typename Ntk>\n")
    writer.write("mockturtle::names_view<Ntk> {}()\n".format(network_name[1]))
    writer.write("{\n")
    writer.write("    mockturtle::names_view<Ntk> ntk{};\n")

    # Write the dog breeds to the file in reversed order
    OR_storage = []
    AND_storage = []
    MAJ_storage = []
    PO_storage = []
    for new_line in full_text:
        res = re.split('\[| |,', new_line)
        if("box" in new_line):
            pass
        elif("invtriangle" in new_line):
            PO_storage.append(res[0])
        elif("triangle" in new_line):
            writer.write("    const auto n_{} = ntk.create_pi(\"n_{}\");\n".format(res[0], res[0]))
        elif("AND" in new_line):
             AND_storage.append(res[0])
        elif("OR" in new_line):
             OR_storage.append(res[0])
        elif("MAJ" in new_line):
             MAJ_storage.append(res[0])
    
    already_inverted = []
    process_node = ""
    childs = []
    for new_line in full_text:
        res = re.split('\[| |,', new_line)
        if('->' in new_line and not 'shape' in new_line):
            if(res[2] in PO_storage):
                writer.write("    ntk.create_po(n_{}, \"{}\");\n".format(res[0], res[2]))
            elif(process_node == ""):
                # print(res[2])
                if("solid" in new_line):
                    childs.append(res[0])
                else:
                    childs.append(res[0] + "i")
                process_node = res[2]
            elif(process_node in res[2]):
                # print(res[2])
                if("solid" in new_line):
                    childs.append(res[0])
                else:
                    childs.append(res[0] + "i")
                if(res[2] in MAJ_storage):
                    if(len(childs))==3:
                        process_node = res[2]
                        if("i" in childs[0] and not childs[0] in already_inverted):
                            already_inverted.append(childs[0])
                            helping_node = childs[0][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[0],helping_node))
                        elif("i" in childs[1] and not childs[1] in already_inverted):
                            already_inverted.append(childs[1])
                            helping_node = childs[1][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[1],helping_node))
                        elif("i" in childs[2] and not childs[2] in already_inverted):
                            already_inverted.append(childs[2])
                            helping_node = childs[2][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[2],helping_node))
                        writer.write("    const auto n_{} = ntk.create_maj(n_{}, n_{}, n_{});\n".format(res[2], childs[0], childs[1], childs[2]))
                        childs.clear()
                    
                else:
                    process_node = res[2]
                    if(res[2] in AND_storage):
                        if("i" in childs[0] and not childs[0] in already_inverted):
                            already_inverted.append(childs[0])
                            helping_node = childs[0][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[0],helping_node))
                        elif("i" in childs[1] and not childs[1] in already_inverted):
                            already_inverted.append(childs[1])
                            helping_node = childs[1][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[1],helping_node))                       
                        writer.write("    const auto n_{} = ntk.create_and(n_{}, n_{});\n".format(res[2], childs[0], childs[1]))
                    if(res[2] in OR_storage):
                        if("i" in childs[0] and not childs[0] in already_inverted):
                            already_inverted.append(childs[0])
                            helping_node = childs[0][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[0],helping_node))
                        elif("i" in childs[1] and not childs[1] in already_inverted):
                            already_inverted.append(childs[1])
                            helping_node = childs[1][:-1]
                            writer.write("    const auto n_{} = ntk.create_not(n_{});\n".format(childs[1],helping_node))
                       
                        writer.write("    const auto n_{} = ntk.create_or(n_{}, n_{});\n".format(res[2], childs[0], childs[1]))
                    childs.clear()
                
            else:
                # print(res[2])
                childs.append(res[0])
                process_node = res[2]


    writer.write("\n")
    writer.write("    return ntk;\n")

    writer.write("}")