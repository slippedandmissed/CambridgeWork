#version 140

in vec3 frag_texcoord;			// texture UV coordinates

out vec3 color;			        // pixel colour

uniform samplerCube skybox; 		  // Cubemap texture sampler

// Tone mapping and display encoding combined
vec3 tonemap(vec3 linearRGB)
{
    float L_white = 0.7; // Controls the brightness of the image

    float inverseGamma = 1./2.2;
    return pow(linearRGB/L_white, vec3(inverseGamma)); // Display encoding - a gamma
}

void main()
{

	vec3 linear_color = vec3(1,1,1);
	linear_color = texture(skybox, frag_texcoord).rgb;

	color = tonemap(linear_color);
}

