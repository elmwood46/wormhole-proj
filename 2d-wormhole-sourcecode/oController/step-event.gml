/// @description do wormhole
r_entrance = point_distance(player.x, player.y, w_entrance.x, w_entrance.y);
r_exit = point_distance(player.x, player.y, w_exit.x, w_exit.y);

// find closest wormhole
if (r_entrance <= r_exit) {
	targ_wormhole = w_entrance;
	r = r_entrance;
} else {
	targ_wormhole = w_exit;
	r = r_exit;
}



//make player wrap around
if (player.x < 0) 
	player.x += room_width;
if (player.x > room_width)
	player.x -= room_width;
if (player.y < 0)
	player.y += room_height;
if (player.y > room_height) 
	player.y -= room_height;
	
//make player z tied to horizontal position
// when player not inside wormhole

	

if (r > wormhole_radius) {
	player.image_xscale = 1;
	player.image_yscale = 1;
	psign = (player.x<=room_width/2) ? -1 : 1;
	player.z = psign;
} else if (r <= wormhole_radius) {
	var savdir = point_direction(player.x, player.y, targ_wormhole.x, targ_wormhole.y);
	
	// change player image scale
	var factor = abs(player.z);
	player.image_angle = savdir + 180;
	player.image_xscale = factor;

	draw_set_colour(c_aqua);
	
	if (r < wormhole_bore) {
		r = wormhole_bore;
		if (targ_wormhole == w_entrance) {
			targ_wormhole = w_exit;
		}
		else {
			targ_wormhole = w_entrance;
		}
		psign*=-1;
		
		player.x = targ_wormhole.x + lengthdir_x(wormhole_bore+2, savdir);
		player.y = targ_wormhole.y - lengthdir_y(wormhole_bore+2, savdir);
		// magic +2 so that player doesn't immediately walk backwards
	}
	// make player z change when enter wormhole
	player.z = psign * get_z(r, wormhole_radius, wormhole_bore);
}

// check for player changing the sizes
	var str_r = "wormhole_radius: "+string(wormhole_radius);
	var str_b = "bore_radius: "+string(wormhole_bore);
	var changed_size = false;
if (mouse_check_button_pressed(mb_left)) {
	if (mouse_x >= oGraph.x - 4 - string_width(str_r) and mouse_x <= oGraph.x -4) {
		if (mouse_y >= oGraph.y-2 and mouse_y <= oGraph.y +8) {
			var prevRadius = oController.wormhole_radius;
			oController.wormhole_radius = get_integer("Choose new wormhole radius: ", oController.wormhole_radius);
			if (oController.wormhole_radius <= oController.wormhole_bore) {
				show_message("Choose a radius that is larger than the bore!");
				oController.wormhole_radius = prevRadius;
			} else {
				changed_size = true;
			}
		}
	}
	 
	if (mouse_x >= oGraph.x - 4 - string_width(str_b) and mouse_x <= oGraph.x -4) { 
		if (mouse_y >= oGraph.y+16 and mouse_y <= oGraph.y + 24) {
			var prevBore =  oController.wormhole_bore;
			oController.wormhole_bore = get_integer("Choose new wormhole bore radius: ", oController.wormhole_bore);
			
			if (oController.wormhole_bore >= oController.wormhole_radius) {
				show_message("Choose a bore that is smaller than the radius!");
				oController.wormhole_bore = prevBore;
			} else {
				changed_size = true;
			}
		}
	}
	
	if (changed_size) {
		with(oController) {
			w_entrance.R = wormhole_radius;
			w_exit.R = wormhole_radius;
		}

		instance_destroy(oGraph);
		instance_create_layer(0, 0, layer, oGraph);
		changed_size = false;
	}

}
