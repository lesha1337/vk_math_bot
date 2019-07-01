import bot_commands
import vkapi
import config
from distance import damerau_levenshtein_distance

cmd_list = ['график', 'калькулятор', 'решить', 'интеграл', 'производная', 'упростить', 'построить', 'помощь', 'привет']
cmd_img_location = config.cmd_img_location

def getAnswer(text):
    
    try:
        ans = eval(text)
        return ans, ''
    except Exception as e:
        print('>>>', e)

    if len(text.split()[0]) > 2 and len(text.split()) > 0:
        input_command = text.split()[0]
        rest = text.replace(input_command, '')
        current_range = len(input_command)

        for c in cmd_list:
            current_range = damerau_levenshtein_distance(c, input_command)

            if current_range < 0.4 * len(input_command):
                fixed_cmd = text.replace(input_command, c)
                return function_branching(fixed_cmd)

        else: 
            return function_branching(text)

def function_branching(text):
    num_set = set()
    var_set = set(['x','y','z','t'])

    for n in range(10):
        num_set.add(str(n))

    for i in range(len(text)-1):
        if text[i] in num_set and text[i+1] in var_set:
            text = text.replace(text[i+1], '*' + text[i+1])

    if text.find('график') == 0 or text.find('построить') == 0:
        inp = text.replace('график', '')
        inp = inp.replace('построить', '')

        img = bot_commands.plot_exp(inp)
        msg = 'график функции f(x) = ' + inp + ':'
        return msg, vkapi.pic_upload(img)

    elif text.find('калькулятор') == 0:
        ans = eval(text.replace('калькулятор', ''))
        return ans, ''

    elif text.find('решить') == 0:
        inp = text.replace('решить', '')
        solution = bot_commands.solve_eq(inp)
        return solution

    elif text.find('производная') == 0:
        inp = text.replace('производная', '')

        msg, img = bot_commands.diff_eq(inp)
        msg = 'производная от ' + str(inp) +':'
        return msg, vkapi.pic_upload(img)

    elif text.find('интеграл') == 0:
        inp = text.replace('интеграл', '')

        msg, img = bot_commands.int_eq(inp)
        msg = 'интеграл от ' + str(inp) +':'
        return msg, vkapi.pic_upload(img)

    elif text.find('упростить') == 0:
        inp = text.replace('упростить', '')
        solution = bot_commands.simpl_eq(inp)
        return solution
    elif text.find('помощь') == 0 or text.find('привет'):
        return help_answer()  

    else:
        try:
            ans = eval(text.replace('калькулятор', ''))
            return ans, ''
        except Exception as e:
            return help_answer()

def help_answer():
    img = cmd_img_location
    return 'Доступен следующий список команд:', vkapi.help_pic()#vkapi.pic_upload(img) #attachment