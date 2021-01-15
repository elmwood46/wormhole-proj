draw_set_font(fCourier);
player = instance_create_layer(room_width/2, room_height/2, layer, oPlayer);

wormhole_radius = 200;
wormhole_bore = 32;
psign = 1;

w_entrance = instance_create_layer(room_width-wormhole_radius*2, 2*room_height/3, layer, oWormhole);
w_exit = instance_create_layer(wormhole_radius*2, 2*room_height/3, layer, oWormhole);

targ_wormhole = noone;

w_entrance.R = wormhole_radius;
w_exit.R = wormhole_radius;
