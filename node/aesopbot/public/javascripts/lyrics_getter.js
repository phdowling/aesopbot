/**
 * Created by dowling on 17/09/16.
 */

var socket = io('http://localhost:3000');

socket.on("general", function (data) {
    console.log(data);
});