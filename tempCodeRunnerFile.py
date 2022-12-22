f(res[4] == "&"):
                        writer.write("    const auto {} = ntk.create_and({}, {});\n".format(res[1], res[3], res[5]))

                elif(res[4] == "|"):
                        wr