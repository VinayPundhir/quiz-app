# helper functions for views


#imports
from .models import (
    Quiz,
    Question,
    Option ,
    Score ,
    Test
)


# functions start from here

def attach_options_to_question( request , options_list , question ):
    """
    join options with related question name
    """
    count_right_options = 0

    for option_name in options_list:

        valid = False

        if option_name + "_valid"  in request.POST:
            valid  = True
            count_right_options += 1

        option_name = request.POST[option_name]
        option = Option (
            option = option_name ,
            valid = valid
        )
        option.question = question
        option.save()

    if count_right_options > 1:
        question.multiple_right_answers = True
        question.save()



def attach_question_to_quiz ( request ):
    """
    join questions to related quiz name
    """
    quiz_name = request.POST['quiz_name']

    try:
        quiz = Quiz.objects.get (
            name = quiz_name
        )

    except:
        quiz = Quiz (
            name = quiz_name
        )
        quiz.save()

    question_name = request.POST['question']

    question = Question(
        question = question_name
    )

    question.quiz = quiz
    question.save()
    return question



def get_quiz_by_name(
        request ,
        quiz 
):
    """    
    helper function for get_quiz view
    return a perticular quiz details in json format
    """
    res = {}
    res['quiz_name']=quiz.name
    res['questions'] = []
    question_number = 1

    for q in quiz.question_set.all():

        que = {}

        que['question'] = q.question
        que['question_id'] = q.id
        que['multiple_right_answers'] = q.multiple_right_answers
        que['question_number'] = question_number

        que['options'] = [
            {
                'option':q.option,
                'id':q.id,
                'tag':tag
            }

            for q , tag in zip(
                q.option_set.all(),
                tags
            )
        ]
        question_number +=1
        res['questions'].append(que)

    has_played = user_played_quiz(
        request ,
        quiz.name
    )
    return res  , has_played




def right_answer( question_id ):
    """
    return right answers of  question
    """
    question = Question.objects.get(
        id = question_id
    )

    options =question.option_set.all()

    right_answers = [
        option.valid
        for option in options
    ]

    return (
        right_answers ,
        options ,
        question
    )




def question_validate( request ):
    """
    function to validate options selected by user
    and resturn json response
    """
    true = True
    false = False
    data = eval(
        list(
            request.POST.keys()
        )[0]
    )

    question_id = data['question_id']

    right_answers , options , question = right_answer( question_id )

    user_answers = [
        data[option]
        for option in options_list
    ]

    #start saving test objects

    option_to_save = ""
    for s , t in zip( user_answers , tags ):
        if s:
            option_to_save += t + ","

    try:
        test = question.test_set.all().get(
            user = request.user
        )


    except:
        print('new test user')
        test = Test()
        test.user = request.user

        test.question = question
        test.answer = option_to_save
        test.save();

    #end


    option_valid_list = [
        option.valid
        for option in options

    ]

    solution = []

    for s ,t in zip( option_valid_list , tags ) :
        if s :
            solution.append(t)

    try:

        print(solution)
        assert right_answers == user_answers
        return ( True , solution )

    except:
        return ( False , solution )


def user_played_quiz( request , quiz_name ):
    """
    check if user has played the quiz
    """
    try:
        quiz = Quiz.objects.get(
            name = quiz_name
        )

        user = quiz.score_set.all().get(
            user = request.user
        )

        return user

    except:
        return False



def save_score_of_quiz( request ) :
    """
    saves user score for a quiz in score model
    """
    data = eval(
        list(
            request.POST.keys()
        )[0]
    )

    score_number = data['score']
    quiz_name = data['quiz']

    try:
        user = user_played_quiz( request , quiz_name )

        print(user,'has played ',quiz_name)

        if user :
            user_has_played = True
            return  user_has_played
        else:
            raise ValueError('user played the quiz')

    except :
        score = Score()

        print('score empty object fetched')
        score.user = request.user
        score.score = score_number

        score.quiz = Quiz.objects.get(
            name = quiz_name
        )

        print('quiz_name set for score ')
        score.save()
        print('score saved')

        user_has_played = False
        return user_has_played


def history_response( request , quiz_name):
    """
    return quiz history dictionary response
    """

    try:
        quiz = Quiz.objects.get(
            name = quiz_name
        )

        score = quiz.score_set.all().get(
            user = request.user
        )
    except:

        print('quiz or score not found for' , request.user)

        return False

    questions = quiz.question_set.all()


    questions_obj_list =[]

    for question in questions:

        right_tags = ""
        question_obj = {}
        question_obj['question'] = question.question

        try:
            test = question.test_set.all().get(
                user = request.user
            )

            answer_from_test = test.answer

        except:
            print('test not found for' , request.user)
            answer_from_test = "Empty"

        right_options,question,options = right_answer(
             question.id
        )

        for option_valid ,tag in zip(right_options,tags):
            if option_valid:
                right_tags += "," + tag

        question_obj['user_selected_options'] = answer_from_test
        question_obj['right_options'] = right_tags

        questions_obj_list.append(
            question_obj
        )

    res ={}

    res['quiz_name'] = quiz.name
    res['score'] = score.score
    res['questions'] = questions_obj_list

    return res



"""
option tags used in question
"""
tags = ['a','b','c','d']



"""
option names used to retreive options value
from request.POST
"""
options_list = [
    'option_a',
    'option_b',
    'option_c',
    'option_d'
]



"""
question object should have these values non empty
"""
required_fields = [
    'quiz_name',
    'question'

]
required_fields.extend(options_list)


