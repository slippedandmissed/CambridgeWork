#version 140
#define PI 3.1415926538

in vec3 wc_frag_normal;        	// fragment normal in world coordinates (wc_)
in vec2 frag_texcoord;			// texture UV coordinates
in vec3 wc_frag_pos;			// fragment position in world coordinates

out vec3 color;			        // pixel colour

uniform sampler2D tex;  		  // 2D texture sampler
uniform samplerCube skybox;		  // Cubemap texture used for reflections
uniform vec3 wc_camera_position;  // Position of the camera in world coordinates

// Tone mapping and display encoding combined
vec3 tonemap(vec3 linearRGB)
{
    float L_white = 0.7; // Controls the brightness of the image

    float inverseGamma = 1./2.2;
    return pow(linearRGB/L_white, vec3(inverseGamma)); // Display encoding - a gamma
}



void main()
{
	vec3 C_diff = texture(tex, frag_texcoord).xyz;
	vec3 C_spec = vec3(1.0, 1.0, 1.0);
	vec3 I_a = vec3(1.0, 1.0, 1.0) * 0.1;
	float k_d = 0.8;
	float k_s = 1.2;
	float alpha = 10;
	float n1 = 1;
	float n2 = 1.517;

	vec3 light_source = vec3(1,3,4);
	vec3 light_color = vec3(0.7, 0.9, 1.0);
	float intensity = 80;

	float distance_to_light = length(light_source - wc_frag_pos);
	vec3 I = light_color * intensity / (4 * PI * distance_to_light * distance_to_light);
	vec3 l = normalize(light_source - wc_frag_pos);
	vec3 r = reflect(l, wc_frag_normal);
	vec3 v = normalize(wc_frag_pos - wc_camera_position);

	vec3 ambient = C_diff * I_a;
	vec3 diffuse = C_diff * k_d * I * max(0, dot(wc_frag_normal, l));
	vec3 specular = C_spec * k_s * I * pow(max(0, dot(r, v)), alpha);


	vec3 reflection_direction = reflect(v, wc_frag_normal);
	vec3 refraction_direction = refract(v, wc_frag_normal, n1/n2);

	float cosThetaI = dot(v, wc_frag_normal);
	float cosThetaT = dot(refraction_direction, wc_frag_normal);

	float R_s = pow(((n1 * cosThetaI) - (n2 * cosThetaT))/((n1 * cosThetaI) + (n2 * cosThetaT)), 2);
	float R_p = pow(((n1 * cosThetaT) - (n2 * cosThetaI))/((n1 * cosThetaT) + (n2 * cosThetaI)), 2);

	float F_R = 0.5 * (R_s + R_p);
	float F_T = 1 - F_R;

	vec3 reflection = texture(skybox, reflection_direction).xyz * F_R;
	vec3 refraction = texture(skybox, refraction_direction).xyz * F_T;



	vec3 linear_color = ambient + diffuse + specular + reflection + refraction;


	color = tonemap(linear_color);
}

