$(document).ready(function(){


    $.ajax({
        url:'./getAllDic',
        type:'get',
        success:function(dicList){
            $.each(JSON.parse(dicList),function(index,obj){
                var number = obj.number;
                var source = obj.source;
                var element = $('.my-select[data-index="'+number+'"]');
                element.find('select').val(source);
            });
        },
        error:function(err){

        }
   });


    $('#change-btn').on('click',function(){
        var isDefaultValue=false;

        var allSelect = $('.my-select');
        var arr=[];
        allSelect.each(function(i,item){
            var obj = {};
            obj.index=parseInt($(item).data('index'));
            obj.source = $(item).find('select').val();
            arr.push(obj);
        });
      
        
    $.each(arr,function(index,obj){
       if(obj.source=='Open this select menu'){
            isDefaultValue=true;
       } 
    });
    
    if(!isDefaultValue){
        $.each(arr,function(index,obj){
            var number = obj.index;
            var source = obj.source;
     
            $.ajax({
                 url:'./addDicOrder',
                 type:'post',
                 data:{
                     number:parseInt(number),
                     source:source
                 },
                 success:function(res){
                     console.log(res);
                     location.replace('./');
                 },
                 error:function(err){
     
                 }
            });
         })
    }else{
        alert('Select all sources');
    }


    });



    $('.form-select').change(function(){
        var arr = [];
        $('.form-select').each(function(index,item){
            var value = $(item).val();
            if(value!='Open this select menu'){
                arr.push(value);
            }

            
        });

        
        if(hasDuplicates(arr)){
            alert('duplicate!');
        }

        $('.form-select option').css('color','#000');    
        $.each(arr,function(index,item){
            $('.form-select option[value="'+item+'"]').css('color','red');
        })
        

    });

})


function hasDuplicates(array) {
    var valuesSoFar = Object.create(null);
    for (var i = 0; i < array.length; ++i) {
        var value = array[i];
        if (value in valuesSoFar) {
            return true;
        }
        valuesSoFar[value] = true;
    }
    return false;
}