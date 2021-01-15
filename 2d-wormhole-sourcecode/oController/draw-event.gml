draw_set_colour(c_white);

with (w_entrance) {
	draw_circle(x, y, R, true);
	draw_circle(x, y, other.wormhole_bore, true);
}
	
with (w_exit) {
	draw_circle(x, y, R, true);
	draw_circle(x, y, other.wormhole_bore, true);
}

//draw plane separation line
draw_set_colour(c_red);
draw_set_alpha(0.25);
draw_line(room_width/2, room_height/3, room_width/2, room_height);
draw_set_alpha(1);

// draw wormhole diagram
draw_sprite(sWormholeDiagram, 0 , 0, 0);

with(oPlayer) {
	event_user(0);
}
