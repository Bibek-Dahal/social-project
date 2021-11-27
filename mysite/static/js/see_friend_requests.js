
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

function confirmBtn(e){
    console.log('confirmed clicked');
    event.preventDefault();
    $.ajax({
        method:'POST',
        headers: {'X-CSRFToken': csrftoken},
        url:`http://127.0.0.1:8000/accept_friend_request/${e}/`,
        success:(response)=>{
            console.log(response)
            $("#confirm").html('you are now friend');
            $("#confirm").attr('disabled',true);
            $('#delete').remove();
            
        },
        error:(response)=>{
            alert(response)
        }
    })

}

function deleteBtn(e){
    event.preventDefault();
    console.log('delete btn clicked');
    $.ajax({
        method:'GET',
        url:`http://127.0.0.1:8000/cancel_friend_request/${e}/`,
        success:(response)=>{
            console.log(response)
            $("#delete").html('deleted');
            $("#delete").attr('disabled',true);
            $('#confirm').remove();
            
        },
        error:(response)=>{
            alert(response)
        }
    })

}