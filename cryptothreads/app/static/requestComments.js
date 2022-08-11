function requestComments(timestamp) {
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    console.log(timestamp)
    $.ajax({
        type: 'GET',
        url: '/get/comment-data/',
        data: {
            'asset': location.pathname.split('/')[2],
            'timestamp': timestamp
        },
        success: function (data) {
            populateComments(data.submissions, data.comments)
            populateTweets(data.tweets)
        },
        error: function () {
            alert("Error: Missing thread for date, choose a different date.")
        },

    })
    console.log(Date.now() / 1000, new Date().getTime())

}

// use requestComments function with the current date as the timestamp
const date = new Date()
const yesterday = (new Date(date.getTime())).setDate(date.getDate() - 1)
requestComments(yesterday / 1000)
document.getElementById("date-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const date = document.getElementsByClassName("date-input")[0].value;
    console.log(date)
    const myDate = date.split("-");
    const newDate = new Date(myDate[0], myDate[1] - 1, myDate[2]);
    requestComments(newDate.getTime() / 1000)
    console.log(newDate.getTime() / 1000)
})