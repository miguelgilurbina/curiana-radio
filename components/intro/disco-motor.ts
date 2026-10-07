import { FRAGMENTO, VERTICE } from "./disco-shader";

// El motor de El Disco: WebGL2, el puntero y los estados (reposo → afinando →
// afinado → la arena se vuelve sello → salida). Es un port directo del script
// del prototipo; el componente (IntroDisco) solo lo monta y escucha sus
// avisos. El DOM que cambia en cada frame (frecuencia, aguja, viento, patrón,
// el polvo y el sello) se toca aquí directo, sin pasar por React.

export interface ElementosDisco {
  raiz: HTMLElement;
  lienzo: HTMLCanvasElement;
  frecuencia: HTMLElement;
  aguja: HTMLElement;
  viento: HTMLElement;
  patron: HTMLElement;
  anillo: HTMLElement;
  velo: HTMLElement;
  /** el lienzo 2D donde vuelan los granos, sobre el shader */
  polvo: HTMLCanvasElement;
  /** el sello nítido, que entra al final del viaje */
  sello: HTMLImageElement;
}

export interface OpcionesDisco {
  /** prefers-reduced-motion: el tiempo se congela y arranca ya afinado */
  lento: boolean;
  /** la máscara del isotipo: el PNG original, dimensiones intactas */
  logo: string;
  /** el sello de la noche (marco, espiral original y type 3c): el destino de
   *  los granos sale de su imagen */
  sello: string;
  onAfinado: () => void;
}

export interface MotorDisco {
  afinado: () => void;
  /** la salida (1.7 s, o nada si es lento); llama a `fin` al terminar */
  salir: (fin: () => void) => void;
  destruir: () => void;
}

const COMPAS = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"];
const CENTRO: [number, number] = [0, 0.09]; // el disco sube 0.09·H
// La arena se vuelve sello (handoff 2026-10-05): 3.200 granos de la espiral
// van a la espiral del sello; 6.200 del resto del disco, al marco y las letras.
const GRANOS_ESPIRAL = 3200;
const GRANOS_RESTO = 6200;
const VIAJE = 3.2; // s

type Punto = [number, number];
interface Grano {
  sx: number;
  sy: number;
  dx: number;
  dy: number;
  del: number;
  giro: number;
  ruido: number;
  t: number;
}

const suave = (a: number, b: number, x: number) => {
  const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return k * k * (3 - 2 * k);
};
const easeInOutCubic = (k: number) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);

/** Los destinos de los granos: los píxeles hueso del sello, en una grilla de
 *  256², separados en la espiral (dentro del marco, arriba de las letras) y
 *  el resto (marco y letras). Mismo corte que el prototipo. */
async function mascaraDelSello(url: string): Promise<{ espiral: Punto[]; resto: Punto[] }> {
  const bmp = await createImageBitmap(await (await fetch(url)).blob());
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const x = c.getContext("2d", { willReadFrequently: true })!;
  x.drawImage(bmp, 0, 0, 256, 256);
  const d = x.getImageData(0, 0, 256, 256).data;
  const espiral: Punto[] = [], resto: Punto[] = [];
  for (let y = 0; y < 256; y++)
    for (let xx = 0; xx < 256; xx++) {
      if (d[(y * 256 + xx) * 4] < 128) continue;
      const u = (xx + 0.5) / 256, v = (y + 0.5) / 256;
      const marco = u < 0.047 || u > 0.953 || v < 0.047 || v > 0.953;
      (!marco && v < 0.64 ? espiral : resto).push([u, v]);
    }
  return { espiral, resto };
}

/** Los orígenes de la espiral de arena: el alfa del isotipo a 170 de ancho. */
function espiralDeArena(lc: HTMLCanvasElement): Punto[] {
  const n = 170, nh = Math.round((n * lc.height) / lc.width);
  const m = document.createElement("canvas");
  m.width = n;
  m.height = nh;
  const mx = m.getContext("2d", { willReadFrequently: true })!;
  mx.drawImage(lc, 0, 0, n, nh);
  const md = mx.getImageData(0, 0, n, nh).data;
  const puntos: Punto[] = [];
  for (let y = 0; y < nh; y++)
    for (let x = 0; x < n; x++) if (md[(y * n + x) * 4 + 3] > 128) puntos.push([(x + 0.5) / n, (y + 0.5) / nh]);
  return puntos;
}

// El PNG del isotipo → alfa: tinta oscura opaca, papel transparente, recortado
// a su caja. Mismo cálculo que el favicon y el prototipo.
async function mascaraDelLogo(url: string): Promise<HTMLCanvasElement> {
  const bmp = await createImageBitmap(await (await fetch(url)).blob());
  const sc = document.createElement("canvas");
  sc.width = bmp.width;
  sc.height = bmp.height;
  const sx = sc.getContext("2d")!;
  sx.drawImage(bmp, 0, 0);
  const idt = sx.getImageData(0, 0, sc.width, sc.height);
  const d = idt.data;
  let x0 = sc.width, y0 = sc.height, x1 = 0, y1 = 0;
  for (let i = 0; i < d.length; i += 4) {
    const a = (Math.max(0, Math.min(255, (255 - (d[i] + d[i + 1] + d[i + 2]) / 3) * 1.25)) * d[i + 3]) / 255;
    d[i] = d[i + 1] = d[i + 2] = 255;
    d[i + 3] = a;
    if (a > 60) {
      const p = i / 4, x = p % sc.width, y = (p / sc.width) | 0;
      if (x < x0) x0 = x;
      if (x > x1) x1 = x;
      if (y < y0) y0 = y;
      if (y > y1) y1 = y;
    }
  }
  sx.putImageData(idt, 0, 0);
  const lw = x1 - x0 + 1, lh = y1 - y0 + 1;
  const lc = document.createElement("canvas");
  lc.width = lw;
  lc.height = lh;
  lc.getContext("2d")!.drawImage(sc, x0, y0, lw, lh, 0, 0, lw, lh);
  return lc;
}

function compilar(gl: WebGL2RenderingContext, tipo: number, fuente: string): WebGLShader {
  const s = gl.createShader(tipo)!;
  gl.shaderSource(s, fuente);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) ?? "shader");
  return s;
}

/** Devuelve null si no hay WebGL2 (o el shader no compila): el componente
 *  cae al isotipo plano con el bloque final ya visible. */
export function arrancarDisco(el: ElementosDisco, op: OpcionesDisco): MotorDisco | null {
  const gl = el.lienzo.getContext("webgl2", { antialias: false });
  if (!gl) return null;

  let pr: WebGLProgram;
  try {
    pr = gl.createProgram()!;
    gl.attachShader(pr, compilar(gl, gl.VERTEX_SHADER, VERTICE));
    gl.attachShader(pr, compilar(gl, gl.FRAGMENT_SHADER, FRAGMENTO));
    gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error("link");
  } catch {
    return null;
  }
  gl.useProgram(pr);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const la = gl.getAttribLocation(pr, "a");
  gl.enableVertexAttribArray(la);
  gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
  const U = (n: string) => gl.getUniformLocation(pr, n);

  // Textura del logo: 1×1 transparente hasta que llega el PNG (el revelado
  // no empieza hasta afinar, así que casi nunca se nota la espera).
  gl.bindTexture(gl.TEXTURE_2D, gl.createTexture());
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.uniform1i(U("uLogo"), 0);
  gl.uniform1f(U("uAsp"), 1);

  let vivo = true;
  let asp = 1; // ancho/alto del isotipo
  let arenaEsp: Punto[] = [];
  mascaraDelLogo(op.logo)
    .then((lc) => {
      if (!vivo) return;
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, lc);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      asp = lc.width / lc.height;
      gl.uniform1f(U("uAsp"), asp);
      arenaEsp = espiralDeArena(lc);
    })
    .catch(() => {
      // sin logo el disco sigue funcionando: se revela la espiral de arena
    });
  let selloEsp: Punto[] = [], selloResto: Punto[] = [];
  mascaraDelSello(op.sello)
    .then((m) => {
      selloEsp = m.espiral;
      selloResto = m.resto;
    })
    .catch(() => {
      // sin máscara los granos van al centro del sello y el sello entra igual
    });

  const px2 = el.polvo.getContext("2d")!;
  let dpr = 1, W = 0, H = 0, R = 0.32;
  // el sello: su lado y su esquina, con su espiral sobre el centro del disco
  let SL = 0, SX = 0, SY = 0;
  function encajar() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    el.lienzo.width = Math.round(W * dpr);
    el.lienzo.height = Math.round(H * dpr);
    gl!.viewport(0, 0, el.lienzo.width, el.lienzo.height);
    R = Math.min(0.32, (0.44 * W) / H);
    // el sello, tan grande como quepa entre la esquina de arriba y el bloque
    // final (que va a 6vh del borde), sin pasar del tamaño del revelado
    const cyL = H / 2 - CENTRO[1] * H;
    const finTop = H - 150 - 0.06 * H;
    SL = Math.max(120, Math.min((0.95 * R * H) / 0.59, (cyL - 70) / 0.38, (finTop - 18 - cyL) / 0.62));
    SX = W / 2 + CENTRO[0] * H - 0.49 * SL;
    SY = cyL - 0.38 * SL;
    Object.assign(el.sello.style, { width: SL + "px", height: SL + "px", left: SX + "px", top: SY + "px" });
    el.sello.sizes = Math.round(SL) + "px";
    el.polvo.width = Math.round(W * dpr);
    el.polvo.height = Math.round(H * dpr);
  }
  encajar();
  const aDisco = (cx: number, cy: number): [number, number] => [
    ((cx - W / 2) / H - CENTRO[0]) / R,
    ((H / 2 - cy) / H - CENTRO[1]) / R,
  ];
  const cX = () => W / 2 + CENTRO[0] * H;
  const cY = () => H / 2 - CENTRO[1] * H;

  let M = 0, Mt = 0, rev = 0, ok = false, salida = 0, tAcc = 0, ultimo = performance.now();
  let morph = 0, granos: Grano[] | null = null;
  let mouse: [number, number] = [9, 9], press = 0, pressT = 0;
  let lastAng: number | null = null, lastW = 0, vel = 0, dir = 45;
  let lpx: number | null = null, lpy: number | null = null;
  let raf = 0;
  const ondas = new Float32Array(32);
  let oi = 0;
  for (let i = 0; i < 8; i++) ondas[i * 4 + 2] = -99;
  function onda(q: [number, number], amp: number) {
    ondas[oi * 4] = q[0];
    ondas[oi * 4 + 1] = q[1];
    ondas[oi * 4 + 2] = tAcc;
    ondas[oi * 4 + 3] = amp;
    oi = (oi + 1) % 8;
  }

  function alMover(e: PointerEvent) {
    el.anillo.style.left = e.clientX + "px";
    el.anillo.style.top = e.clientY + "px";
    mouse = aDisco(e.clientX, e.clientY);
    if (lpx !== null && lpy !== null) {
      const vx = e.clientX - lpx, vy = e.clientY - lpy, sp = Math.hypot(vx, vy);
      vel = vel * 0.9 + sp * 0.1;
      if (sp > 1) dir = ((Math.atan2(vx, -vy) * 180) / Math.PI + 360) % 360;
      const ang = Math.atan2(e.clientY - cY(), e.clientX - cX());
      const rad = Math.hypot(e.clientX - cX(), e.clientY - cY());
      // Unas 2.2 vueltas alrededor del centro afinan; presionando, ×1.4.
      if (lastAng !== null && rad > 24 && !ok) {
        let da = ang - lastAng;
        if (da > Math.PI) da -= 2 * Math.PI;
        if (da < -Math.PI) da += 2 * Math.PI;
        Mt = Math.min(1, Mt + (Math.abs(da) / (Math.PI * 2 * 2.2)) * (press ? 1.4 : 1));
      }
      lastAng = ang;
      if (tAcc - lastW > (press ? 0.18 : 0.55) && sp > 3) {
        onda(mouse, press ? 0.55 : 0.25);
        lastW = tAcc;
      }
    }
    lpx = e.clientX;
    lpy = e.clientY;
  }
  function alBajar(e: PointerEvent) {
    if ((e.target as Element | null)?.closest("button, a")) return;
    press = 1;
    el.raiz.dataset.baja = "";
    onda(aDisco(e.clientX, e.clientY), 0.9);
    if (!ok) Mt = Math.min(1, Mt + 0.03);
  }
  function alSubir() {
    press = 0;
    delete el.raiz.dataset.baja;
  }
  function alSalir() {
    lpx = lpy = null;
    lastAng = null;
    el.anillo.style.left = "-99px";
  }

  el.raiz.addEventListener("pointermove", alMover);
  el.raiz.addEventListener("pointerdown", alBajar);
  el.raiz.addEventListener("pointerleave", alSalir);
  window.addEventListener("pointerup", alSubir);
  window.addEventListener("pointercancel", alSubir);
  window.addEventListener("resize", encajar);

  // La arena se levanta y se reordena en el sello: la espiral viaja a la
  // espiral; el resto del disco, al marco y las letras. Los de afuera
  // despegan primero (retardo = radio · 0.22).
  function sembrarGranos() {
    const cx = cX(), cy = cY(), g: Grano[] = [];
    const elegir = (a: Punto[]) => a[(Math.random() * a.length) | 0];
    const aPantalla = (u: number, v: number): Punto => [
      W / 2 + (CENTRO[0] + (u - 0.5) * 0.95 * R) * H,
      H / 2 - (CENTRO[1] + ((0.5 - v) * 0.95 * R) / asp) * H,
    ];
    for (let i = 0; i < GRANOS_ESPIRAL + GRANOS_RESTO; i++) {
      let s: Punto, d: Punto;
      if (i < GRANOS_ESPIRAL && arenaEsp.length && selloEsp.length) {
        const a = elegir(arenaEsp);
        s = aPantalla(a[0], a[1]);
        d = elegir(selloEsp);
      } else {
        const r = Math.sqrt(Math.random()) * R * H, th = Math.random() * Math.PI * 2;
        s = [cx + Math.cos(th) * r, cy - Math.sin(th) * r];
        d = selloResto.length ? elegir(selloResto) : [0.5, 0.5];
      }
      const rs = Math.hypot(s[0] - cx, s[1] - cy) / (R * H);
      g.push({
        sx: s[0],
        sy: s[1],
        dx: SX + d[0] * SL,
        dy: SY + d[1] * SL,
        del: i < GRANOS_ESPIRAL ? 0.12 + Math.random() * 0.2 : rs * 0.22 + Math.random() * 0.14,
        giro: (i < GRANOS_ESPIRAL ? 0.6 : 1.6) * (0.7 + Math.random() * 0.6),
        ruido: Math.random() * 6.28,
        t: Math.random() < 0.12 ? 1.8 : 1.15,
      });
    }
    granos = g;
  }
  function dibujarGranos() {
    const cx = cX(), cy = cY();
    px2.setTransform(dpr, 0, 0, dpr, 0, 0);
    px2.clearRect(0, 0, W, H);
    if (morph >= 1 || !granos) {
      granos = [];
      return;
    }
    const fin = 1 - suave(0.9, 1, morph);
    px2.fillStyle = "rgba(243,234,212," + 0.92 * fin + ")";
    for (const p of granos) {
      const k = easeInOutCubic(Math.min(1, Math.max(0, (morph - p.del) / 0.6)));
      let x = p.sx + (p.dx - p.sx) * k, y = p.sy + (p.dy - p.sy) * k;
      // remolino: el viento hace girar la arena alrededor del centro y la suelta al llegar
      const th = p.giro * Math.sin(Math.PI * k), ox = x - cx, oy = y - cy;
      const c = Math.cos(th), sn = Math.sin(th);
      x = cx + ox * c - oy * sn;
      y = cy + ox * sn + oy * c;
      const j = Math.sin(Math.PI * k) * 5;
      x += Math.sin(p.ruido + morph * 9) * j;
      y += Math.cos(p.ruido * 1.3 + morph * 7) * j;
      px2.fillRect(x, y, p.t, p.t);
    }
  }

  function afinado() {
    if (ok) return;
    ok = true;
    Mt = 1;
    onda([0, 0], 1.2);
    op.onAfinado();
  }

  const uRes = U("uRes"), uDpr = U("uDpr"), uR = U("uR"), uC = U("uC"), uT = U("uT"), uM = U("uM");
  const uRev = U("uRev"), uExit = U("uExit"), uMouse = U("uMouse"), uPress = U("uPress"), uW = U("uW");
  const uFund = U("uFund");

  function frame(ahora: number) {
    const dt = Math.min(0.05, (ahora - ultimo) / 1000);
    ultimo = ahora;
    if (!op.lento) tAcc += dt * (1 + salida * 3);
    M += (Mt - M) * Math.min(1, dt * 2.2);
    if (M > 0.985 && !ok) afinado();
    if (ok) rev = Math.min(1, rev + dt * 0.55);
    // con la espiral a medio revelar, la arena se levanta y viaja al sello
    if (rev > 0.55 && morph < 1) {
      if (!granos) sembrarGranos();
      morph = Math.min(1, morph + dt / VIAJE);
      dibujarGranos();
    }
    // el disco se funde al fondo en el primer 28 % del viaje; el sello nítido
    // entra entre el 84 % y el 100 %, mientras los granos se apagan
    const fundido = suave(0, 0.28, morph);
    el.sello.style.opacity = String(suave(0.84, 1, morph) * (1 - salida));
    el.sello.style.transform = "scale(" + (1 + salida * 0.25) + ")";
    pressT += ((press ? 1 : 0) - pressT) * Math.min(1, dt * 8);
    const k = Math.min(1, M / 0.985);
    el.frecuencia.textContent = (87.5 + 1.3 * k).toFixed(1);
    el.aguja.style.left = k * 100 + "%";
    el.viento.textContent = String(Math.round(9 + vel * 0.9)).padStart(2, "0") + " km/h " + COMPAS[Math.round(dir / 45) % 8];
    el.patron.textContent = ok ? "espiral" : k < 0.15 ? "surcos" : k < 0.6 ? "remolino" : "vórtice";
    gl!.uniform2f(uRes, el.lienzo.width, el.lienzo.height);
    gl!.uniform1f(uDpr, dpr);
    gl!.uniform1f(uR, R);
    gl!.uniform2f(uC, CENTRO[0], CENTRO[1]);
    gl!.uniform1f(uT, tAcc);
    gl!.uniform1f(uM, M);
    gl!.uniform1f(uRev, rev);
    gl!.uniform1f(uExit, salida);
    gl!.uniform1f(uFund, fundido);
    gl!.uniform2f(uMouse, mouse[0], mouse[1]);
    gl!.uniform1f(uPress, pressT);
    gl!.uniform4fv(uW, ondas);
    gl!.drawArrays(gl!.TRIANGLES, 0, 3);
    raf = requestAnimationFrame(frame);
  }

  if (op.lento) {
    // sin movimiento: arranca afinado, con el sello ya hecho
    M = Mt = 1;
    rev = 1;
    morph = 1;
    afinado();
  }
  raf = requestAnimationFrame(frame);

  return {
    afinado,
    salir(fin) {
      if (op.lento) {
        fin();
        return;
      }
      const ini = performance.now(), dur = 1700;
      const paso = (ahora: number) => {
        if (!vivo) return;
        const k = Math.min((ahora - ini) / dur, 1);
        salida = k * k * (3 - 2 * k);
        // velo negro desde el 55 %
        if (k > 0.55) el.velo.style.opacity = String((k - 0.55) / 0.45);
        if (k < 1) requestAnimationFrame(paso);
        else fin();
      };
      requestAnimationFrame(paso);
    },
    destruir() {
      vivo = false;
      cancelAnimationFrame(raf);
      el.raiz.removeEventListener("pointermove", alMover);
      el.raiz.removeEventListener("pointerdown", alBajar);
      el.raiz.removeEventListener("pointerleave", alSalir);
      window.removeEventListener("pointerup", alSubir);
      window.removeEventListener("pointercancel", alSubir);
      window.removeEventListener("resize", encajar);
      // Sin loseContext(): en modo estricto React monta dos veces sobre el
      // mismo <canvas>, y getContext devolvería el contexto ya perdido. Al
      // desmontar de verdad, el contexto se va con el canvas.
    },
  };
}
