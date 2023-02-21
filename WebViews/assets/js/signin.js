$(document).ready(function(){


   $('#signin-btn').on('click',function(){
       var email = $('#email').val();
       var pw = $('#password').val();
      
      

      $.ajax({
          url:'./getUserByEmailAndPW',
          type:'post',
          data:{
              email:email,
              pw:pw
          },
          success:function(msg){
             if(msg=='ok'){
                location.replace('./');
             }else{
                alert('Please enter the information'); 
             }
          },
          error:function(err){

          }
      })

   })
})