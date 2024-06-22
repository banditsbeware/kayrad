var W = window.innerWidth, H = window.innerHeight

var mouse = { x: 0.9 * W, y: 0.9 * H }
// $(window).on('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; })
// $(window).on('mouseleave', () => { mouse.x = -1, mouse.y = -1 })

var ctx, canvas = $(`<canvas width=${W} height=${H}></canvas>`)
canvas.css({ 'position': 'absolute', 'top': '0', 'left': '0', 'z-index': '-1' })

$('body').append(canvas)
ctx = canvas[0].getContext('2d')

const randInt = (l, h) => Math.floor( l + Math.random() * (h - l) )

// $('html').css('cursor', 'none')

var A, A0 = 20, k = 1/100, f = 3
var step = 5

ctx.strokeStyle = '#fff'
ctx.lineWidth = 1

let t, t0 = new Date()

function animate() {
  requestAnimationFrame(animate)

  ctx.clearRect(0, 0, W, H)

  if (mouse.x >=0 && mouse.y >= 0) {
    t = (new Date() - t0) / 1000

    A = A0 + (A0)*Math.sin(t)

    ctx.beginPath()
    ctx.ellipse(mouse.x, mouse.y, A, A, 0, 0, 2*Math.PI)
    ctx.moveTo(mouse.x, mouse.y)
    for (let x=mouse.x; x<=W; x += step) ctx.lineTo(x, mouse.y + (A * Math.sin(k*x - (t*f)) ))
    ctx.moveTo(mouse.x, mouse.y)
    for (let x=mouse.x; x>=0; x -= step) ctx.lineTo(x, mouse.y + (A * Math.sin(k*x - (t*f)) ))
    ctx.moveTo(mouse.x, mouse.y)
    for (let y=mouse.y; y<=H; y += step) ctx.lineTo(mouse.x + (A * Math.sin(k*y - (t*f)) ), y) 
    ctx.moveTo(mouse.x, mouse.y)
    for (let y=mouse.y; y>=0; y -= step) ctx.lineTo(mouse.x + (A * Math.sin(k*y - (t*f)) ), y) 
    ctx.stroke()
  }
}

animate()
