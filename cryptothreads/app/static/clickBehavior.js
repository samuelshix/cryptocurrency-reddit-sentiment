$(document).ready(function () {
    $('#all').click(function () {
        const asset = location.pathname.split('/')[2];
        window.location.href = '/chart/' + asset + '/all';
    })
    $('#year').click(function () {
        const asset = location.pathname.split('/')[2];
        window.location.href = '/chart/' + asset + '/year';
    })
    $('#month').click(function () {
        const asset = location.pathname.split('/')[2];
        window.location.href = '/chart/' + asset + '/month';
    })
    $('#week').click(function () {
        const asset = location.pathname.split('/')[2];
        window.location.href = '/chart/' + asset + '/week';
    })
})
