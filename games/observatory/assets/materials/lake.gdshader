shader_type spatial;
render_mode cull_disabled;

varying vec3 world_position;

void vertex() {
	world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	vec2 p = world_position.xz;
	float ripple_a = sin(p.x * 2.8 + p.y * 1.15 + TIME * 1.1);
	float ripple_b = cos(p.x * 1.1 - p.y * 3.9 - TIME * 0.7);
	vec3 ripple_normal = normalize(vec3(ripple_a * 0.075, 1.0, ripple_b * 0.06));
	NORMAL = normalize((VIEW_MATRIX * vec4(ripple_normal, 0.0)).xyz);
	float fresnel = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0);
	vec3 deep_water = vec3(0.045, 0.18, 0.18);
	vec3 sky_reflection = vec3(0.32, 0.51, 0.56);
	ALBEDO = mix(deep_water, sky_reflection, fresnel * 0.8);
	ROUGHNESS = 0.27;
	METALLIC = 0.18;
	SPECULAR = 0.6;
}
