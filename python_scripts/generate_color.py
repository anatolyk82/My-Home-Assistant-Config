
light_id = data.get('entity_id')

def hsv_to_rgb(h, s, v):
	""" HSV values in [0..1] and returns [r, g, b] values from 0 to 255 """
	h_i = int(h*6)
	f = h*6 - h_i
	p = v * (1 - s)
	q = v * (1 - f*s)
	t = v * (1 - (1 - f) * s)
	if h_i == 0:
		r, g, b = v, t, p

	if h_i == 1:
		r, g, b = q, v, p

	if h_i == 2:
		r, g, b = p, v, t

	if h_i == 3:
		r, g, b = p, q, v

	if h_i == 4:
		r, g, b = t, p, v

	if h_i == 5:
		r, g, b = v, p, q

	return [int(r*256), int(g*256), int(b*256)]

h = random.random()
rgb = hsv_to_rgb(h, 0.99, 0.99)

service_data = { 'entity_id': light_id, 'rgb_color': rgb }
hass.services.call('light', 'turn_on', service_data, False)

