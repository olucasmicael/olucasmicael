// Cor final + reflexo na agua.
// in0 = trails (usa o canal G), in1 = blur pequeno, in2 = blur grande
// Nucleo forte -> branco levemente roxo; partes fracas e glow -> roxo
// dessaturado. Fundo fica preto.
uniform float uTime;
uniform vec3  uCore;      // cor do nucleo (branco-lilas)
uniform vec3  uGlow;      // cor do glow (roxo)
uniform float uGlowAmt;
uniform float uSat;       // saturacao final (0 = cinza, 1 = cores cheias)
uniform float uExposure;
uniform float uHorizon;   // y da linha d'agua (0 desliga o reflexo)
uniform float uReflect;   // intensidade do reflexo

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

vec3 scene(vec2 uv)
{
	float c  = texture(sTD2DInputs[0], uv).g;
	float b1 = texture(sTD2DInputs[1], uv).g;
	float b2 = texture(sTD2DInputs[2], uv).g;

	vec3 col = mix(uGlow, uCore, smoothstep(.25, 1.1, c)) * (1. - exp(-c * 1.6));
	col += uGlow * (b1 * .8 + b2 * 1.3) * uGlowAmt;
	return col;
}

void main()
{
	vec2 uv = vUV.st;
	vec3 col;

	if (uv.y >= uHorizon)
	{
		col = scene(uv);
	}
	else
	{
		float d = (uHorizon - uv.y) / max(uHorizon, 1e-4);   // 0 na linha d'agua, 1 embaixo
		float ripple = (vnoise(vec2(uv.x * 4., uv.y * 120. + uTime * 1.3)) - .5) * .035 * (.3 + d);
		float ry = uHorizon + (uHorizon - uv.y) * 1.8
		         + (vnoise(vec2(uv.x * 25., uv.y * 260. - uTime * 2.)) - .5) * .012;
		vec3 r = scene(vec2(uv.x + ripple, ry));
		float glint = smoothstep(.5, .9, vnoise(vec2(uv.x * 70., uv.y * 380. + uTime * 4.)));
		col = r * uReflect * (1. - d * .6) * (.45 + glint * .9);
	}

	col = 1. - exp(-col * uExposure);
	float l = dot(col, vec3(.2126, .7152, .0722));
	col = mix(vec3(l), col, uSat);

	// vinheta leve + grao
	vec2 v = uv - .5;
	col *= 1. - dot(v, v) * .5;
	col += (hash12(uv * 1000. + fract(uTime) * 100.) - .5) * .012;

	fragColor = TDOutputSwizzle(vec4(max(col, 0.), 1.));
}
