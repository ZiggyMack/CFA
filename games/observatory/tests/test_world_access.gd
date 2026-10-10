extends SceneTree
## Physics integration: every interaction has a connected walking approach.
## Run headlessly with --path games/observatory --script res://tests/test_world_access.gd.

const WorldScript = preload("res://scripts/world_builder.gd")
const PlayerScript = preload("res://scripts/player.gd")
const GRID_MIN := Vector2(-12.0, -17.5)
const GRID_STEP := 0.5
const GRID_SIZE := Vector2i(47, 61)
const NEIGHBORS := [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]

var _checks := 0
var _failures := 0
var _world: Node3D
var _player: CharacterBody3D
var _space: PhysicsDirectSpaceState3D
var _shape: CapsuleShape3D
var _query: PhysicsShapeQueryParameters3D


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	_world = WorldScript.new()
	root.add_child(_world)
	_world.build()
	_player = PlayerScript.new()
	root.add_child(_player)
	_player.set_physics_process(false)
	_player.position = _world.spawn_position() + Vector3(0, 0.12, 0)
	await physics_frame
	await physics_frame
	_space = _world.get_world_3d().direct_space_state
	_shape = CapsuleShape3D.new()
	_shape.radius = 0.28
	_shape.height = 1.7
	_query = PhysicsShapeQueryParameters3D.new()
	_query.shape = _shape
	_query.collision_mask = 1
	_query.margin = 0.002
	_query.exclude = [_player.get_rid()]
	await _test_spawn_movement()
	_test_phase("hauling", false)
	_world.update_story(true, "crossing")
	await physics_frame
	await physics_frame
	_test_phase("crossing", true)
	_expect(_world.get_node("RestoredWater").visible, "Restoring supply makes fountain water visible")
	_expect(not _world.get_node("WaterHaulingBuckets").visible, "Return after repair removes the water-hauling buckets")
	_expect(_world.get_node("CrossingWorkResumed").visible, "Return after repair adds the new crossing planks")
	_world.update_story(false, "hauling")
	_expect(not _world.get_node("RestoredWater").visible, "Reset removes restored fountain water")
	_expect(_world.get_node("WaterHaulingBuckets").visible, "Reset brings the hauling arrangement back")
	print("World access checks: %d passed / %d total" % [_checks - _failures, _checks])
	quit(0 if _failures == 0 else 1)


func _test_spawn_movement() -> void:
	var spawn: Vector3 = _world.spawn_position()
	for frame in range(60):
		_player.velocity = Vector3(0, -2.0, -3.4)
		_player.move_and_slide()
		await physics_frame
	_expect(_player.position.z < spawn.z - 2.8, "The actual player can walk forward from spawn")
	_expect(absf(_player.position.x - spawn.x) < 0.05, "Spawn movement is not deflected by hidden collision")
	_expect(absf(_player.position.y) < 0.06 and _player.is_on_floor(), "The actual player settles on the level courtyard floor")
	_player.position = spawn


func _test_phase(phase: String, repaired: bool) -> void:
	var open_cells: Dictionary = {}
	for x in range(GRID_SIZE.x):
		for z in range(GRID_SIZE.y):
			var cell := Vector2i(x, z)
			_query.transform = Transform3D(Basis.IDENTITY, _cell_position(cell) + Vector3(0, 0.86, 0))
			_query.motion = Vector3.ZERO
			if _space.intersect_shape(_query, 1).is_empty():
				open_cells[cell] = true
	var spawn: Vector3 = _world.spawn_position()
	var origin := Vector2i(roundi((spawn.x - GRID_MIN.x) / GRID_STEP), roundi((spawn.z - GRID_MIN.y) / GRID_STEP))
	_expect(open_cells.has(origin), phase + ": spawn fits the player's actual capsule")
	if not open_cells.has(origin):
		return
	var reachable: Dictionary = {origin: true}
	var queue: Array[Vector2i] = [origin]
	var cursor := 0
	while cursor < queue.size():
		var cell := queue[cursor]
		cursor += 1
		for offset: Vector2i in NEIGHBORS:
			var next := cell + offset
			if reachable.has(next) or not open_cells.has(next):
				continue
			_query.transform = Transform3D(Basis.IDENTITY, _cell_position(cell) + Vector3(0, 0.86, 0))
			_query.motion = _cell_position(next) - _cell_position(cell)
			var travel: PackedFloat32Array = _space.cast_motion(_query)
			if travel[0] > 0.999:
				reachable[next] = true
				queue.append(next)
	_expect(reachable.size() > 1000, phase + ": courtyard and connecting paths form a substantial walkable region")
	for hotspot: Dictionary in _world.hotspots:
		var candidate := Vector3.INF
		var best_distance := INF
		var target: Vector3 = hotspot.position
		for cell: Vector2i in reachable:
			var standing := _cell_position(cell)
			var eye := standing + Vector3(0, 1.63, 0)
			var distance := eye.distance_to(target)
			if distance >= best_distance or distance > float(hotspot.radius) or distance < 0.01:
				continue
			var forward := (target - eye).normalized()
			if absf(asin(forward.y)) > 1.35:
				continue
			if _selected_hotspot(eye, forward) == hotspot.id:
				candidate = standing
				best_distance = distance
		_expect(candidate != Vector3.INF, phase + ": reachable, selectable interaction for " + str(hotspot.id))
		if candidate != Vector3.INF:
			print("  %s / %s: stand %s, eye distance %.2fm" % [phase, hotspot.id, str(candidate), best_distance])
	var mara_position: Vector3 = _world.get_node("Mara").position
	_expect((mara_position.x > 6.0) == repaired, phase + ": Mara's physical placement communicates the current work")
	print("  %s: %d connected standing cells of %d unobstructed cells" % [phase, reachable.size(), open_cells.size()])


func _selected_hotspot(eye: Vector3, forward: Vector3) -> String:
	# Match main.gd's distance, cone, obstruction tolerance, and ranking rules.
	var selected := ""
	var best_score := INF
	for hotspot: Dictionary in _world.hotspots:
		var target: Vector3 = hotspot.position
		var offset := target - eye
		var distance := offset.length()
		if distance > float(hotspot.radius) or distance < 0.01:
			continue
		var alignment := forward.dot(offset / distance)
		if alignment < 0.65:
			continue
		var ray := PhysicsRayQueryParameters3D.create(eye, target, 1, [_player.get_rid()])
		var hit: Dictionary = _space.intersect_ray(ray)
		if not hit.is_empty() and (hit.position as Vector3).distance_to(target) > 0.7:
			continue
		var score := distance * 0.15 + (1.0 - alignment) * 4.0
		if score < best_score:
			best_score = score
			selected = hotspot.id
	return selected


func _cell_position(cell: Vector2i) -> Vector3:
	return Vector3(GRID_MIN.x + cell.x * GRID_STEP, 0.0, GRID_MIN.y + cell.y * GRID_STEP)


func _expect(condition: bool, message: String) -> void:
	_checks += 1
	if not condition:
		_failures += 1
		push_error(message)
