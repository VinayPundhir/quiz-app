# decorators for forms validation

# imports are here

from .models import (
    Quiz,
    Question,
    Option
)

from django.shortcuts import render
from django.http import HttpResponseRedirect



# decorators start from here

def question_isvalid ( required_fields = [] , template = None ):
    """
    check form fields empty or not 
    """
    def decorator( func ):

        def wrapper_func( request ) :

            for arg in required_fields:
                print(arg in request.POST)

                if len(request.POST[arg]) == 0:
                  
                  if arg == "quiz_name":
                    
                    print(arg,request.POST[arg],'has 0 length')
                    return render( request , template , {
                        'errors' : 'empty fields not allowed',
                        'color' : 'danger',
                        'quiz_name' : request.POST['quiz_name']
                    })
                
            return func(request) 

        return wrapper_func

    return decorator



def context_present( context_list = [] , return_url =None ) :
    """
    check whether a context_name avaliable to a page before rendering
    """
    def decorator( func ):
    
        def wrapper_func( request ) :

            for context_name in context_list: 

                if ( context_name in request.POST ) :
                    if ( len(request.POST[context_name]) > 0 ):
                        print('context exist')
                    else:
                        return HttpResponseRedirect( return_url )
                else: 
                    print('context not given')
                    return HttpResponseRedirect( return_url )

            return func( request ) 

        return wrapper_func

    return decorator




def select_one_option_atleast( options_list = [] ,template = None):
    """
    check form must have one valid option
    """
    def decorator ( func ):

        def wrapper_func( request ):

            valid_option_count = 0

            for option in options_list:
                if option+'_valid' in request.POST :
                    valid_option_count += 1

            if valid_option_count < 1 :
                return render( request , template , {
                        'errors' : 'select atleast one check box',
                        'color' : 'danger',
                        'quiz_name' : request.POST['quiz_name']
                    })

            return func(request)

        return wrapper_func

    return decorator




def no_get_request( return_to ):
    """
    reject any GET request
    """
    def decorator ( func ):

        def wrapper_func( request ):
            print('found get reuqest', request.method)
            if request.method == "GET" :
                
                return HttpResponseRedirect(
                    return_to 
                )
 
            else :
 
                return func(request)

        return wrapper_func

    return decorator
     
    


            
