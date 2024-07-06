var W = window.innerWidth, H = window.innerHeight

var ctx, canvas = $(`<canvas width=${W} height=${H}></canvas>`)
canvas.css({ 'position': 'absolute', 'top': '0', 'left': '0', 'z-index': '-1' })

$('body').append(canvas)
ctx = canvas[0].getContext('2d')

var c1 = 'rgba(183,195,243,0.2)', c2 = '#404e5c'

var now, then = Date.now(), color, cs = W / 20;

var off = 0;

function animate() {
  requestAnimationFrame( animate );

  now = Date.now();

  if ( now - then > 1000 / 10 ) {
    off -= 1;
    if (Math.abs(off) > cs) off = 0;

    then = Date.now();
    var R = [], C = [];
    for (let i = 0; i < Math.floor( W / cs ); i++) C.push( Math.random() < 0.5 ? 1 : 0 );
    for (let i = 0; i < Math.floor( H / cs ); i++) R.push( Math.random() < 0.5 ? 1 : 0 );
    
    for (let c=0; c < C.length; c++) {
      color = C[c] ? c1 : c2;
      for (let r = 0; r <= 1.5*H; r += cs) {
        ctx.beginPath();
        color = color == c1 ? c2 : c1;
        ctx.strokeStyle = color;
        ctx.moveTo(c * cs - off, r - off);
        ctx.lineTo(c * cs - off, cs + r - off);
        ctx.stroke();
      }
    }
    
    for (let r=0; r < R.length; r++) {
      color = R[r] ? c1 : c2;
      for (let c = 0; c <= 1.5*W; c += cs) {
        ctx.beginPath();
        color = color == c1 ? c2 : c1;
        ctx.strokeStyle = color;
        ctx.moveTo(c      - off, r * cs - off);
        ctx.lineTo(c + cs - off, r * cs - off);
        ctx.stroke();
      }
    }
  }
    
}
animate();