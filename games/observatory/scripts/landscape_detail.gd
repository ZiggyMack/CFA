extends Node3D
## Authored landscape detail. All surfaces are visual: the existing courtyard
## remains the sole authority for collision and interaction positions.
## Geometry is batched by material; every leaf shares one small instanced mesh.

var _random := RandomNumberGenerator.new()
var _surfaces: Dictionary = {}
var _surface_materials: Dictionary = {}
var _leaf_transforms: Array[Transform3D] = []
var _leaf_colors: Array[Color] = []
var _built := false


func build(materials: Dictionary) -> void:
	if _built:
		return
	_built = true
	_random.seed = 20260912
	_prepare_materials(materials)
	_build_horizon()
	_build_observatory()
	_tree(Vector3(-10.4, 0, 9), 1.0, 0.0)
	_tree(Vector3(-10.5, 0, 5.9), 0.75, 1.7)
	_tree(Vector3(8.3, 0, -13.7), 1.2, 3.1)
	_tree(Vector3(10.0, 0, 1.1), 0.8, 0.8)
	_garden(Vector2(-10.4, 7.2), Vector2(2.3, 9.6), 104)
	_garden(Vector2(7.8, -12.8), Vector2(4.0, 4.4), 85)
	_garden(Vector2(9.7, 0.5), Vector2(1.8, 4.6), 48)
	_finish_leaves()
	_finish_surfaces()


func _prepare_materials(materials: Dictionary) -> void:
	_surface_materials["bark"] = _mat(Color("68634d"))
	_surface_materials["grass"] = _mat(Color("78805b"), true)
	_surface_materials["flowers"] = _mat(Color("b5ab81"), true)
	(_surface_materials["grass"] as StandardMaterial3D).cull_mode = BaseMaterial3D.CULL_DISABLED
	(_surface_materials["flowers"] as StandardMaterial3D).cull_mode = BaseMaterial3D.CULL_DISABLED
	_surface_materials["rock"] = materials.get("shadow_stone", _mat(Color("9b9e89")))
	_surface_materials["distant_rock"] = _mat(Color("657e77"), true)
	_surface_materials["far_terrain"] = _mat(Color("829aa1"), true)
	_surface_materials["middle_terrain"] = _mat(Color("587a7a"), true)
	_surface_materials["island"] = _mat(Color("426857"), true)
	_surface_materials["observatory_stone"] = _mat(Color("cac7af"))
	_surface_materials["observatory_roof"] = _mat(Color("6f8d83"))
	_surface_materials["observatory_shadow"] = _mat(Color("586b66"))
	_surface_materials["observatory_metal"] = _mat(Color("c9b382"))
	# Painted distance layers retain their blue/green separation under the
	# Compatibility renderer's limited highlight range. Courtyard surfaces
	# and the observatory still receive real light and shadows.
	for key in ["far_terrain", "middle_terrain", "island", "distant_rock"]:
		var material := _surface_materials[key] as StandardMaterial3D
		material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		material.albedo_color = material.albedo_color.linear_to_srgb()


func _mat(color: Color, vertex_color: bool = false) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	# Use restrained diffuse reflectance for solid-color surfaces. The old
	# bright swatches clipped in direct sun on the target Compatibility GPU.
	material.albedo_color = color.srgb_to_linear()
	material.roughness = 0.94
	material.vertex_color_use_as_albedo = vertex_color
	return material


func _surface(key: String) -> SurfaceTool:
	if not _surfaces.has(key):
		var surface := SurfaceTool.new()
		surface.begin(Mesh.PRIMITIVE_TRIANGLES)
		surface.set_material(_surface_materials[key])
		_surfaces[key] = surface
	return _surfaces[key] as SurfaceTool


func _triangle(key: String, a: Vector3, b: Vector3, c: Vector3, tint: Color = Color.WHITE) -> void:
	if (c - a).cross(b - a).length_squared() < 0.0000000001:
		return
	var surface := _surface(key)
	# Godot considers clockwise faces front-facing. Keep all authored normals
	# explicit so flat rock faces and curved branches light consistently.
	var normal := (c - a).cross(b - a).normalized()
	surface.set_normal(normal)
	surface.set_color(tint)
	surface.set_uv(Vector2.ZERO)
	surface.add_vertex(a)
	surface.set_uv(Vector2.RIGHT)
	surface.add_vertex(b)
	surface.set_uv(Vector2.ONE)
	surface.add_vertex(c)


func _quad(key: String, a: Vector3, b: Vector3, c: Vector3, d: Vector3, tint: Color = Color.WHITE) -> void:
	_triangle(key, a, b, c, tint)
	_triangle(key, a, c, d, tint)


func _branch(a: Vector3, b: Vector3, radius_a: float, radius_b: float, key: String = "bark", sides: int = 7) -> void:
	var direction := (b - a).normalized()
	var tangent := direction.cross(Vector3.FORWARD)
	if tangent.length_squared() < 0.001:
		tangent = direction.cross(Vector3.RIGHT)
	tangent = tangent.normalized()
	var binormal := direction.cross(tangent).normalized()
	for index in range(sides):
		var angle_a := TAU * float(index) / float(sides)
		var angle_b := TAU * float(index + 1) / float(sides)
		var ring_a := tangent * cos(angle_a) + binormal * sin(angle_a)
		var ring_b := tangent * cos(angle_b) + binormal * sin(angle_b)
		_quad(key, a + ring_a * radius_a, b + ring_a * radius_b,
			b + ring_b * radius_b, a + ring_b * radius_a)
		_triangle(key, b, b + ring_b * radius_b, b + ring_a * radius_b)


func _tree(origin: Vector3, size: float, turn: float) -> void:
	# Irregular forked olive-like trees: clear trunks, open branching, and
	# small elongated leaves. No opaque canopy balls or alpha overdraw.
	var fork := origin + Vector3(0.13, 1.45, -0.08) * size
	_branch(origin + Vector3(0, 0.02, 0), fork, 0.16 * size, 0.095 * size)
	for root_index in range(5):
		var root_angle := float(root_index) * TAU / 5.0 + turn
		_branch(origin + Vector3(cos(root_angle) * 0.34, 0.065, sin(root_angle) * 0.34) * size,
			origin + Vector3(0.035, 0.48, -0.01) * size, 0.043 * size, 0.065 * size)
	for limb in range(7):
		var angle := turn + float(limb) * 2.399963
		var elevation := _random.randf_range(2.6, 3.4)
		var reach := _random.randf_range(0.95, 1.50)
		var elbow := origin + Vector3(cos(angle) * reach * 0.45, 2.10 + float(limb % 3) * 0.15, sin(angle) * reach * 0.45) * size
		var tip := origin + Vector3(cos(angle) * reach, elevation, sin(angle) * reach) * size
		_branch(fork, elbow, 0.073 * size, 0.044 * size)
		_branch(elbow, tip, 0.044 * size, 0.016 * size)
		for twig in range(5):
			var twig_angle := angle + _random.randf_range(-1.3, 1.3)
			var junction := elbow.lerp(tip, 0.36 + float(twig) * 0.15)
			var twig_tip := junction + Vector3(cos(twig_angle) * _random.randf_range(0.30, 0.65),
				_random.randf_range(0.18, 0.62), sin(twig_angle) * _random.randf_range(0.30, 0.65)) * size
			_branch(junction, twig_tip, 0.015 * size, 0.004 * size, "bark", 5)
			for leaf_index in range(24):
				var leaf_angle := _random.randf_range(0.0, TAU)
				var scatter := Vector3(cos(leaf_angle) * _random.randf_range(0.06, 0.37),
					_random.randf_range(-0.19, 0.22), sin(leaf_angle) * _random.randf_range(0.06, 0.37)) * size
				var position := junction.lerp(twig_tip, _random.randf_range(0.25, 1.12)) + scatter
				var leaf_size := _random.randf_range(0.75, 1.20) * size
				var basis := Basis.from_euler(Vector3(_random.randf_range(-0.6, 0.6), leaf_angle, _random.randf_range(-0.7, 0.7)))
				_leaf_transforms.append(Transform3D(basis.scaled(Vector3.ONE * leaf_size), position))
				var shade := _random.randf_range(0.70, 1.20)
				_leaf_colors.append(Color(shade * 0.93, shade, shade * 0.86, 1.0))


func _finish_leaves() -> void:
	# One draw batch for all 3,360 leaves. Opaque double-sided geometry avoids
	# alpha-tested foliage's fill-rate cost on the original Quadro hardware.
	var leaf_material := _mat(Color("81916a"), true)
	leaf_material.cull_mode = BaseMaterial3D.CULL_DISABLED
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	surface.set_material(leaf_material)
	var points := [Vector3(-0.20, 0.015, 0), Vector3(-0.03, 0, 0.055), Vector3(0.19, 0.028, 0),
		Vector3(-0.03, 0, -0.055), Vector3(0, 0.034, 0)]
	for corner in range(4):
		surface.set_normal(Vector3.UP)
		surface.add_vertex(points[corner])
		surface.add_vertex(points[(corner + 1) % 4])
		surface.add_vertex(points[4])
	var instances := MultiMesh.new()
	instances.transform_format = MultiMesh.TRANSFORM_3D
	instances.use_colors = true
	instances.mesh = surface.commit()
	instances.instance_count = _leaf_transforms.size()
	for index in range(_leaf_transforms.size()):
		instances.set_instance_transform(index, _leaf_transforms[index])
		instances.set_instance_color(index, _leaf_colors[index])
	var canopy := MultiMeshInstance3D.new()
	canopy.name = "IndividualOliveLeaves"
	canopy.multimesh = instances
	canopy.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	add_child(canopy)


func _garden(center: Vector2, extent: Vector2, count: int) -> void:
	for index in range(count):
		var origin := Vector3(center.x + _random.randf_range(-0.48, 0.48) * extent.x, 0.067,
			center.y + _random.randf_range(-0.48, 0.48) * extent.y)
		var height := _random.randf_range(0.12, 0.32)
		var shade := _random.randf_range(0.70, 1.16)
		var tint := Color(shade, shade, shade * 0.89, 1)
		for blade in range(6):
			var angle := TAU * float(blade) / 6.0 + float(index)
			var axis := Vector3(cos(angle), 0, sin(angle))
			var side := Vector3(-sin(angle), 0, cos(angle)) * 0.018
			var base := origin + axis * 0.035
			var bend := origin + axis * height * 0.28 + Vector3.UP * height * 0.62
			var tip := origin + axis * height * 0.70 + Vector3.UP * height
			_quad("grass", base - side, bend - side * 0.55, bend + side * 0.55, base + side, tint)
			_triangle("grass", bend - side * 0.55, tip, bend + side * 0.55, tint)
		if index % 6 == 0:
			var flower_top := origin + Vector3(0.04, height * 1.35, -0.02)
			_branch(origin, flower_top, 0.009, 0.004, "grass", 4)
			for petal in range(5):
				var angle := float(petal) * TAU / 5.0
				var edge := Vector3(cos(angle), 0, sin(angle)) * 0.04
				_triangle("flowers", flower_top, flower_top + edge + Vector3(0.012, 0.008, 0.012),
					flower_top + edge - Vector3(0.012, -0.008, 0.012))
		if index % 11 == 0:
			_rock(origin - Vector3(0, 0.04, 0), Vector3(_random.randf_range(0.09, 0.24),
				_random.randf_range(0.06, 0.14), _random.randf_range(0.10, 0.22)), "rock", float(index))


func _build_horizon() -> void:
	# Long overlapping ridgelines with distinct peaks and foothills replace
	# the repeated conical primitives. All scenery is beyond the lake edge.
	_landmass(Vector3(89, -1.4, -95), Vector2(70, 46), 22.0, 0.3, "far_terrain")
	_landmass(Vector3(136, -1.4, 13), Vector2(50, 70), 17.0, 2.1, "far_terrain")
	_landmass(Vector3(88, -1.1, -67), Vector2(41, 24), 13.0, 1.4, "middle_terrain")
	_landmass(Vector3(92, -1.1, 52), Vector2(52, 31), 12.0, 4.1, "middle_terrain")
	_landmass(Vector3(49, -0.9, -45), Vector2(23, 17), 4.1, 2.7, "island")
	# Broken rock ledges below the island give the observatory a visible shore.
	for index in range(18):
		var angle := TAU * float(index) / 18.0
		var position := Vector3(49 + cos(angle) * 18.5, -0.48, -45 + sin(angle) * 12.8)
		_rock(position, Vector3(3.5, _random.randf_range(0.8, 2.0), 2.2), "distant_rock", angle)


func _landmass(origin: Vector3, extent: Vector2, peak: float, phase: float, key: String) -> void:
	const RINGS := 10
	const SEGMENTS := 44
	# Concentric irregular contour rings create rounded shorelines without a
	# flat ribbon silhouette. The top is a broad ridge, not a cone's single tip.
	for ring in range(RINGS):
		var inner := float(ring) / float(RINGS)
		var outer := float(ring + 1) / float(RINGS)
		for segment in range(SEGMENTS):
			var a := TAU * float(segment) / float(SEGMENTS)
			var b := TAU * float(segment + 1) / float(SEGMENTS)
			var p0 := _terrain_point(origin, extent, peak, phase, inner, a)
			var p1 := _terrain_point(origin, extent, peak, phase, outer, a)
			var p2 := _terrain_point(origin, extent, peak, phase, outer, b)
			var p3 := _terrain_point(origin, extent, peak, phase, inner, b)
			var normal := (p2 - p0).cross(p1 - p0).normalized()
			var light := maxf(0.0, normal.dot(Vector3(-0.4, 0.82, -0.4).normalized()))
			var shade := 0.77 + light * 0.19 + 0.035 * sin(a * 4.0 + phase) + 0.025 * inner
			_quad(key, p0, p1, p2, p3, Color(shade, shade, shade, 1))


func _terrain_point(origin: Vector3, extent: Vector2, peak: float, phase: float, radius: float, angle: float) -> Vector3:
	var irregular := 1.0 + 0.11 * sin(angle * 5.0 + phase) + 0.055 * cos(angle * 9.0 - phase)
	var x := cos(angle) * radius
	var z := sin(angle) * radius
	var profile := pow(maxf(0.0, 1.0 - radius * radius), 1.45)
	var ridge := 0.70 + 0.22 * sin(x * 5.2 + phase) + 0.14 * cos(z * 7.0 - phase) + 0.06 * sin((x + z) * 13.0)
	return origin + Vector3(x * extent.x * irregular, profile * ridge * peak, z * extent.y * irregular)


func _rock(origin: Vector3, size: Vector3, key: String, turn: float) -> void:
	var top := origin + Vector3(size.x * 0.12, size.y, -size.z * 0.10)
	for index in range(7):
		var a := float(index) * TAU / 7.0 + turn
		var b := float(index + 1) * TAU / 7.0 + turn
		var bottom_a := origin + Vector3(cos(a) * size.x, 0, sin(a) * size.z)
		var bottom_b := origin + Vector3(cos(b) * size.x, 0, sin(b) * size.z)
		var shoulder_a := origin + Vector3(cos(a) * size.x * 0.76, size.y * (0.58 + 0.12 * sin(a * 3.0)), sin(a) * size.z * 0.71)
		var shoulder_b := origin + Vector3(cos(b) * size.x * 0.76, size.y * (0.58 + 0.12 * sin(b * 3.0)), sin(b) * size.z * 0.71)
		_quad(key, bottom_a, bottom_b, shoulder_b, shoulder_a)
		_triangle(key, top, shoulder_a, shoulder_b)


func _build_observatory() -> void:
	# A destination the player can recognize from this courtyard: stepped
	# limestone terraces, a columned drum, a copper dome, and an instrument.
	var origin := Vector3(49, 2.4, -46)
	_branch(origin - Vector3.UP * 3.0, origin, 7.4, 7.4, "observatory_stone", 32)
	for level in range(3):
		var radius := 7.7 - float(level) * 0.75
		_branch(origin + Vector3(0, float(level) * 0.43, 0), origin + Vector3(0, float(level + 1) * 0.43, 0),
			radius, radius, "observatory_stone", 32)
	var drum := origin + Vector3(0, 1.29, 0)
	_branch(drum, drum + Vector3(0, 4.9, 0), 4.0, 4.0, "observatory_stone", 32)
	for index in range(16):
		var angle := TAU * float(index) / 16.0
		var radial := Vector3(cos(angle), 0, sin(angle))
		var tangent := Vector3(-sin(angle), 0, cos(angle))
		var sill := drum + radial * 4.025 + Vector3.UP * 1.9
		_quad("observatory_shadow", sill - tangent * 0.33, sill + tangent * 0.33,
			sill + tangent * 0.33 + Vector3.UP * 1.6, sill - tangent * 0.33 + Vector3.UP * 1.6)
		var column := drum + radial * 5.4
		_branch(column, column + Vector3.UP * 4.5, 0.22, 0.17, "observatory_stone", 8)
		_branch(column + Vector3.UP * 4.2, column + Vector3.UP * 4.5, 0.35, 0.35, "observatory_stone", 8)
	_branch(drum + Vector3.UP * 4.5, drum + Vector3.UP * 4.9, 5.9, 5.9, "observatory_stone", 32)
	_dome(drum + Vector3.UP * 4.9, 4.9, 3.25)
	var instrument := drum + Vector3(0, 8.0, 0)
	_branch(instrument, instrument + Vector3.UP * 1.15, 0.12, 0.10, "observatory_metal", 8)
	_branch(instrument + Vector3(-0.8, 0.75, 0.0), instrument + Vector3(1.45, 1.65, 0.0), 0.19, 0.25, "observatory_shadow", 12)
	# Low gallery on the side breaks up the otherwise symmetrical drum.
	_box("observatory_stone", origin + Vector3(6.6, 2.3, 0.5), Vector3(5.6, 2.2, 3.7))
	_box("observatory_roof", origin + Vector3(6.6, 3.47, 0.5), Vector3(6.0, 0.22, 4.1))
	for index in range(4):
		_box("observatory_shadow", origin + Vector3(4.8 + float(index) * 1.2, 2.6, 2.36), Vector3(0.55, 1.0, 0.035))


func _dome(origin: Vector3, radius: float, height: float) -> void:
	for ring in range(8):
		var elevation_a := float(ring) * PI * 0.5 / 8.0
		var elevation_b := float(ring + 1) * PI * 0.5 / 8.0
		for segment in range(32):
			var a := float(segment) * TAU / 32.0
			var b := float(segment + 1) * TAU / 32.0
			var p0 := origin + Vector3(cos(a) * cos(elevation_a) * radius, sin(elevation_a) * height, sin(a) * cos(elevation_a) * radius)
			var p1 := origin + Vector3(cos(a) * cos(elevation_b) * radius, sin(elevation_b) * height, sin(a) * cos(elevation_b) * radius)
			var p2 := origin + Vector3(cos(b) * cos(elevation_b) * radius, sin(elevation_b) * height, sin(b) * cos(elevation_b) * radius)
			var p3 := origin + Vector3(cos(b) * cos(elevation_a) * radius, sin(elevation_a) * height, sin(b) * cos(elevation_a) * radius)
			_quad("observatory_roof", p0, p3, p2, p1)
	# Fine standing seams create highlights on the copper roof.
	for rib in range(16):
		var angle := float(rib) * TAU / 16.0
		for ring in range(6):
			var a := float(ring) * PI * 0.5 / 6.0
			var b := float(ring + 1) * PI * 0.5 / 6.0
			var p0 := origin + Vector3(cos(angle) * cos(a) * radius * 1.002, sin(a) * height + 0.015, sin(angle) * cos(a) * radius * 1.002)
			var p1 := origin + Vector3(cos(angle) * cos(b) * radius * 1.002, sin(b) * height + 0.015, sin(angle) * cos(b) * radius * 1.002)
			_branch(p0, p1, 0.025, 0.025, "observatory_metal", 4)


func _box(key: String, center: Vector3, size: Vector3) -> void:
	var a := center - size * 0.5
	var b := center + size * 0.5
	_quad(key, Vector3(a.x, a.y, b.z), Vector3(a.x, b.y, b.z), Vector3(b.x, b.y, b.z), Vector3(b.x, a.y, b.z))
	_quad(key, Vector3(b.x, a.y, a.z), Vector3(b.x, b.y, a.z), Vector3(a.x, b.y, a.z), Vector3(a.x, a.y, a.z))
	_quad(key, Vector3(a.x, a.y, a.z), Vector3(a.x, b.y, a.z), Vector3(a.x, b.y, b.z), Vector3(a.x, a.y, b.z))
	_quad(key, Vector3(b.x, a.y, b.z), Vector3(b.x, b.y, b.z), Vector3(b.x, b.y, a.z), Vector3(b.x, a.y, a.z))
	_quad(key, Vector3(a.x, b.y, b.z), Vector3(a.x, b.y, a.z), Vector3(b.x, b.y, a.z), Vector3(b.x, b.y, b.z))


func _finish_surfaces() -> void:
	for key: String in _surfaces:
		var mesh := (_surfaces[key] as SurfaceTool).commit()
		var instance := MeshInstance3D.new()
		instance.name = "Landscape_" + key
		instance.mesh = mesh
		instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		add_child(instance)
	_surfaces.clear()
	_leaf_transforms.clear()
	_leaf_colors.clear()
