import tkinter as tk
from xmlrpc.client import ServerProxy

line_id = None
line_points = []

def draw_line(event: tk.Event):
  global line_id
  line_points.extend((event.x, event.y))
  if line_id is not None:
    canvas.delete(line_id)
  line_id = canvas.create_line(line_points)

  proxy.draw_line(event.x, event.y)

def set_start(event: tk.Event):
  line_points.extend((event.x, event.y))

  proxy.set_start(event.x, event.y)

def end_line(event=None):
  global line_id
  line_points.clear()
  line_id = None

  proxy.end_line()

root = tk.Tk()
root.title('Client')

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

proxy = ServerProxy('http://localhost:8000/')

canvas.bind('<Button-1>', set_start)
canvas.bind('<B1-Motion>', draw_line)
canvas.bind('<ButtonRelease-1>', end_line)

while True:
  try:
    canvas.update()
    proxy.update()
  except (Exception, KeyboardInterrupt):
    proxy.delete('all')
    proxy.update()
    exit(0)
