/// @description move

up = keyboard_check(ord("W"));
left = keyboard_check(ord("A"));
right = keyboard_check(ord("D"));
down = keyboard_check(ord("S"));

moveHorz = (right - left);
moveDown = (down - up);

if (abs(moveHorz) || abs(moveDown))
	dir = point_direction(0, 0, moveHorz, moveDown);

if (keyboard_check(vk_control)) {
	x += moveHorz;
	y += moveDown;
} else {
	x += moveHorz*spd;
	y += moveDown*spd;
}
