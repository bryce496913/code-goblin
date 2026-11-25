extends Node2D

const FLOOR := Rect2(88, 114, 624, 282)
const SPEED := 180.0
const REACH := 48.0
const SCRAP := Vector2(225, 280)
const CUSTOMER := Vector2(400, 280)
const BENCH := Vector2(575, 280)
const PAPER := Color("#f0dfbb")
const MUTED := Color("#b4b8a8")
const GOLD := Color("#edb65b")
const MINT := Color("#9bd5ad")

enum Repair { WAITING, ACCEPTED, COMPLETE }

var repair := Repair.WAITING
var has_scrap := false
var goblin := Vector2(120, 280)
var facing := 1.0
var message := "Pip has been waiting at the counter."


func _physics_process(delta: float) -> void:
	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var keyboard := Vector2(
		float(Input.is_physical_key_pressed(KEY_D)) - float(Input.is_physical_key_pressed(KEY_A)),
		float(Input.is_physical_key_pressed(KEY_S)) - float(Input.is_physical_key_pressed(KEY_W))
	)
	if keyboard != Vector2.ZERO:
		direction = keyboard.normalized()
	var room := FLOOR.grow(-20)
	goblin = (goblin + direction * SPEED * delta).clamp(room.position, room.end)
	if direction.x != 0:
		facing = signf(direction.x)
	queue_redraw()


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode == KEY_E or event.is_action_pressed("ui_accept"):
			interact()
			get_viewport().set_input_as_handled()


func interact() -> void:
	if goblin.distance_to(SCRAP) <= REACH and not has_scrap and repair != Repair.COMPLETE:
		has_scrap = true
		message = "Picked up one piece of scrap."
	elif goblin.distance_to(CUSTOMER) <= REACH:
		match repair:
			Repair.WAITING:
				repair = Repair.ACCEPTED
				message = "Pip left a broken lantern at your bench. It needs one piece of scrap."
			Repair.ACCEPTED:
				message = "Pip: The tunnel gets dark. That lantern is my only light."
			Repair.COMPLETE:
				message = "Pip: It works! Next stop, somewhere with a roof."
	elif goblin.distance_to(BENCH) <= REACH:
		if repair == Repair.WAITING:
			message = "Talk to Pip before starting a repair."
		elif repair == Repair.COMPLETE:
			message = "The lantern is fixed. The bench can rest for a minute."
		elif not has_scrap:
			message = "You need one piece of scrap. Check the salvage tray."
		else:
			has_scrap = false
			repair = Repair.COMPLETE
			message = "Repair complete! Pip's lantern is shining again."


func _draw() -> void:
	draw_rect(Rect2(0, 0, 800, 520), Color("#141d20"))
	draw_rect(FLOOR.grow(7), Color("#65766b"))
	draw_rect(FLOOR, Color("#303e3d"))
	for x in range(96, 712, 32):
		draw_line(Vector2(x, 124), Vector2(x, 388), Color("#394846"))
	for y in range(124, 396, 32):
		draw_line(Vector2(96, y), Vector2(704, y), Color("#394846"))
	draw_rect(Rect2(96, 122, 608, 54), Color("#273130"))
	draw_rect(Rect2(96, 180, 608, 4), GOLD)
	draw_rect(Rect2(96, 378, 608, 10), Color("#495953"))
	label(Vector2(84, 48), "Goblin: Last Stop to Montauk", PAPER, 29)
	label(Vector2(85, 79), "REPAIR SHOP  /  ONE LANTERN, ONE PIECE OF SCRAP", MUTED, 15)
	label(Vector2(112, 155), "SUBWAY PLATFORM B", MUTED, 15)
	label(Vector2(553, 155), "WORK LIGHT ON", MINT, 14)

	station(SCRAP, "SALVAGE", GOLD)
	station(CUSTOMER, "PIP", MINT)
	station(BENCH, "REPAIR BENCH", GOLD)
	if not has_scrap and repair != Repair.COMPLETE:
		draw_colored_polygon(PackedVector2Array([SCRAP + Vector2(-11, -2),
			SCRAP + Vector2(2, -17), SCRAP + Vector2(12, -2), SCRAP + Vector2(4, 8)]), GOLD)
	draw_circle(CUSTOMER + Vector2(-10, -17), 6, Color("#c08f85"))
	draw_circle(CUSTOMER + Vector2(10, -17), 6, Color("#c08f85"))
	draw_circle(CUSTOMER + Vector2(0, -4), 15, Color("#b4999f"))
	draw_circle(CUSTOMER + Vector2(-5, -6), 2, Color("#252930"))
	draw_circle(CUSTOMER + Vector2(5, -6), 2, Color("#252930"))
	draw_rect(Rect2(BENCH + Vector2(-19, -11), Vector2(38, 18)), Color("#725845"))
	draw_rect(Rect2(BENCH + Vector2(-6, -23), Vector2(12, 14)),
		MINT if repair == Repair.COMPLETE else Color("#6f756a"))

	draw_set_transform(goblin, 0.0, Vector2(facing, 1))
	draw_ellipse_shadow()
	draw_circle(Vector2(-10, -12), 6, Color("#a5ada7"))
	draw_circle(Vector2(9, -12), 6, Color("#a5ada7"))
	draw_circle(Vector2.ZERO, 15, Color("#b8c5b9"))
	draw_rect(Rect2(-13, -6, 25, 8), Color("#333a42"))
	draw_circle(Vector2(6, -2), 2, PAPER)
	draw_rect(Rect2(-10, 9, 20, 5), Color("#d37561"))
	draw_set_transform(Vector2.ZERO)

	var prompt := "Move with WASD or arrow keys. Press E near a station."
	if goblin.distance_to(SCRAP) <= REACH and not has_scrap and repair != Repair.COMPLETE:
		prompt = "E  Pick up scrap"
	elif goblin.distance_to(CUSTOMER) <= REACH:
		prompt = "E  Talk to Pip"
	elif goblin.distance_to(BENCH) <= REACH:
		prompt = "E  Use repair bench"
	label(Vector2(88, 428), message, MINT if repair == Repair.COMPLETE else PAPER, 19)
	label(Vector2(88, 464), prompt, MUTED, 16)
	label(Vector2(88, 493), "SCRAP: %d     LANTERN: %s" % [int(has_scrap),
		["WAITING", "IN REPAIR", "FIXED"][repair]], GOLD, 14)


func draw_ellipse_shadow() -> void:
	draw_circle(Vector2(-11, 12), 8, Color("#212b2b"))
	draw_circle(Vector2(0, 12), 10, Color("#212b2b"))
	draw_circle(Vector2(11, 12), 8, Color("#212b2b"))


func station(position: Vector2, name_text: String, color: Color) -> void:
	draw_rect(Rect2(position - Vector2(31, 30), Vector2(62, 57)), Color("#253231"))
	if goblin.distance_to(position) <= REACH:
		draw_arc(position, 30, 0, TAU, 24, color, 2, true)
	var width := ThemeDB.fallback_font.get_string_size(name_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 14).x
	label(position + Vector2(-width / 2, 50), name_text, color, 14)


func label(position: Vector2, value: String, color: Color, size: int) -> void:
	draw_string(ThemeDB.fallback_font, position, value, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)
