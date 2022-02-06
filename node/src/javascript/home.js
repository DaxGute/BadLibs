var canvas = document.getElementById('backgroundCanvas')
canvas.width = window.innerWidth
canvas.height = window.innerHeight
var ctx = canvas.getContext('2d')

var socket = io();


document.getElementById('Noun').addEventListener('click', () => {
    socket.emit('anotherArticle')
    document.getElementById('secArt').innerHTML = "..."
    document.getElementById('firstArt').innerHTML = "..."
    document.getElementById('newTitle').innerHTML = "Loading..."

})
// socket.on('getArticle', message => {
//     var titleArray = message.split('☃')

//     document.getElementById('secArt').innerHTML = titleArray[0]
//     document.getElementById('firstArt').innerHTML = titleArray[1]
//     document.getElementById('newTitle').innerHTML = titleArray[2]
// })


canvasAnimationFrames()
updateBox()

function updateBox(){
   
        document.getElementById("choiceBox").classList.add("fade-in")
        document.getElementById("choiceBox").classList.remove("fade-out")

}


requestAnimationFrame(canvasAnimationFrames);
var startTime = Date.now()
var pos = 1000
var currentVel = 0
var mousehasmoved = false
function canvasAnimationFrames() {
    var endTime = Date.now()
    var difference = endTime - startTime
    if (difference > (1/30)) {
        ctx.fillStyle = "#48C8A9";
        ctx.strokeStyle = "#F0F231"
        ctx.lineWidth = 5
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        if (mousehasmoved){
            pos += currentVel
        }
        pos += 1

        // ctx.fillStyle = "rgb(" + (72 + (pos/200%20)) + ", " + (200 + (pos/100%20)) + ", "  + (169 - (pos/200%20)) + ")" 
        drawLoops(pos)
    }
    mousehasmoved = false
    requestAnimationFrame(canvasAnimationFrames);
}

window.onresize = windowResized;
function windowResized(){
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
}

document.addEventListener('mousemove', e => {
    currentVel = Math.sqrt(Math.pow(e.movementX,2) + Math.pow(e.movementY,2))
    mousehasmoved = true;
  });


function drawLoops(pos){ //TODO: it isn't completely smooth
    var width = window.innerWidth
    var height = window.innerHeight
    var verticalRadius = 0.05 * width
    var horizontalRadius = 0.05 * height

    //left going down
    var arcCenterX = -0.05 * width + (pos%(width*20))/20
    for (let index = 0; index < (height/(verticalRadius*2)); index++) {
        var arcCenterY = index * 2 * (0.05 * width) + (pos%(2.5*height)) - 1.25*height

        ctx.beginPath();
        if(index%2 == 0){
            ctx.arc(arcCenterX, arcCenterY, verticalRadius, -Math.PI/2, Math.PI/2);
        }else{
            ctx.arc(arcCenterX, arcCenterY, verticalRadius, Math.PI/2, -Math.PI/2);
        }
        ctx.stroke();
    }




    //right going up
    var arcCenterX = 1.05 * width - (pos%(width*20))/20
    for (let index = 0; index < (height/(verticalRadius*2)); index++) {
        var arcCenterY = index * 2 * (0.05 * width) - (pos%(2.5*height)) + 1.25*height
        ctx.beginPath();
        if(index%2 == 0){
            ctx.arc(arcCenterX, arcCenterY, verticalRadius, Math.PI/2, -Math.PI/2);
        }else{
            ctx.arc(arcCenterX, arcCenterY, verticalRadius, -Math.PI/2, Math.PI/2);
        }
        ctx.stroke();
    }

    //top going left
    var arcCenterY = -0.05 * height + (pos%(height*20))/20
    for (let index = 0; index < (width/(horizontalRadius*2)); index++) {
        var arcCenterX = index * 2 * (0.05 * height) - (pos%(2.5*width)) + 1.25*width

        ctx.beginPath();
        if(index%2 == 0){
            ctx.arc(arcCenterX, arcCenterY, horizontalRadius, 0, Math.PI);
        }else{
            ctx.arc(arcCenterX, arcCenterY, horizontalRadius, Math.PI, 0);
        }
        ctx.stroke();
    }

    //bottom going right
    var arcCenterY = 1.05 * height - (pos%(height*20))/20
    for (let index = 0; index < (width/(horizontalRadius*2)); index++) {
        var arcCenterX = index * 2 * (0.05 * height) + (pos%(2.5*width)) - 1.25*width

        ctx.beginPath();
        if(index%2 == 0){
            ctx.arc(arcCenterX, arcCenterY, horizontalRadius, Math.PI, 0);
        }else{
            ctx.arc(arcCenterX, arcCenterY, horizontalRadius, 0, Math.PI);
        }
        ctx.stroke();
    }

}

