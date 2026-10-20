"""
Monta no TouchDesigner a rede "audio_streaks": linhas de luz horizontais que
reagem a musica, com fiapos de feedback, glow branco-roxo dessaturado, fundo
preto e reflexo na agua.

Uso (Textport do TD, Alt+T):

    ROOT = r'C:/caminho/para/olucasmicael/touchdesigner/audio_streaks'
    exec(open(ROOT + '/build_audio_streaks.py', encoding='utf-8').read())

Opcional antes do exec:
    PARENT = op('/project1')   # onde criar o COMP (padrao: /project1)

Rodar de novo recria o COMP do zero. Os shaders ficam em ROOT/shaders e os
Text DATs ficam sincronizados com os arquivos: edite o .glsl e o TD recarrega.
"""

import os

ROOT = globals().get('ROOT')
if not ROOT or not os.path.isdir(os.path.join(ROOT, 'shaders')):
    raise RuntimeError('Defina ROOT com a pasta touchdesigner/audio_streaks antes do exec().')
SHADERS = os.path.join(ROOT, 'shaders').replace('\\', '/')
PARENT = globals().get('PARENT') or op('/project1')
NAME = 'audio_streaks'
TAG = '[audio_streaks]'


class Expr(str):
    """Marca um valor como expressao Python do parametro."""


def setp(o, **kw):
    for name, value in kw.items():
        p = getattr(o.par, name, None)
        if p is None:
            print(TAG, 'aviso: %s nao tem o parametro %s' % (o.path, name))
            continue
        try:
            if isinstance(value, Expr):
                p.expr = str(value)
            else:
                p.val = value
        except Exception as e:
            print(TAG, 'aviso: %s.par.%s = %r falhou: %s' % (o.path, name, value, e))


def uniforms(glsl, items):
    """items: lista de (nome, valor ou tupla de valores/Expr).

    O GLSL TOP mudou de nome de parametro entre versoes do TD: as novas usam
    a sequencia 'vec' (vec0name, vec0valuex...), as antigas uniname0/value0x.
    """
    seq = getattr(getattr(glsl, 'seq', None), 'vec', None)
    if seq is not None:
        seq.numBlocks = max(seq.numBlocks, len(items))
        fmt_name, fmt_val = 'vec%dname', 'vec%dvalue%s'
    else:
        fmt_name, fmt_val = 'uniname%d', 'value%d%s'
    for i, (name, vals) in enumerate(items):
        if not isinstance(vals, (tuple, list)):
            vals = (vals,)
        setp(glsl, **{fmt_name % i: name})
        setp(glsl, **{fmt_val % (i, c): v for c, v in zip('xyzw', vals)})


def text_dat(comp, name, filename, x, y):
    path = SHADERS + '/' + filename
    d = comp.create(textDAT, name)
    with open(path, encoding='utf-8') as f:
        d.text = f.read()
    setp(d, file=path, syncfile=True)
    d.nodeX, d.nodeY = x, y
    return d


def glsl(comp, name, shader, inputs, x, y, custom_res=False):
    g = comp.create(glslTOP, name)
    for i, src in enumerate(inputs):
        g.inputConnectors[i].connect(src)
    dat = text_dat(comp, name + '_pixel', shader, x, y - 150)
    setp(g, pixeldat=dat.name, format='rgba16float')
    if custom_res:
        setp(g, outputresolution='custom',
             resolutionw=Expr('parent().par.Width'),
             resolutionh=Expr('parent().par.Height'))
    g.nodeX, g.nodeY = x, y
    return g


def custom_params(comp):
    page = comp.appendCustomPage('Streaks')

    def add(kind, name, label, default, lo=None, hi=None):
        pg = getattr(page, 'append' + kind)(name, label=label)
        defaults = default if isinstance(default, (tuple, list)) else (default,)
        for p, v in zip(pg, defaults):
            p.default = v
            p.val = v
            if lo is not None:
                p.normMin, p.normMax = lo, hi

    src = page.appendMenu('Source', label='Fonte de audio')[0]
    src.menuNames = ['device', 'file']
    src.menuLabels = ['Audio Device In', 'Arquivo']
    page.appendFile('File', label='Arquivo de audio')
    add('Int', 'Width', 'Largura', 1080)
    add('Int', 'Height', 'Altura', 1350)
    add('Float', 'Gain', 'Ganho do audio', 3.0, 0, 20)
    add('Float', 'Tilt', 'Realce dos agudos', 6.0, 0, 20)
    add('Float', 'Attack', 'Ataque', 0.6, 0, 1)
    add('Float', 'Release', 'Release', 0.08, 0, 1)
    add('Toggle', 'Speclog', 'Espectro ja e log', 0)
    add('Int', 'Rows', 'Linhas', 14, 2, 40)
    add('Float', 'Thick', 'Espessura (px)', 2.2, 0.5, 8)
    add('Float', 'Decay', 'Duracao dos fiapos', 0.965, 0.8, 0.995)
    add('Float', 'Warp', 'Torcao', 0.0028, 0, 0.01)
    add('Float', 'Drift', 'Queda', 0.0005, -0.003, 0.003)
    add('Float', 'Spread', 'Espalhar lateral', 0.0003, 0, 0.003)
    add('Float', 'Cut', 'Corte do rastro', 0.002, 0, 0.02)
    add('Float', 'Emit', 'Faiscas', 0.5, 0, 1)
    add('RGB', 'Core', 'Cor do nucleo', (0.97, 0.94, 1.0))
    add('RGB', 'Glowcolor', 'Cor do glow', (0.50, 0.42, 0.95))
    add('Float', 'Glow', 'Glow', 0.75, 0, 3)
    add('Float', 'Bloomsmall', 'Blur pequeno (px)', 4, 0, 40)
    add('Float', 'Bloomlarge', 'Blur grande (px)', 24, 0, 120)
    add('Float', 'Sat', 'Saturacao', 0.7, 0, 1.5)
    add('Float', 'Exposure', 'Exposicao', 1.1, 0, 4)
    add('Float', 'Horizon', 'Linha d\'agua', 0.14, 0, 0.5)
    add('Float', 'Reflect', 'Reflexo', 0.55, 0, 1.5)


def build():
    old = PARENT.op(NAME)
    if old is not None:
        old.destroy()
    comp = PARENT.create(baseCOMP, NAME)
    custom_params(comp)
    P = 'parent().par.'

    # --- audio -----------------------------------------------------------
    dev = comp.create(audiodeviceinCHOP, 'audio_device')
    dev.nodeX, dev.nodeY = 0, 300
    fil = comp.create(audiofileinCHOP, 'audio_file')
    fil.nodeX, fil.nodeY = 0, 150
    setp(fil, file=Expr(P + 'File'))

    sw = comp.create(switchCHOP, 'audio_src')
    sw.inputConnectors[0].connect(dev)
    sw.inputConnectors[1].connect(fil)
    setp(sw, index=Expr(P + 'Source.menuIndex'))
    sw.nodeX, sw.nodeY = 200, 225

    mon = comp.create(audiodeviceoutCHOP, 'audio_monitor')
    mon.inputConnectors[0].connect(fil)
    setp(mon, active=Expr(P + 'Source.menuIndex == 1'))
    mon.nodeX, mon.nodeY = 200, 50

    spec = comp.create(audiospectrumCHOP, 'spectrum')
    spec.inputConnectors[0].connect(sw)
    spec.nodeX, spec.nodeY = 400, 225

    spec_null = comp.create(nullCHOP, 'spectrum_null')
    spec_null.inputConnectors[0].connect(spec)
    spec_null.nodeX, spec_null.nodeY = 600, 225

    spec_tex = comp.create(choptoTOP, 'spectrum_tex')
    setp(spec_tex, chop=spec_null.name, format='rgba32float')
    spec_tex.nodeX, spec_tex.nodeY = 800, 225

    # --- suavizacao do espectro (feedback) -------------------------------
    spec_fb = comp.create(feedbackTOP, 'spectrum_fb')
    spec_fb.inputConnectors[0].connect(spec_tex)
    spec_fb.nodeX, spec_fb.nodeY = 1000, 100
    smooth = glsl(comp, 'spectrum_smooth', 'spec_smooth.glsl', [spec_tex, spec_fb], 1200, 225)
    setp(spec_fb, top=smooth.name)
    uniforms(smooth, [('uAttack', Expr(P + 'Attack')), ('uRelease', Expr(P + 'Release'))])

    # --- linhas ----------------------------------------------------------
    lines = glsl(comp, 'lines', 'lines.glsl', [smooth], 1400, 225, custom_res=True)
    uniforms(lines, [
        ('uTime', Expr('absTime.seconds')),
        ('uGain', Expr(P + 'Gain')),
        ('uRows', Expr(P + 'Rows')),
        ('uRange', (Expr(P + 'Horizon + 0.08'), 0.93)),
        ('uThick', Expr(P + 'Thick')),
        ('uTilt', Expr(P + 'Tilt')),
        ('uLogIn', Expr(P + 'Speclog')),
    ])

    # --- fiapos (feedback com curl noise) --------------------------------
    fb = comp.create(feedbackTOP, 'trails_fb')
    fb.inputConnectors[0].connect(lines)
    fb.nodeX, fb.nodeY = 1600, 100
    trails = glsl(comp, 'trails', 'trails.glsl', [lines, fb], 1800, 225)
    setp(fb, top=trails.name)
    uniforms(trails, [
        ('uTime', Expr('absTime.seconds')),
        ('uDecay', Expr(P + 'Decay')),
        ('uWarp', Expr(P + 'Warp')),
        ('uDrift', Expr(P + 'Drift')),
        ('uSpread', Expr(P + 'Spread')),
        ('uCut', Expr(P + 'Cut')),
        ('uEmit', Expr(P + 'Emit')),
    ])

    # --- bloom -----------------------------------------------------------
    blur_s = comp.create(blurTOP, 'bloom_small')
    blur_s.inputConnectors[0].connect(trails)
    setp(blur_s, size=Expr(P + 'Bloomsmall'))
    blur_s.nodeX, blur_s.nodeY = 2000, 300
    blur_l = comp.create(blurTOP, 'bloom_large')
    blur_l.inputConnectors[0].connect(trails)
    setp(blur_l, size=Expr(P + 'Bloomlarge'))
    blur_l.nodeX, blur_l.nodeY = 2000, 150

    # --- cor + reflexo ---------------------------------------------------
    grade = glsl(comp, 'grade', 'grade.glsl', [trails, blur_s, blur_l], 2200, 225)
    uniforms(grade, [
        ('uTime', Expr('absTime.seconds')),
        ('uCore', (Expr(P + 'Corer'), Expr(P + 'Coreg'), Expr(P + 'Coreb'))),
        ('uGlow', (Expr(P + 'Glowcolorr'), Expr(P + 'Glowcolorg'), Expr(P + 'Glowcolorb'))),
        ('uGlowAmt', Expr(P + 'Glow')),
        ('uSat', Expr(P + 'Sat')),
        ('uExposure', Expr(P + 'Exposure')),
        ('uHorizon', Expr(P + 'Horizon')),
        ('uReflect', Expr(P + 'Reflect')),
    ])

    out = comp.create(outTOP, 'out1')
    out.inputConnectors[0].connect(grade)
    out.nodeX, out.nodeY = 2400, 225

    comp.nodeX, comp.nodeY = 0, 0
    try:
        comp.viewer = True
    except Exception:
        pass
    print(TAG, 'pronto:', comp.path, '- abra os parametros do COMP (pagina Streaks).')
    return comp


build()
