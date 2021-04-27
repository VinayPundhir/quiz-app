from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here

class Quiz( models.Model ):
    """
    stores quizes 
    """
    name = models.TextField()
    
    def __str__( self ):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'get_quiz', 
            kwargs = {
                'pk': self.pk
            }
        )




class Question( models.Model ):
    """
    stores questions
    """
    quiz  = models.ForeignKey( 
        Quiz,
        on_delete = models.CASCADE 
    )
    question = models.TextField()
    
    multiple_right_answers = models.BooleanField( default = False )
   

    def __str__( self ):
        return self.question

    def get_absolute_url(self):
        return reverse(
            'create_question', 
            kwargs = {
                'pk': self.pk
            }
        )


class Option ( models.Model ):
    """
    stores all option whether wrong or right
    """
    question = models.ForeignKey(
        Question,
        on_delete = models.CASCADE
    )
    option = models.TextField()
    valid = models.BooleanField()

    def __str__( self ):
        return self.option

    def get_absolute_url(self):
        return reverse(
            'create_option', 
            kwargs = {
                'pk': self.pk
            }
        )
        



class Score ( models.Model ):
    """
    store score of quiz
    """
    user = models.ForeignKey( 
        User , on_delete = models.CASCADE
    ) 
    quiz = models.ForeignKey ( 
        Quiz , 
        on_delete = models.CASCADE 
    )
    score = models.IntegerField()

    def __str__( self ):
        return self.user.username

    def get_absolute_url(self):
        return reverse(
            'get_score', 
            kwargs = {
                'pk': self.pk
            }
        )



class Test ( models.Model ):
    """
    table to store answer given to a question
    """
    user = models.ForeignKey( 
        User , on_delete = models.CASCADE
    ) 
    question = models.ForeignKey ( 
        Question , 
        on_delete = models.CASCADE 
    )
    answer = models.TextField()

    def __str__( self ):
        return self.user.username

    def get_absolute_url(self):
        return reverse(
            'get_test', 
            kwargs = {
                'pk': self.pk
            }
        )




          

    

    
           


   









 

