extends SceneTree
## Run: godot --headless --path games/observatory --script res://tests/test_story.gd

const StoryState = preload("res://scripts/story_state.gd")
var _failures: int = 0
var _checks: int = 0


func _initialize() -> void:
	_test_inspection_is_read_only()
	_test_echo_solution()
	_test_coupler_solution_and_tool_changes()
	_test_deferral_and_late_repair()
	_test_save_resume()
	_test_invalid_saves_are_atomic()
	if _failures == 0:
		print("Story checks passed: %d" % _checks)
	else:
		push_error("Story checks failed: %d of %d" % [_failures, _checks])
	quit(0 if _failures == 0 else 1)


func _test_inspection_is_read_only() -> void:
	var state = StoryState.new()
	var before: Dictionary = state.snapshot()
	for id: String in ["resident_mara", "resident_ivo", "pump", "bench", "lever", "bypass", "regulator", "archive", "return_marker", "ending", "plaque"]:
		var dialog: Dictionary = state.describe(id)
		_expect(typeof(dialog.get("title")) == TYPE_STRING and not dialog["title"].is_empty(), "A hotspot has a title: " + id)
		_expect(typeof(dialog.get("text")) == TYPE_STRING and not dialog["text"].contains("unavailable"), "A hotspot has loaded text: " + id)
		_expect(typeof(dialog.get("choices")) == TYPE_ARRAY, "A hotspot has a choice list: " + id)
		for option: Dictionary in dialog["choices"]:
			_expect(typeof(option.get("label")) == TYPE_STRING and typeof(option.get("action")) == TYPE_STRING, "Choice contract: " + id)
	state.journal()
	state.objective()
	state.choose("continue_visit")
	state.choose("unknown_action")
	_expect(state.snapshot() == before, "Inspection, closing, and an unknown action never advance the chapter")
	state.choose("finish_chapter")
	_expect(not state.ending_seen, "Cannot finish without explicitly returning")
	state.choose("preserve_record")
	_expect(state.journal().contains("TEST 14"), "An explicit archive action preserves the correction in the journal")
	_expect(not state.water_restored and not state.return_seen, "Optional archive reading does not repair or advance the return")


func _test_echo_solution() -> void:
	var state = StoryState.new()
	state.choose("equip_echo")
	state.choose("hold_echo")
	_expect(not state.snapshot()["bypass_held"], "The echo cannot hold the bypass without recording the lever")
	state.choose("record_lever")
	state.choose("hold_echo")
	_expect(state.snapshot()["bypass_held"], "A recorded echo holds the bypass")
	state.choose("install_regulator")
	_expect(not state.water_restored, "A bypass hold alone cannot replace a missing spare")
	state.describe("archive")
	state.describe("resident_ivo")
	_expect(state.snapshot()["bypass_held"], "Reading and wandering do not expire an echo hold")
	state.choose("take_regulator")
	state.choose("install_regulator")
	_expect(state.water_restored, "The echo solution restores water")
	_expect(not state.snapshot()["bypass_held"], "Normal service releases the bypass hold")
	_expect(state.settlement_phase == "hauling" and not state.return_seen, "Repair alone does not move the residents")
	_expect(not state.describe("resident_ivo")["title"].contains("shared lift"), "Crossing dialogue waits for the return")
	state.choose("return_to_courtyard")
	_expect(state.settlement_phase == "crossing", "An explicit repaired return regroups the residents")
	state.choose("finish_chapter")
	_expect(state.ending_seen, "The repaired branch can end without reading the archive")


func _test_coupler_solution_and_tool_changes() -> void:
	var state = StoryState.new()
	state.choose("take_regulator")
	state.choose("install_regulator")
	_expect(not state.water_restored, "The spare alone cannot be installed without a bypass hold")
	state.choose("equip_coupler")
	state.choose("hold_coupler")
	_expect(state.snapshot()["bypass_held"], "The coupler can hold directly through the inspection opening")
	_expect(not state.snapshot()["echo_recorded"], "The coupler needs no recording")
	state.choose("equip_echo")
	_expect(not state.snapshot()["bypass_held"], "Changing equipment releases the old tool's hold")
	state.choose("install_regulator")
	_expect(not state.water_restored, "A released hold cannot be used to install the regulator")
	state.choose("hold_coupler")
	_expect(not state.snapshot()["bypass_held"], "A tool action cannot operate an unequipped tool")
	state.choose("equip_coupler")
	state.choose("hold_coupler")
	state.choose("release_bypass")
	_expect(not state.snapshot()["bypass_held"], "An explicit release stops a hold")
	state.choose("hold_coupler")
	state.choose("install_regulator")
	_expect(state.water_restored, "The coupler solution restores water")


func _test_deferral_and_late_repair() -> void:
	var state = StoryState.new()
	state.describe("return_marker")
	_expect(not state.return_seen, "Inspecting the return marker does not trigger a scene change")
	state.choose("return_to_courtyard")
	_expect(state.return_seen and state.settlement_phase == "hauling", "An unrepaired return preserves water hauling")
	state.choose("finish_chapter")
	_expect(state.ending_seen, "Deferral can reach a complete ending")
	state.choose("continue_visit")
	state.choose("equip_coupler")
	_expect(state.objective().contains("bypass"), "Resuming work after a deferred ending restores practical repair guidance")
	state.choose("take_regulator")
	state.choose("hold_coupler")
	state.choose("install_regulator")
	_expect(state.water_restored and state.settlement_phase == "hauling", "A deferred ending does not prevent a later repair or silently regroup the crew")
	_expect(state.objective().contains("Return"), "A later repair points to the updated return")
	_expect(state.describe("ending")["title"] == "A change still to see", "The old ending waits for the new consequence to be seen")
	state.choose("return_to_courtyard")
	_expect(state.settlement_phase == "crossing", "A later repaired return replaces the earlier hauling state")
	_expect(state.describe("ending")["title"].contains("next thing"), "The ending reflects the later repaired visit")
	state.reset()
	_expect(state.snapshot() == StoryState.new().snapshot(), "Reset restores a new visit")


func _test_save_resume() -> void:
	var state = StoryState.new()
	state.choose("equip_echo")
	state.choose("record_lever")
	state.choose("hold_echo")
	state.choose("preserve_record")
	var saved_text: String = JSON.stringify(state.snapshot())
	var parsed: Variant = JSON.parse_string(saved_text)
	var restored = StoryState.new()
	_expect(restored.restore(parsed), "A JSON round trip restores a mid-puzzle save, including a numeric version parsed as float")
	_expect(restored.snapshot() == state.snapshot(), "All puzzle and archive state survives save/resume")
	restored.choose("take_regulator")
	restored.choose("install_regulator")
	_expect(restored.water_restored, "A resumed echo hold can complete the repair")
	restored.choose("return_to_courtyard")
	restored.choose("finish_chapter")
	var ended = StoryState.new()
	_expect(ended.restore(restored.snapshot()), "A completed chapter restores")
	_expect(ended.ending_seen and ended.settlement_phase == "crossing", "A restored ending retains its consequence")


func _test_invalid_saves_are_atomic() -> void:
	var state = StoryState.new()
	state.choose("preserve_record")
	var before: Dictionary = state.snapshot()
	var invalid: Array[Dictionary] = [{}, {"version": 1}]
	var edits: Array[Dictionary] = [
		{"version": 2},
		{"version": "1"},
		{"water_restored": "false"},
		{"water_restored": 0},
		{"tool": "unknown"},
		{"settlement_phase": "unknown"},
		{"settlement_phase": "crossing"},
		{"ending_seen": true},
		{"water_restored": true},
		{"bypass_held": true},
		{"tool": "echo", "bypass_held": true},
		{"echo_recorded": true},
		{"water_restored": true, "tool": "coupler", "regulator_collected": true, "bypass_held": true}
	]
	for edit: Dictionary in edits:
		var bad: Dictionary = before.duplicate(true)
		bad.merge(edit, true)
		invalid.append(bad)
	var missing: Dictionary = before.duplicate(true)
	missing.erase("archive_read")
	invalid.append(missing)
	for bad: Dictionary in invalid:
		_expect(not state.restore(bad), "Malformed or impossible save is rejected: " + str(bad))
		_expect(state.snapshot() == before, "A rejected save leaves the existing state untouched")


func _expect(condition: bool, description: String) -> void:
	_checks += 1
	if not condition:
		_failures += 1
		push_error(description)
