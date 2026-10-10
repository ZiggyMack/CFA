extends SceneTree
## Exercises the actual scene's save and menu integration without touching visit.json.
## Run headless without --smoke-test, which intentionally disables persistence.

const MAIN_SCENE = preload("res://scenes/main.tscn")
var _checks: int = 0
var _failures: int = 0
var _save_path: String = ""
var _scene: Node3D


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var test_dir: String = ProjectSettings.globalize_path("res://.local")
	DirAccess.make_dir_recursive_absolute(test_dir)
	var suffix: String = str(OS.get_process_id()) + "-" + str(Time.get_ticks_usec())
	_save_path = test_dir.path_join("test-visit-save-" + suffix + ".json")
	while FileAccess.file_exists(_save_path) or FileAccess.file_exists(_save_path + ".tmp"):
		_save_path += ".unique"
	_scene = MAIN_SCENE.instantiate()
	root.add_child(_scene)
	# _ready only displays the title. Redirect before any started/save action.
	_expect(not _scene.started, "The scene begins at its title without a started visit")
	_scene.save_path = _save_path
	_scene.set_process(false)
	_scene.player.set_physics_process(false)
	await process_frame
	await _test_start_and_repair()
	_test_save_overwrite_and_load()
	await _test_pause_and_reset()
	await _test_missing_and_corrupt()
	_scene.started = false
	_scene.queue_free()
	await process_frame
	if _failures == 0:
		for owned_path: String in [_save_path, _save_path + ".tmp"]:
			if FileAccess.file_exists(owned_path):
				_expect(DirAccess.remove_absolute(owned_path) == OK, "Remove only this run's temporary save: " + owned_path)
	if _failures == 0:
		print("Visit integration checks passed: %d; temporary saves cleaned." % _checks)
	else:
		push_error("Visit integration checks failed: %d of %d. Test artifact: %s" % [_failures, _checks, _save_path])
	quit(0 if _failures == 0 else 1)


func _test_start_and_repair() -> void:
	_scene.player.position = Vector3(4.0, 0.4, -3.0)
	_scene.player.rotation.y = 1.2
	_scene.player.camera.rotation.x = -0.4
	_scene._choose("@new")
	await process_frame
	_expect(_scene.started and not _scene.modal, "Choosing a new visit starts the world and closes the title")
	_expect(_scene.player.position.is_equal_approx(_home_position()), "A new visit resets the player to the entrance")
	_expect(is_zero_approx(_scene.player.rotation.y) and is_zero_approx(_scene.player.camera.rotation.x), "A new visit resets look direction")
	_expect(FileAccess.file_exists(_save_path), "A new visit writes the isolated save")
	for action: String in ["equip_coupler", "take_regulator", "hold_coupler", "install_regulator"]:
		_scene._choose(action)
		await process_frame
	_expect(_scene.story.water_restored and _scene.story.settlement_phase == "hauling", "Scene choices repair the water without silently moving the crew")
	_scene.player.position = Vector3(3.0, 0.2, -10.0)
	_scene._choose("return_to_courtyard")
	await process_frame
	_expect(_scene.story.return_seen and _scene.story.settlement_phase == "crossing", "The scene's return action advances the crew's consequence")
	_expect(_scene.player.position.is_equal_approx(_home_position()), "The return action brings the player back to the courtyard")
	_expect(_scene.modal and _scene.current_dialog.get("title") == "Hands for the crossing", "The return explains its consequence before the visitor continues")


func _test_save_overwrite_and_load() -> void:
	_scene.player.position = Vector3(-3.1, 0.22, -8.4)
	_scene.player.rotation.y = 1.234
	_scene.player.camera.rotation.x = -0.36
	_scene.sound_enabled = false
	_scene._save_visit(false)
	var first: Dictionary = _read_save()
	_expect(_saved_position(first).is_equal_approx(_scene.player.position), "A save contains the actual player position")
	_expect(is_equal_approx(float(first.get("yaw", 0.0)), 1.234) and is_equal_approx(float(first.get("pitch", 0.0)), -0.36), "A save contains the actual look angles")
	_expect(_same_json(first.get("story", {}), _scene.story.snapshot()), "A save contains the repaired story")
	var wanted_position: Vector3 = Vector3(2.5, 0.31, -3.2)
	var wanted_yaw: float = -0.72
	var wanted_pitch: float = 0.24
	_scene.player.position = wanted_position
	_scene.player.rotation.y = wanted_yaw
	_scene.player.camera.rotation.x = wanted_pitch
	_scene.sound_enabled = true
	_scene._save_visit(false)
	var wanted: Dictionary = _read_save()
	_expect(_saved_position(wanted).is_equal_approx(wanted_position), "A second save replaces an existing file on Windows")
	_expect(not FileAccess.file_exists(_save_path + ".tmp"), "Successful replacement consumes the temporary file")
	# Change live progress without requesting an autosave, then exercise loading
	# during an already started visit. Restoring a signal-driven state must not
	# overwrite the save with the pre-load player position.
	_scene.started = false
	_scene.story.reset()
	_scene.player.position = Vector3(7.0, 0.6, 5.0)
	_scene.player.rotation.y = 2.0
	_scene.player.camera.rotation.x = -0.8
	_scene.sound_enabled = false
	_scene.started = true
	_expect(_scene._load_visit(), "An existing valid visit loads")
	_expect(_same_json(_scene.story.snapshot(), wanted["story"]), "Loading restores the complete story")
	_expect(_scene.player.position.is_equal_approx(wanted_position), "Loading restores the player position")
	_expect(is_equal_approx(_scene.player.rotation.y, wanted_yaw) and is_equal_approx(_scene.player.camera.rotation.x, wanted_pitch), "Loading restores both look angles")
	_expect(_scene.sound_enabled, "Loading restores the sound preference")
	_expect(_read_save() == wanted, "Loading during a started visit does not overwrite the save with pre-load values")
	_scene.player.position = Vector3(-5.0, 0.45, 4.0)
	_expect(_scene._load_visit(), "The same saved visit can be loaded a second time")
	_expect(_scene.player.position.is_equal_approx(wanted_position), "A second load restores the same saved position")
	_expect(_scene.sound_enabled, "A second load preserves the original saved sound preference")


func _test_pause_and_reset() -> void:
	var before: Dictionary = _scene.story.snapshot()
	var position_before: Vector3 = _scene.player.position
	var file_before: String = FileAccess.get_file_as_string(_save_path)
	_scene._show_pause()
	await process_frame
	_expect(_scene.modal and not _scene.player.enabled, "Pause opens a modal and freezes player control")
	_scene._choose("@reset_confirm")
	await process_frame
	_expect(_scene.current_dialog.get("title") == "Begin again?", "Reset first presents a confirmation")
	_expect(_scene.story.snapshot() == before and _scene.player.position.is_equal_approx(position_before), "Opening reset confirmation does not reset progress or position")
	_expect(FileAccess.get_file_as_string(_save_path) == file_before, "Opening reset confirmation does not replace the save")
	var cancel: Button = _find_button("Keep this visit")
	_expect(cancel != null, "Reset confirmation offers a keep-visit button")
	if cancel != null:
		cancel.pressed.emit()
	await process_frame
	_expect(not _scene.modal and _scene.player.enabled, "The keep-visit button returns to play")
	_expect(_scene.story.snapshot() == before and FileAccess.get_file_as_string(_save_path) == file_before, "Cancel keeps progress and its saved file")
	_scene._show_pause()
	await process_frame
	_scene._choose("@reset_confirm")
	await process_frame
	var escape := InputEventAction.new()
	escape.action = "pause_visit"
	escape.pressed = true
	_scene._unhandled_input(escape)
	_expect(not _scene.modal and _scene.story.snapshot() == before, "Escape backs out of confirmation without resetting")
	_scene._choose("reset_chapter")
	await process_frame
	_expect(_scene.current_dialog.get("title") == "Begin again?" and _scene.story.snapshot() == before, "The chapter-ending reset choice also uses confirmation")
	_scene._choose("@new")
	await process_frame
	_expect(not _scene.story.water_restored and not _scene.story.return_seen and not _scene.story.ending_seen, "Confirming a new visit resets the chapter")
	_expect(_scene.player.position.is_equal_approx(_home_position()), "Confirming a new visit resets the player")
	_expect(_same_json(_read_save().get("story", {}), _scene.story.snapshot()), "Confirmed reset replaces the saved story")


func _test_missing_and_corrupt() -> void:
	_scene._choose("equip_echo")
	await process_frame
	_scene._choose("record_lever")
	await process_frame
	var before: Dictionary = _scene.story.snapshot()
	var position_before: Vector3 = Vector3(1.5, 0.2, -2.0)
	_scene.player.position = position_before
	if FileAccess.file_exists(_save_path):
		_expect(DirAccess.remove_absolute(_save_path) == OK, "Remove this run's save to exercise the missing-file case")
	_expect(not _scene._load_visit(), "A missing save returns false")
	_expect(_scene.story.snapshot() == before and _scene.player.position.is_equal_approx(position_before), "A missing save preserves current progress and position")
	_expect(not FileAccess.file_exists(_save_path), "A failed missing-file load does not create a save")
	for corrupt_text: String in ["{ this is not JSON", "{\"version\":1}", "{\"version\":2,\"story\":{}}", "{\"version\":1,\"story\":{\"water_restored\":\"true\"}}"]:
		_write_test_save(corrupt_text)
		_expect(not _scene._load_visit(), "A corrupt or incomplete save returns false")
		_expect(_scene.story.snapshot() == before and _scene.player.position.is_equal_approx(position_before), "A corrupt save leaves current progress and position untouched")
		_expect(FileAccess.get_file_as_string(_save_path) == corrupt_text, "A rejected corrupt save remains unchanged")


func _home_position() -> Vector3:
	return _scene.player.home + Vector3(0.0, 0.12, 0.0)


func _find_button(text: String) -> Button:
	for child: Node in _scene.panel_body.get_children():
		if child is Button and child.text == text:
			return child
	return null


func _read_save() -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(_save_path))
	return parsed if parsed is Dictionary else {}


func _same_json(first: Variant, second: Variant) -> bool:
	# JSON parses all numeric values as floats; normalize both operands before
	# comparing deeply, including integer save-version fields from live state.
	return JSON.parse_string(JSON.stringify(first)) == JSON.parse_string(JSON.stringify(second))


func _saved_position(data: Dictionary) -> Vector3:
	var values: Array = data.get("player", [INF, INF, INF])
	return Vector3(float(values[0]), float(values[1]), float(values[2]))


func _write_test_save(text: String) -> void:
	var file := FileAccess.open(_save_path, FileAccess.WRITE)
	_expect(file != null, "Write isolated corrupt-save fixture")
	if file != null:
		file.store_string(text)
		file.close()


func _expect(condition: bool, description: String) -> void:
	_checks += 1
	if not condition:
		_failures += 1
		push_error(description)
