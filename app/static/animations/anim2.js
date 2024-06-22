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
ctx.lineWidth = 1

class Dot {
  constructor(x, y, v) {
    this.x = x
    this.y = y
    this.vx = v * (Math.random() - 0.5)
    this.vy = v * (Math.random() - 0.5)
  }
  nudge(A) { 
    if (this.x < 0 || W < this.x) this.vx = -this.vx
    if (this.y < 0 || H < this.y) this.vy = -this.vy
    this.x += this.vx; this.y += this.vy 
  }
}

const bezier = (p0, p1, p2) => {
  ctx.moveTo(p0.x, p0.y)
  ctx.beginPath()
  ctx.strokeWidth = 5
  let x, y;
  for (let t = 0; t <= 1; t += 1/grain) {
    x = p1.x + (1-t)**2 * (p0.x - p1.x) + t**2 * (p2.x - p1.x)
    y = p1.y + (1-t)**2 * (p0.y - p1.y) + t**2 * (p2.y - p1.y)
    ctx.lineTo(x, y)
  }
  ctx.lineTo(p2.x, p2.y)
  ctx.stroke()
  dash(p0, p1)
  dash(p1, p2)
  dot(p0, 'white'); dot(p1); dot(p2, 'white');
}

const dash = (a, b) => {
  ctx.save()
  ctx.setLineDash([10, 40])
  ctx.strokeStyle = 'grey'
  ctx.beginPath()
  ctx.moveTo(a.x, a.y)
  ctx.lineTo(b.x, b.y)
  ctx.stroke()
  ctx.restore()
}

const dot = (p, color) => {
  ctx.save()
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.ellipse(p.x, p.y, 5, 5, 0, 0, 2*Math.PI)
  if (color) ctx.fill()
  ctx.stroke()
  ctx.restore()
}

const grain = 30
const N = randInt(1, 10)

let _points, points = Array()
let p0, p1, p2

for (let i = 0; i < N * 3; i++) 
  points.push(new Dot(randInt(0, W), randInt(0, H), randInt(1, 5)))

function animate() {
  requestAnimationFrame(animate)
  ctx.clearRect(0, 0, W, H)

  points.map(p => p.nudge())
  _points = Array.from(points)

  while (_points.length) {
    p0 = _points.pop()
    p1 = _points.pop()
    p2 = _points.pop() 
    bezier(p0, p1, p2)
  }

}

animate()