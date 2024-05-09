import tkinter as tk
from xmlrpc.server import SimpleXMLRPCServer

line_id = None
line_points = []

def draw_line(x, y):
  global line_id
  line_points.extend((x, y))
  if line_id is not None:
    canvas.delete(line_id)
  line_id = canvas.create_line(line_points)

def set_start(x, y):
  line_points.extend((x, y))

def end_line():
  global line_id
  line_points.clear()
  line_id = None

root = tk.Tk()
root.title('Server')

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)

server.register_function(root.update, 'update')
server.register_function(canvas.delete, 'delete')
server.register_function(draw_line, 'draw_line')
server.register_function(set_start, 'set_start')
server.register_function(end_line, 'end_line')

server.serve_forever()