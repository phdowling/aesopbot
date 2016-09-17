/**
 * Created by dowling on 17/09/16.
 */

var socket = io('http://localhost');
console.log("TEST");
socket.on("general", function (data) {
    console.log(data);
});