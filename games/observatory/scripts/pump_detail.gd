extends Node3D
## Visual detail in CommunalPump's local coordinates. Parent this below the
## existing pump; the original housing, collision, lamp, and hotspots remain.

var _materials: Dictionary = {}
var _surfaces: Dictionary = {}
var _needle: MeshInstance3D
var _built := false


func build(materials: Dictionary) -> void:
	if _built:
		return
	_built = true
	_materials = materials.duplicate()
	for entry in [["green", "527d73"], ["new_green", "7ca396"], ["dark_green", "324e4b"],
		["brass", "c19b58"], ["new_brass", "e3c57d"], ["rust", "9d6450"]]:
		if not _materials.has(entry[0]):
			_materials[entry[0]] = _material(Color(entry[1]))
	_materials["iron"] = _material(Color("605c4e"), 0.50)
	_materials["dial"] = _material(Color("d9d1af"))
	_materials["dial_ink"] = _material(Color("27332f"))
	_materials["needle"] = _material(Color("864833"))
	_cast_housing()
	_pipework()
	_service_hardware()
	_pressure_gauge()
	_finish()
	set_water_restored(false)


func set_water_restored(restored: bool) -> void:
	# Optional connection to the same state that drives the existing lamp.
	# There is no second simulation or interaction hidden in this visual.
	if is_instance_valid(_needle):
		_needle.rotation.z = deg_to_rad(-28.0 if restored else 128.0)


func _material(color: Color, metallic: float = 0.0) -> StandardMaterial3D:
	var result := StandardMaterial3D.new()
	result.albedo_color = color
	result.metallic = metallic
	result.roughness = 0.72
	return result


func _surface(key: String) -> SurfaceTool:
	if not _surfaces.has(key):
		var surface := SurfaceTool.new()
		surface.begin(Mesh.PRIMITIVE_TRIANGLES)
		surface.set_material(_materials[key])
		_surfaces[key] = surface
	return _surfaces[key] as SurfaceTool


func _triangle(key: String, a: Vector3, b: Vector3, c: Vector3, normal_a: Vector3 = Vector3.ZERO,
	normal_b: Vector3 = Vector3.ZERO, normal_c: Vector3 = Vector3.ZERO) -> void:
	var cross := (c - a).cross(b - a)
	if cross.length_squared() < 0.000000000001:
		return
	var face_normal := cross.normalized()
	var surface := _surface(key)
	for vertex in [[a, normal_a], [b, normal_b], [c, normal_c]]:
		var point: Vector3 = vertex[0]
		var normal: Vector3 = vertex[1]
		surface.set_normal(face_normal if normal == Vector3.ZERO else normal)
		# One model metre maps to one UV unit, without stretching every face
		# across a whole texture. Material-specific tiling remains upstream.
		if absf(face_normal.y) > 0.6:
			surface.set_uv(Vector2(point.x, point.z))
		elif absf(face_normal.x) > 0.6:
			surface.set_uv(Vector2(point.z, -point.y))
		else:
			surface.set_uv(Vector2(point.x, -point.y))
		surface.add_vertex(point)


func _quad(key: String, a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> void:
	_triangle(key, a, b, c)
	_triangle(key, a, c, d)


func _cylinder(key: String, a: Vector3, b: Vector3, radius: float, sides: int = 16,
	end_radius: float = -1.0, cap: bool = true) -> void:
	var direction := (b - a).normalized()
	var tangent := direction.cross(Vector3.FORWARD)
	if tangent.length_squared() < 0.001:
		tangent = direction.cross(Vector3.RIGHT)
	tangent = tangent.normalized()
	var binormal := direction.cross(tangent).normalized()
	var radius_b := radius if end_radius < 0.0 else end_radius
	for index in range(sides):
		var angle_a := TAU * float(index) / float(sides)
		var angle_b := TAU * float(index + 1) / float(sides)
		var normal_a := tangent * cos(angle_a) + binormal * sin(angle_a)
		var normal_b := tangent * cos(angle_b) + binormal * sin(angle_b)
		var p0 := a + normal_a * radius
		var p1 := b + normal_a * radius_b
		var p2 := b + normal_b * radius_b
		var p3 := a + normal_b * radius
		_triangle(key, p0, p1, p2, normal_a, normal_a, normal_b)
		_triangle(key, p0, p2, p3, normal_a, normal_b, normal_b)
		if cap:
			_triangle(key, b, p2, p1)
			_triangle(key, a, p0, p3)


func _cast_housing() -> void:
	# The flat functional housing becomes a cast machine with rounded upper
	# shoulders. Its old lip reads as the removable head's lower flange.
	var profile: Array[Vector2] = [Vector2(-0.55, 1.94), Vector2(-0.55, 2.05),
		Vector2(-0.535, 2.135), Vector2(-0.492, 2.212), Vector2(-0.428, 2.272),
		Vector2(-0.348, 2.31), Vector2(-0.25, 2.323), Vector2(0.25, 2.323),
		Vector2(0.348, 2.31), Vector2(0.428, 2.272), Vector2(0.492, 2.212),
		Vector2(0.535, 2.135), Vector2(0.55, 2.05), Vector2(0.55, 1.94)]
	var center := Vector2(0.0, 2.10)
	for index in range(profile.size()):
		var a := profile[index]
		var b := profile[(index + 1) % profile.size()]
		var front_a := Vector3(a.x, a.y, 0.367)
		var front_b := Vector3(b.x, b.y, 0.367)
		var back_a := Vector3(a.x, a.y, -0.367)
		var back_b := Vector3(b.x, b.y, -0.367)
		_triangle("green", Vector3(center.x, center.y, 0.367), front_a, front_b)
		_triangle("green", Vector3(center.x, center.y, -0.367), back_b, back_a)
		_quad("green", front_a, back_a, back_b, front_b)
	# Cast feet and rounded front reinforcement rails add thickness at the
	# base without projecting into the player's approach to the service panel.
	_box("dark_green", Vector3(0, 0.245, 0), Vector3(1.16, 0.14, 0.85))
	for x in [-0.49, 0.49]:
		_cylinder("green", Vector3(x, 0.33, 0.326), Vector3(x, 1.96, 0.326), 0.032, 12)
		_box("iron", Vector3(x, 0.32, 0.25), Vector3(0.16, 0.06, 0.27))
		_cylinder("brass", Vector3(x, 0.35, 0.30), Vector3(x, 0.377, 0.30), 0.041, 6)
	# Four side fins are modest heat-dissipating ribs, rounded at the front.
	for height in [1.19, 1.33, 1.47, 1.61]:
		for x in [-0.529, 0.529]:
			_box("dark_green", Vector3(x, height, -0.04), Vector3(0.057, 0.043, 0.47))
	# Head seam, fasteners, and a lifting eye make assembly legible up close.
	for x in [-0.40, 0.40]:
		_hex_bolt(Vector3(x, 2.125, 0.376), 0.026)
	_ring("iron", Vector3(0, 2.375, 0), 0.080, 0.018, 20, 6)
	_cylinder("iron", Vector3(0, 2.285, 0), Vector3(0, 2.325, 0), 0.051, 12)


func _pipework() -> void:
	# A bent return on the left and a service loop on the right distinguish
	# the machine's silhouette from a rectangular pedestal.
	var left: Array[Vector3] = [Vector3(-0.75, 0.24, -0.14), Vector3(-0.75, 1.23, -0.14)]
	for index in range(1, 9):
		var angle := float(index) * PI * 0.5 / 8.0
		left.append(Vector3(-0.50 - cos(angle) * 0.25, 1.23 + sin(angle) * 0.25, -0.14))
	left.append(Vector3(-0.44, 1.48, -0.14))
	_pipe("green", left, 0.077)
	_union(Vector3(-0.75, 0.43, -0.14), Vector3.UP, 0.10)
	_union(Vector3(-0.75, 1.05, -0.14), Vector3.UP, 0.103)
	_cylinder("iron", Vector3(-0.59, 1.48, -0.14), Vector3(-0.51, 1.48, -0.14), 0.14, 16)
	var right: Array[Vector3] = [Vector3(0.72, 0.24, -0.01), Vector3(0.72, 0.88, -0.01)]
	for index in range(1, 9):
		var angle := float(index) * PI * 0.5 / 8.0
		right.append(Vector3(0.48 + cos(angle) * 0.24, 0.88 + sin(angle) * 0.24, -0.01))
	_pipe("green", right, 0.068)
	_union(Vector3(0.72, 0.36, -0.01), Vector3.UP, 0.091)
	_union(Vector3(0.72, 0.73, -0.01), Vector3.UP, 0.10)
	_cylinder("brass", Vector3(0.72, 0.71, -0.01), Vector3(0.72, 0.71, 0.22), 0.032, 12)
	_valve_wheel(Vector3(0.72, 0.71, 0.235))
	# The existing outlet is retained as the back of a short, downturned spout.
	var spout: Array[Vector3] = [Vector3(0.22, 1.03, 0.56), Vector3(0.22, 1.03, 0.68)]
	for index in range(1, 7):
		var angle := float(index) * PI * 0.5 / 6.0
		spout.append(Vector3(0.22, 0.94 + cos(angle) * 0.09, 0.68 + sin(angle) * 0.09))
	spout.append(Vector3(0.22, 0.90, 0.77))
	_pipe("brass", spout, 0.061)
	_cylinder("iron", Vector3(0.22, 0.885, 0.77), Vector3(0.22, 0.891, 0.77), 0.047, 16)
	_union(Vector3(0.22, 1.03, 0.575), Vector3.BACK, 0.085)


func _pipe(key: String, points: Array[Vector3], radius: float) -> void:
	const SIDES := 12
	var rings: Array[PackedVector3Array] = []
	var normals: Array[PackedVector3Array] = []
	var previous_tangent := Vector3.ZERO
	for index in range(points.size()):
		var direction := (points[mini(index + 1, points.size() - 1)] - points[maxi(0, index - 1)]).normalized()
		var tangent := previous_tangent - direction * previous_tangent.dot(direction)
		if tangent.length_squared() < 0.001:
			tangent = direction.cross(Vector3.FORWARD)
			if tangent.length_squared() < 0.001:
				tangent = direction.cross(Vector3.RIGHT)
		tangent = tangent.normalized()
		previous_tangent = tangent
		var binormal := direction.cross(tangent).normalized()
		var ring := PackedVector3Array()
		var ring_normals := PackedVector3Array()
		for side in range(SIDES):
			var angle := float(side) * TAU / float(SIDES)
			var normal := tangent * cos(angle) + binormal * sin(angle)
			ring.append(points[index] + normal * radius)
			ring_normals.append(normal)
		rings.append(ring)
		normals.append(ring_normals)
	for index in range(rings.size() - 1):
		for side in range(SIDES):
			var next := (side + 1) % SIDES
			_triangle(key, rings[index][side], rings[index + 1][side], rings[index + 1][next],
				normals[index][side], normals[index + 1][side], normals[index + 1][next])
			_triangle(key, rings[index][side], rings[index + 1][next], rings[index][next],
				normals[index][side], normals[index + 1][next], normals[index][next])


func _union(center: Vector3, axis: Vector3, radius: float) -> void:
	_cylinder("brass", center - axis * 0.083, center + axis * 0.083, radius, 12)
	_cylinder("new_brass", center - axis * 0.043, center + axis * 0.043, radius * 1.13, 6)
	for offset in [-0.081, -0.062, 0.060, 0.079]:
		_cylinder("iron", center + axis * offset, center + axis * (offset + 0.006), radius * 1.02, 16)


func _valve_wheel(center: Vector3) -> void:
	_ring("dark_green", center, 0.15, 0.021, 24, 6)
	for index in range(5):
		var angle := float(index) * TAU / 5.0
		_cylinder("brass", center, center + Vector3(cos(angle), sin(angle), 0) * 0.14, 0.013, 6)
	_cylinder("iron", center - Vector3.BACK * 0.015, center + Vector3.BACK * 0.018, 0.043, 6)


func _ring(key: String, center: Vector3, major: float, minor: float, segments: int, sides: int) -> void:
	for segment in range(segments):
		var a := float(segment) * TAU / float(segments)
		var b := float(segment + 1) * TAU / float(segments)
		for side in range(sides):
			var c := float(side) * TAU / float(sides)
			var d := float(side + 1) * TAU / float(sides)
			var radial_a := Vector3(cos(a), sin(a), 0)
			var radial_b := Vector3(cos(b), sin(b), 0)
			var na := radial_a * cos(c) + Vector3.BACK * sin(c)
			var nb := radial_b * cos(c) + Vector3.BACK * sin(c)
			var nc := radial_b * cos(d) + Vector3.BACK * sin(d)
			var nd := radial_a * cos(d) + Vector3.BACK * sin(d)
			var p0 := center + radial_a * major + na * minor
			var p1 := center + radial_b * major + nb * minor
			var p2 := center + radial_b * major + nc * minor
			var p3 := center + radial_a * major + nd * minor
			_triangle(key, p0, p2, p1, na, nc, nb)
			_triangle(key, p0, p3, p2, na, nd, nc)


func _service_hardware() -> void:
	# Small hinges and a proper latch frame the existing service door.
	for y in [1.38, 1.73]:
		_cylinder("iron", Vector3(-0.289, y - 0.068, 0.413), Vector3(-0.289, y + 0.068, 0.413), 0.022, 12)
		_box("brass", Vector3(-0.246, y, 0.431), Vector3(0.088, 0.05, 0.019))
		_hex_bolt(Vector3(-0.231, y, 0.446), 0.013)
	_box("iron", Vector3(0.275, 1.48, 0.432), Vector3(0.043, 0.15, 0.035))
	_cylinder("brass", Vector3(0.275, 1.42, 0.456), Vector3(0.275, 1.51, 0.456), 0.017, 10)
	# An uneven welded edge describes a repair without a text label.
	for index in range(15):
		var x := -0.331 + float(index) * 0.040
		var lift := sin(float(index) * 2.17) * 0.004
		for y in [0.440, 0.803]:
			_cylinder("iron", Vector3(x, y + lift, 0.409), Vector3(x + 0.024, y - lift, 0.409), 0.007, 5)
	for x in [-0.335, 0.238]:
		for index in range(9):
			var y := 0.45 + float(index) * 0.040
			_cylinder("iron", Vector3(x, y, 0.409), Vector3(x + 0.004, y + 0.025, 0.409), 0.007, 5)
	for x in [-0.255, 0.155]:
		for y in [0.51, 0.73]:
			_hex_bolt(Vector3(x, y, 0.431), 0.024)
	# A few irregular paint losses concentrate on handles and vulnerable edges.
	for index in range(7):
		var y := 0.38 + float(index) * 0.21
		var width := 0.012 + 0.006 * sin(float(index) * 1.7)
		_triangle("rust", Vector3(-0.502, y, 0.346), Vector3(-0.502 + width, y + 0.031, 0.346),
			Vector3(-0.502 + width * 1.5, y + 0.003, 0.346))


func _hex_bolt(center: Vector3, radius: float) -> void:
	_cylinder("iron", center - Vector3.BACK * 0.004, center + Vector3.BACK * 0.003, radius * 1.23, 14)
	_cylinder("brass", center + Vector3.BACK * 0.003, center + Vector3.BACK * 0.022, radius, 6)
	_box("iron", center + Vector3.BACK * 0.0225, Vector3(radius * 0.94, 0.006, 0.0015))


func _pressure_gauge() -> void:
	var center := Vector3(0.265, 1.855, 0.470)
	_cylinder("iron", center - Vector3.BACK * 0.047, center + Vector3.BACK * 0.027, 0.134, 32)
	_cylinder("dial", center + Vector3.BACK * 0.028, center + Vector3.BACK * 0.029, 0.117, 32)
	_ring("brass", center + Vector3.BACK * 0.030, 0.126, 0.008, 32, 6)
	for index in range(25):
		var angle := deg_to_rad(225.0 - float(index) * 11.25)
		var radial := Vector3(cos(angle), sin(angle), 0)
		var tangent := Vector3(-sin(angle), cos(angle), 0) * (0.0021 if index % 2 == 0 else 0.0013)
		var start := 0.080 if index % 2 == 0 else 0.091
		var a := center + radial * start + Vector3.BACK * 0.0305
		var b := center + radial * 0.107 + Vector3.BACK * 0.0305
		_quad("dial_ink", a - tangent, a + tangent, b + tangent, b - tangent)
	# Arc labels are geometry: no external font texture or extra label draws.
	# A fixed scale under the needle is intentionally free of fake telemetry.
	_box("dial_ink", center + Vector3(0, -0.061, 0.031), Vector3(0.029, 0.006, 0.001))
	_box("dial_ink", center + Vector3(0, -0.073, 0.031), Vector3(0.044, 0.003, 0.001))
	_cylinder("iron", center + Vector3.BACK * 0.033, center + Vector3.BACK * 0.040, 0.013, 16)
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	surface.set_material(_materials["needle"])
	surface.set_normal(Vector3.BACK)
	surface.add_vertex(Vector3(-0.006, -0.019, 0))
	surface.add_vertex(Vector3(0, 0.095, 0))
	surface.add_vertex(Vector3(0.006, -0.019, 0))
	_needle = MeshInstance3D.new()
	_needle.name = "PressureNeedle"
	_needle.position = center + Vector3.BACK * 0.036
	_needle.mesh = surface.commit()
	add_child(_needle)


func _box(key: String, center: Vector3, size: Vector3) -> void:
	var a := center - size * 0.5
	var b := center + size * 0.5
	_quad(key, Vector3(a.x, a.y, b.z), Vector3(a.x, b.y, b.z), Vector3(b.x, b.y, b.z), Vector3(b.x, a.y, b.z))
	_quad(key, Vector3(b.x, a.y, a.z), Vector3(b.x, b.y, a.z), Vector3(a.x, b.y, a.z), Vector3(a.x, a.y, a.z))
	_quad(key, Vector3(a.x, a.y, a.z), Vector3(a.x, b.y, a.z), Vector3(a.x, b.y, b.z), Vector3(a.x, a.y, b.z))
	_quad(key, Vector3(b.x, a.y, b.z), Vector3(b.x, b.y, b.z), Vector3(b.x, b.y, a.z), Vector3(b.x, a.y, a.z))
	_quad(key, Vector3(a.x, b.y, b.z), Vector3(a.x, b.y, a.z), Vector3(b.x, b.y, a.z), Vector3(b.x, b.y, b.z))


func _finish() -> void:
	for key: String in _surfaces:
		var mesh := (_surfaces[key] as SurfaceTool).commit()
		var instance := MeshInstance3D.new()
		instance.name = "PumpDetail_" + key
		instance.mesh = mesh
		instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		add_child(instance)
	_surfaces.clear()
