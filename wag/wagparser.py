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

class WagParser(argparse.ArgumentParser):
    def __init__(self, default=None, *args, **kwargs):
        super(WagParser, self).__init__(*args, **kwargs)
        self.order = []
        self.command_list = {}
        self.default = default

    def arg_function(self, *args, **kwargs):
        """
        
        Allows the decorated function to be called when its flag is passed.
        All functions with this decorator lose the ability to specify an
        action.  It is always changed to 'store_true'.  

        Note: If you care about priority the functions at the top of the 
        source file will have higher priority than the functions at the bottom of the
        source file.
        
        """
        kwargs['action']='store_true'
        the_arg = self.add_argument(*args, **kwargs)
        self.order.append(the_arg.dest)
        def wrapped(func):
            self.command_list[the_arg.dest] = func
            return func
        return wrapped

    def run_parser(self, funcs):
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
        args = self.parse_args()
        if type(funcs) != list():
            funcs = list(funcs)

        for func in funcs:
            args = func(args) 
        
        results = {}
        for dest in self.order:
            if getattr(args,dest):
                results[dest] = self.command_list[dest](args)
            
        if results == {} and self.default:
            results['default'] = self.default(args)
        return results
