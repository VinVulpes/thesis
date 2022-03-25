from pyparsing import Word, Literal, alphas,ZeroOrMore,Suppress

source = "a, b, c,d"
wd = Word(alphas)
wd_list1 = wd + Word(',' + wd)
print(wd_list1.parseString(source))

 # often, delimiters that are useful during parsing are just in the
 # way afterward - use Suppress to keep them out of the parsed output
wd_list2 = wd + ZeroOrMore(Suppress(',') + wd)
print(wd_list2.parseString(source))