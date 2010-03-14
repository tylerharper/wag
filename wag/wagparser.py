"""

This module allows us to call functions when a its flag is detected.
For example:

    @arg_function('-f', '--feed')
    def feed(args):
        #do something.

if we pass -f or --feed on the command line the feed function should be run
and all of the other arguments will be passed into it.

"""
import argparse

parser = argparse.ArgumentParser(prog='wag', description='tail you rss feeds')
order = []
command_list = {}

def arg_function(*args, **kwargs):
    """
    
    Allows the decorated function to be called when its flag is passed.
    All functions with this decorator lose the ability to specify an
    action.  It is always changed to 'store_true'.  

    Note: If you care about priority the functions at the top of the 
    source file will have higher priority than the functions at the bottom of the
    source file.
    
    """
    kwargs['action']='store_true'
    the_arg = parser.add_argument(*args, **kwargs)
    order.append(the_arg.dest)
    def wrapped(func):
        command_list[the_arg.dest] = func
        return func
    return wrapped

def run_parser(default, funcs):
    """
    This does all the heavy lifting and will actually run your program
    It finds which functions to call and when.
    
    Once your functions have ran it will return your functions return values
    in a dictionary with the following format {argparse_dest: return_value}
    
    funcs is a list of callable objects that get called right after the args 
    are parsed. It takes the list of arguments and modifies them. Each function 
    in the list must have the following siginature:
        func(args):
            return newargs
    
    """
    args = parser.parse_args()
    if type(funcs) != list():
        funcs = list(funcs)

    for func in funcs:
        args = func(args) 
    
    results = {}
    for dest in order:
        if getattr(args,dest):
            results[dest] = command_list[dest](args)
        
    if results == {}:
        results['default'] = default(args)
    return results
    
def add_argument(*args, **kwargs):
    """This function just makes your code look pretty"""
    return parser.add_argument(*args, **kwargs)
