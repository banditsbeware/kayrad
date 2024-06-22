var W = window.innerWidth, H = window.innerHeight

var mouse = { x: -1, y: -1 }
$(window).on('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; })
$(window).on('mouseleave', () => { mouse.x = -1, mouse.y = -1 })

var ctx, canvas = $(`<canvas width=${W} height=${H}></canvas>`)
canvas.css({ 'position': 'absolute', 'top': '0', 'left': '0', 'z-index': '-1' })

$('body').append(canvas)
ctx = canvas[0].getContext('2d')

const randInt = (l, h) => Math.floor( l + Math.random() * (h - l) )

ctx.strokeStyle = '#fff'
ctx.fillStyle = 'rgba(183, 195, 243, 0.4)'
ctx.lineWidth = 1

var D = 300 * Math.random() + 50

function pt(x, y, z) { return { x, y, z } }

let proj = function(p, D) {
  let sf = D / (D - p.z)
  return { x: p.x * sf, y: p.y * sf }
}

class square {
  constructor(s, r, t, z) {
    this.s = s
    this.r = r
    this.t = t
    this.z = z
  }

  points() {
    let x = this.r * Math.cos(this.t), y = this.r * Math.sin(this.t)
    let dx = this.s * Math.sin(this.t), dy = this.s * Math.cos(this.t)
    this.a = pt( x + dx, y - dy, this.z + this.s )
    this.b = pt( x - dx, y + dy, this.z + this.s )
    this.c = pt( x - dx, y + dy, this.z - this.s )
    this.d = pt( x + dx, y - dy, this.z - this.s )
  }

  draw(ox, oy) {
    this.points()
    let a = proj(this.a, D), b = proj(this.b, D), 
        c = proj(this.c, D), d = proj(this.d, D)
    ctx.beginPath()
    ctx.moveTo(ox + a.x, oy - a.y)
    ctx.lineTo(ox + b.x, oy - b.y)
    ctx.lineTo(ox + c.x, oy - c.y)
    ctx.lineTo(ox + d.x, oy - d.y)
    ctx.closePath()
    ctx.stroke()
  }
}

var R = Math.min(W,H), BIGZ = 10*D, NEARZ = D 

var Z = () => -BIGZ * Math.random() + NEARZ

var tiles = Array()
for (let i =0; i < 500; i++) 
  tiles.push(new square(20, R/2 + R/2 * Math.random(), Math.random() * Math.PI*2, Z()))

var dz = 2 * Math.random(), dt = 0.0005 * Math.random() - 0.00025
function animate() {
  requestAnimationFrame(animate)
  ctx.clearRect(0, 0, W, H)

  for (let s of tiles) {
    s.t += dt, s.z += dz
    if (s.z -50 > 0) s.z = -BIGZ
    s.draw(W/2, H/2)
  }
}

animate()