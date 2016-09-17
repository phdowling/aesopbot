/**
 * Created by dowling on 17/09/16.
 */

var socket = io('http://philippd.me/');
console.log("TEST");
socket.on("general", function (data) {
    console.log(data);
});

socket.on("lyrics", function (data) {
    console.log("GEN: " + JSON.stringify(data));
});

socket.on("seed", function (data) {
    console.log("SEED: " + JSON.stringify(data));
});