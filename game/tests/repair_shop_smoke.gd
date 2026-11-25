extends SceneTree

var failed := false


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	var shop = load("res://scenes/repair_shop.tscn").instantiate()
	root.add_child(shop)
	await physics_frame

	await walk_right(0.58)
	await press_interact()
	check(shop.has_scrap, "Goblin picked up scrap")

	await walk_right(0.97)
	await press_interact()
	check(shop.repair == shop.Repair.ACCEPTED, "Pip assigned the lantern repair")

	await walk_right(0.97)
	await press_interact()
	check(shop.repair == shop.Repair.COMPLETE, "The bench completed the repair")
	check(not shop.has_scrap, "The repair consumed one scrap")
	check(shop.message.begins_with("Repair complete!"), "The player received completion feedback")
	await press_interact()
	check(shop.repair == shop.Repair.COMPLETE, "Repeating the interaction preserves completion")
	quit(int(failed))


func walk_right(seconds: float) -> void:
	Input.action_press("ui_right")
	await create_timer(seconds, true, true).timeout
	Input.action_release("ui_right")
	await physics_frame


func press_interact() -> void:
	var key := InputEventKey.new()
	key.physical_keycode = KEY_E
	key.keycode = KEY_E
	key.pressed = true
	Input.parse_input_event(key)
	Input.flush_buffered_events()
	await process_frame
	var release := key.duplicate() as InputEventKey
	release.pressed = false
	Input.parse_input_event(release)
	Input.flush_buffered_events()


func check(condition: bool, description: String) -> void:
	if condition:
		print("PASS: " + description)
	else:
		failed = true
		push_error(description)
