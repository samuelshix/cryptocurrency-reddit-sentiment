function populateComments(submissions, comments) {
  var commentsElement = document.getElementById("comments");
  var submissionElement = document.getElementById("reddit_thread")
  var topComment = document.getElementById("top-comment")
  var topCommentText = document.getElementById("top-comment-text")
  var topCommentScore = document.getElementById("top-comment-score")
  var topCommentDate = document.getElementById("top-comment-date")
  var subreddits = document.getElementById("subreddits")
  var socialTitle = document.getElementById("social-media-title")
  socialTitle.style.display = "block"
  subreddits.childNodes.forEach((child, i) => {
    if ((i % 2) === 1) {
      child.style.display = 'none'
    }
  })
  topComment.style.display = 'block'
  commentsElement.innerHTML = ''
  var date = (new Date(submissions[0].date)).toDateString()
  submissions.forEach(submission => {
    subreddit = document.getElementsByClassName(submission.subreddit)[0]
    subreddit.style.display = 'inline-block'
    subreddit.innerText = `r/${submission.subreddit}`
    submissionElement.style.display = 'block';
    subreddit.click(function () {
      submissionElement.children[0].setAttribute('href', 'https://www.reddit.com/' + submission.id)
    })
    submissionElement.children[0].setAttribute('href', 'https://www.reddit.com/' + submission.id)
    submissionElement.children[0].innerText = 'View Thread: ' + date
  });
  comments.forEach((comment, i) => {
    if (i === 0) {
      topCommentText.innerText = comment.text
      topCommentScore.innerText = comment.score
      topCommentDate.innerText = date
    }
    var element = document.createElement('div')
    element.className = `comment_${comment.subreddit} collapse show`
    element.classList.add("card")
    var commentScore = document.createElement('p')
    commentScore.innerText = `Score: ${comment.score} | Subreddit: r/${comment.subreddit}`
    commentScore.style.fontWeight = 500
    var commentText = document.createElement('p')
    commentText.innerText = comment.text
    element.appendChild(commentScore)
    element.appendChild(commentText)
    commentsElement.appendChild(element)
    const dateEle = document.getElementsByClassName("current-date")[0]
    dateEle.innerText = date
  })

}
let disabled;
function populateTweets(tweets) {
  // console.log(tweets)
  const error = document.createElement('p')
  const twitterLabel = document.getElementById("twitter")
  const switchToggle = document.getElementById("switchInput")
  const infoPopup = document.getElementsByClassName("popup")[0]
  const slider = document.getElementsByClassName("slider")[0]
  var tweetsElement = document.querySelector(".tweets_card .card-body");
  tweetsElement.innerHTML = ''
  slider.style.backgroundColor = "rgba(255, 87, 30, 1)"
  slider.style.boxShadow = "0 0 1em #e66800"
  slider.style.cursor = "pointer"
  infoPopup.style.display = "none"
  switchToggle.removeAttribute('disabled')
  twitterLabel.style.color = "black"
  if (tweets.length === 0) {
    disabled = true
    slider.style.backgroundColor = "lightgrey"
    slider.style.boxShadow = "0 0 0 rgba(0,0,0,0)"
    slider.style.cursor = "default"
    infoPopup.style.display = "block"
    switchToggle.setAttribute('disabled', 'disabled')
    twitterLabel.style.color = "lightgrey"
    error.innerText = "Tweets are only available from 7/25/2022 and onward due to API constraints."

    tweetsElement.appendChild(error)
  }
  tweets.forEach(tweet => {
    var tweetLink = document.createElement('a')
    tweetLink.href = `https://twitter.com/u/status/${tweet.id}`
    tweetLink.target = "_blank"
    var tweetEle = document.createElement('div')
    var tweetText = document.createElement('p')
    tweetText.innerText = tweet.text
    var tweet_retweets = document.createElement('p')
    tweet_retweets.innerText = `Likes: ${tweet.likes} | Retweets: ${tweet.retweets}`
    tweetEle.classList.add("card")
    tweetEle.appendChild(tweet_retweets)
    tweetEle.appendChild(tweetText)
    tweetLink.appendChild(tweetEle)
    tweetsElement.appendChild(tweetLink)
  })
}

function togglePlatform() {
  const inputs = document.getElementsByTagName("input");
  const redditComments = document.getElementsByClassName("comments_card")[0]
  const tweets = document.getElementsByClassName("tweets_card")[0]
  const redditLabel = document.getElementById("reddit")
  const twitterLabel = document.getElementById("twitter")
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].type === 'checkbox') {
      const toggle = inputs[i]
      if (!toggle.checked) {
        redditComments.style.display = 'block'
        tweets.style.display = "none"
        redditLabel.style.color = "rgba(255, 87, 30, 1)"
        twitterLabel.style.color = "black"
      } else {
        redditComments.style.display = 'none'
        tweets.style.display = "block"
        redditLabel.style.color = "black"
        twitterLabel.style.color = "rgb(88, 194, 255)"
      }
    }
  }
}

function displayInfo() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}