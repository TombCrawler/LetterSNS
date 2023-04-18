document.addEventListener("DOMContentLoaded", function(){

    const each_items = document.querySelectorAll(".posts")
      each_items.forEach((i) =>{
        // i.style.border = "1px solid black";
        i.style.width = "700px"
        i.style.width = "80%";
        i.style.margin = "30px 10px 20px 30px";
        i.style.padding = "10px";
        i.style.borderRadius = "25px";
      });

      document.querySelector("#backup").onclick = function(event){
        if (!confirm("Would you like to backup data?")){
          event.preventDefault();
        }
      }

});


// Fade out Django messages
document.addEventListener("DOMContentLoaded", function(){
var m = document.getElementsByClassName("alert");  // Return an array

setTimeout(function(){
   if (m && m.length) {
       m[0].classList.add('hide');
   }
}, 3000);
});




// the like feature
document.addEventListener("DOMContentLoaded", function() {
  const likeButtons = document.querySelectorAll('.like-button');
  likeButtons.forEach(button => {
    button.addEventListener('click', function() {
      const postId = this.closest('.posts').dataset.postId;
      const csrftoken = getCookie('csrftoken');
      fetch(`like_post/${postId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
      })
      .then(response => response.json())
      .then(data => {     
        if (data.success) {
          console.log(data)
          updateLikeCount(this.closest('.posts'), data.like_count, data.liked);
          // this.removeEventListener('click', arguments.callee);
          this.innerHTML = '<i class="fa fa-heart"></i>';
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });


  const unlikeButtons = document.querySelectorAll('.unlike-button');
  unlikeButtons.forEach(button => {
    button.addEventListener('click', function() {
      const postId = this.closest('.posts').dataset.postId;
      const csrftoken = getCookie('csrftoken');
      fetch(`unlike_post/${postId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log(data)
          updateLikeCount(this.closest('.posts'), data.like_count);
          // this.removeEventListener('click', arguments.callee);
          this.innerHTML = '<i class="fa fa-heart-broken"></i>';
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });
  


  function updateLikeCount(post, count, liked) {
    const likeCountSpan = post.querySelector('.like-count');
    likeCountSpan.innerHTML = count;
    const likeButton = post.querySelector('.like-button');
    const unlikeButton = post.querySelector('.unlike-button');
    if (liked) {
      likeButton.style.display = 'none';
      unlikeButton.style.display = 'inline-block';
    } else {
      likeButton.style.display = 'inline-block';
      unlikeButton.style.display = 'none';
    }
  }

      function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
});