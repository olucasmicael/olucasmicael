// Feedback com campo de fluxo (curl noise): gera os fiapos/penas que
// escorrem das linhas. in0 = linhas, in1 = Feedback TOP (frame anterior)
// Saida: R = estado dos fiapos (so isso realimenta), G = imagem final
// (linhas + fiapos), que e o que o grade usa.
uniform float uTime;
uniform float uDecay;   // 0.9..0.98  quanto o rastro dura
uniform float uWarp;    // forca do redemoinho
uniform float uDrift;   // queda vertical (positivo = escorre pra baixo)
uniform float uSpread;  // espalhamento horizontal
uniform float uCut;     // corta o rastro fraco (evita nevoa entre linhas)
uniform float uEmit;    // quanto da linha vira faisca (0..1)

out vec4 fragColor;

float hash12(vec2 p)
{
	vec3 p3 = fract(vec3(p.xyx) * .1031);
	p3 += dot(p3, p3.yzx + 33.33);
	return fract((p3.x + p3.y) * p3.z);
}

float vnoise(vec2 p)
{
	vec2 i = floor(p), f = fract(p);
	vec2 u = f * f * (3. - 2. * f);
	return mix(mix(hash12(i), hash12(i + vec2(1, 0)), u.x),
	           mix(hash12(i + vec2(0, 1)), hash12(i + vec2(1, 1)), u.x), u.y);
}

float fbm(vec2 p)
{
	float a = .5, s = 0.;
	for (int i = 0; i < 4; i++)
	{
		s += a * vnoise(p);
		p = p * 2.07 + 17.1;
		a *= .5;
	}
	return s;
}

void main()
{
	vec2 uv = vUV.st;
	float src = texture(sTD2DInputs[0], uv).r;

	vec2 p = uv * vec2(7., 16.) + vec2(uTime * .07, uTime * .3);
	float e = .02;
	float n  = fbm(p);
	float nx = fbm(p + vec2(e, 0.));
	float ny = fbm(p + vec2(0., e));
	vec2 curl = vec2(ny - n, -(nx - n)) / e;

	vec2 off = curl * uWarp + vec2((uv.x - .3) * -uSpread, uDrift);
	vec2 q = uv + off;

	// amostra unica: sem difusao, os fiapos continuam finos
	float prev = texture(sTD2DInputs[1], q).r;

	// so pontos esparsos e brilhantes da linha soltam fiapos
	float spark = smoothstep(1. - uEmit, 1., vnoise(vec2(uv.x * 90. + uTime * 2., uv.y * 30. - uTime * 6.)));
	float wisp = max(src * spark * 2.5, prev * uDecay - uCut);

	fragColor = TDOutputSwizzle(vec4(wisp, max(src, wisp), 0., 1.));
}
