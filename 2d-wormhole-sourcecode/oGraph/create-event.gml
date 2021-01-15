/// @description graph object plots the wormhole curve and shows the player position on the curve

r_max = 648;//648; // must be greater than wormhole radius
gWidth = 600;
gHeight = 200;

x = room_width/2 - gWidth/3;
y = 32 + gHeight/2;

axes_col = c_white;
curve_col = c_white;
dot_col = c_red;
dot_radius = 4;

// get a set of points for the sqrt curve
siz = 1500;
pts[siz] = {};

b = oController.wormhole_bore;
R = oController.wormhole_radius;

// get set of points for radius ranging from wormhole_radius to wormhole_bore
// first half is positive down, second half is negative continuing down finishing at -1
for (var i = 0; i < siz/2; i++) {
	var radiusPoint = R-((R-b)*2*i/siz);
	pts[i] = new Vector2(radiusPoint, get_z(radiusPoint, R, b));
	pts[siz - 1 - i] = new Vector2(radiusPoint, -get_z(radiusPoint, R, b));
}
