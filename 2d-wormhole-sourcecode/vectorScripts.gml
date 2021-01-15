function Vector2(_x, _y) constructor {
	x = _x;
	y = _y;
	static normalize = function() {
		len = hypot(x, y);
		x = x/len;
		y = y/len;
	}
}

function Vector3(_x, _y, _z) constructor {
	x = _x;
	y = _y;
	z = _z;
	static normalize = function() {
		len = sqrt(x*x + y*y + z*z);
		x /= len;
		y /= len;
		z /= len;
	}
}
		

function hypot(_x, _y) {
	return sqrt(_x*_x + _y*_y);
}

function vadd(_v1, _v2) {
	return new Vector2(_v1.x+_v2.x, _v1.y+_v2.y);
}

function vsub(_v1, _v2) {
	return new Vector2(_v1.x-_v2.x, _v1.y-_v2.y);
}

function vdist(_v1, _v2) {
	return hypot(_v2.x-_v1.x, _v2.y-_v1.y);
}

function vlen(_v1) {
	return hypot(_v1.x, _v1.y);
}

function vdot(_v1, _v2) {
	return _v1.x*_v2.x + _v1.y*_v2.y;
}

function v3dot(_v1, _v2) {
	return _v1.x*_v2.x + _v1.y*_v2.y + _v1.z*_v2.z;
}
