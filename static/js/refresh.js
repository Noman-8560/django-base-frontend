$(document).ready(function (event) {
    window.onbeforeunload = function () {
        return "Are you sure you want to leave?";
    }
});