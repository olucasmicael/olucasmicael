// Suaviza o espectro no tempo: ataque rapido, release lento.
// in0 = espectro cru (CHOP to TOP), in1 = feedback deste mesmo TOP
uniform float uAttack;
uniform float uRelease;

out vec4 fragColor;

void main()
{
	float cur  = texture(sTD2DInputs[0], vUV.st).r;
	float prev = texture(sTD2DInputs[1], vUV.st).r;
	float k = cur > prev ? uAttack : uRelease;
	fragColor = TDOutputSwizzle(vec4(mix(prev, cur, k)));
}
