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

    def operation_hours(self, hours):
        hours = hours['open']
        print(hours)
        listofhours = []
        dayofweek = {
            0:"Mon",
            1:"Tue",
            2:"Wed",
            3:"Thu",
            4:"Fri",
            5:"Sat",
            6:"Sun"
        }
            
        for i in hours:
            start_time = 'None'
            end_time = 'None'
            day_convert = 'None'
            if 'start' in i:
                if int(i['start']) >= 1300:
                    start_time = str(int(i['start']) - 1200) + " " + "PM"
                    if start_time[0] == '0':
                        start_time = start_time[1:]
                else:
                    start_time = i['start'] + " " + "AM"
                    if start_time[0] == '0':
                        start_time = start_time[1:]
            if 'end' in i:
                if int(i['end']) >= 1300:
                    end_time = str(int(i['end']) - 1200) + " " + "PM"
                    if end_time[0] == '0':
                        end_time = end_time[1:]
                else:
                    end_time = i['end'] + " " + "AM"
                    if end_time[0] == '0':
                        end_time = end_time[1:]
            if 'day' in i:
                day_convert = dayofweek.get(i['day'])

            time = {
               'start' : start_time,
               "end" : end_time,
               "day" : day_convert
            }
            listofhours.append(time)
        return listofhours
