import signal
import os, fcntl, array, keyboard

dev_filename = '/dev/lcdi2c'
dev_meta_filename = '/sys/class/alphalcd/lcdi2c/meta'

cols = 0
rows = 0
bufferlength = 0

ioctls = dict()

f = os.open(dev_meta_filename, os.O_RDONLY)

def quit_app():
  try: 
    f.close()
  except:
    pass
  print("Closed {}. Exit".format(dev_filename))
  exit(1)

def handler(signum, frame):
  quit_app()
signal.signal(signal.SIGINT, handler)

if f:
  print("Opened {}".format(dev_filename))
  meta = os.read(f, 512).decode('ascii').rstrip().split("\n")
  os.close(f)
  cols, rows = [int(meta[v].split(":")[1]) for v in range(2,0,-1)]
  bufferlength = cols * rows
  try:
    iioc = meta.index("IOCTLS:") + 1
  except ValueError as e:
    print("No IOCTLS section in meta file")
    raise e
  ioctls = dict(k.split("=") for k in [s.lstrip() for s in meta[iioc:]])
else:
    print("Unable to open meta file for driver.")
    quit_app()

""" Supported IOCTLs 

dict_keys(['GETCHAR', 'SETCHAR', 'GETPOSITION', 'SETPOSITION', 'RESET', 
'HOME', 'GETBACKLIGHT', 'SETBACKLIGHT', 'GETCURSOR', 'SETCURSOR', 'GETBLINK', 
'SETBLINK', 'SCROLLHZ', 'GETCUSTOMCHAR', 'SETCUSTOMCHAR', 'CLEAR'])

"""

f = open(dev_filename, 'rb+')

def write_ioctl(cmd: str, value):
  if cmd not in ioctls:
    print("[ERROR] Not supported IOCTL: {}".format(cmd))
    return 1
  cmd_hex = ioctls[cmd]
  s = array.array('B')
  if isinstance(value, str):
    value = bytes(value, encoding='ascii')
  s.extend(value)
  f = open(dev_filename, 'rb+')
  fcntl.ioctl(f, int(cmd_hex, base=16), s)
  f.close()
  return s

def write(input: str):
  output = bytes(input, encoding='ascii')
  f = open(dev_filename, 'rb+')
  f.write(output)
  f.close()

def get_cursor():
  return write_ioctl('GETPOSITION', [0,0])

def set_cursor(x, y):
  return write_ioctl('SETPOSITION', [x, y])

def move_cursor(delta_x, delta_y):
  x, y = get_cursor()
  new_x = x + delta_x
  new_y = y + delta_y
  if new_x < 0: new_x = cols-1
  if new_y < 0: new_y = rows-1
  return set_cursor(new_x, new_y)

write_ioctl('CLEAR', '1')
write_ioctl('SETBLINK', '1')
write_ioctl('SETBLINK', '1')
write_ioctl('SETPOSITION', [0,0])



while True:
  event = keyboard.read_event()

  valid_char_events = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                  'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u',
                  'v', 'w', 'x', 'y', 'z',
                  '0', '1', '2', '3', '4', 
                  '5', '6', '7', '8', '9']                 

  if event.event_type == keyboard.KEY_DOWN:
    if event.name in valid_char_events:
      char = event.name
      x, y = get_cursor()
      if x == cols-1: y += 1
      write(char)
      set_cursor(x+1, y)

    if event.name == 'space':
      write(' ')

    if event.name == 'enter':
      write('\n')
      # col, row = write_ioctl('GETPOSITION', [0,0])
      x, y = get_cursor()
      write(' '*cols)
      # write_ioctl('SETPOSITION', [col, row])
      set_cursor(x, y)

    if event.name == 'backspace':
      move_cursor(-1, 0)
      write(' ')
      move_cursor(-1, 0)

    if event.name in ['up', 'down', 'left', 'right']:
      # col, row = write_ioctl('GETPOSITION', [0,0])
      x, y = get_cursor()
      dt_x=0
      dt_y=0
      if event.name == 'up'    : dt_y = -1
      if event.name == 'down'  : dt_y =  1 
      if event.name == 'left'  : dt_x = -1
      if event.name == 'right' : dt_x =  1 
      move_cursor(dt_x, dt_y)

    if event.name == 'esc':
      quit_app()

# print(pos)
# write('Hello')
# keyboard.wait('esc')

########################################
f.close()