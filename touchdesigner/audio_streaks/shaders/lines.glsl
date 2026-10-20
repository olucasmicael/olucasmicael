// Linhas horizontais de luz, uma por banda de frequencia (grave embaixo).
// Ao longo do X cada linha "desdobra" as sub-frequencias da sua banda,
// por isso ela quebra em segmentos com brilhos diferentes.
// in0 = espectro suavizado
uniform float uTime;
uniform float uGain;
uniform float uRows;
uniform vec2  uRange;   // y da linha de baixo e da de cima (0..1)
uniform float uThick;   // espessura do nucleo em pixels
uniform float uTilt;    // compensa agudos (espectro cai nas altas)
uniform float uLogIn;   // 1 se o Audio Spectrum CHOP ja entrega o eixo em log

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

// f: 0..1 em escala log (~30 Hz .. ~13 kHz a 44.1 kHz)
float spec(float f)
{
	f = clamp(f, 0., 1.);
	float x = uLogIn > .5 ? f : exp(mix(log(0.0015), log(0.6), f));
	float a = texture(sTD2DInputs[0], vec2(x, 0.25)).r;
	float b = texture(sTD2DInputs[0], vec2(x, 0.75)).r;
	return max(a, b) * (1. + f * uTilt);
}

float compress(float v) { return 1. - exp(-v * uGain); }

void main()
{
	vec2 uv = vUV.st;
	float resY = uTDOutputInfo.res.w;
	float sp = (uRange.y - uRange.x) / max(uRows - 1., 1.);
	float fi = (uv.y - uRange.x) / sp;

	float acc = 0.;
	for (int k = -1; k <= 1; k++)
	{
		float i = floor(fi + .5) + float(k);
		if (i < 0. || i > uRows - 1.)
			continue;

		float yc = uRange.x + i * sp;
		float r  = hash12(vec2(i, 7.31));
		float lo = i / uRows;
		float hi = (i + 1.) / uRows;

		// energia media da banda -> comprimento da linha
		float eBand = 0.;
		for (int s = 0; s < 6; s++)
			eBand += spec(mix(lo, hi, (float(s) + .5) / 6.));
		eBand = compress(eBand / 6.);

		// sub-frequencia ao longo do X -> brilho local
		float eX = compress(spec(mix(lo, hi, uv.x)));

		float len  = .04 + eBand * (0.95 + r * .25);
		float mask = smoothstep(len, len - .12, uv.x);

		// quebra em segmentos quando a banda esta fraca
		float seg = smoothstep(.3, .55, vnoise(vec2(uv.x * 7. + i * 13.7, uTime * .25 + r * 9.)));
		seg = mix(seg, 1., clamp(eBand * 1.3, 0., 1.));

		float wob = (vnoise(vec2(uv.x * 5. + uTime * .6, i * 3.1)) - .5) * .008 * (.4 + eBand);
		float dy  = (uv.y - yc - wob) * resY;
		float w   = uThick * (.6 + 1.8 * eX);
		float core = exp(-dy * dy / (w * w));
		float halo = exp(-abs(dy) / (uThick * 5.));

		float flick = .7 + .6 * vnoise(vec2(uv.x * 45. - uTime * 3., i * 11.));

		acc += (core + .03 * halo) * mask * seg * flick * (.2 + 1.4 * eX) * (.3 + eBand);
	}

	fragColor = TDOutputSwizzle(vec4(vec3(acc), 1.));
}
