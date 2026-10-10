extends Node3D
## Authored courtyard with shared photo materials and batched architectural detail.
## Positions in hotspots are world coordinates; this builder stays at the origin.

const VisualMaterials = preload("res://scripts/visual_materials.gd")

var hotspots: Array[Dictionary] = []
var _materials: Dictionary = {}
var _mara: Node3D
var _ivo: Node3D
var _buckets: Node3D
var _flow: Node3D
var _crossing_repairs: Node3D
var _pump_lamp: MeshInstance3D
var _pump_detail: Node3D
var _built := false


func spawn_position() -> Vector3:
	return Vector3(0.0, 0.0, 9.0)


func build() -> void:
	if _built:
		return
	_built = true
	_make_materials()
	_build_ground_and_horizon()
	_build_courtyard()
	_build_pump_room()
	_build_archive()
	_build_lakeside()
	_build_residents()
	var architecture = preload("res://scripts/architecture_detail.gd").new()
	add_child(architecture)
	architecture.build(_materials)
	var landscape = preload("res://scripts/landscape_detail.gd").new()
	add_child(landscape)
	landscape.build(_materials)
	_pump_detail = preload("res://scripts/pump_detail.gd").new()
	get_node("CommunalPump").add_child(_pump_detail)
	_pump_detail.build(_materials)
	update_story(false, "hauling")


func update_story(water_restored: bool, settlement_phase: String) -> void:
	if not _built:
		return
	_flow.visible = water_restored
	if is_instance_valid(_pump_detail):
		_pump_detail.set_water_restored(water_restored)
	_pump_lamp.material_override = _materials["water"] if water_restored else _materials["rust"]
	var working_at_crossing := water_restored and settlement_phase == "crossing"
	_buckets.visible = not working_at_crossing
	_crossing_repairs.visible = working_at_crossing
	if working_at_crossing:
		_mara.position = Vector3(7.2, 0.0, -6.0)
		_ivo.position = Vector3(9.0, 0.0, -8.1)
		_mara.rotation.y = -PI / 2.0
		_ivo.rotation.y = PI / 2.0
	else:
		_mara.position = Vector3(2.7, 0.0, 2.8)
		_ivo.position = Vector3(-1.5, 0.0, 0.4)
		_mara.rotation.y = -0.5
		_ivo.rotation.y = 0.5
	_set_hotspot_position("resident_mara", _mara.position + Vector3(0, 1.15, 0))
	_set_hotspot_position("resident_ivo", _ivo.position + Vector3(0, 1.15, 0))


func _make_materials() -> void:
	_material("stone", Color("c8bfa3"))
	_material("pale", Color("e2d7b9"))
	_material("shadow_stone", Color("9b9e89"))
	_material("green", Color("527d73"))
	_material("new_green", Color("7ca396"))
	_material("dark_green", Color("324e4b"))
	_material("brass", Color("c19b58"), 0.35)
	_material("new_brass", Color("e3c57d"), 0.45)
	_material("rust", Color("9d6450"))
	_material("wood", Color("867657"))
	_material("dark_wood", Color("544d3e"))
	_material("grass", Color("37422d"))
	_material("leaf", Color("566f63"))
	_material("leaf_light", Color("7e9072"))
	_material("hill", Color("718886"))
	_material("far_hill", Color("9daaa0"))
	_material("water", Color("69a6a0"), 0.15)
	_material("lake", Color("628d88"), 0.05)
	_material("cloth_mara", Color("9c7860"))
	_material("cloth_ivo", Color("637b91"))
	_material("skin", Color("bfaa87"))
	_material("ink", Color("253e3b"))
	_material("paper", Color("efe1b7"))
	VisualMaterials.apply(_materials)


func _material(key: String, color: Color, metal: float = 0.0) -> void:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.82
	material.metallic = metal
	_materials[key] = material


func _build_ground_and_horizon() -> void:
	# A single solid floor provides continuous, level movement throughout the visit.
	_box(self, "Ground", Vector3(25, 0.6, 32), Vector3(-0.5, -0.3, -2.5), "paving", true)
	_box(self, "Lake", Vector3(140, 0.12, 220), Vector3(82, -0.38, -30), "lake")
	_box(self, "WestGarden", Vector3(2.6, 0.06, 10), Vector3(-10.4, 0.03, 7.2), "grass")
	_box(self, "NorthGarden", Vector3(4.3, 0.06, 4.7), Vector3(7.8, 0.03, -12.8), "grass")
	_box(self, "EastGarden", Vector3(2.1, 0.06, 5), Vector3(9.7, 0.03, 0.5), "grass")
	# Low walls keep every interaction within the playable walking surface.
	_box(self, "WestBoundary", Vector3(0.5, 1.25, 32), Vector3(-12.75, 0.625, -2.5), "shadow_stone", true)
	_box(self, "EastBoundary", Vector3(0.5, 0.85, 32), Vector3(11.75, 0.425, -2.5), "pale", true)
	_box(self, "SouthBoundary", Vector3(25, 1.05, 0.5), Vector3(-0.5, 0.525, 13.25), "shadow_stone", true)
	_box(self, "NorthBoundary", Vector3(25, 1.3, 0.5), Vector3(-0.5, 0.65, -18.25), "shadow_stone", true)
	_tree(Vector3(-10.4, 0, 9), 1.0)
	_tree(Vector3(-10.5, 0, 5.9), 0.75)
	_tree(Vector3(8.3, 0, -13.7), 1.2)
	_tree(Vector3(10.0, 0, 1.1), 0.8)


func _build_courtyard() -> void:
	# Open colonnade frames the route without a roof obscuring the sky.
	for x in [-4.3, 4.3]:
		for z in [10.9, 5.8]:
			_column(Vector3(x, 0, z), 3.7)
		_box(self, "ColonnadeLintel", Vector3(0.65, 0.35, 5.8), Vector3(x, 3.72, 8.35), "pale")
	_box(self, "ArrivalArch", Vector3(9.2, 0.45, 0.7), Vector3(0, 3.72, 10.9), "pale")
	_label(self, "THE OBSERVATORY", Vector3(0, 3.07, 10.49), 38, Color("d7c79e"), false)
	# An empty shallow basin, then a clear, visible water stream after repair.
	_cylinder(self, "FountainBase", 1.4, 0.23, Vector3(0.6, 0.115, 0.3), "shadow_stone", true, 1.4, 16)
	_cylinder(self, "FountainBasin", 1.2, 0.5, Vector3(0.6, 0.39, 0.3), "pale", false, 1.32, 16)
	_cylinder(self, "DryBasin", 1.09, 0.02, Vector3(0.6, 0.65, 0.3), "shadow_stone", false, 1.09, 16)
	_cylinder(self, "FountainColumn", 0.21, 1.45, Vector3(0.6, 1.05, 0.3), "green", false, 0.21, 10)
	_cylinder(self, "FountainCrown", 0.48, 0.15, Vector3(0.6, 1.77, 0.3), "brass", false, 0.43, 12)
	_flow = _group(self, "RestoredWater")
	_cylinder(_flow, "BasinWater", 1.08, 0.025, Vector3(0.6, 0.675, 0.3), "water", false, 1.08, 16)
	for offset in [Vector3(0.3, 0, 0), Vector3(-0.3, 0, 0), Vector3(0, 0, 0.3), Vector3(0, 0, -0.3)]:
		_cylinder(_flow, "FallingWater", 0.035, 1.05, Vector3(0.6, 1.22, 0.3) + offset, "water", false, 0.026, 6)
	_buckets = _group(self, "WaterHaulingBuckets")
	_bucket(_buckets, Vector3(3.1, 0, 2.0))
	_bucket(_buckets, Vector3(3.65, 0, 2.3))
	_bucket(_buckets, Vector3(-1.9, 0, -0.35))
	_box(self, "ArrivalPlaque", Vector3(1.7, 0.65, 0.15), Vector3(2.8, 1.15, 8.0), "green", true)
	_box(self, "PlaquePost", Vector3(0.12, 1.15, 0.12), Vector3(2.8, 0.575, 8.0), "brass")
	_label(self, "WATER BEFORE\nTHE CROSSING", Vector3(2.8, 1.19, 8.10), 27, Color("efe1b7"), false)
	_hotspot("plaque", "Arrival plaque", Vector3(2.8, 1.2, 8.3), 2.0)
	_sign("PUMP ROOM", Vector3(-4.8, 2.6, 2.8))
	_sign("ARCHIVE", Vector3(3.0, 2.5, -9.8))


func _build_pump_room() -> void:
	_box(self, "PumpRoomBack", Vector3(0.5, 3.1, 13), Vector3(-12.0, 1.55, -1.5), "shadow_stone", true)
	_box(self, "PumpRoomNorth", Vector3(7.2, 3.1, 0.5), Vector3(-8.65, 1.55, -8.0), "shadow_stone", true)
	_box(self, "PumpRoomSouth", Vector3(7.2, 1.6, 0.5), Vector3(-8.65, 0.8, 5.0), "pale", true)
	for z in [-7.5, -3.5, 4.5]:
		_column(Vector3(-5.1, 0, z), 3.1)
	_box(self, "PumpRoomLintel", Vector3(0.6, 0.36, 13), Vector3(-5.1, 3.16, -1.5), "pale")
	_box(self, "PumpRoomRearLintel", Vector3(7.2, 0.36, 0.65), Vector3(-8.65, 3.16, -7.8), "pale")
	# The housing follows the first Comfy concept; the patch tells its next story.
	var pump := _group(self, "CommunalPump")
	pump.position = Vector3(-10, 0, -5.65)
	_box(pump, "Footing", Vector3(1.7, 0.18, 1.2), Vector3(0, 0.09, 0), "pale", true)
	_box(pump, "Housing", Vector3(1.0, 1.85, 0.65), Vector3(0, 1.1, 0), "green", true)
	_box(pump, "TopLip", Vector3(1.16, 0.12, 0.82), Vector3(0, 2.05, 0), "new_green")
	_box(pump, "ServicePanel", Vector3(0.55, 0.6, 0.075), Vector3(0, 1.55, 0.365), "dark_green")
	_box(pump, "ServicePanelFace", Vector3(0.46, 0.50, 0.04), Vector3(0, 1.55, 0.42), "green")
	_box(pump, "RepairPlate", Vector3(0.55, 0.34, 0.045), Vector3(-0.05, 0.62, 0.365), "brass")
	for x in [-0.255, 0.155]:
		for y in [0.51, 0.73]:
			_sphere(pump, "PatchRivet", 0.027, Vector3(x, y, 0.4), "dark_green")
	_box(pump, "WornPanelEdge", Vector3(0.028, 0.35, 0.023), Vector3(0.25, 1.57, 0.452), "brass")
	_cylinder(pump, "OldPipe", 0.082, 0.97, Vector3(-0.67, 0.66, 0), "green")
	_cylinder(pump, "NewCoupling", 0.13, 0.23, Vector3(-0.67, 1.15, 0), "new_brass")
	var fitting := _cylinder(pump, "OutletFitting", 0.12, 0.28, Vector3(0.22, 1.03, 0.48), "new_brass")
	fitting.rotation.x = PI / 2.0
	var socket := _cylinder(pump, "LeverSocket", 0.08, 0.1, Vector3(-0.24, 1.03, 0.4), "dark_green")
	socket.rotation.x = PI / 2.0
	_pump_lamp = _sphere(pump, "PressureLamp", 0.06, Vector3(0, 1.63, 0.475), "rust")
	_hotspot("pump", "Inspect the water pump", Vector3(-10, 1.3, -4.95), 2.2)
	# Distinct stations stay far enough apart to make aiming at each unambiguous.
	_box(self, "LeverPedestal", Vector3(0.65, 1.1, 0.55), Vector3(-7, 0.55, -6.0), "green", true)
	var lever := _cylinder(self, "SeparateServiceLever", 0.045, 0.55, Vector3(-7, 1.35, -6.0), "brass")
	lever.rotation.z = -0.38
	_sphere(self, "LeverGrip", 0.095, Vector3(-6.90, 1.60, -6.0), "dark_wood")
	_label(self, "SERVICE LEVER", Vector3(-7, 1.95, -6.0), 22)
	_hotspot("lever", "Service lever", Vector3(-7, 1.35, -5.75), 1.9)
	_box(self, "BypassPedestal", Vector3(0.7, 1.0, 0.6), Vector3(-7, 0.5, -1.3), "green", true)
	var bypass := _cylinder(self, "BypassWheel", 0.22, 0.07, Vector3(-7, 1.13, -1.3), "brass", false, 0.22, 10)
	bypass.rotation.x = PI / 3.0
	_label(self, "BYPASS", Vector3(-7, 1.73, -1.3), 24)
	_hotspot("bypass", "Water bypass", Vector3(-7, 1.15, -0.93), 1.9)
	_box(self, "RegulatorMount", Vector3(0.8, 1.0, 0.5), Vector3(-10.2, 0.5, -0.7), "shadow_stone", true)
	_cylinder(self, "RegulatorCollar", 0.19, 0.27, Vector3(-10.2, 1.13, -0.7), "new_brass", false, 0.19, 10)
	_label(self, "REGULATOR", Vector3(-10.2, 1.75, -0.7), 23)
	_hotspot("regulator", "Regulator fitting", Vector3(-10.2, 1.2, -0.30), 1.9)
	# These pipes show the relationship between controls without obstructing walking.
	_box(self, "LeverSupplyPipe", Vector3(0.11, 0.08, 4.7), Vector3(-7, 0.04, -3.65), "brass")
	_box(self, "RegulatorFeedPipe", Vector3(3.25, 0.08, 0.11), Vector3(-8.6, 0.04, -1.3), "green")
	_box(self, "PumpFeedPipe", Vector3(0.11, 0.08, 4.7), Vector3(-10.2, 0.04, -3.0), "green")
	_bench(self, Vector3(-9.6, 0, 3.0), 2.5, true)
	_cylinder(self, "EchoSpool", 0.22, 0.16, Vector3(-10.2, 1.02, 3.0), "brass", false, 0.22, 12)
	_box(self, "CouplerTool", Vector3(0.7, 0.12, 0.16), Vector3(-9.1, 1.0, 3.0), "new_green")
	_cylinder(self, "CouplerGrip", 0.11, 0.2, Vector3(-8.83, 1.03, 3.0), "brass")
	_label(self, "BORROW A TOOL", Vector3(-9.6, 1.65, 3.0), 25)
	_hotspot("bench", "Tool bench", Vector3(-9.6, 1.05, 3.6), 2.2)


func _build_archive() -> void:
	# The archive is an open arcade: it remains reachable whichever choice is made.
	_box(self, "ArchiveBack", Vector3(8.6, 3.6, 0.5), Vector3(0.5, 1.8, -17.0), "shadow_stone", true)
	for x in [-3.5, 4.5]:
		_column(Vector3(x, 0, -11.5), 3.6)
		_column(Vector3(x, 0, -16.5), 3.6)
		_box(self, "ArchiveSideLintel", Vector3(0.7, 0.4, 5.7), Vector3(x, 3.65, -14), "pale")
	_box(self, "ArchiveFrontLintel", Vector3(8.7, 0.45, 0.7), Vector3(0.5, 3.65, -11.5), "pale")
	_box(self, "ArchiveRearLintel", Vector3(8.7, 0.45, 0.7), Vector3(0.5, 3.65, -16.5), "pale")
	_label(self, "THE ARCHIVE", Vector3(0.5, 3.03, -11.08), 37, Color("d9c798"), false)
	_box(self, "ArchiveTable", Vector3(2.5, 0.18, 1.1), Vector3(0.8, 0.97, -14.3), "wood", true)
	for x in [-0.1, 1.7]:
		_box(self, "ArchiveTableLeg", Vector3(0.17, 0.9, 0.7), Vector3(x, 0.45, -14.3), "dark_wood")
	_box(self, "PreservedRecord", Vector3(0.82, 0.035, 0.55), Vector3(0.55, 1.085, -14.2), "paper")
	_box(self, "CorrectionRecord", Vector3(0.37, 0.04, 0.48), Vector3(1.2, 1.09, -14.2), "new_green")
	_hotspot("archive", "Read the preserved finding", Vector3(0.8, 1.25, -13.65), 2.4)
	_label(self, "A FINDING, AND ITS CORRECTION", Vector3(0.8, 1.78, -14.35), 22)
	for x in [-2.6, 3.6]:
		_box(self, "RecordShelf", Vector3(1.2, 2.25, 0.45), Vector3(x, 1.125, -16.35), "dark_green", true)
		for y in [0.6, 1.2, 1.8]:
			_box(self, "ArchiveVolumes", Vector3(0.97, 0.37, 0.40), Vector3(x, y, -16.08), "paper")
	# Return is an explicit interaction instead of a silent time trigger.
	_cylinder(self, "ReturnWaystone", 0.38, 0.78, Vector3(3.0, 0.39, -8.7), "green", true, 0.32, 8)
	_cylinder(self, "WaystoneCap", 0.36, 0.07, Vector3(3.0, 0.82, -8.7), "brass", false, 0.36, 8)
	_label(self, "RETURN TO THE COURTYARD", Vector3(3.0, 1.45, -8.7), 23)
	_hotspot("return_marker", "Return to the courtyard", Vector3(3.0, 1.0, -8.4), 2.1)


func _build_lakeside() -> void:
	_bench(self, Vector3(8.3, 0, 5.0), 2.3)
	_label(self, "A MOMENT BY THE LAKE", Vector3(8.3, 1.8, 5.0), 24)
	_hotspot("ending", "Rest by the lake", Vector3(8.3, 1.0, 5.7), 2.2)
	# The crossing extends into scenery; this chapter stops at its working approach.
	_box(self, "CrossingApproach", Vector3(5.0, 0.09, 3.1), Vector3(9.0, 0.045, -6.8), "wood")
	for z in [-8.25, -5.35]:
		_box(self, "BridgeBeam", Vector3(11, 0.23, 0.18), Vector3(15.4, -0.15, z), "dark_wood")
		for x in [10.7, 14.0, 17.3, 20.6]:
			_box(self, "CrossingPost", Vector3(0.15, 2.1, 0.15), Vector3(x, 0.2, z), "wood")
		_box(self, "CrossingHandrail", Vector3(11, 0.12, 0.12), Vector3(15.4, 1.1, z), "wood")
	for x in [10.7, 11.4, 12.1, 14.9, 15.6, 18.4, 19.1, 19.8, 20.5]:
		_box(self, "OldBridgePlank", Vector3(0.60, 0.10, 2.8), Vector3(x, 0.04, -6.8), "wood")
	_crossing_repairs = _group(self, "CrossingWorkResumed")
	for x in [12.8, 13.5, 14.2, 16.3, 17.0, 17.7]:
		_box(_crossing_repairs, "NewBridgePlank", Vector3(0.60, 0.10, 2.8), Vector3(x, 0.04, -6.8), "pale")
	for index in range(3):
		_box(self, "WaitingTimber", Vector3(2.4, 0.13, 0.4), Vector3(7.4, 0.10 + index * 0.14, -9.4), "wood")
	_label(self, "THE CROSSING", Vector3(8.8, 2.6, -8.8), 29)


func _build_residents() -> void:
	_mara = _resident("Mara", "cloth_mara")
	_ivo = _resident("Ivo", "cloth_ivo")
	_hotspot("resident_mara", "Talk to Mara", Vector3.ZERO, 2.2)
	_hotspot("resident_ivo", "Talk to Ivo", Vector3.ZERO, 2.2)


func _resident(resident_name: String, _cloth: String) -> Node3D:
	var person := _group(self, resident_name)
	var shape := CylinderShape3D.new()
	shape.radius = 0.30
	shape.height = 0.88
	_body(person, "Coat", shape, Vector3(0, 0.94, 0))
	var detail = preload("res://scripts/resident_detail.gd").new()
	person.add_child(detail)
	detail.build(_materials, resident_name)
	_label(person, resident_name, Vector3(0, 2.04, 0), 29)
	return person


func _tree(at: Vector3, size: float) -> void:
	var tree := _group(self, "CourtyardTree")
	tree.position = at
	tree.scale = Vector3.ONE * size
	# Retain the original collision shell; the landscape module supplies the tree.
	var shape := CylinderShape3D.new()
	shape.radius = 0.12
	shape.height = 2.8
	_body(tree, "Trunk", shape, Vector3(0, 1.4, 0))


func _column(at: Vector3, height: float) -> void:
	_box(self, "ColumnFoot", Vector3(0.79, 0.23, 0.79), at + Vector3(0, 0.115, 0), "pale", true)
	_cylinder(self, "Column", 0.23, height - 0.35, at + Vector3(0, height / 2.0, 0), "stone", true, 0.21, 8)
	_box(self, "ColumnCapital", Vector3(0.7, 0.22, 0.7), at + Vector3(0, height - 0.11, 0), "pale")


func _bench(parent: Node3D, at: Vector3, width: float, workbench: bool = false) -> void:
	var height := 0.90 if workbench else 0.48
	_box(parent, "BenchTop", Vector3(width, 0.14, 0.70), at + Vector3(0, height, 0), "wood", true)
	for x in [-width * 0.36, width * 0.36]:
		_box(parent, "BenchLeg", Vector3(0.14, height, 0.60), at + Vector3(x, height / 2.0, 0), "dark_green")
	if not workbench:
		_box(parent, "BenchBack", Vector3(width, 0.4, 0.10), at + Vector3(0, 0.93, -0.31), "wood")


func _bucket(parent: Node3D, at: Vector3) -> void:
	_cylinder(parent, "Bucket", 0.19, 0.37, at + Vector3(0, 0.185, 0), "green", false, 0.23, 10)
	_cylinder(parent, "BucketOpening", 0.195, 0.01, at + Vector3(0, 0.378, 0), "dark_green", false, 0.195, 10)
	_box(parent, "BucketHandle", Vector3(0.45, 0.035, 0.035), at + Vector3(0, 0.5, 0), "brass")


func _sign(caption: String, at: Vector3) -> void:
	_label(self, caption, at, 29)


func _hotspot(id: String, label: String, at: Vector3, radius: float) -> void:
	hotspots.append({"id": id, "label": label, "position": at, "radius": radius})


func _set_hotspot_position(id: String, at: Vector3) -> void:
	for hotspot in hotspots:
		if hotspot["id"] == id:
			hotspot["position"] = at
			return


func _group(parent: Node3D, node_name: String) -> Node3D:
	var group := Node3D.new()
	group.name = node_name
	parent.add_child(group)
	return group


func _box(parent: Node3D, node_name: String, size: Vector3, at: Vector3, material: String, collision: bool = false) -> MeshInstance3D:
	var mesh := BoxMesh.new()
	mesh.size = size
	var instance := _instance(parent, node_name, mesh, at, material)
	if collision:
		var shape := BoxShape3D.new()
		shape.size = size
		_body(parent, node_name, shape, at)
	return instance


func _cylinder(parent: Node3D, node_name: String, radius: float, height: float, at: Vector3, material: String, collision: bool = false, top_radius: float = -1.0, segments: int = 12) -> MeshInstance3D:
	var mesh := CylinderMesh.new()
	mesh.bottom_radius = radius
	mesh.top_radius = radius if top_radius < 0.0 else top_radius
	mesh.height = height
	mesh.radial_segments = segments
	mesh.rings = 1
	var instance := _instance(parent, node_name, mesh, at, material)
	if collision:
		var shape := CylinderShape3D.new()
		shape.radius = maxf(mesh.bottom_radius, mesh.top_radius)
		shape.height = height
		_body(parent, node_name, shape, at)
	return instance


func _sphere(parent: Node3D, node_name: String, radius: float, at: Vector3, material: String) -> MeshInstance3D:
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	mesh.radial_segments = 12
	mesh.rings = 6
	return _instance(parent, node_name, mesh, at, material)


func _instance(parent: Node3D, node_name: String, mesh: Mesh, at: Vector3, material: String) -> MeshInstance3D:
	var instance := MeshInstance3D.new()
	instance.name = node_name
	instance.mesh = VisualMaterials.meter_uvs(mesh) if mesh is BoxMesh or mesh is CylinderMesh else mesh
	instance.position = at
	instance.material_override = _materials[material]
	instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF if material in ["lake", "water"] or node_name == "Ground" else GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	parent.add_child(instance)
	return instance


func _body(parent: Node3D, node_name: String, shape: Shape3D, at: Vector3) -> void:
	var body := StaticBody3D.new()
	body.name = node_name + "Collision"
	body.position = at
	var collider := CollisionShape3D.new()
	collider.shape = shape
	body.add_child(collider)
	parent.add_child(body)


func _label(parent: Node3D, caption: String, at: Vector3, font_size: int = 24, color: Color = Color("ede0bb"), billboard: bool = true) -> void:
	var label := Label3D.new()
	label.name = "WayfindingLabel"
	label.visibility_range_begin = 2.0 if billboard else 0.0
	label.visibility_range_end = 7.0 if billboard else 18.0
	label.visibility_range_end_margin = 1.5
	label.text = caption
	label.font_size = font_size
	label.pixel_size = 0.004 if billboard else 0.007
	label.position = at
	label.modulate = color
	label.outline_modulate = Color("293f3d")
	label.outline_size = 5
	label.no_depth_test = false
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED if billboard else BaseMaterial3D.BILLBOARD_DISABLED
	parent.add_child(label)
