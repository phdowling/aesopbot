/**
 * Created by dowling on 17/09/16.
 */

var socket = io('http://philippd.me/');
console.log("TEST");
socket.on("general", function (data) {
    console.log(data);
});

socket.on("lyrics", function (data) {
    //console.log("GEN: " + JSON.stringify(data));
    var htmlIzed = "<span class='seed'>" + data.replace(/(?:\r\n|\r|\n)/g, '<br />') + "</span>>";
    var container = $(".container");
    container.html(container.html() + htmlIzed);
});

socket.on("seed", function (data) {
    console.log("SEED: " + JSON.stringify(data));
    var htmlIzed = data.replace(/(?:\r\n|\r|\n)/g, '<br />');

    var container = $(".container");
    container.empty();
    container.html(htmlIzed);
});