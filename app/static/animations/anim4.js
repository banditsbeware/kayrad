var W = window.innerWidth, H = window.innerHeight

var ctx, canvas = $(`<canvas width=${W} height=${H}></canvas>`)
canvas.css({ 'position': 'absolute', 'top': '0', 'left': '0', 'z-index': '-1' })

$('body').append(canvas)
ctx = canvas[0].getContext('2d')

var c1 = '#404e5c', c2 = '#505e6c'

var p, cs = Math.floor( W / 100 );

function animate() {
  requestAnimationFrame( animate );

  for (let r = 0; r <= Math.floor( W / cs ); r++ ) {
    for (let c = 0; c <= Math.floor( H / cs ); c++ ) {
      ctx.fillStyle = Math.random() < 0.5 ? c1 : c2;
      ctx.fillRect( r * cs, c * cs, cs, cs );
    }
  }
}
animate();