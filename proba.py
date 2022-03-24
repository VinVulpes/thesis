from pyparsing import Word, Literal, alphas

salutation = Word(alphas + "'")
comma = Literal(",")
greetee = Word(alphas)
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation

tests = ("Hello, World!",
         "Hey, Jude!",
         "Hi, Mom!",
         "G'day, Mate!",
         "Yo, Adrian!",
         "Howdy, Pardner!",
         "Whattup, Dude!")

for t in tests:
    print(t, "->", greeting.parseString(t))
