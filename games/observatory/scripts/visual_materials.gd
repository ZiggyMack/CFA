extends RefCounted
## Selected CC0 photo materials. UVs are in meters, shared across mesh batches.

static func apply(materials: Dictionary) -> void:
	materials["paving"] = _photo("stone_floor", Color("e5ded1"), 0.19, 0.72)
	materials["stone"] = _photo("stone_wall_03", Color("e9dfc7"), 0.45, 0.28)
	materials["pale"] = _photo("stone_wall_03", Color("fff4dc"), 0.55, 0.18)
	materials["shadow_stone"] = _photo("stone_wall_03", Color("b8b5a5"), 0.45, 0.46)
	materials["wood"] = _photo("wood_planks", Color("dfc49b"), 0.48, 0.64)
	materials["dark_wood"] = _photo("wood_planks", Color("887964"), 0.48, 0.64)
	for key in ["green", "new_green", "dark_green"]:
		var paint: StandardMaterial3D = materials[key]
		paint.roughness = 0.48
		paint.metallic = 0.18
	for key in ["brass", "new_brass"]:
		var metal: StandardMaterial3D = materials[key]
		metal.roughness = 0.33
		metal.metallic = 0.72
	var lake := ShaderMaterial.new()
	lake.shader = load("res://assets/materials/lake.gdshader")
	materials["lake"] = lake
	var flowing: StandardMaterial3D = materials["water"]
	flowing.roughness = 0.2
	flowing.metallic = 0.2


static func _photo(asset: String, tint: Color, scale: float, relief: float) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	var prefix := "res://assets/materials/" + asset
	material.albedo_texture = load(prefix + "_diff_1k.jpg")
	material.albedo_color = tint
	material.normal_enabled = true
	material.normal_texture = load(prefix + "_nor_gl_1k.jpg")
	material.normal_scale = relief
	material.roughness_texture = load(prefix + "_rough_1k.jpg")
	material.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
	material.roughness = 0.94
	material.uv1_scale = Vector3.ONE * scale
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	return material


static func meter_uvs(mesh: PrimitiveMesh) -> ArrayMesh:
	var arrays := mesh.get_mesh_arrays()
	var points: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var normals: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
	var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
	for index in range(points.size()):
		var point := points[index]
		var normal := normals[index]
		if mesh is BoxMesh or absf(normal.y) > 0.99:
			if absf(normal.y) > 0.9:
				uvs[index] = Vector2(point.x, point.z * signf(normal.y))
			elif absf(normal.x) > 0.9:
				uvs[index] = Vector2(-point.z * signf(normal.x), -point.y)
			else:
				uvs[index] = Vector2(point.x * signf(normal.z), -point.y)
		elif mesh is CylinderMesh:
			uvs[index] = Vector2(uvs[index].x * TAU * maxf(mesh.bottom_radius, mesh.top_radius), -point.y)
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	var converted := ArrayMesh.new()
	converted.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	var surface := SurfaceTool.new()
	surface.create_from(converted, 0)
	surface.generate_tangents()
	return surface.commit()
