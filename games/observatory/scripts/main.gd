extends Node3D

const PlayerScript = preload("res://scripts/player.gd")
const WorldScript = preload("res://scripts/world_builder.gd")
const StoryScript = preload("res://scripts/story_state.gd")
const INK := Color("102728")
const PAPER := Color("eee7d5")
const GOLD := Color("d7bb7d")
const DRAFT_LABELS := {"original": "The practical repair", "curiosity": "What we leave for others"}

var world: Node3D
var player: CharacterBody3D
var story: RefCounted
var hud: Control
var overlay: Control
var panel: PanelContainer
var panel_body: VBoxContainer
var panel_scroll: ScrollContainer
var objective_label: Label
var hint_label: Label
var toast_label: Label
var stats_label: Label
var tool_label: Label
var crosshair: Label
var current_hotspot: String = ""
var current_dialog: Dictionary = {}
var modal: bool = true
var started: bool = false
var show_stats: bool = false
var toast_time: float = 0.0
var autosave_time: float = 0.0
var local_dir: String
var save_path: String
var ambient: AudioStreamPlayer
var water_sound: AudioStreamPlayer3D
var sound_enabled: bool = true
var frame_samples: Array[float] = []
var capture_mode: bool = false
var last_frame_usec: int = 0
var restoring_visit: bool = false

func _ready() -> void:
	Engine.max_fps = 60
	local_dir = OS.get_environment("OBSERVATORY_DATA_DIR")
	if local_dir.is_empty():
		local_dir = ProjectSettings.globalize_path("res://.local") if FileAccess.file_exists("res://project.godot") else OS.get_executable_path().get_base_dir().path_join("user_data")
	DirAccess.make_dir_recursive_absolute(local_dir)
	save_path = local_dir.path_join("visit.json")
	_install_inputs()
	_build_light()
	world = WorldScript.new()
	add_child(world)
	world.build()
	player = PlayerScript.new()
	add_child(player)
	player.home = world.spawn_position()
	player.return_home()
	story = StoryScript.new()
	story.changed.connect(_story_changed)
	_build_ui()
	_build_audio()
	_story_changed(false)
	_show_title()
	if "--smoke-test" in OS.get_cmdline_user_args():
		call_deferred("_smoke_test")
	elif "--capture" in OS.get_cmdline_user_args():
		call_deferred("_capture_scene")

func _install_inputs() -> void:
	var keys := {"walk_forward": KEY_W, "walk_back": KEY_S, "walk_left": KEY_A, "walk_right": KEY_D,
		"look_left": KEY_LEFT, "look_right": KEY_RIGHT, "look_up": KEY_UP, "look_down": KEY_DOWN,
		"hurry": KEY_SHIFT, "interact": KEY_E, "journal": KEY_TAB, "pause_visit": KEY_ESCAPE,
		"stats": KEY_F3, "mute": KEY_M}
	for action: String in keys:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		var key := InputEventKey.new()
		key.physical_keycode = keys[action]
		InputMap.action_add_event(action, key)

func _build_light() -> void:
	var high_quality := "--high-quality" in OS.get_cmdline_user_args() and RenderingServer.get_current_rendering_method() == "forward_plus"
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var sky_material := ProceduralSkyMaterial.new()
	sky_material.sky_top_color = Color("6f9bb8")
	sky_material.sky_horizon_color = Color("d5e0db")
	sky_material.ground_bottom_color = Color("3d5350")
	sky_material.ground_horizon_color = Color("d5e0db")
	sky_material.sun_angle_max = 4.0
	sky.sky_material = sky_material
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("a9c1d7")
	env.ambient_light_energy = 0.32
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.tonemap_white = 6.0
	env.fog_enabled = true
	env.fog_light_color = Color("b1c4c9")
	env.fog_density = 0.0018
	if high_quality:
		get_viewport().msaa_3d = Viewport.MSAA_4X
		RenderingServer.directional_shadow_atlas_set_size(4096, false)
		env.ssao_enabled = true
		env.ssao_radius = 1.1
		env.ssao_intensity = 1.25
		env.ssil_enabled = true
		env.ssil_intensity = 0.55
		env.ssr_enabled = true
		env.glow_enabled = true
		env.glow_intensity = 0.25
		print("OBSERVATORY_GRAPHICS high: Forward+ / MSAA4 / SSAO / SSIL / SSR")
	else:
		print("OBSERVATORY_GRAPHICS standard: Compatibility baseline")
	var environment := WorldEnvironment.new()
	environment.environment = env
	add_child(environment)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-42, -42, 0)
	sun.light_color = Color("fff0cc")
	sun.light_energy = 0.92
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 100.0 if high_quality else 45.0
	sun.shadow_bias = 0.045
	sun.shadow_normal_bias = 0.65
	add_child(sun)

func _build_audio() -> void:
	if DisplayServer.get_name() == "headless":
		return
	ambient = AudioStreamPlayer.new()
	ambient.stream = load("res://assets/audio/lakeside.wav")
	if ambient.stream is AudioStreamWAV:
		ambient.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		ambient.stream.loop_end = int(ambient.stream.get_length() * ambient.stream.mix_rate)
	ambient.volume_db = -23.0
	add_child(ambient)
	ambient.play()
	water_sound = AudioStreamPlayer3D.new()
	water_sound.stream = load("res://assets/audio/water.wav")
	if water_sound.stream is AudioStreamWAV:
		water_sound.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		water_sound.stream.loop_end = int(water_sound.stream.get_length() * water_sound.stream.mix_rate)
	water_sound.position = Vector3(0, 0.8, 0)
	water_sound.volume_db = -12.0
	water_sound.max_distance = 18.0
	water_sound.unit_size = 4.0
	add_child(water_sound)
	water_sound.play()
	_update_audio()

func _build_ui() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	hud = Control.new()
	hud.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(hud)
	var theme := Theme.new()
	theme.default_font_size = 21
	theme.set_color("font_color", "Label", PAPER)
	theme.set_color("font_color", "Button", PAPER)
	theme.set_color("font_hover_color", "Button", PAPER)
	theme.set_color("font_focus_color", "Button", PAPER)
	for state: String in ["normal", "hover", "pressed", "focus"]:
		var style := StyleBoxFlat.new()
		style.bg_color = Color("284443") if state == "normal" else Color("3e6158")
		style.border_color = GOLD if state == "focus" else Color("628678")
		style.set_border_width_all(2 if state == "focus" else 1)
		style.set_corner_radius_all(5)
		style.content_margin_left = 18
		style.content_margin_right = 18
		style.content_margin_top = 10
		style.content_margin_bottom = 10
		theme.set_stylebox(state, "Button", style)
	hud.theme = theme
	var heading := _label("THE OBSERVATORY", 18, GOLD)
	heading.position = Vector2(32, 24)
	hud.add_child(heading)
	objective_label = _label("", 19, PAPER)
	objective_label.position = Vector2(32, 54)
	objective_label.size = Vector2(740, 56)
	objective_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hud.add_child(objective_label)
	tool_label = _label("", 16, GOLD)
	tool_label.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_LEFT)
	tool_label.position = Vector2(32, -58)
	hud.add_child(tool_label)
	var controls := _label("WASD  walk     Mouse / arrows  look     E  interact     Tab  journal     Esc  pause", 16, PAPER)
	controls.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_LEFT)
	controls.position = Vector2(32, -31)
	hud.add_child(controls)
	crosshair = _label("·", 34, PAPER)
	crosshair.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	crosshair.position = Vector2(-5, -24)
	hud.add_child(crosshair)
	hint_label = _label("", 22, PAPER)
	hint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint_label.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	hint_label.position = Vector2(-440, -112)
	hint_label.size = Vector2(880, 42)
	hud.add_child(hint_label)
	toast_label = _label("", 18, GOLD)
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	toast_label.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
	toast_label.position = Vector2(-520, 28)
	toast_label.size = Vector2(488, 50)
	hud.add_child(toast_label)
	stats_label = _label("", 15, GOLD)
	stats_label.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
	stats_label.position = Vector2(-270, 80)
	stats_label.size = Vector2(238, 60)
	stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	hud.add_child(stats_label)
	overlay = Control.new()
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hud.add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0.025, 0.065, 0.067, 0.56)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(dim)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)
	panel = PanelContainer.new()
	panel.custom_minimum_size.x = 760
	var panel_style := StyleBoxFlat.new()
	panel_style.bg_color = Color(0.057, 0.127, 0.13, 0.97)
	panel_style.border_color = Color("6a8275")
	panel_style.set_border_width_all(1)
	panel_style.set_corner_radius_all(9)
	panel_style.content_margin_left = 32
	panel_style.content_margin_right = 32
	panel_style.content_margin_top = 28
	panel_style.content_margin_bottom = 28
	panel.add_theme_stylebox_override("panel", panel_style)
	center.add_child(panel)
	panel_body = VBoxContainer.new()
	panel_body.add_theme_constant_override("separation", 12)
	panel_body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	panel.add_child(panel_body)

func _label(text: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.45))
	label.add_theme_constant_override("shadow_offset_x", 1)
	label.add_theme_constant_override("shadow_offset_y", 1)
	return label

func _show_dialog(data: Dictionary, close_label: String = "Back to the world") -> void:
	current_dialog = data
	modal = true
	player.freeze(true)
	overlay.show()
	crosshair.hide()
	hint_label.text = ""
	for child in panel_body.get_children():
		panel_body.remove_child(child)
		child.queue_free()
	var eyebrow := _label("WATER BEFORE THE CROSSING", 14, GOLD)
	panel_body.add_child(eyebrow)
	var title := _label(str(data.get("title", "The Observatory")), 32, PAPER)
	title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	panel_body.add_child(title)
	var body := _label(str(data.get("text", "")), 21, PAPER)
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.custom_minimum_size.x = 680
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	panel_scroll = ScrollContainer.new()
	var button_count: int = data.get("choices", []).size() + (1 if close_label != "" else 0)
	panel_scroll.custom_minimum_size = Vector2(700, clampi(370 - button_count * 34, 90, 260))
	panel_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel_body.add_child(panel_scroll)
	panel_scroll.add_child(body)
	var first_button: Button = null
	for choice: Dictionary in data.get("choices", []):
		var button := Button.new()
		button.text = str(choice.get("label", "Continue"))
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.pressed.connect(_choose.bind(str(choice.get("action", ""))))
		panel_body.add_child(button)
		if first_button == null:
			first_button = button
	if close_label != "":
		var close := Button.new()
		close.text = close_label
		close.pressed.connect(_close_dialog)
		panel_body.add_child(close)
		if first_button == null:
			first_button = close
	if first_button != null:
		call_deferred("_focus_button", weakref(first_button))
	panel_scroll.set_deferred("scroll_vertical", 0)

func _focus_button(reference: WeakRef) -> void:
	var button: Variant = reference.get_ref()
	if is_instance_valid(button) and button.is_inside_tree():
		button.grab_focus()

func _show_title() -> void:
	var choices: Array[Dictionary] = []
	if FileAccess.file_exists(save_path):
		choices.append({"label": "Continue your visit", "action": "@load"})
		choices.append({"label": "Begin a new visit…", "action": "@reset_confirm"})
	else:
		choices.append({"label": "Enter the courtyard", "action": "@new"})
	choices.append({"label": "Leave for now", "action": "@quit"})
	_show_dialog({"title": "Water Before the Crossing", "text": "The fountain is quiet. Someone is still carrying water.\n\nExplore a lakeside settlement, borrow a tool, and follow what changes. There is time to look around.\n\nWASD to walk · mouse or arrow keys to look · E to speak or inspect.\nYour visit saves automatically. Esc opens the pause menu.", "choices": choices}, "")

func _show_pause() -> void:
	_show_dialog({"title": "A moment by the lake", "text": "Take your time. Reading and wandering do not advance a hidden deadline.", "choices": [
		{"label": "Journal and discoveries", "action": "@journal"},
		{"label": "Story workshop · compare the writing", "action": "@drafts"},
		{"label": "Return to the courtyard entrance", "action": "@home"},
		{"label": "Sound: " + ("on" if sound_enabled else "off") + "  ·  toggle", "action": "@sound"},
		{"label": "Begin a new visit…", "action": "@reset_confirm"},
		{"label": "Save and leave", "action": "@quit"}]})

func _show_drafts(note: String = "") -> void:
	var text: String = "Try two versions of the writing in this same place. Switching keeps your repairs, equipment, discoveries and position.\n\nThe practical repair: the original, direct telling.\nWhat we leave for others: more personal observations, quieter questions, and the same working repair.\n\nReading now: " + str(DRAFT_LABELS.get(story.draft_id, DRAFT_LABELS.original)) + "."
	if not note.is_empty():
		text += "\n\n" + note
	var choices: Array[Dictionary] = []
	for id: String in DRAFT_LABELS:
		if id != story.draft_id:
			choices.append({"label": "Read “" + str(DRAFT_LABELS[id]) + "”", "action": "@draft_" + id})
	choices.append({"label": "Return to pause menu", "action": "@pause"})
	_show_dialog({"title": "The same place, another telling", "text": text, "choices": choices})

func _choose(action: String) -> void:
	if action == "reset_chapter":
		_choose("@reset_confirm")
		return
	match action:
		"@new":
			started = true
			story.reset()
			player.return_home()
			_save_visit()
			_close_dialog()
		"@load":
			if _load_visit():
				started = true
				_close_dialog()
			else:
				_show_dialog({"title": "The visit could not be restored", "text": "The saved file is missing or incomplete. You can begin a fresh visit; the old file has not been changed.", "choices": [{"label": "Begin a fresh visit", "action": "@new"}]}, "")
		"@home":
			player.return_home()
			_save_visit()
			_close_dialog()
		"@journal":
			_show_dialog({"title": "Your field notes", "text": story.journal(), "choices": []})
		"@pause":
			_show_pause()
		"@drafts":
			_show_drafts()
		"@draft_original", "@draft_curiosity":
			if story.select_draft(action.trim_prefix("@draft_")):
				if started:
					_save_visit(false)
				_show_drafts("Walk back to a resident or reopen a discovery to read this version.")
			else:
				_show_drafts("That draft could not be loaded. The current writing and your visit have been kept.")
		"@sound":
			sound_enabled = not sound_enabled
			_update_audio()
			_show_pause()
		"@reset_confirm":
			_show_dialog({"title": "Begin again?", "text": "This starts the chapter over and replaces your saved visit.", "choices": [{"label": "Begin a fresh visit", "action": "@new"}]}, "Keep this visit")
		"@quit":
			if started:
				_save_visit()
			get_tree().quit()
		_:
			var reply: Dictionary = story.choose(action)
			if action == "return_to_courtyard":
				player.return_home()
				_save_visit()
			if not reply.is_empty():
				_show_dialog(reply)
			else:
				_close_dialog()

func _close_dialog() -> void:
	if not started:
		_show_title()
		return
	modal = false
	overlay.hide()
	crosshair.show()
	player.freeze(false)
	current_dialog = {}

func _story_changed(save: bool = true) -> void:
	world.update_story(story.water_restored, story.settlement_phase)
	if objective_label != null:
		objective_label.text = story.objective()
		tool_label.text = "Equipment  ·  " + ({"echo": "Echo spool", "coupler": "Long-reach coupler"}.get(story.tool, "Hands free"))
	if water_sound != null:
		_update_audio()
	if save and started and not restoring_visit:
		_save_visit()

func _update_audio() -> void:
	if ambient != null:
		ambient.volume_db = -23 if sound_enabled else -80
	if water_sound != null:
		water_sound.volume_db = -12 if sound_enabled and story.water_restored else -80

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_visit"):
		if started:
			if modal:
				_close_dialog()
			else:
				_show_pause()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed("stats"):
		show_stats = not show_stats
	elif event.is_action_pressed("mute"):
		sound_enabled = not sound_enabled
		_update_audio()
	elif event.is_action_pressed("journal") and started:
		if modal:
			_close_dialog()
		else:
			_choose("@journal")
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed("interact") and not modal and current_hotspot != "":
		_show_dialog(story.describe(current_hotspot))
		get_viewport().set_input_as_handled()

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT and started and not modal:
		_show_pause()
	elif what == NOTIFICATION_WM_CLOSE_REQUEST and started:
		_save_visit()

func _process(delta: float) -> void:
	toast_time = maxf(toast_time - delta, 0.0)
	toast_label.visible = toast_time > 0.0
	stats_label.visible = show_stats
	stats_label.text = "%d fps · %.1f ms\nF3 hides this display" % [Engine.get_frames_per_second(), delta * 1000.0]
	if not modal:
		_update_target()
		autosave_time += delta
		if autosave_time > 12.0:
			autosave_time = 0.0
			_save_visit(false)
	if capture_mode:
		var now_usec: int = Time.get_ticks_usec()
		if last_frame_usec > 0:
			frame_samples.append(float(now_usec - last_frame_usec) / 1000.0)
		last_frame_usec = now_usec

func _update_target() -> void:
	current_hotspot = ""
	var best_score: float = INF
	var label: String = ""
	var eye: Vector3 = player.camera.global_position
	var forward: Vector3 = -player.camera.global_basis.z
	for hotspot: Dictionary in world.hotspots:
		var target: Vector3 = hotspot.position
		var offset: Vector3 = target - eye
		var distance: float = offset.length()
		if distance > float(hotspot.radius) or distance < 0.01:
			continue
		var alignment: float = forward.dot(offset / distance)
		if alignment < 0.65:
			continue
		var query := PhysicsRayQueryParameters3D.create(eye, target, 1, [player.get_rid()])
		var hit: Dictionary = get_world_3d().direct_space_state.intersect_ray(query)
		if not hit.is_empty() and (hit.position as Vector3).distance_to(target) > 0.7:
			continue
		var score: float = distance * 0.15 + (1.0 - alignment) * 4.0
		if score < best_score:
			best_score = score
			current_hotspot = hotspot.id
			label = hotspot.label
	hint_label.text = "E  ·  " + label if current_hotspot != "" else ""
	crosshair.modulate = GOLD if current_hotspot != "" else PAPER

func _save_visit(notify: bool = true) -> void:
	if capture_mode or "--smoke-test" in OS.get_cmdline_user_args():
		return
	var data: Dictionary = {"version": 1, "story": story.snapshot(), "player": [player.position.x, player.position.y, player.position.z], "yaw": player.rotation.y, "pitch": player.camera.rotation.x, "sound": sound_enabled, "draft": story.draft_id}
	var temporary: String = save_path + ".tmp"
	var file := FileAccess.open(temporary, FileAccess.WRITE)
	if file == null:
		_toast("Could not save this visit")
		return
	file.store_string(JSON.stringify(data, "\t"))
	file.close()
	var error: Error = DirAccess.rename_absolute(temporary, save_path)
	if error != OK:
		_toast("Could not replace the saved visit")
	elif notify:
		_toast("Visit saved")

func _load_visit() -> bool:
	if not FileAccess.file_exists(save_path):
		return false
	var parser := JSON.new()
	if parser.parse(FileAccess.get_file_as_string(save_path)) != OK:
		return false
	var data: Variant = parser.data
	if not data is Dictionary or data.get("version") != 1 or not data.get("story") is Dictionary:
		return false
	restoring_visit = true
	var restored_story: bool = story.restore(data.story)
	restoring_visit = false
	if not restored_story:
		return false
	var saved_draft: Variant = data.get("draft", "original")
	if not saved_draft is String or not story.select_draft(saved_draft):
		story.select_draft("original")
	player.return_home()
	var position_data: Variant = data.get("player", [])
	if position_data is Array and position_data.size() == 3:
		var valid: bool = true
		for item: Variant in position_data:
			valid = valid and (item is float or item is int) and is_finite(float(item))
		if valid:
			var restored := Vector3(float(position_data[0]), float(position_data[1]), float(position_data[2]))
			if absf(restored.x) < 13 and restored.z > -18 and restored.z < 13 and restored.y > -1 and restored.y < 3:
				player.position = restored
	var yaw: Variant = data.get("yaw", 0.0)
	var pitch: Variant = data.get("pitch", 0.0)
	if (yaw is float or yaw is int) and is_finite(float(yaw)):
		player.rotation.y = float(yaw)
	if (pitch is float or pitch is int) and is_finite(float(pitch)):
		player.camera.rotation.x = clampf(float(pitch), -1.35, 1.35)
	sound_enabled = data.get("sound", true) == true
	_story_changed(false)
	return true

func _toast(text: String) -> void:
	toast_label.text = text
	toast_time = 2.5

func _exit_tree() -> void:
	if ambient != null:
		ambient.stop()
		ambient.stream = null
	if water_sound != null:
		water_sound.stop()
		water_sound.stream = null

func _smoke_test() -> void:
	await get_tree().physics_frame
	started = true
	if not FileAccess.file_exists("res://project.godot"):
		for private_directory: String in ["res://builds", "res://.local", "res://tests"]:
			assert(not DirAccess.dir_exists_absolute(private_directory), "Private development directory was packed: " + private_directory)
		print("OBSERVATORY_PACK_PRIVATE_DIRS_ABSENT")
	var before: Dictionary = story.snapshot()
	assert(story.select_draft("curiosity"), "Second story draft is missing or invalid")
	assert(story.describe("resident_mara").text.contains("swallows"), "Second story draft did not load")
	assert(story.select_draft("original"), "Original story draft is missing or invalid")
	assert(story.snapshot() == before, "Changing drafts altered visit progress")
	for hotspot: Dictionary in world.hotspots:
		var data: Dictionary = story.describe(hotspot.id)
		assert(data.has("title") and data.has("text"), "Missing interaction: " + hotspot.id)
		_show_dialog(data)
		await get_tree().process_frame
	_close_dialog()
	player.enabled = false
	var start_y: float = player.position.y
	for index in range(45):
		await get_tree().physics_frame
	assert(player.is_on_floor(), "Spawn has no reachable floor")
	assert(absf(player.position.y - start_y) < 0.5, "Spawn fell through geometry")
	print("OBSERVATORY_SMOKE_OK interactions=%d floor=true drafts=2" % world.hotspots.size())
	get_tree().quit()

func _capture_scene() -> void:
	capture_mode = true
	started = true
	_close_dialog()
	player.freeze(true)
	modal = true
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var location: String = "courtyard"
	if "--lake" in args:
		location = "lake"
		player.position = Vector3(9.5, 0.1, 5.3)
		player.camera.look_at(Vector3(45, 5.0, -42))
	elif "--pump" in args:
		location = "pump"
		player.position = Vector3(-6.7, 0.1, -2.7)
		player.camera.look_at(Vector3(-10, 1.1, -5.1))
	elif "--archive" in args:
		location = "archive"
		player.position = Vector3(2, 0.1, -9)
		player.camera.look_at(Vector3(1, 1.4, -14))
	elif "--dialog" in args:
		location = "dialog"
		_show_dialog(story.describe("bench"))
	elif "--drafts" in args:
		location = "story_workshop"
		story.select_draft("curiosity")
		_show_drafts()
	elif "--draft-dialog" in args:
		location = "mara_second_draft"
		story.select_draft("curiosity")
		_show_dialog(story.describe("resident_mara"))
	elif "--pause" in args:
		location = "pause_menu"
		_show_pause()
	if "--repaired" in args:
		world.update_story(true, "crossing")
		location += "_repaired"
	for index in range(90):
		await get_tree().process_frame
	frame_samples.clear()
	for index in range(180):
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var screenshot := get_viewport().get_texture().get_image()
	var screenshot_path := local_dir.path_join(location + ".png")
	screenshot.save_png(screenshot_path)
	frame_samples.sort()
	var sum: float = 0.0
	for sample: float in frame_samples:
		sum += sample
	var metrics := {"location": location, "samples": frame_samples.size(), "mean_ms": sum / maxf(frame_samples.size(), 1), "p95_ms": frame_samples[int(frame_samples.size() * 0.95)], "adapter": RenderingServer.get_video_adapter_name(), "renderer": RenderingServer.get_current_rendering_method(), "viewport": [get_viewport().get_visible_rect().size.x, get_viewport().get_visible_rect().size.y], "screenshot": screenshot_path, "note": "Stationary scene sample of wall-clock process intervals including UI; not a complete play-through benchmark."}
	var report := FileAccess.open(local_dir.path_join(location + ".metrics.json"), FileAccess.WRITE)
	report.store_string(JSON.stringify(metrics, "\t"))
	report.close()
	print("OBSERVATORY_CAPTURE " + JSON.stringify(metrics))
	get_tree().quit()
