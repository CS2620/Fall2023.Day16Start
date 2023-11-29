def close_to(one, two):
  return one[0] - two[0] + one[1] - two[1] + one[2] - two[2] < .01

def rgb_to_hsv(r, g, b):
  """
  Given r,g,b in [0,255], find the h,s,v
  in [0,1]
  """
  r = r/255
  g = g/255
  b = b/255

  v = max(r,g,b)
  n = min(r,g,b)

  if v == n:
    return (0, 0, v)

  s = (v - n)/v

  base_angle = 0
  offset_angle = 0

  if v == r:
    base_angle = 0
    offset_angle = (g - b)/(v-n)*60
  elif v == g:
    base_angle = 120
    offset_angle = (b-r)/(v-n)*60
  elif v == b:
    base_angle = 240
    offset_angle = (r-g)/(v-n)*60

  final_angle = base_angle + offset_angle

  if final_angle < 0:
    final_angle += 360

  h = final_angle
  
  return (h/360, s, v)

def hsv_to_rgb(h,s,v):
  """
  Given h,s,v in [0,1], get 
  r,g,b in [0,255]
  """

  r = -1
  g = -1
  b = -1

  if h  > 5/6:
    h = h - 1
  n = (1-s)*v
  

  diff_r = abs(h - 0 if h > 0 else h)
  diff_g = abs(1/3 - h)
  diff_b = abs(2/3 - h)

  if diff_r < diff_g and diff_r < diff_g:
    r = v
    if  h < 0: # we are rotated toward blue (negative)
      g = n
      b = 6*(h)*(n-v)+n
    else: # we are rotated toward green (positive)
      b = n
      g = 6*h*v-6*h*n+n
  elif diff_g < diff_r and diff_g < diff_b:
    g = v
    if h < 1/3: # we are rotated toward red (negative)
      b = n
      r = (6*h-2)*(n-v)+n
    else: # we are rotated toward blue (positive)
      r = n
      b = (6*h-2)*(v-n)+n
  else:
    b = v
    if h < 2/3: # we are rotated toward green (negative)
      r = n
      g = (6*h-4)*(n-v) + n
    else: #we are rotated toward red (positive)
      g = n
      r = (6*h-4)*(v-n)+n

  return (int(r*255+.5), int(g*255+.5), int(b*255+.5))

assert rgb_to_hsv(255, 0, 0) == (0, 1, 1)
assert rgb_to_hsv(0, 255, 0) == (1/3, 1, 1)
assert rgb_to_hsv(0, 0, 255) == (2/3, 1, 1)
assert rgb_to_hsv(0, 0, 0) == (0, 0, 0)
assert rgb_to_hsv(255, 255, 255) == (0, 0, 1)
assert rgb_to_hsv(128, 128, 128) == (0, 0, 128/255)

#Red rotated toward blue
temp = rgb_to_hsv(255, 0, 100)
rgb = hsv_to_rgb(*temp)
assert rgb == (255, 0, 100)
#Red rotated toward green
temp = rgb_to_hsv(255, 100, 0)
rgb = hsv_to_rgb(*temp)
assert rgb == (255, 100, 0)


#Green rotated toward red
temp = rgb_to_hsv(100, 255, 0)
rgb = hsv_to_rgb(*temp)
assert rgb == (100, 255, 0)
#Green rotated toward blue
temp = rgb_to_hsv(0, 255, 100)
rgb = hsv_to_rgb(*temp) 
assert rgb == (0, 255, 100)

#Blue rotated toward green
temp = rgb_to_hsv(0, 100, 255)
rgb = hsv_to_rgb(*temp)
assert  rgb == (0, 100, 255)
#Blue rotated toward red
temp = rgb_to_hsv(100, 0, 255)
assert hsv_to_rgb(*temp) == (100, 0, 255)

# Random colors, compared to GIMP conversion
temp = rgb_to_hsv(6, 29, 35)
assert close_to(temp, (.534, .82, .137))




def rgb_to_cmyk(r, g, b):
  _r, _g, _b = r/255, g/255, b/255
  maximum = max(_r, _g, _b)

  k = 1-maximum
  if k == 1:
    return (0,0,0,1)
  c = (1-_r-k)/(1-k)
  m = (1-_g-k)/(1-k)
  y = (1-_b-k)/(1-k)
  return (int(c*255),int(m*255),int(y*255),int(k*255))