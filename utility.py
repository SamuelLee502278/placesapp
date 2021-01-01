class UtilityClass:

    def capitalizeinput(self, input):
        input = input.split()
        input = [x.capitalize() for x in input]
        input = " ".join(input)  
        return input

    def addelementstring(self, original, elementtoadd):
        original = original.split()
        original.append(elementtoadd)
        newstring = ''.join(original)
        return newstring
    
