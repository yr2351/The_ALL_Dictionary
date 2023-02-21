var firebaseConfig = {
    apiKey: "AIzaSyD9kEvCKokZO5uEqNkwSn29Fj5J-_pWuvs",
    authDomain: "thealldictionary-b4454.firebaseapp.com",
    projectId: "thealldictionary-b4454",
    storageBucket: "thealldictionary-b4454.appspot.com",
    messagingSenderId: "775694189580",
    appId: "1:775694189580:web:194bbb6ec8900e6b759a29",
    measurementId: "G-CEJH250MDB"
  };

$(document).ready(function(){
    firebase.initializeApp(firebaseConfig);
    var storage = firebase.storage();
    var file;
    var isChangePW=false;
    var isDel=false;

    $('input#newProfile').on('change',function(){
        file = $(this)[0].files[0];
    });


    $('#upload-file').on('click',function(){
        var storageRef = storage.ref().child(file.name);

        storageRef.put(file).then(function(snapshot) {
            console.log('upload!');
            storageRef.getDownloadURL().then(function(url){
               
                $.ajax({
                    url:'./addImgUrlToUser',
                    type:'post',
                    data:{
                        img_url:url
                    },
                    success:function(res){
                        if(res=='ok'){
                            alert('Image upload completed!');
                            $('#my-img').attr('src',url);
                            $('.btn-close').trigger('click');
                        }
                    },
                    error:function(err){

                    }
                })
            });
        });
    });



    $('#originPassword').on('keyup',function(){
        var typedPassword = $(this).val();
        var md5Password = $.md5(typedPassword)
        if(md5Password==originalPassword){
           $('#pw-msg').html('');
           isChangePW=true;
        }else{
            $('#pw-msg').html('password is different!');
            isChangePW=false;
        }
    });


    $('#change-pw-btn').on('click',function(){
        var newPassword = $('#newPassword').val()
        var md5NewPassword = $.md5(newPassword)
        if(isChangePW){
            $.ajax({
                url:'./changePw',
                type:'post',
                data:{
                    pw: md5NewPassword
                },
                success:function(res){
                   
                    if(res=='ok'){
                        $('.btn-close').trigger('click');
                    }
                },
                error:function(err){
                    console.log(err);
                }
            })
        }else{
            alert('Try again!');
        }
    });


    $('#change-name-btn').on('click',function(){
        if($('#editName').val().length>0){
            $.ajax({
                url:'./changeName',
                type:'post',
                data:{
                    name:$('#editName').val()
                },
                success:function(res){
                   
                    if(res=='ok'){
                        $('#name').html($('#editName').val());
                        $('.btn-close').trigger('click');
                    }
                },
                error:function(err){
                    console.log(err);
                }
            })
        }else{
            alert('Name is empty!');
        }
    });



    $('#pw-for-del').on('keyup',function(){
        var typedPassword = $(this).val();
        var md5Password = $.md5(typedPassword)

        if(originalPassword==md5Password){
            $('#del-msg').html('');
            isDel=true;
        }else{
            $('#del-msg').html('password is different!');
            isDel=false;
        }
    });

    $('#delete-btn').on('click',function(){
        var con = confirm('Are you sure you want to delete your account?');
        if(con){
            if(isDel){
                $.ajax({
                    url:'./delUser',
                    type:'post',
                    success:function(res){
                        if(res=='ok'){
                            alert("Your account is deleted!");
                            location.replace('./');
                        } 
                    },
                    error:function(err){
                    }
                })
            }else{
                alert("Try again!");
            }
        }
        
    });

})