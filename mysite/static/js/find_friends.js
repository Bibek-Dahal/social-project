
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function myfun(e){
    console.log(event)
    event.preventDefault();
    console.log(e)
   let x = $('form').attr('class')
   console.log(x)
    if ($(`input[id=${e}]`).val() === 'cancel request'){
         let my_url = `http://127.0.0.1:8000/cancel_friend_request/${x}/`
         $.ajax({
             type:'POST',
             headers: {'X-CSRFToken': csrftoken},
             url:my_url,
             success:(response)=>{
                 console.log(response)
                 $(`#${e}`).prop('value','add friend');
             },
             error:(response)=>{
                 alert(response)
             }
         })
    }
    
    else{
        let my_url = `http://127.0.0.1:8000/add_friend/${e}/`
         $.ajax({
             type:'POST',
             headers: {'X-CSRFToken': csrftoken},
             url:my_url,
             success:(response)=>{
                 console.log(response)
                 $(`#${e}`).prop('value','cancel request');
                 $('form').prop('class',response.fr_id)  
             },
             error:(response)=>{
                 alert(response)
             }
         })
    }
   
}