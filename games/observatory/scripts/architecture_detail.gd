extends Node3D
## Static masonry and joinery fitted to the original courtyard's collision shell.
## Every material is one mesh batch; no new collision, labels, or story state.

var _batches: Dictionary = {}
var _vertex_counts: Dictionary = {}
var _materials: Dictionary = {}
var _built := false


func build(materials: Dictionary) -> void:
	if _built:
		return
	_built = true
	_materials = materials
	_colonnade()
	_archive()
	_pump_arcade()
	_courtyard_inlay()
	_commit_batches()


func _colonnade() -> void:
	for x in [-4.3, 4.3]:
		for z in [10.9, 5.8]:
			_dressed_column(Vector3(x, 0, z), 3.7)
		_arch(Vector3(x, 2.42, 8.35), 2.55, 0.98, 0.23, 0.46, "stone", PI / 2.0)
		_cornice(Vector3(x, 3.73, 8.35), 5.8, PI / 2.0)
	_arch(Vector3(0, 2.44, 10.9), 4.3, 0.96, 0.24, 0.46, "stone")
	_cornice(Vector3(0, 3.73, 10.9), 9.2)
	# Tiny blocks beneath the cornice read as individual stones at walking distance.
	for index in range(19):
		_box(Vector3(0.14, 0.16, 0.16), Vector3(-4.05 + index * 0.45, 3.54, 10.49), "pale")
	# A rear threshold completes the rhythm, without adding a cross-wall.
	_box(Vector3(8.3, 0.013, 0.22), Vector3(0, 0.012, 5.8), "pale")
	_box(Vector3(8.3, 0.014, 0.025), Vector3(0, 0.014, 5.64), "brass")


func _archive() -> void:
	for x in [-3.5, 4.5]:
		for z in [-11.5, -16.5]:
			_dressed_column(Vector3(x, 0, z), 3.6)
		_arch(Vector3(x, 2.38, -14), 2.5, 0.97, 0.22, 0.47, "stone", PI / 2.0)
		_cornice(Vector3(x, 3.66, -14), 5.8, PI / 2.0)
	for z in [-11.5, -16.5]:
		_arch(Vector3(0.5, 2.4, z), 4.0, 0.93, 0.23, 0.48, "stone")
		_cornice(Vector3(0.5, 3.66, z), 8.8)
	# An open timber roof gives real stripes of sunlight and still admits the sky.
	for index in range(10):
		_box(Vector3(8.15, 0.14, 0.19), Vector3(0.5, 4.055, -16.35 + index * 0.53), "dark_wood")
	for x in [-2.95, 3.95]:
		_box(Vector3(0.18, 0.20, 5.6), Vector3(x, 4.12, -14), "wood")
	_box(Vector3(8.65, 0.30, 0.62), Vector3(0.5, 0.15, -16.96), "stone")
	_box(Vector3(8.65, 0.12, 0.65), Vector3(0.5, 3.48, -16.96), "pale")
	_window(Vector3(0.5, 2.19, -16.707), 1.6, 1.86)
	_for_each_shelf()
	# A masonry oculus and brass tracery give the archive a readable skyline.
	_arch(Vector3(0.5, 4.64, -16.5), 0.54, 0.54, 0.13, 0.28, "pale", 0.0, TAU, 40)
	_disc(Vector3(0.5, 4.64, -16.49), 0.535, 0.07, "dark_green", Basis(Vector3.RIGHT, PI / 2.0))
	_arch(Vector3(0.5, 4.64, -16.44), 0.42, 0.42, 0.026, 0.045, "brass", 0.0, TAU, 36)
	_box(Vector3(0.84, 0.035, 0.055), Vector3(0.5, 4.64, -16.40), "brass")
	_box(Vector3(0.035, 0.84, 0.055), Vector3(0.5, 4.64, -16.40), "brass")
	_box(Vector3(1.45, 0.15, 0.53), Vector3(0.5, 4.02, -16.5), "pale")


func _pump_arcade() -> void:
	for z in [-7.5, -3.5, 4.5]:
		_dressed_column(Vector3(-5.1, 0, z), 3.1)
	_arch(Vector3(-5.1, 2.32, -5.5), 2.0, 0.48, 0.21, 0.43, "stone", PI / 2.0)
	_arch(Vector3(-5.1, 2.32, 0.5), 4.0, 0.48, 0.21, 0.43, "stone", PI / 2.0)
	_cornice(Vector3(-5.1, 3.16, -1.5), 13.2, PI / 2.0)
	_cornice(Vector3(-8.65, 3.16, -7.8), 7.3)
	# Copings and plinths cover the original shell edges; nothing crosses a route.
	_box(Vector3(0.70, 0.26, 13.15), Vector3(-12, 0.13, -1.5), "stone")
	_box(Vector3(0.72, 0.14, 13.15), Vector3(-12, 3.13, -1.5), "pale")
	_box(Vector3(7.2, 0.26, 0.67), Vector3(-8.65, 0.13, -8.0), "stone")
	_box(Vector3(7.35, 0.14, 0.73), Vector3(-8.65, 1.66, 5.0), "pale")
	for z in [-4.3, 0.3, 3.3]:
		_window(Vector3(-11.72, 1.93, z), 1.14, 1.42, PI / 2.0)
	_window(Vector3(-7.15, 1.94, -7.72), 1.26, 1.44)
	# Stone bond at the unplastered edges shows scale without another full wall.
	for y in [0.49, 1.02, 1.55, 2.08, 2.61]:
		_box(Vector3(0.047, 0.022, 12.8), Vector3(-11.725, y, -1.5), "stone")
		_box(Vector3(6.95, 0.022, 0.047), Vector3(-8.65, y, -7.725), "stone")


func _dressed_column(at: Vector3, height: float) -> void:
	# The smoother shaft encloses the original eight-sided one, sharing its axis.
	_cylinder(at + Vector3(0, height / 2.0, 0), 0.245, 0.225, height - 0.35, "stone", 24)
	_cylinder(at + Vector3(0, 0.25, 0), 0.34, 0.32, 0.105, "pale", 24)
	_cylinder(at + Vector3(0, 0.345, 0), 0.29, 0.255, 0.10, "stone", 24)
	_cylinder(at + Vector3(0, height - 0.345, 0), 0.25, 0.29, 0.12, "pale", 24)
	_cylinder(at + Vector3(0, height - 0.245, 0), 0.29, 0.36, 0.09, "stone", 24)
	_box(Vector3(0.80, 0.065, 0.80), at + Vector3(0, height - 0.055, 0), "pale")
	for fraction in [0.35, 0.66]:
		_cylinder(at + Vector3(0, height * fraction, 0), 0.246, 0.246, 0.009, "shadow_stone", 24)


func _cornice(at: Vector3, length: float, yaw: float = 0.0) -> void:
	_box(Vector3(length, 0.09, 0.78), at + Vector3(0, 0.21, 0), "stone", yaw)
	_box(Vector3(length + 0.13, 0.095, 0.92), at + Vector3(0, 0.30, 0), "pale", yaw)
	_box(Vector3(length - 0.05, 0.045, 0.73), at + Vector3(0, 0.14, 0), "brass", yaw)


func _window(at: Vector3, width: float, height: float, yaw: float = 0.0) -> void:
	var basis := Basis(Vector3.UP, yaw)
	# A dark inset and projecting jambs imply depth inside the existing solid wall.
	_box(Vector3(width, height, 0.035), at, "ink", yaw)
	_box(Vector3(width - 0.12, height - 0.12, 0.035), at + basis * Vector3(0, 0, 0.025), "dark_green", yaw)
	for side in [-1.0, 1.0]:
		_box(Vector3(0.15, height + 0.20, 0.22), at + basis * Vector3(side * (width + 0.12) / 2.0, 0, 0.055), "pale", yaw)
	_box(Vector3(width + 0.43, 0.14, 0.34), at + basis * Vector3(0, -height / 2.0 - 0.075, 0.12), "stone", yaw)
	_box(Vector3(width + 0.32, 0.18, 0.26), at + basis * Vector3(0, height / 2.0 + 0.06, 0.075), "pale", yaw)
	_box(Vector3(0.045, height - 0.08, 0.09), at + basis * Vector3(0, 0, 0.077), "brass", yaw)
	_box(Vector3(width - 0.07, 0.045, 0.09), at + basis * Vector3(0, height * 0.13, 0.077), "brass", yaw)
	# Recessed panels remain opaque; these are masonry detail, not new sightlines.
	_arch(at + basis * Vector3(0, height * 0.17, 0.077), width * 0.42, height * 0.27, 0.035, 0.04, "brass", yaw, PI, 16)


func _for_each_shelf() -> void:
	var book_materials: Array[String] = ["rust", "green", "cloth_ivo", "dark_wood", "paper", "dark_green"]
	for x in [-2.6, 3.6]:
		for side in [-1.0, 1.0]:
			_box(Vector3(0.09, 2.33, 0.16), Vector3(x + side * 0.6, 1.17, -15.88), "wood")
		_box(Vector3(1.40, 0.12, 0.62), Vector3(x, 2.33, -16.22), "wood")
		for row in range(3):
			var shelf_y := 0.395 + row * 0.6
			_box(Vector3(1.24, 0.065, 0.22), Vector3(x, shelf_y, -15.85), "wood")
			for book in range(9):
				var book_height := 0.31 + float((book * 3 + row) % 5) * 0.018
				var book_x: float = x - 0.44 + book * 0.11
				var book_y := shelf_y + 0.035 + book_height / 2.0
				var material_key: String = book_materials[(book + row * 2) % book_materials.size()]
				_box(Vector3(0.084, book_height, 0.048), Vector3(book_x, book_y, -15.846), material_key)
				for band in [-0.095, 0.095]:
					_box(Vector3(0.060, 0.010, 0.009), Vector3(book_x, book_y + band, -15.816), "brass")


func _courtyard_inlay() -> void:
	var at := Vector3(0.6, 0.014, 0.3)
	_floor_ring(at, 3.35, 0.030, "brass", 96)
	_floor_ring(at, 1.67, 0.025, "brass", 64)
	for index in range(32):
		var angle := float(index) * TAU / 32.0
		var length := 0.21 if index % 4 == 0 else 0.10
		var point := at + Vector3(sin(angle), 0, cos(angle)) * (3.35 - length / 2.0)
		_box(Vector3(0.027, 0.007, length), point, "brass", angle)
	for index in range(4):
		var angle := float(index) * PI / 2.0
		var basis := Basis(Vector3.UP, angle)
		var tip := at + basis * Vector3(0, 0.002, 3.01)
		var left := at + basis * Vector3(-0.17, 0.002, 2.4)
		var back := at + basis * Vector3(0, 0.002, 2.58)
		var right := at + basis * Vector3(0.17, 0.002, 2.4)
		_quad("pale", tip, left, back, right, Vector3.UP)


func _floor_ring(at: Vector3, radius: float, width: float, material_key: String, segments: int) -> void:
	for index in range(segments):
		var a := float(index) * TAU / segments
		var b := float(index + 1) * TAU / segments
		var first := Vector3(cos(a), 0, sin(a))
		var second := Vector3(cos(b), 0, sin(b))
		_quad(material_key, at + first * radius, at + second * radius, at + second * (radius - width), at + first * (radius - width), Vector3.UP)


func _arch(at: Vector3, half_width: float, rise: float, thickness: float, depth: float, material_key: String, yaw: float = 0.0, extent: float = PI, segments: int = 28) -> void:
	var basis := Basis(Vector3.UP, yaw)
	var full_ring := is_equal_approx(extent, TAU)
	for index in range(segments):
		# Mortar-sized gaps make individual voussoirs legible, not a smooth tube.
		var gap := 0.003 if not full_ring else 0.0005
		var a := float(index) * extent / segments + gap
		var b := float(index + 1) * extent / segments - gap
		var ia := Vector3(cos(a) * half_width, sin(a) * rise, -depth / 2.0)
		var ib := Vector3(cos(b) * half_width, sin(b) * rise, -depth / 2.0)
		var oa := Vector3(cos(a) * (half_width + thickness), sin(a) * (rise + thickness), -depth / 2.0)
		var ob := Vector3(cos(b) * (half_width + thickness), sin(b) * (rise + thickness), -depth / 2.0)
		var offset := Vector3(0, 0, depth)
		var front := basis * Vector3.FORWARD
		_quad_transformed(material_key, ia, ib, ob, oa, front, basis, at)
		_quad_transformed(material_key, oa + offset, ob + offset, ib + offset, ia + offset, -front, basis, at)
		var inner_normal := basis * -Vector3(cos((a + b) / 2.0) / half_width, sin((a + b) / 2.0) / rise, 0).normalized()
		_quad_transformed(material_key, ib, ia, ia + offset, ib + offset, inner_normal, basis, at)
		_quad_transformed(material_key, oa, ob, ob + offset, oa + offset, -inner_normal, basis, at)
		var edge_a := basis * Vector3(sin(a), -cos(a), 0)
		var edge_b := basis * Vector3(-sin(b), cos(b), 0)
		_quad_transformed(material_key, ia, oa, oa + offset, ia + offset, edge_a, basis, at)
		_quad_transformed(material_key, ob, ib, ib + offset, ob + offset, edge_b, basis, at)


func _quad_transformed(material_key: String, a: Vector3, b: Vector3, c: Vector3, d: Vector3, normal: Vector3, basis: Basis, origin: Vector3) -> void:
	_quad(material_key, origin + basis * a, origin + basis * b, origin + basis * c, origin + basis * d, normal)


func _quad(material_key: String, a: Vector3, b: Vector3, c: Vector3, d: Vector3, normal: Vector3) -> void:
	var surface: SurfaceTool = _batch(material_key)
	var points: Array[Vector3] = [a, b, c, d]
	var uvs: Array[Vector2] = [Vector2.ZERO, Vector2(a.distance_to(b), 0), Vector2(a.distance_to(b), b.distance_to(c)), Vector2(0, b.distance_to(c))]
	# Godot uses clockwise front faces, independently of explicit lighting normals.
	var indices: Array = [0, 2, 1, 0, 3, 2] if (b - a).cross(c - a).dot(normal) > 0.0 else [0, 1, 2, 0, 2, 3]
	for index in indices:
		surface.set_normal(normal.normalized())
		surface.set_uv(uvs[index])
		surface.add_vertex(points[index])
		# Primitive meshes append indexed vertices, so handmade faces need indices too.
		surface.add_index(_vertex_counts[material_key])
		_vertex_counts[material_key] += 1


func _box(size: Vector3, at: Vector3, material_key: String, yaw: float = 0.0) -> void:
	var mesh := BoxMesh.new()
	mesh.size = size
	_append_mesh(mesh, material_key, Transform3D(Basis(Vector3.UP, yaw), at))


func _cylinder(at: Vector3, bottom: float, top: float, height: float, material_key: String, segments: int = 24) -> void:
	var mesh := CylinderMesh.new()
	mesh.bottom_radius = bottom
	mesh.top_radius = top
	mesh.height = height
	mesh.radial_segments = segments
	mesh.rings = 1
	_append_mesh(mesh, material_key, Transform3D(Basis.IDENTITY, at))


func _disc(at: Vector3, radius: float, depth: float, material_key: String, basis: Basis) -> void:
	var mesh := CylinderMesh.new()
	mesh.bottom_radius = radius
	mesh.top_radius = radius
	mesh.height = depth
	mesh.radial_segments = 40
	mesh.rings = 1
	_append_mesh(mesh, material_key, Transform3D(basis, at))


func _append_mesh(mesh: Mesh, material_key: String, transform: Transform3D) -> void:
	var arrays := mesh.surface_get_arrays(0)
	var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var normals: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
	var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
	# Primitive UVs are atlases, rather than meters. Match the handmade masonry
	# faces so ordinary repeating textures have one consistent physical scale.
	if mesh is BoxMesh:
		var half_size: Vector3 = mesh.size / 2.0
		for index in range(vertices.size()):
			var point: Vector3 = vertices[index] + half_size
			var normal: Vector3 = normals[index].abs()
			if normal.x > 0.9:
				uvs[index] = Vector2(point.z, point.y)
			elif normal.y > 0.9:
				uvs[index] = Vector2(point.x, point.z)
			else:
				uvs[index] = Vector2(point.x, point.y)
	elif mesh is CylinderMesh:
		var radius: float = (mesh.top_radius + mesh.bottom_radius) / 2.0
		var slant_ratio: float = sqrt(mesh.height * mesh.height + pow(mesh.top_radius - mesh.bottom_radius, 2.0)) / mesh.height
		for index in range(vertices.size()):
			var point: Vector3 = vertices[index]
			if absf(normals[index].y) > 0.999:
				uvs[index] = Vector2(point.x + radius, point.z + radius)
			else:
				# Native U preserves the duplicate seam's distinct 0 and 1 values.
				uvs[index] = Vector2(uvs[index].x * TAU * radius, (mesh.height / 2.0 - point.y) * slant_ratio)
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	var metric_mesh := ArrayMesh.new()
	metric_mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	_batch(material_key).append_from(metric_mesh, 0, transform)
	_vertex_counts[material_key] += vertices.size()


func _batch(material_key: String) -> SurfaceTool:
	if not _batches.has(material_key):
		var surface := SurfaceTool.new()
		surface.begin(Mesh.PRIMITIVE_TRIANGLES)
		_batches[material_key] = surface
		_vertex_counts[material_key] = 0
	return _batches[material_key]


func _commit_batches() -> void:
	for material_key in _batches:
		var surface: SurfaceTool = _batches[material_key]
		surface.generate_tangents()
		surface.index()
		var mesh: ArrayMesh = surface.commit()
		mesh.surface_set_material(0, _materials[material_key])
		var instance := MeshInstance3D.new()
		instance.name = "Architecture_" + material_key
		instance.mesh = mesh
		instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		add_child(instance)
	_batches.clear()
	_vertex_counts.clear()
