/// @description fires every frame, 60fps
// draw axes
draw_set_colour(axes_col);
draw_line(x, y, x+gWidth, y);
draw_line(x, y-gHeight/2, x, y+gHeight/2);
draw_text(x - 4, y-gHeight/2-20, "Z");
draw_text(x + gWidth + 8, y - 7, "R");
var str_r = "wormhole_radius: "+string(R);
var str_b = "bore_radius: "+string(b);
draw_text(x - 4 - string_width(str_r), y, str_r);
draw_text(x - 4 - string_width(str_b), y+16, str_b);

// draw vertical axis scales
draw_line(x -4, y + gHeight/2 * pts[0].y,
			x + 4, y + gHeight/2 * pts[0].y);
draw_text(x-24, y + gHeight/2 * pts[0].y - 4, "-1");
draw_line(x + 4, y + gHeight/2 * pts[siz-1].y,
			x + -4, y + gHeight/2 * pts[siz-1].y);
draw_text(x-20, y + gHeight/2 * pts[siz-1].y - 5, "1");
			
// draw horizontal axis scales
draw_line(x + gWidth*pts[0].x/r_max, y+4, x + gWidth*pts[0].x/r_max, y-4);
draw_text(x + gWidth*pts[0].x/r_max - 4, y+8, string(R));

// draw the curve
draw_set_colour(curve_col);
for (var i = 1; i < siz; i++) {
	var xx = x + gWidth * pts[i-1].x/r_max;
	var yy = y + gHeight/2 * pts[i-1].y;
	var xx1 = x + gWidth * pts[i].x/r_max;
	var yy1 = y + gHeight/2 * pts[i].y;
	draw_line(xx, yy, xx1, yy1);
}

// upper line
draw_line(x + gWidth* pts[0].x/r_max, y + gHeight/2 * pts[0].y,
			x + gWidth, y + gHeight/2 * pts[0].y);
// lower line
draw_line(x + gWidth* pts[0].x/r_max, y + gHeight/2 * pts[siz-1].y,
			x + gWidth, y + gHeight/2 * pts[siz-1].y);

// draw the player point
draw_set_colour(dot_col);
pt = new Vector2(oController.r, oPlayer.z);
var xx = x + gWidth * pt.x/r_max;
var yy = y - gHeight/2 * oPlayer.z;
draw_circle(xx, yy, dot_radius, false);
draw_text(xx - 32, yy - 20, "("+string(pt.x)+","+string(pt.y)+")");


