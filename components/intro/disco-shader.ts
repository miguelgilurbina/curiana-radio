// Los shaders de El Disco, tal cual del prototipo del handoff
// (design_handoff_intro_v1_disco/Intro v1 El Disco.html). Un solo triángulo a
// pantalla completa; todo el disco sale del fragment shader. Las capas, de
// fondo a frente, están descritas en BRAND_MVP.md §9. Los valores del grano
// están aprobados: no suavizar. Única desviación del prototipo, la costura de
// atan en el radio izquierdo (2026-09-29): el antialias ya no la ve (era un
// filete con la espiral hecha) y a medio armar se reparte en una cuña (era un
// corte recto en los surcos). Con la espiral hecha el disco es idéntico.

export const VERTICE = `#version 300 es
in vec2 a; void main(){ gl_Position = vec4(a,0.,1.); }`;

export const FRAGMENTO = `#version 300 es
precision highp float;
uniform vec2 uRes; uniform float uT, uM, uRev, uExit, uDpr, uR;
uniform vec2 uC, uMouse; uniform float uPress;
uniform vec4 uW[8];
uniform sampler2D uLogo; uniform float uAsp;
out vec4 o;
float hash(vec2 p){ p = fract(p*vec2(123.34,456.21)); p += dot(p,p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
  return mix(mix(hash(i),hash(i+vec2(1,0)),f.x), mix(hash(i+vec2(0,1)),hash(i+1.),f.x), f.y); }
float fbm(vec2 p){ float s=0., a=.5; for(int i=0;i<4;i++){ s+=a*vn(p); p=p*2.03+17.; a*=.5; } return s; }
const float TAU = 6.2831853;
void main(){
  vec2 fc = gl_FragCoord.xy;
  vec2 p = (fc - .5*uRes) / uRes.y;
  vec2 px = floor(fc / uDpr);
  float grain = hash(px), g2 = hash(floor(fc/(2.*uDpr)) + 3.1);
  float clump = fbm(px*.05);
  vec3 bg = vec3(.027,.035,.051), ink = vec3(.035,.03,.024);
  vec3 gold = vec3(.902,.706,.235), bone = vec3(.933,.902,.831);
  vec2 q = (p - uC) / uR;                 // disco unitario
  float dd = length(q);
  // borde de arena derramada
  float edgeN = (fbm(q*9. + uT*.05) - .5) * .05 + (grain - .5) * .035;
  float inDisc = smoothstep(1.005, .99, dd + edgeN);
  vec3 col = bg;
  // granos sueltos fuera del disco
  float stray = step(.9965, grain) * smoothstep(1.35, 1.0, dd);
  col = mix(col, gold*.7, stray);
  if (inDisc > 0.) {
    // campo 1: surcos horizontales del viento
    float w = fbm(q*2.1 + vec2(uT*.03, 0.));
    float f1 = q.y*11. + sin(q.x*3.2 + w*3. + uT*.12)*.9 + (w - .5)*2.2 - uT*.05;
    // campo 2: espiral ovalada como el isotipo
    vec2 e = q * vec2(.9, 1.15);
    float r = length(e), a = atan(e.y, e.x);
    // el mismo ángulo con la costura del otro lado (eje +x): sólo para medir
    // el antialias, ver aa más abajo
    float a2 = atan(-e.y, -e.x) + TAU*.5;
    float grow = uM * 1.6;
    float wm = smoothstep(grow + .28, grow - .05, r) * smoothstep(0., .06, uM);
    // Mientras el anillo se arma (0 < wm < 1) la espiral tiene que pasar de
    // no dar vuelta a dar una, y con la mezcla lineal todo ese salto caía en
    // el semieje −x: un corte recto en los surcos. Se reparte en una cuña que
    // sólo existe a medio armar (ancho ∝ wm·(1−wm)): con la espiral hecha o
    // sin empezar, u = a/TAU y el disco es el del prototipo.
    float u = a/TAU;
    float cuna = .9 * 4.*wm*(1. - wm);
    if (cuna > 1e-3) u *= 1. - smoothstep(TAU*.5 - cuna, TAU*.5, abs(a));
    float f2 = r*9. - u - uT*.04 + (fbm(q*3.)-.5)*.14;
    float f = mix(f1, f2, wm);
    for (int i = 0; i < 8; i++) {
      vec4 k = uW[i]; float age = uT - k.z;
      if (age > 0. && age < 5.) {
        float dq = length(q - k.xy);
        f += k.w * exp(-pow((dq - age*.35)*9., 2.)) * exp(-age*.8);
      }
    }
    vec2 gm = q - uMouse;
    f += (.3 + .25*uPress) * exp(-dot(gm, gm) * 40.);
    f += uExit*uExit*10.*r;
    float lit = .5 + .5*sin(TAU*f + .95), h = .5 + .5*sin(TAU*f);
    float b = smoothstep(.1, .96, .62*lit + .38*h);
    // atan salta de π a −π en el semieje −x: f salta ahí en wm (1 con la
    // espiral hecha). El seno no lo ve —período 1—, pero fwidth sí, y el
    // antialias pintaba un filete gris a lo largo del radio izquierdo. f2b es
    // f con la costura del otro lado; el menor de los dos fwidth no ve
    // ninguna de las dos. f no cambia: el disco se dibuja igual.
    float f2b = f - wm*(a2 - a)/TAU;
    float aa = min(fwidth(f), fwidth(f2b));
    b = mix(.4, b, clamp(1. - aa*1.6, 0., 1.));
    // domo: el disco es una colina vista de frente
    float dome = sqrt(max(0., 1. - dd*dd));
    b *= .55 + .45*dome + .2*(q.y*.5 + .5);
    b *= .86 + .24*clump;
    b += (grain - .5) * .15 + (g2 - .5) * .11;
    b += step(.975, grain) * .34 * (.4 + b);
    b -= step(grain, .04) * .3;
    b = clamp(b, 0., 1.);
    // la espiral original sale del centro
    vec2 luv = vec2(q.x/.95 + .5, .5 - q.y/(.95/uAsp));
    float lg = 0.;
    if (luv.x > 0. && luv.x < 1. && luv.y > 0. && luv.y < 1.) lg = texture(uLogo, luv).a;
    b = mix(b, b*.45, uRev * smoothstep(.8, .55, dd) * (1. - lg));
    b = mix(b, .97, lg * uRev);
    vec3 sand = mix(gold, bone, .08 + lg*uRev*.8);
    vec3 dc = mix(ink, sand, pow(b, 1.25));
    dc += bone*.05*lg*uRev*(.6 + .4*sin(uT*1.4));
    col = mix(col, dc, inDisc);
  }
  col *= 1. - uExit;
  o = vec4(col, 1.);
}`;
