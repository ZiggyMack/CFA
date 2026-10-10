extends SceneTree
## Run: godot --headless --path games/observatory --script res://tests/test_story_drafts.gd

const StoryState = preload("res://scripts/story_state.gd")
const HOTSPOTS: Array[String] = ["resident_mara", "resident_ivo", "pump", "bench",
	"lever", "bypass", "regulator", "archive", "return_marker", "ending", "plaque"]
var _failures: int = 0
var _checks: int = 0
var _change_events: int = 0


func _initialize() -> void:
	_test_switch_preserves_visit()
	_test_both_drafts_and_tools()
	_test_deferral_and_late_repair()
	_test_rejected_drafts_are_atomic()
	_test_loaded_content_is_owned()
	if _failures == 0:
		print("Story draft checks passed: %d" % _checks)
	else:
		push_error("Story draft checks failed: %d of %d" % [_failures, _checks])
	quit(0 if _failures == 0 else 1)


func _test_switch_preserves_visit() -> void:
	var state = StoryState.new()
	_expect(state.draft_id == "original", "A new story keeps the original draft as its default")
	state.choose("equip_echo")
	state.choose("record_lever")
	state.choose("hold_echo")
	state.choose("take_regulator")
	state.choose("preserve_record")
	var before: Dictionary = state.snapshot()
	var original_dialog: Dictionary = state.describe("resident_mara")
	var original_journal: String = state.journal()
	state.changed.connect(_on_changed)
	_change_events = 0
	_expect(state.select_draft("curiosity"), "The bundled curiosity draft loads")
	_expect(state.draft_id == "curiosity", "The active draft identifies the selected writing")
	_expect(state.describe("resident_mara")["text"] != original_dialog["text"], "The alternative draft changes the resident's writing")
	_expect(state.snapshot() == before, "Switching mid-repair preserves the exact version-1 visit")
	_expect(state.describe("resident_mara")["choices"] == original_dialog["choices"], "A prose change keeps available actions unchanged")
	_expect(state.journal().contains(state.describe("archive")["text"]), "An already preserved archive copy displays the selected draft")
	_expect(_change_events == 0, "Selecting a draft does not emit a story-change event")
	_expect(state.select_draft("original"), "The original draft can be restored")
	_expect(state.describe("resident_mara") == original_dialog and state.journal() == original_journal, "Switching back restores the original writing and journal copy")
	_expect(state.snapshot() == before and _change_events == 0, "Comparing both drafts has no mechanical side effects")
	_expect(not before.has("draft") and before["version"] == 1, "Draft selection stays outside the existing story save schema")
	state.select_draft("curiosity")
	state.choose("install_regulator")
	_expect(state.water_restored, "The held echo still completes the repair after comparing drafts")
	var restored = StoryState.new()
	restored.select_draft("curiosity")
	_expect(restored.restore(before), "A pre-comparison version-1 snapshot restores under the selected draft")
	_expect(restored.draft_id == "curiosity" and restored.snapshot() == before, "Restoring mechanics preserves the chosen writing")
	restored.reset()
	_expect(restored.draft_id == "curiosity", "Beginning another visit retains the selected draft")
	_expect(restored.snapshot() == StoryState.new().snapshot(), "Reset still restores all original mechanical defaults")


func _test_both_drafts_and_tools() -> void:
	for draft: String in ["original", "curiosity"]:
		for equipment: String in ["echo", "coupler"]:
			var state = StoryState.new()
			_expect(state.select_draft(draft), "Playable draft is available: " + draft)
			_check_readable(state, draft + " arrival")
			state.choose("equip_" + equipment)
			state.choose("install_regulator")
			_expect(not state.water_restored, "Draft does not bypass repair prerequisites: " + draft + "/" + equipment)
			state.choose("take_regulator")
			if equipment == "echo":
				state.choose("record_lever")
			state.choose("hold_" + equipment)
			state.choose("install_regulator")
			_expect(state.water_restored and state.settlement_phase == "hauling", "Repair works and still awaits a return: " + draft + "/" + equipment)
			var before: Dictionary = state.snapshot()
			state.select_draft("curiosity" if draft == "original" else "original")
			_expect(state.snapshot() == before, "Comparing a repaired visit does not regroup the residents")
			state.select_draft(draft)
			state.choose("return_to_courtyard")
			_expect(state.settlement_phase == "crossing", "The explicit return reveals the repaired consequence: " + draft)
			_check_readable(state, draft + " repaired")
			state.choose("finish_chapter")
			_expect(state.ending_seen, "The chapter closes with either draft and tool: " + draft + "/" + equipment)


func _test_deferral_and_late_repair() -> void:
	for draft: String in ["original", "curiosity"]:
		var state = StoryState.new()
		state.select_draft(draft)
		state.choose("return_to_courtyard")
		_expect(state.return_seen and state.settlement_phase == "hauling", "Deferral preserves water hauling: " + draft)
		_check_readable(state, draft + " deferred")
		state.choose("finish_chapter")
		_expect(state.ending_seen and not state.water_restored, "Deferral reaches a complete ending: " + draft)
		var before: Dictionary = state.snapshot()
		state.select_draft("curiosity" if draft == "original" else "original")
		_expect(state.snapshot() == before, "Comparing a deferred ending preserves the open repair")
		state.choose("equip_coupler")
		state.choose("hold_coupler")
		state.choose("take_regulator")
		state.choose("install_regulator")
		_expect(state.water_restored and state.settlement_phase == "hauling", "A late repair remains possible after a draft switch")
		state.choose("return_to_courtyard")
		_expect(state.settlement_phase == "crossing", "The later return replaces the deferred consequence")


func _test_rejected_drafts_are_atomic() -> void:
	var state = StoryState.new()
	state.select_draft("curiosity")
	state.choose("equip_coupler")
	state.choose("hold_coupler")
	state.choose("preserve_record")
	var before: Dictionary = state.snapshot()
	var dialog_before: Dictionary = state.describe("resident_mara")
	var journal_before: String = state.journal()
	var valid: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(StoryState.CONTENT_PATH))
	var malformed := JSON.new()
	malformed.parse("{invalid")
	var invalid: Array = [null, [], "not a chapter", {}, malformed.data]
	var wrong_chapter: Dictionary = valid.duplicate(true)
	wrong_chapter["chapter_id"] = "some_other_chapter"
	invalid.append(wrong_chapter)
	var wrong_entries: Dictionary = valid.duplicate(true)
	wrong_entries["entries"] = []
	invalid.append(wrong_entries)
	var missing_entry: Dictionary = valid.duplicate(true)
	missing_entry["entries"].erase("ending_repaired")
	invalid.append(missing_entry)
	var renamed_entry: Dictionary = valid.duplicate(true)
	renamed_entry["entries"]["unknown_ending"] = renamed_entry["entries"]["ending_repaired"]
	renamed_entry["entries"].erase("ending_repaired")
	invalid.append(renamed_entry)
	var extra_entry: Dictionary = valid.duplicate(true)
	extra_entry["entries"]["unknown_entry"] = {"title": "Extra", "text": "Not part of this chapter."}
	invalid.append(extra_entry)
	var wrong_entry: Dictionary = valid.duplicate(true)
	wrong_entry["entries"]["ending_repaired"] = "not an entry"
	invalid.append(wrong_entry)
	for field: String in ["title", "text"]:
		for value: Variant in [null, 17, true, "", " \n\t", "x".repeat(StoryState.MAX_TEXT_LENGTH + 1)]:
			var bad_field: Dictionary = valid.duplicate(true)
			bad_field["entries"]["ending_repaired"][field] = value
			invalid.append(bad_field)
		var missing_field: Dictionary = valid.duplicate(true)
		missing_field["entries"]["ending_repaired"].erase(field)
		invalid.append(missing_field)
	var long_title: Dictionary = valid.duplicate(true)
	long_title["entries"]["ending_repaired"]["title"] = "x".repeat(StoryState.MAX_TITLE_LENGTH + 1)
	invalid.append(long_title)
	state.changed.connect(_on_changed)
	_change_events = 0
	for candidate: Variant in invalid:
		_expect(not state.select_draft_content("original", candidate), "Invalid or incomplete draft is rejected")
		_expect(state.draft_id == "curiosity" and state.describe("resident_mara") == dialog_before, "A rejected draft preserves active text and its ID")
		_expect(state.snapshot() == before and state.journal() == journal_before, "A rejected draft preserves the full visit and archive copy")
	_expect(not state.select_draft("unknown") and not state.select_draft_content("unknown", valid), "Unknown draft IDs cannot select files or in-memory content")
	_expect(state.snapshot() == before and state.draft_id == "curiosity" and _change_events == 0, "Rejected selections never emit story changes or partially apply content")


func _test_loaded_content_is_owned() -> void:
	var state = StoryState.new()
	var content: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(StoryState.CONTENT_PATH))
	_expect(state.select_draft_content("original", content), "A complete in-memory draft passes the same validation")
	var before: Dictionary = state.describe("resident_mara")
	content["entries"]["mara_arrival"]["text"] = "Changed after loading"
	content["entries"].clear()
	_expect(state.describe("resident_mara") == before, "Later caller edits cannot mutate already validated active content")


func _check_readable(state: RefCounted, phase: String) -> void:
	var before: Dictionary = state.snapshot()
	var all_readable: bool = true
	for hotspot: String in HOTSPOTS:
		var dialog: Dictionary = state.describe(hotspot)
		all_readable = all_readable and typeof(dialog.get("title")) == TYPE_STRING and not dialog["title"].is_empty()
		all_readable = all_readable and typeof(dialog.get("text")) == TYPE_STRING and not dialog["text"].is_empty() and not dialog["text"].contains("unavailable")
	_expect(all_readable, "All interactions have readable content in " + phase)
	_expect(state.snapshot() == before, "Reading the selected draft never advances " + phase)


func _on_changed() -> void:
	_change_events += 1


func _expect(condition: bool, description: String) -> void:
	_checks += 1
	if not condition:
		_failures += 1
		push_error(description)
