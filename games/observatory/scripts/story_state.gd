extends RefCounted
## Chapter rules remain independent of movement, rendering, and dialog widgets.
## Inspecting a hotspot is read-only. Every consequence requires choose().

signal changed

const SAVE_VERSION: int = 1
const CONTENT_PATH: String = "res://data/chapter.json"
const DRAFT_PATHS: Dictionary = {
	"original": CONTENT_PATH,
	"curiosity": "res://data/drafts/curiosity.json"
}
const CHAPTER_ID: String = "water_before_the_crossing"
const REQUIRED_ENTRY_IDS: Array[String] = [
	"mara_arrival", "ivo_arrival", "mara_deferred", "ivo_deferred",
	"mara_crossing", "ivo_crossing", "pump_broken", "pump_restored", "bench",
	"archive", "plaque", "return_deferred", "return_repaired", "arrive_deferred",
	"arrive_repaired", "ending_deferred", "ending_repaired"
]
const MAX_DRAFT_BYTES: int = 524288
const MAX_TITLE_LENGTH: int = 160
const MAX_TEXT_LENGTH: int = 12000

var draft_id: String = "original"

var water_restored: bool = false
var return_seen: bool = false
var ending_seen: bool = false
var tool: String = ""
var settlement_phase: String = "hauling"

var _echo_recorded: bool = false
var _bypass_held: bool = false
var _regulator_collected: bool = false
var _archive_read: bool = false
var _entries: Dictionary = {}


func _init() -> void:
	if not select_draft("original"):
		push_error("Observatory chapter text could not be loaded: " + CONTENT_PATH)


func select_draft(id: String) -> bool:
	# Only bundled drafts are selectable; callers cannot supply arbitrary paths.
	if not DRAFT_PATHS.has(id):
		return false
	var path: String = DRAFT_PATHS[id]
	if not FileAccess.file_exists(path):
		return false
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	if file.get_length() > MAX_DRAFT_BYTES:
		file.close()
		return false
	var encoded: String = file.get_as_text()
	file.close()
	var parser := JSON.new()
	if parser.parse(encoded) != OK:
		return false
	return select_draft_content(id, parser.data)


func select_draft_content(id: String, content: Variant) -> bool:
	# Validate the complete replacement before changing the active text. The
	# helper also allows authoring tools and tests to check an in-memory draft.
	# Selecting prose never advances the visit or emits the story-change signal.
	if not DRAFT_PATHS.has(id) or typeof(content) != TYPE_DICTIONARY:
		return false
	if content.get("chapter_id") != CHAPTER_ID:
		return false
	var entries: Variant = content.get("entries")
	if typeof(entries) != TYPE_DICTIONARY or entries.size() != REQUIRED_ENTRY_IDS.size():
		return false
	var validated: Dictionary = {}
	for key: String in REQUIRED_ENTRY_IDS:
		var entry: Variant = entries.get(key)
		if typeof(entry) != TYPE_DICTIONARY:
			return false
		var title: Variant = entry.get("title")
		var text: Variant = entry.get("text")
		if typeof(title) != TYPE_STRING or typeof(text) != TYPE_STRING:
			return false
		if title.strip_edges().is_empty() or text.strip_edges().is_empty():
			return false
		if title.length() > MAX_TITLE_LENGTH or text.length() > MAX_TEXT_LENGTH:
			return false
		# Copy only display fields, without retaining aliases to caller data.
		validated[key] = {"title": title, "text": text}
	_entries = validated
	draft_id = id
	return true


func describe(id: String) -> Dictionary:
	match id:
		"resident_mara", "resident_ivo":
			var resident: String = "mara" if id == "resident_mara" else "ivo"
			var phase: String = "crossing" if settlement_phase == "crossing" else ("deferred" if return_seen else "arrival")
			return _entry(resident + "_" + phase)
		"pump":
			return _entry("pump_restored" if water_restored else "pump_broken")
		"bench":
			var options: Array = []
			if tool != "echo":
				options.append(_choice("Equip the echo spool", "equip_echo"))
			if tool != "coupler":
				options.append(_choice("Equip the long-reach coupler", "equip_coupler"))
			var result: Dictionary = _entry("bench", options)
			result["text"] += "\n\nEquipped: " + _tool_name() + "."
			return result
		"lever":
			if water_restored:
				return _dialog("The service lever", "The lever rests in its normal position. The repaired regulator is keeping the supply steady.")
			if tool == "echo":
				if _echo_recorded:
					return _dialog("The recorded movement", "Your spool has the lever's movement. At the bypass station, start its repeating echo to hold the water on the service route. The loop has no time limit.")
				return _dialog("Record the service lever", "You can lift the spring-return lever while the spool records. The recording will repeat steadily when you start it at the bypass. It will not run out while you explore.", [_choice("Record the lever movement", "record_lever")])
			if tool == "coupler":
				return _dialog("A lever within reach", "The coupler can reach this lever through the inspection opening at the bypass station. Fit it there to keep the bypass open while your hands are free.")
			return _dialog("A spring-return lever", "The lever closes when released. Borrow an echo spool or a long-reach coupler from the workbench before trying to fit the regulator.")
		"bypass":
			return _describe_bypass()
		"regulator":
			if _regulator_collected:
				return _dialog("The regulator rack", "The spare is fitted in the pump." if water_restored else "You already have the spare regulator. Hold the bypass open, then install it at the bypass station.")
			return _dialog("A spare, kept ready", "A replacement regulator rests in an oiled cloth. Its gasket is sound. Someone has left the right part where the next repairer could find it.", [_choice("Take the spare regulator", "take_regulator")])
		"archive":
			var options: Array = [] if _archive_read else [_choice("Keep a copy in my journal", "preserve_record")]
			return _entry("archive", options)
		"plaque":
			return _entry("plaque")
		"return_marker":
			return _entry("return_repaired" if water_restored else "return_deferred", [_choice("Return to the courtyard", "return_to_courtyard"), _choice("Keep exploring for now", "continue_visit")])
		"ending":
			if not return_seen:
				return _dialog("The lakeside bench", "The bench catches the afternoon light. Take a walk up the upper path, then return to see how Mara and Ivo are getting on. The archive is there if you feel curious.")
			if water_restored and settlement_phase != "crossing":
				return _dialog("A change still to see", "The pump is running now. Return to the courtyard from the upper path once more to see what the crew can do with the restored supply.")
			var options: Array = [_choice("Keep exploring", "continue_visit"), _choice("Begin a fresh visit", "reset_chapter")] if ending_seen else [_choice("Close this chapter", "finish_chapter")]
			return _entry("ending_repaired" if settlement_phase == "crossing" else "ending_deferred", options)
	return _dialog("The Observatory", "The path is open. Take your time.")


func choose(action: String) -> Dictionary:
	match action:
		"equip_echo", "equip_coupler":
			var next_tool: String = "echo" if action == "equip_echo" else "coupler"
			if next_tool != tool:
				tool = next_tool
				_bypass_held = false
			return _updated("bench")
		"record_lever":
			if tool != "echo" or water_restored:
				return describe("lever")
			_echo_recorded = true
			return _updated("lever")
		"hold_echo":
			if water_restored or tool != "echo" or not _echo_recorded:
				return describe("bypass")
			_bypass_held = true
			return _updated("bypass")
		"hold_coupler":
			if water_restored or tool != "coupler":
				return describe("bypass")
			_bypass_held = true
			return _updated("bypass")
		"release_bypass":
			_bypass_held = false
			return _updated("bypass")
		"take_regulator":
			_regulator_collected = true
			return _updated("regulator")
		"install_regulator":
			if water_restored or not _bypass_held or not _regulator_collected:
				return describe("bypass")
			water_restored = true
			_bypass_held = false
			return _updated("pump")
		"preserve_record":
			_archive_read = true
			return _updated("archive")
		"return_to_courtyard":
			return_seen = true
			settlement_phase = "crossing" if water_restored else "hauling"
			changed.emit()
			return _entry("arrive_repaired" if water_restored else "arrive_deferred")
		"finish_chapter":
			if not return_seen or (water_restored and settlement_phase != "crossing"):
				return describe("ending")
			ending_seen = true
			return _updated("ending")
		"reset_chapter":
			reset()
			return {}
		"continue_visit":
			return {}
	return {}


func objective() -> String:
	if water_restored and settlement_phase != "crossing":
		return "Water is running. Return from the upper path to see the crew regroup."
	if not water_restored and not tool.is_empty():
		if _bypass_held:
			return "Fit the spare regulator at the bypass." if _regulator_collected else "The bypass is held open. Collect the spare regulator from its rack."
		if tool == "echo" and not _echo_recorded:
			return "Record the service lever with the echo spool. The regulator is on the rack."
		return "Hold the bypass open with your tool, then fit the spare regulator."
	if ending_seen:
		return "Chapter complete. Keep exploring, revisit the repair, or begin a fresh visit."
	if return_seen:
		return "Visit the lakeside bench to close the chapter. The workshop stays open."
	return "Meet the residents. Borrow a tool from the workbench, or explore the upper path."


func journal() -> String:
	var lines: PackedStringArray = PackedStringArray([
		"WATER BEFORE THE CROSSING",
		"The water-hauling arrangement uses the people needed for a shared lift at the crossing.",
		"Equipped: " + _tool_name() + ".",
		"No hidden deadline. Reading, walking, and closing a conversation do not advance the return scene."
	])
	if _echo_recorded:
		lines.append("The echo spool holds a recording of the service lever. Its bypass loop has no countdown.")
	if _regulator_collected:
		lines.append("The spare regulator is installed." if water_restored else "The spare regulator is in your care, ready to install.")
	if _bypass_held:
		lines.append("The bypass is held open. It stays open until released or you change tools.")
	if water_restored:
		lines.append("The repair restored water to the fountain.")
	if return_seen:
		lines.append("On your latest return, the crew gathered at the crossing." if settlement_phase == "crossing" else "On your latest return, the crew was still occupied with the water-hauling arrangement. The pump can still be repaired.")
	if _archive_read:
		lines.append("ARCHIVE COPY\n" + str(_entries.get("archive", {}).get("text", "")))
	return "\n\n".join(lines)


func snapshot() -> Dictionary:
	return {
		"version": SAVE_VERSION,
		"water_restored": water_restored,
		"return_seen": return_seen,
		"ending_seen": ending_seen,
		"tool": tool,
		"settlement_phase": settlement_phase,
		"echo_recorded": _echo_recorded,
		"bypass_held": _bypass_held,
		"regulator_collected": _regulator_collected,
		"archive_read": _archive_read
	}


func restore(data: Dictionary) -> bool:
	# Validate the whole snapshot before changing any live field. JSON numbers
	# can arrive as floats, so accept version 1.0 while rejecting other versions.
	var version: Variant = data.get("version")
	if typeof(version) not in [TYPE_INT, TYPE_FLOAT] or version != SAVE_VERSION:
		return false
	for key: String in ["water_restored", "return_seen", "ending_seen", "echo_recorded", "bypass_held", "regulator_collected", "archive_read"]:
		if typeof(data.get(key)) != TYPE_BOOL:
			return false
	if typeof(data.get("tool")) != TYPE_STRING or data["tool"] not in ["", "echo", "coupler"]:
		return false
	if typeof(data.get("settlement_phase")) != TYPE_STRING or data["settlement_phase"] not in ["hauling", "crossing"]:
		return false
	if data["water_restored"] and (not data["regulator_collected"] or data["bypass_held"] or data["tool"] == ""):
		return false
	if data["bypass_held"] and (data["tool"] == "" or (data["tool"] == "echo" and not data["echo_recorded"])):
		return false
	if data["echo_recorded"] and data["tool"] == "":
		return false
	if data["settlement_phase"] == "crossing" and (not data["return_seen"] or not data["water_restored"]):
		return false
	if data["ending_seen"] and not data["return_seen"]:
		return false
	water_restored = data["water_restored"]
	return_seen = data["return_seen"]
	ending_seen = data["ending_seen"]
	tool = data["tool"]
	settlement_phase = data["settlement_phase"]
	_echo_recorded = data["echo_recorded"]
	_bypass_held = data["bypass_held"]
	_regulator_collected = data["regulator_collected"]
	_archive_read = data["archive_read"]
	changed.emit()
	return true


func reset() -> void:
	water_restored = false
	return_seen = false
	ending_seen = false
	tool = ""
	settlement_phase = "hauling"
	_echo_recorded = false
	_bypass_held = false
	_regulator_collected = false
	_archive_read = false
	changed.emit()


func _describe_bypass() -> Dictionary:
	if water_restored:
		return _dialog("The service bypass", "The new regulator is fitted. The temporary hold is released and the pump is supplying the fountain normally.")
	if _bypass_held:
		var options: Array = []
		if _regulator_collected:
			options.append(_choice("Install the spare regulator", "install_regulator"))
		options.append(_choice("Release the bypass hold", "release_bypass"))
		var detail: String = "Your echo repeats the lever movement steadily." if tool == "echo" else "The coupler holds the lever through the inspection opening."
		detail += " Your hands are free. There is no timer.\n\n"
		detail += "The spare is ready. Fit it here to restore the supply." if _regulator_collected else "Collect the spare regulator from the rack, then return here to install it. The hold will remain in place."
		return _dialog("The bypass is held open", detail, options)
	if tool == "coupler":
		return _dialog("Through the inspection opening", "The lever is visible through a narrow opening. The long-reach coupler can reach it from here and keep it raised while you fit the regulator.", [_choice("Hold the lever with the coupler", "hold_coupler")])
	if tool == "echo" and _echo_recorded:
		return _dialog("Replay at the bypass", "The spool can replay your recording of the service lever. Its echo will loop until released, keeping the bypass open while you fit the regulator.", [_choice("Start the repeating echo", "hold_echo")])
	if tool == "echo":
		return _dialog("An echo needs a recording", "First record the service lever at its station. Then return here and use the spool's repeating echo to hold the bypass open.")
	return _dialog("A hand needed elsewhere", "The spring lever must stay raised while you replace the regulator here. Borrow either tool from the workbench. The long-reach coupler fits through the inspection opening; the echo spool repeats a recorded movement.")


func _tool_name() -> String:
	match tool:
		"echo":
			return "echo spool"
		"coupler":
			return "long-reach coupler"
	return "no tool"


func _entry(key: String, choices: Array = []) -> Dictionary:
	var entry: Dictionary = _entries.get(key, {})
	return _dialog(str(entry.get("title", "The Observatory")), str(entry.get("text", "Chapter text is unavailable.")), choices)


func _dialog(title: String, text: String, choices: Array = []) -> Dictionary:
	return {"title": title, "text": text, "choices": choices}


func _choice(label: String, action: String) -> Dictionary:
	return {"label": label, "action": action}


func _updated(id: String) -> Dictionary:
	changed.emit()
	return describe(id)
