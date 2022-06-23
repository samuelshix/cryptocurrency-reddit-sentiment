function populateComments(submissions, comments) {
    // var click_date = (new Date(submission.date)).toDateString()
    var comments_element = document.getElementById("comments");
    var submission_element = document.getElementById("reddit_thread")
    var top_comment = document.getElementById("top-comment")
    var top_comment_text = document.getElementById("top-comment-text")
    var top_comment_score = document.getElementById("top-comment-score")
    var top_comment_date = document.getElementById("top-comment-date")
    // var subreddits = document.getElementById("subreddits")
    // subreddits.innerHTML = ''
    top_comment.style.display = 'block'
    comments_element.innerHTML = ''
    var date = (new Date(submissions[0].date)).toDateString()
    submissions.forEach(submission => {
      subreddit = document.getElementsByClassName(submission.subreddit)[0]
      subreddit.style.display = 'inline-block'
      subreddit.innerText = `r/${submission.subreddit}`
      submission_element.style.display = 'block';
        subreddit.click(function(){
          submission_element.children[0].setAttribute('href', 'https://www.reddit.com/'+ submission.id)
        })
        submission_element.children[0].setAttribute('href', 'https://www.reddit.com/'+ submission.id)
        submission_element.children[0].innerText = 'View Thread: '+ date
    });
    comments.forEach((comment,i) => {
      if(i===0) {
        top_comment_text.innerText = comment.text
        top_comment_score.innerText = comment.score
        top_comment_date.innerText = date        
      }
      var element = document.createElement('div')
      element.className = `comment_${comment.subreddit} collapse show`
      element.classList.add("card")
      var comment_score = document.createElement('p')
      comment_score.innerText = `Score: ${comment.score} | Subreddit: r/${comment.subreddit}`
      comment_score.style.fontWeight = 500
      var comment_text = document.createElement('p')
      comment_text.innerText = comment.text
      element.appendChild(comment_score)
      element.appendChild(comment_text)
      comments_element.appendChild(element)
    })
    }