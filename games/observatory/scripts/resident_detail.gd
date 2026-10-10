extends Node3D
## Small, original human silhouettes for the existing resident interaction bodies.
## Local origin is the soles; the face looks toward +Z. No animation or collision.

var _materials: Dictionary = {}
var _batches: Dictionary = {}
var _vertex_counts: Dictionary = {}
var _built := false


func build(materials: Dictionary, variant: String) -> void:
	if _built:
		return
	_built = true
	var is_mara := variant.to_lower() == "mara"
	_palette(materials, is_mara)
	_body(is_mara)
	_arms(is_mara)
	_head(is_mara)
	_commit()


func _palette(source: Dictionary, is_mara: bool) -> void:
	var cloth_key := "cloth_mara" if is_mara else "cloth_ivo"
	var cloth: Color = source[cloth_key].albedo_color
	var skin: Color = source["skin"].albedo_color
	_solid("cloth", cloth)
	_solid("cloth_shadow", cloth.darkened(0.20))
	_solid("cloth_light", cloth.lightened(0.16))
	_solid("skin", skin)
	_solid("skin_shadow", skin.darkened(0.23))
	_solid("hair", Color("41372f") if is_mara else Color("56534a"))
	_solid("ivory", Color("d5cfb9"))
	_solid("ink", Color("262c29"))
	_solid("trousers", Color("484944") if is_mara else Color("454b4c"))
	_solid("brass", Color("b79b65"), 0.30)


func _solid(key: String, color: Color, metallic: float = 0.0) -> void:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.91
	material.metallic = metallic
	_materials[key] = material


func _body(is_mara: bool) -> void:
	for side in [-1.0, 1.0]:
		var step: float = 0.015 * side
		var hip := Vector3(side * 0.133, 0.66, 0)
		var knee := Vector3(side * 0.142, 0.37, step)
		var ankle := Vector3(side * 0.145, 0.14, step)
		_bone(hip, knee, 0.102, 0.084, "trousers", 10)
		_bone(knee, ankle, 0.080, 0.067, "trousers", 10)
		_ellipsoid(Vector3(side * 0.145, 0.095, 0.048 + step), Vector3(0.093, 0.092, 0.151), "ink", 12, 5)
		_ellipsoid(Vector3(side * 0.145, 0.033, 0.060 + step), Vector3(0.095, 0.029, 0.157), "ink", 12, 4)
		_bone(Vector3(side * 0.145, 0.12, step), Vector3(side * 0.145, 0.23, step), 0.078, 0.073, "ink", 10)
		for lace in range(3):
			_bone(Vector3(side * 0.145 - 0.038, 0.153 - lace * 0.008, 0.045 + lace * 0.022 + step), Vector3(side * 0.145 + 0.038, 0.153 - lace * 0.008, 0.045 + lace * 0.022 + step), 0.003, 0.003, "cloth_shadow", 5)
	# Rings contain half width, half depth, height, and fore/aft offset.
	var waist := 0.241 if is_mara else 0.26
	_loft([
		Vector4(0.275, 0.150, 0.535, 0.008),
		Vector4(0.283, 0.161, 0.68, 0.005),
		Vector4(waist, 0.143, 0.97, 0.0),
		Vector4(0.278, 0.160, 1.19, -0.006),
		Vector4(0.278, 0.143, 1.29, -0.006),
		Vector4(0.166, 0.117, 1.363, -0.007)
	], "cloth", 14)
	# An open collar, lapels, pockets, and seams give the torso an authored scale.
	_triangle("ivory", Vector3(-0.073, 1.38, 0.096), Vector3(0.073, 1.38, 0.096), Vector3(0, 1.16, 0.159), Vector3(0, 0.12, 1))
	for side in [-1.0, 1.0]:
		_quad("cloth_light", Vector3(side * 0.072, 1.376, 0.105), Vector3(side * 0.165, 1.318, 0.111), Vector3(side * 0.105, 1.17, 0.171), Vector3(side * 0.038, 1.239, 0.162), Vector3(0, 0.15, 1))
		_quad("cloth_shadow", Vector3(side * 0.091, 0.916, 0.146), Vector3(side * 0.230, 0.903, 0.129), Vector3(side * 0.223, 0.753, 0.155), Vector3(side * 0.090, 0.758, 0.175), Vector3(0, 0, 1))
		_bone(Vector3(side * 0.091, 0.916, 0.151), Vector3(side * 0.230, 0.903, 0.135), 0.004, 0.004, "cloth_light", 5)
	for button in range(4):
		_ellipsoid(Vector3(0.016, 1.119 - button * 0.134, 0.159), Vector3(0.009, 0.009, 0.006), "brass", 6, 3)
	_bone(Vector3(0, 0.553, 0.161), Vector3(0, 0.958, 0.150), 0.0035, 0.0035, "cloth_shadow", 5)
	_bone(Vector3(0, 0.961, 0.15), Vector3(0, 1.148, 0.161), 0.0035, 0.0035, "cloth_shadow", 5)
	_bone(Vector3(0, 1.344, 0), Vector3(0, 1.482, 0.002), 0.065, 0.061, "skin", 12)


func _arms(is_mara: bool) -> void:
	for side in [-1.0, 1.0]:
		var shoulder := Vector3(side * 0.271, 1.285, -0.008)
		var elbow := Vector3(side * 0.363, 1.052, 0.012)
		var wrist := Vector3(side * 0.370, 0.827, 0.037)
		if is_mara and side > 0:
			elbow = Vector3(0.375, 1.041, 0.023)
			wrist = Vector3(0.34, 0.846, 0.116)
		_bone(shoulder, elbow, 0.102, 0.076, "cloth", 12)
		_ellipsoid(shoulder + Vector3(0, -0.018, 0), Vector3(0.096, 0.095, 0.10), "cloth", 10, 5)
		_ellipsoid(elbow, Vector3(0.077, 0.072, 0.072), "cloth", 10, 5)
		_bone(elbow, wrist, 0.073, 0.050, "cloth", 12)
		var cuff_dir := (elbow - wrist).normalized()
		_bone(wrist - cuff_dir * 0.009, wrist + cuff_dir * 0.043, 0.054, 0.058, "cloth_light", 12)
		_hand(wrist - cuff_dir * 0.035, side)


func _hand(at: Vector3, side: float) -> void:
	_ellipsoid(at + Vector3(0, -0.036, 0), Vector3(0.036, 0.058, 0.026), "skin", 10, 5)
	for finger in range(4):
		var finger_x := (float(finger) - 1.5) * 0.017
		var length := 0.035 - absf(float(finger) - 1.5) * 0.004
		_bone(at + Vector3(finger_x, -0.065, 0.003), at + Vector3(finger_x, -0.065 - length, 0.006), 0.008, 0.005, "skin", 6)
	_bone(at + Vector3(-side * 0.023, -0.014, 0.013), at + Vector3(-side * 0.047, -0.046, 0.026), 0.014, 0.010, "skin", 6)


func _head(is_mara: bool) -> void:
	_loft([
		Vector4(0.047, 0.061, 1.439, 0.019),
		Vector4(0.086, 0.085, 1.481, 0.017),
		Vector4(0.113, 0.103, 1.563, 0.003),
		Vector4(0.117, 0.108, 1.643, -0.010),
		Vector4(0.101, 0.094, 1.712, -0.018),
		Vector4(0.061, 0.060, 1.749, -0.020),
		Vector4(0.011, 0.016, 1.765, -0.020)
	], "skin", 16)
	for side in [-1.0, 1.0]:
		_ellipsoid(Vector3(side * 0.120, 1.591, -0.017), Vector3(0.025, 0.036, 0.020), "skin", 10, 5)
		_ellipsoid(Vector3(side * 0.136, 1.592, -0.009), Vector3(0.007, 0.019, 0.011), "skin_shadow", 8, 4)
		_ellipsoid(Vector3(side * 0.043, 1.624, 0.094), Vector3(0.030, 0.015, 0.013), "skin_shadow", 10, 5)
		_ellipsoid(Vector3(side * 0.043, 1.625, 0.103), Vector3(0.024, 0.010, 0.006), "ivory", 10, 4)
		_ellipsoid(Vector3(side * 0.043, 1.625, 0.109), Vector3(0.008, 0.0085, 0.004), "ink", 8, 4)
		_bone(Vector3(side * 0.020, 1.654, 0.096), Vector3(side * 0.068, 1.650, 0.091), 0.005, 0.004, "hair", 5)
	# The nose has a bridge, projecting tip, and shaded underside instead of a bead.
	var bridge := Vector3(0, 1.635, 0.105)
	var tip := Vector3(0, 1.572, 0.149)
	var left := Vector3(-0.019, 1.558, 0.105)
	var right := Vector3(0.019, 1.558, 0.105)
	_triangle("skin", bridge, left, tip, Vector3(-0.6, 0.1, 1))
	_triangle("skin", bridge, tip, right, Vector3(0.6, 0.1, 1))
	_triangle("skin_shadow", left, right, tip, Vector3(0, -0.8, 0.5))
	_bone(Vector3(-0.024, 1.521, 0.111), Vector3(0, 1.518, 0.117), 0.0027, 0.003, "skin_shadow", 5)
	_bone(Vector3(0, 1.518, 0.117), Vector3(0.024, 1.521, 0.111), 0.003, 0.0027, "skin_shadow", 5)
	_hair_cap(is_mara)
	if is_mara:
		_ellipsoid(Vector3(0, 1.664, -0.143), Vector3(0.069, 0.073, 0.053), "hair", 12, 6)
		_bone(Vector3(-0.049, 1.697, -0.147), Vector3(0.039, 1.72, -0.147), 0.008, 0.008, "brass", 6)
	else:
		for side in [-1.0, 1.0]:
			_bone(Vector3(side * 0.111, 1.627, -0.006), Vector3(side * 0.110, 1.582, -0.003), 0.010, 0.008, "hair", 6)


func _hair_cap(is_mara: bool) -> void:
	var segments := 18
	var rows := 6
	for row in range(rows):
		for segment in range(segments):
			var points: Array = []
			var normals: Array = []
			for corner in [Vector2i(0, 0), Vector2i(1, 0), Vector2i(1, 1), Vector2i(0, 1)]:
				var angle := float(segment + corner.x) * TAU / segments
				var front := maxf(sin(angle), 0.0)
				var extent := lerpf(1.79 if is_mara else 1.65, 1.13, front)
				var polar := maxf(0.018, float(row + corner.y) * extent / rows)
				var unit := Vector3(sin(polar) * cos(angle), cos(polar), sin(polar) * sin(angle))
				points.append(Vector3(0, 1.622, -0.020) + unit * Vector3(0.124, 0.153, 0.118))
				normals.append((unit / Vector3(0.124, 0.153, 0.118)).normalized())
			_emit_quad("hair", points, normals)


func _loft(rings: Array, material_key: String, segments: int) -> void:
	for ring_index in range(rings.size() - 1):
		for segment in range(segments):
			var points: Array = []
			var normals: Array = []
			for corner in [Vector2i(0, 0), Vector2i(1, 0), Vector2i(1, 1), Vector2i(0, 1)]:
				var angle := float(segment + corner.x) * TAU / segments
				var index: int = ring_index + corner.y
				var ring: Vector4 = rings[index]
				points.append(_ring_point(ring, angle))
				var before: Vector4 = rings[maxi(0, index - 1)]
				var after: Vector4 = rings[mini(rings.size() - 1, index + 1)]
				var rise := _ring_point(after, angle) - _ring_point(before, angle)
				var around := Vector3(-ring.x * sin(angle), 0, ring.y * cos(angle))
				normals.append(rise.cross(around).normalized())
			_emit_quad(material_key, points, normals)
	for end in [0, rings.size() - 1]:
		var ring: Vector4 = rings[end]
		var normal := Vector3.DOWN if end == 0 else Vector3.UP
		for segment in range(segments):
			_triangle(material_key, Vector3(0, ring.z, ring.w), _ring_point(ring, float(segment) * TAU / segments), _ring_point(ring, float(segment + 1) * TAU / segments), normal)


func _ring_point(ring: Vector4, angle: float) -> Vector3:
	return Vector3(cos(angle) * ring.x, ring.z, sin(angle) * ring.y + ring.w)


func _quad(key: String, a: Vector3, b: Vector3, c: Vector3, d: Vector3, normal: Vector3) -> void:
	_emit_quad(key, [a, b, c, d], [normal, normal, normal, normal])


func _emit_quad(key: String, points: Array, normals: Array) -> void:
	var surface: SurfaceTool = _batch(key)
	var cross: Vector3 = (points[1] - points[0]).cross(points[2] - points[0])
	var indices: Array = [0, 2, 1, 0, 3, 2] if cross.dot(normals[0] + normals[1] + normals[2]) > 0 else [0, 1, 2, 0, 2, 3]
	for index in indices:
		surface.set_normal(normals[index].normalized())
		surface.set_uv(Vector2(points[index].x, points[index].y))
		surface.add_vertex(points[index])
		surface.add_index(_vertex_counts[key])
		_vertex_counts[key] += 1


func _triangle(key: String, a: Vector3, b: Vector3, c: Vector3, normal: Vector3) -> void:
	var points: Array = [a, b, c]
	var indices: Array = [0, 2, 1] if (b - a).cross(c - a).dot(normal) > 0 else [0, 1, 2]
	var surface: SurfaceTool = _batch(key)
	for index in indices:
		surface.set_normal(normal.normalized())
		surface.set_uv(Vector2(points[index].x, points[index].y))
		surface.add_vertex(points[index])
		surface.add_index(_vertex_counts[key])
		_vertex_counts[key] += 1


func _bone(from: Vector3, to: Vector3, bottom_radius: float, top_radius: float, key: String, segments: int) -> void:
	var mesh := CylinderMesh.new()
	mesh.bottom_radius = bottom_radius
	mesh.top_radius = top_radius
	mesh.height = from.distance_to(to)
	mesh.radial_segments = segments
	mesh.rings = 0
	var basis := Basis(Quaternion(Vector3.UP, (to - from).normalized()))
	_append(mesh, key, Transform3D(basis, (from + to) / 2.0))


func _ellipsoid(at: Vector3, radii: Vector3, key: String, segments: int, rings: int) -> void:
	var mesh := SphereMesh.new()
	mesh.radius = 1.0
	mesh.height = 2.0
	mesh.radial_segments = segments
	mesh.rings = rings
	_append(mesh, key, Transform3D(Basis.from_scale(radii), at))


func _append(mesh: Mesh, key: String, transform: Transform3D) -> void:
	_batch(key).append_from(mesh, 0, transform)
	_vertex_counts[key] += mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size()


func _batch(key: String) -> SurfaceTool:
	if not _batches.has(key):
		var surface := SurfaceTool.new()
		surface.begin(Mesh.PRIMITIVE_TRIANGLES)
		_batches[key] = surface
		_vertex_counts[key] = 0
	return _batches[key]


func _commit() -> void:
	for key in _batches:
		var surface: SurfaceTool = _batches[key]
		surface.index()
		var mesh: ArrayMesh = surface.commit()
		mesh.surface_set_material(0, _materials[key])
		var instance := MeshInstance3D.new()
		instance.name = "Resident_" + key
		instance.mesh = mesh
		instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		add_child(instance)
	_batches.clear()
	_vertex_counts.clear()
