extends CharacterBody3D

var camera: Camera3D
var enabled: bool = false
var sensitivity: float = 0.0022
var speed: float = 3.4
var home: Vector3 = Vector3(0, 0.2, 9)

func _ready() -> void:
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 0.35
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.28
	capsule.height = 1.7
	var collider := CollisionShape3D.new()
	collider.shape = capsule
	collider.position.y = 0.86
	add_child(collider)
	camera = Camera3D.new()
	camera.position.y = 1.63
	camera.fov = 70.0
	camera.near = 0.08
	camera.far = 180.0
	add_child(camera)
	camera.make_current()

func _unhandled_input(event: InputEvent) -> void:
	if not enabled or Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		return
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * sensitivity)
		camera.rotation.x = clampf(camera.rotation.x - event.relative.y * sensitivity, -1.35, 1.35)

func _physics_process(delta: float) -> void:
	var direction := Vector3.ZERO
	if enabled:
		var axes := Input.get_vector("walk_left", "walk_right", "walk_forward", "walk_back")
		direction = (transform.basis * Vector3(axes.x, 0, axes.y)).normalized()
		var turn := Input.get_axis("look_right", "look_left")
		rotate_y(turn * delta * 1.5)
		var tilt := Input.get_axis("look_down", "look_up")
		camera.rotation.x = clampf(camera.rotation.x + tilt * delta, -1.35, 1.35)
	var pace := speed * (1.5 if enabled and Input.is_action_pressed("hurry") else 1.0)
	velocity.x = move_toward(velocity.x, direction.x * pace, delta * 15.0)
	velocity.z = move_toward(velocity.z, direction.z * pace, delta * 15.0)
	if not is_on_floor():
		velocity.y -= 18.0 * delta
	else:
		velocity.y = -0.2
	move_and_slide()
	if global_position.y < -8:
		return_home()

func return_home() -> void:
	global_position = home + Vector3(0, 0.12, 0)
	velocity = Vector3.ZERO
	rotation = Vector3.ZERO
	camera.rotation = Vector3.ZERO

func freeze(value: bool) -> void:
	enabled = not value
	velocity = Vector3.ZERO
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE if value else Input.MOUSE_MODE_CAPTURED
