///@function get_z
///@param r - the distance from centre of wormhole
///@param R - the radius of the wormhole
///@param b - the bore radius of the wormhole
///@description this function simply takes the dimensions of the wormhole and uses
/// them to map z as a function of r continuously in a semiellipse
function get_z(r, R, b){
	return sqrt(abs(1-(power(r-R, 2)/power(R-b, 2))));
}

function get_tangent(r, R, b) {
	return (r-R)*(power(r-R, 2)-power(R-b, 2))/(power(R-b,4)*power(abs(power((r-R)/(R-b), 2) - 1), 1.5));
}