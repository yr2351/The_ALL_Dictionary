$(document).ready(function(){


   $('#signup-btn').on('click',function(){
       var email = $('#email').val();
       var pw = $('#password').val();
       var name = $('#name').val();


      $.ajax({
          url:'./addUser',
          type:'post',
          data:{
              email:email,
              pw:pw,
              name:name
          },
          success:function(msg){
             alert(msg);
             if(msg=='Successfully registered'){
                 //가입 성공.
                 location.replace('./');
             }else if(msg=='already'){
                //이미 가입됨.
                alert(msg);
             }
          },
          error:function(err){

          }
      })

   })
})