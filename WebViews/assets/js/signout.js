$(document).ready(function(){


    $('#signout-btn').on('click',function(){


        var con = confirm('Are you sure you want to sign out??');

        if(con){
            $.ajax({
                url:'./signout',
                type:'post',
                data:{
                },
                success:function(msg){
                   if(msg=='ok'){
                      location.replace('./');
                   }else{
                      alert('Fail to sign out'); 
                   }
                },
                error:function(err){
      
                }
            });
        }

      
    })
 })