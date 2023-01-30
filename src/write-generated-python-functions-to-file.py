at about line 1168:

        if self._formula_status > 0: #!!!!!!!!!!!!!! right after this !!!
            # set _julia_func_basename
            self._julia_exact_func_expr = \
                self._julia_func_expr(self._data, False, True)
            ffilename = "%s.py" % self._julia_func_basename
            try:
                f = open(ffilename, 'w')
                f.write("def %se%s" % (self._julia_func_basename,
                    self._julia_exact_func_expr))

                if self._data.m != 1:  # functions in other formats
                    data1 = _FDData(self._data.n, self._data.points,
                                    list(map(lambda x: Fraction(x, self._data.m),
                                            self._data.k)),
                                    1, self._data.coefs)
                    self._julia_exact_func_expr1  = \
                        self._julia_func_expr(data1, False, True)
                    #lambda_fde1 = self._lambda_expr(data1, False)
                    f.write("\n\ndef %se1%s" % (self._julia_func_basename,
                        self._julia_exact_func_expr1))

                    self._julia_decimal_func_expr = \
                        self._julia_func_expr(data1, True, True)
                    #lambda_fdd = self._lambda_expr(data1, False)
                    f.write("\n\ndef %sd%s" % (self._julia_func_basename,
                        self._julia_exact_func_expr1))

                    count = 3

                # furtehrmore, prepare some data for experiments with the
                # generated Python functions in the Python script file.
                print("\n\nfrom math import sin, cos, tan, pi, exp, log", \
                        file = f)
                print("f, i, h = sin, 501, 0.01", file = f)  # x[i] = 5
                print("x = [ 0.01 * i for i in range(0, 1001) ]", file = f)

                f.write("\ndef printexampleresult(suffix, exact):\n")
                print("    apprx = ", self._julia_func_basename, suffix,
                      "(sin, x, 501, 0.01)", file = f, sep = '')
                print("    relerr = abs((apprx - exact) / exact) * 100", file = f)
                print("    spaces = \"\"", file = f)
                print("    if suffix != \"e1\":", file = f)
                print("        spaces  = \" \"", file = f)
                print("    print(\"   ", self._julia_func_basename,
                      "\%s(f, x, i, h)  \"\% suffix)", file = f, sep = '', end = '')
                print("    print(spaces, \"# result: ", "\"%.16f\" \% apprx sep='' end = ''",
                      sep = '', file = f)
                print("    print(\"relative error = \", \"\%.8f\%\%\" \% relerr, sep = '')",
                      file = f)
                # end of printexampleresult

                print("Usage: %de(sin, x, i, h)" % (self._julia_func_basename), \
                        file = f)

                # sine is taken as the example b/c
                # sin^(n)(x) = sin(n π/2 + x), simply
                print("\nexact = sin(self._data.n * pi /2 + 5) # x[501] = 5", file = f)
                print("printexampleresult(\"e\", exact)", file = f)
                if count == 3:
                    print("printexampleresult(\"e1\", exact)", file = f)
                    print("printexampleresult(\"d\", exact)", file = f)
                length = len(self._julia_func_basename)
                if count == 3:
                    length += 1
                print("print(\" \" * ", length + 17, "\"# cp:     \", \"%.16f\\n\" % exact, sep = '', end = '')",
                      sep = '', file = f)
                # m = 1? no decimal formula
            except:
                import sys
                print("Error:", sys.exc_info()[0])
            finally:
                f.close()