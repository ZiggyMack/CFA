extends SceneTree
## Exercise draft menus and optional save metadata using only a run-owned save.

const MAIN_SCENE = preload("res://scenes/main.tscn")
var _checks: int = 0
var _failures: int = 0
var _scene: Node3D
var _save_path: String

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var directory: String = ProjectSettings.globalize_path("res://.local")
	DirAccess.make_dir_recursive_absolute(directory)
	_save_path = directory.path_join("test-draft-menu-%s-%s.json" % [OS.get_process_id(), Time.get_ticks_usec()])
	while FileAccess.file_exists(_save_path):
		_save_path += ".unique"
	_scene = MAIN_SCENE.instantiate()
	root.add_child(_scene)
	_scene.save_path = _save_path
	_scene.set_process(false)
	_scene.player.set_physics_process(false)
	await process_frame
	_scene._choose("@new")
	_scene._choose("equip_echo")
	_scene._choose("record_lever")
	_scene._choose("take_regulator")
	_scene._choose("preserve_record")
	_scene.player.position = Vector3(2.4, 0.3, -4.0)
	_scene.player.rotation.y = 0.7
	_scene.player.camera.rotation.x = -0.25
	var before: Dictionary = _scene.story.snapshot()
	var position: Vector3 = _scene.player.position
	var original_text: String = _scene.story.describe("resident_mara").text
	_scene._show_pause()
	_expect(_has_action("@drafts"), "Pause menu offers the story workshop")
	_scene._choose("@drafts")
	_expect(_scene.modal and _scene.player.enabled == false, "The workshop pauses movement")
	_expect(_has_action("@draft_curiosity") and not _has_action("@draft_original"), "Original draft offers the alternative only")
	_scene._choose("@draft_curiosity")
	await process_frame
	_expect(_scene.story.draft_id == "curiosity", "Menu switches to the second draft")
	_expect(_scene.story.describe("resident_mara").text != original_text, "The resident now speaks the revised text")
	_expect(_scene.story.snapshot() == before, "Changing prose preserves the entire puzzle/discovery state")
	_expect(_scene.player.position == position, "Changing prose preserves the player's position")
	_expect(is_equal_approx(_scene.player.rotation.y, 0.7) and is_equal_approx(_scene.player.camera.rotation.x, -0.25), "Changing prose preserves look direction")
	_expect(_has_action("@draft_original") and not _has_action("@draft_curiosity"), "Selected draft is reflected in menu choices")
	_expect(_scene.current_dialog.text.contains("What we leave for others"), "Menu identifies the current telling")
	var saved: Dictionary = _read_save()
	_expect(saved.get("version") == 1 and saved.get("draft") == "curiosity", "Selection saves as optional metadata in visit version 1")
	_expect(saved.get("story") == JSON.parse_string(JSON.stringify(before)), "Selection saves the existing story progress")
	_scene.story.select_draft("original")
	_expect(_scene._load_visit(), "Saved visit with a draft restores")
	_expect(_scene.story.draft_id == "curiosity", "Loading restores the selected draft")
	_expect(_scene.story.snapshot() == before and _scene.player.position.is_equal_approx(position), "Loading keeps the saved progress and position")
	var legacy: Dictionary = saved.duplicate(true)
	legacy.erase("draft")
	_write_save(legacy)
	_expect(_scene._load_visit(), "Old version-1 visit without draft metadata restores")
	_expect(_scene.story.draft_id == "original", "Old visits use the original writing")
	_expect(_scene.story.snapshot() == before, "Old-visit compatibility preserves progress")
	for invalid: Variant in ["missing-draft", "../../other-file", 2, {}, null]:
		var invalid_save: Dictionary = saved.duplicate(true)
		invalid_save["draft"] = invalid
		_write_save(invalid_save)
		_scene.story.select_draft("curiosity")
		_expect(_scene._load_visit(), "Unknown optional draft metadata does not lose a valid visit")
		_expect(_scene.story.draft_id == "original" and _scene.story.snapshot() == before, "Invalid draft falls back to original without changing progress")
	_scene._choose("@draft_curiosity")
	_scene._choose("@pause")
	_expect(_has_action("@drafts"), "Workshop can return to the pause menu")
	_scene._close_dialog()
	_expect(not _scene.modal and _scene.player.enabled, "The visitor can resume moving after comparison")
	_scene._choose("hold_echo")
	_scene._choose("install_regulator")
	_scene._choose("return_to_courtyard")
	_expect(_scene.story.water_restored and _scene.story.settlement_phase == "crossing", "The original puzzle still completes after changing drafts")
	_expect(_scene.current_dialog.text.contains("finding places along the rope"), "Return consequence uses the selected draft")
	_scene._choose("@draft_original")
	_expect(_scene.story.water_restored and _scene.story.settlement_phase == "crossing", "Switching back keeps the completed repair and consequence")
	_expect(_scene.story.describe("resident_mara").text.contains("both hands"), "Switching back restores the original resident writing")
	_scene.started = false
	_scene.queue_free()
	await process_frame
	if _failures == 0:
		for path: String in [_save_path, _save_path + ".tmp"]:
			if FileAccess.file_exists(path):
				_expect(DirAccess.remove_absolute(path) == OK, "Remove this test's own temporary save")
	if _failures == 0:
		print("Draft menu checks passed: %d; temporary saves cleaned." % _checks)
	else:
		push_error("Draft menu checks failed: %d of %d. Test artifact: %s" % [_failures, _checks, _save_path])
	quit(0 if _failures == 0 else 1)

func _has_action(action: String) -> bool:
	for choice: Dictionary in _scene.current_dialog.get("choices", []):
		if choice.get("action") == action:
			return true
	return false

func _read_save() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(_save_path))

func _write_save(data: Dictionary) -> void:
	var file := FileAccess.open(_save_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(data))
	file.close()

func _expect(condition: bool, message: String) -> void:
	_checks += 1
	if not condition:
		_failures += 1
		push_error("FAIL: " + message)
