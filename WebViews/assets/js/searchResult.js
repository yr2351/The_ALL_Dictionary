$(document).ready(function(){


    $.ajax({
        url:'../getAllDic',
        type:'get',
        success:function(dicList){

            if(dicList=='fail' || dicList=='[]'){
                dicList='[{"email": "0", "number": 1, "source": "Merriam Websters Learner"}, {"email": "0", "number": 2, "source": "Merriam Webster"}, {"email": "0", "number": 3, "source": "Oxford Dictionary"}, {"email": "0", "number": 4, "source": "Urban Dictionary"}, {"email": "0", "number": 5, "source": "Wikipedia"}, {"email": "0", "number": 6, "source": "Google News"}, {"email": "0", "number": 7, "source": "Google Photo"}, {"email": "0", "number": 8, "source": "Youtube"}]';
            }
            $.each(JSON.parse(dicList),function(index,obj){
                var number = obj.number;
                var source = obj.source;                

                var el = $('#fake-list').find('.list-group-item[data-source="'+source+'"]').clone();
                $('#real-list').append(el);

            });
        },
        error:function(err){

        }
   });

})