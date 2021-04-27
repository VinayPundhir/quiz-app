

  // function to match the answers in a quiz and
  //disable submit button after clicking once

  var gb , total = 0 ;

  async function freez( ){

      let id = this;
      gb=id;

      if ( id == "" ){
         return
      }

      score = document.getElementById('score');
      solution = document.getElementById('solution'+this.id);
      button =   document.getElementById('button'+this.id);
      button.type="hidden";

      data = await axios({
         method : 'post',
         url : '/validate_question',
         data : JSON.stringify({
                 question_id : this.id,
                 option_a :  gb[1].checked,
                 option_b :  gb[2].checked ,
                 option_c :  gb[3].checked ,
                 option_d :  gb[4].checked
         }) ,
         headers: {
            "X-CSRFToken": this['csrfmiddlewaretoken'].value
         },
      }).
      then( res => res.data )
      .catch( e => {
         alert(e);
      });

      let result = this.querySelectorAll(
          ".result" + this.id
      )[0]


      if ( data.option_valid ) {
         result.innerHTML = "right answer";
         result.style = 'color:green';
         total  = total + 1;
         score.innerHTML =  " "+total;
      }

      else  {
         result.innerHTML = "wrong answer";
         result.style = 'color:red';
      }

      solution.innerHTML = "solution" + " : " + data.solution

   }




  // timer function

  var hour = 0,mn = 0 ,sec = 1 , counter;

  function inc(){

     if ( sec % 60 == 0 ){
          mn = mn + 1;
          sec = 0;
      }

      counter =document.getElementById('counter');
      counter.innerHTML = mn+" min : "+sec+" sec";
      //hour = hour + 1;
      sec = sec + 1

  }
  setInterval( inc ,1000)




  //finish  button script

  var res ,q

  async function finish(){

      let token = this['csrfmiddlewaretoken'].value ;

      let quiz_name = document.getElementById('quiz-name').innerHTML.trim();

      res = await axios({
         method : 'post',
         url : '/save_score',
         data : JSON.stringify({

                 score : total ,
                 quiz  : quiz_name
         }) ,
         headers: {
            "X-CSRFToken": token
         },
      }).
      then( res => res.data )
      .catch( e => {
         alert(e);
      });

     let msg ;

     if( res.user_has_played ){
         msg = 'Quiz already taken '

     }else{
         msg = 'Response has been saved . '+ 'Time taken ' + mn + ":" + sec + " "+ "Score " + total;
     }

     q = document.getElementById('msgbox');

     q.style = "display:visible;height:30%;width:100%;background:white;";

     document.getElementById('message').innerHTML = msg;

     
  }



  //function to end a running quiz and show results

  function show_msg(){

   document.getElementById('msgbox').style = 'display:none';
   document.getElementById('counter').style = "display:none"; 
  }





