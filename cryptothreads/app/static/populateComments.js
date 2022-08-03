function populateComments(submissions, comments) {
  var comments_element = document.getElementById("comments");
  var submission_element = document.getElementById("reddit_thread")
  var top_comment = document.getElementById("top-comment")
  var top_comment_text = document.getElementById("top-comment-text")
  var top_comment_score = document.getElementById("top-comment-score")
  var top_comment_date = document.getElementById("top-comment-date")
  var subreddits = document.getElementById("subreddits")
  var socialTitle = document.getElementById("social-media-title")
  socialTitle.style.display = "block"
  subreddits.childNodes.forEach((child, i) => {
    if ((i % 2) === 1) {
      child.style.display = 'none'
    }
  })
  top_comment.style.display = 'block'
  comments_element.innerHTML = ''
  var date = (new Date(submissions[0].date)).toDateString()
  submissions.forEach(submission => {
    subreddit = document.getElementsByClassName(submission.subreddit)[0]
    subreddit.style.display = 'inline-block'
    subreddit.innerText = `r/${submission.subreddit}`
    submission_element.style.display = 'block';
    subreddit.click(function () {
      submission_element.children[0].setAttribute('href', 'https://www.reddit.com/' + submission.id)
    })
    submission_element.children[0].setAttribute('href', 'https://www.reddit.com/' + submission.id)
    submission_element.children[0].innerText = 'View Thread: ' + date
  });
  comments.forEach((comment, i) => {
    if (i === 0) {
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
function populateTweets(tweets) {
  var tweets_element = document.querySelector(".tweets_card .card-body");
  tweets_element.innerHTML = ''
  if (tweets.length === 0) { tweets_element.innerHTML = "Tweets are only available from 7/25/2022 and onward due to API constraints." }
  tweets.forEach(tweet => {
    var tweet_link = document.createElement('a')
    tweet_link.href = `https://twitter.com/u/status/${tweet.id}`
    tweet_link.target = "_blank"
    var tweet_element = document.createElement('div')
    var tweet_text = document.createElement('p')
    tweet_text.innerText = tweet.text
    var tweet_retweets = document.createElement('p')
    tweet_retweets.innerText = `Likes: ${tweet.likes} | Retweets: ${tweet.retweets}`
    tweet_element.classList.add("card")
    tweet_element.appendChild(tweet_retweets)
    tweet_element.appendChild(tweet_text)
    tweet_link.appendChild(tweet_element)
    tweets_element.appendChild(tweet_link)
  })
}

function togglePlatform() {
  const inputs = document.getElementsByTagName("input");
  const reddit_comments = document.getElementsByClassName("comments_card")[0]
  const tweets = document.getElementsByClassName("tweets_card")[0]
  const reddit_label = document.getElementById("reddit")
  const twitter_label = document.getElementById("twitter")
  console.log(reddit_label)
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].type === 'checkbox') {
      const toggle = inputs[i]
      if (toggle.checked) {
        reddit_comments.style.display = 'none'
        tweets.style.display = "block"
        reddit_label.style.color = "black"
        twitter_label.style.color = "rgb(88, 194, 255)"
      } else {
        reddit_comments.style.display = 'block'
        tweets.style.display = "none"
        reddit_label.style.color = "rgba(255, 87, 30, 1)"
        twitter_label.style.color = "black"
      }
    }
  }
}