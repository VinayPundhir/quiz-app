# view are imports

from django.shortcuts import render
from django.http import (
    JsonResponse ,
    HttpResponse ,
    HttpResponseRedirect
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import (
    login ,
    logout ,
    authenticate
)

from django.views.generic import (
    ListView ,
    DetailView
)

from .models import (
    Quiz,
    Question,
    Option ,
    Score ,
    Test
)

from django.views.generic import ListView
from .decorators import (
    question_isvalid ,
    select_one_option_atleast ,
    context_present ,
    no_get_request
)

from .helpers import  (
    attach_question_to_quiz ,
    attach_options_to_question ,
    get_quiz_by_name ,
    options_list ,
    required_fields ,
    question_validate ,
    save_score_of_quiz ,
    history_response ,
    user_played_quiz
)






# views are here.

class ListQuiz( ListView ):
   """
   return all available quizes names
   """
   model = Quiz
   template_name = 'list.html'
   queryset = Quiz.objects.all()
   context_object_name = 'quiz_list'



def create_quiz(request):
    """
    return home page
    """
    if request.method=='POST':

        return HttpResponseRedirect(
            '/get_quiz/' +
            str( request.POST['quiz_name'] )
        )

    else:
        return render(
            request,
            'create_quiz.html'
        )




@login_required
def get_quiz(request , pk ):
    """
    start a quiz from quiz list
    """
    if request.method=='GET':
        try:
            quiz = Quiz.objects.get(
                id =  pk
            )

            
        except:
            return HttpResponseRedirect(
                '/'    
            )

        
        user = user_played_quiz(
            request ,
            quiz.name
        )

        if user :
            return render(
                request ,
                'msg.html' ,
                {
                    'msg' : 'You have played this quiz'
                }
            ) 
          
        res , has_played = get_quiz_by_name(
            request ,
            quiz
        )

        return render(
            request ,
            'detail_quiz.html' ,
            {
                'quiz': res ,
                'has_played' : has_played
            }
         )




@no_get_request(
    return_to = '/'
)

def validate_question( request ):
    """
    check whether user selects right option
    """

    if request.method == 'POST':

        response , solution = question_validate( request )

        if response:
           return JsonResponse({
                'option_valid' : True ,
                'solution' : solution
            } , safe = False )

        else:
           return JsonResponse({
            'option_valid' : False ,
            'solution' : solution
           },safe=False)



@login_required
@no_get_request(
    return_to = '/'
)
@context_present(
    context_list = ['quiz_name'],
    return_url = '/'
)
def create_question( request ):
    """
    return empty question and options form
    """

    if request.method == 'POST':
        quiz_name = request.POST['quiz_name']
        try:
            q = Quiz.objects.get(
                name = str(quiz_name)
                )
           
            return render (
                request,
                'create_quiz.html',
                {
                    'error' : 'Quiz already exists'
                }
            )
        except:
            return render(request ,
                'create_question.html', {
                "quiz_name" : quiz_name
                }
            )



@no_get_request(
    return_to = '/'
)
@select_one_option_atleast(
    options_list,
    template = 'create_question.html'
)
@question_isvalid (
    required_fields,
    template ='create_question.html'
)

def save_question( request ):
    """
    saves question deatils from question form
    """

    if request.method == 'POST':

        question = attach_question_to_quiz(request)

        attach_options_to_question(
            request ,
            options_list ,
            question
        )

        return render(
            request ,
            'create_question.html' , {
            "quiz_name" : request.POST['quiz_name'],
            "errors" : "create new question ",
            "color" : "info"
            }
        )




@no_get_request(
    return_to = '/'
)
def save_score( request ):
     """
     save score for every user
     """
     if request.method == 'POST':

         user_has_played = save_score_of_quiz(
             request
         )

         if user_has_played :
             return JsonResponse({
                 'user_has_played' : True ,
             },safe=False)

         else:
             return JsonResponse({
                 'user_has_played' : False ,
             },safe=False)






def register( request ):
    """
    register user
    """
    
    error = ""

    if request.method == "POST":

        user = str( request.POST['username'] )
        passw = str( request.POST['password'] )
        passw_retyped = str(request.POST['retyped_password'])
 

        print(passw ,passw_retyped)
        
        if passw != passw_retyped :
            error = "passwords don't match"
  
            return render(
                request ,
                'authenticate.html' ,
                {
                    'action' : 'register' ,
                    'login_or_register' : 'register' ,
                    'error' : error
                }
             )

        try:
            user = User(
                username = user ,
                password = passw
            )
            user.set_password(passw)
            user.save()


        except:
            error = 'user already exists '

            return render(
                request ,
                'authenticate.html' ,
                {
                    'action' : 'register' ,
                    'login_or_register' : 'register' ,
                    'error' : error
                }
            )

        return HttpResponseRedirect(
            '/login'
        )

    if request.method == "GET":

        return render(
            request ,
                'authenticate.html' ,
                {
                    'action' : 'register' ,
                    'login_or_register' : 'register'
                }
            )




def user_login( request ):
    """
    user login view
    """
    signup_link = True

    if request.method == "POST":
       
        user = request.POST['username']
        passw = request.POST['password']

        user = authenticate(
            request ,
            username = user ,
            password = passw
        )

        if user :
            login(request,user)
        else:
            return render(
                request ,
                'authenticate.html' ,
                {
                    'action' : 'login' ,
                    'login_or_register' : 'login' ,
                    'error' : 'wrong credentials' ,
                    'link_to_signup' : signup_link
                }
            )


        return HttpResponseRedirect(
            '/' ,
            {
                'user':user
            }
        )

    if request.method == "GET":

        return render(
            request ,
                    'authenticate.html' ,
                    {
                        'action' : 'login' ,
                        'login_or_register' : 'login' ,
                        'link_to_signup' : signup_link
                    }
                )



@login_required
def user_logout( request ):
    """
    user logout view
    """
    if request.user.is_authenticated:

        logout(request)

    return HttpResponseRedirect(
            '/'
        )


@login_required
def history( request , quiz_name ):
    """
    returns quiz history
    """
    if request.method == "GET":

       response = history_response(
           request ,
           quiz_name
       )

       print(response)

       return render (
            request ,
            'history.html',
            {
                'quiz_data' : response
            }
       )
