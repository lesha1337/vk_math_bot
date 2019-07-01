import requests
import datetime
import matplotlib as mpl
import config

from sympy import *
from sympy.plotting import plot

directory = config.dir
url = config.def_url

x, y, z, t = symbols('x y z t')

def solve_eq(eq):
    # x, y, z, t = symbols('x y z t')
    eq = eq.split('=')
    solution = solve(eq[0] + '-(' + eq[1]+ ')')

    return  solution, ''

def plot_exp(expression):
    mpl.use('agg')
    # x, y, z, t = symbols('x y z t')
    graph = plot(expression, show=False)
    backend = graph.backend(graph)
    backend.process_series()

    name = str(datetime.datetime.now()) + '.png'
    backend.fig.savefig(directory+name, dpi=200)

    return url+name

def int_eq(eq):
    eq = '(' + eq + ')'
    eq = eq.replace('^', '**')

    lat_str = latex(integrate(eq, x)) + ' + C'
    ans = str(integrate(eq, x)).replace('**', '^') + ' + C' 
    
    img_name = str(datetime.datetime.now()) + '.png'
    # lat_str = eq_str + lat_str
    formula_as_file(lat_str, directory+img_name)

    return ans, url+img_name

def diff_eq(eq):
    eq = '(' + eq + ')'
    eq = eq.replace('^', '**')

    lat_str = latex(diff(eq, x))
    ans = str(diff(eq, x)).replace('**', '^')

    img_name = str(datetime.datetime.now()) + '.png'
    formula_as_file(lat_str, directory+img_name)

    return ans, url+img_name

def simpl_eq(eq):
    eq = '(' + eq + ')'
    eq = eq.replace('^', '**')
    ans = str(simplify(eq)).replace('**', '^')
    return ans, ''


def formula_as_file( formula, tfile):
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{300} \huge %s' % formula )
    f = open(tfile, 'wb' )
    f.write( r.content )
    f.close()