// La escena de la intro: el remolino serigráfico (shader), el túnel de ecos
// y la espiral 3D del isotipo al frente. IntroCuriana la importa
// dinámicamente para que three.js viaje en su propio chunk y no con la
// landing cuando la intro ya se vio en la sesión.
//
// Los colores son las tintas del arte de BRAND_MVP.md §3 — mismo hex que
// --color-arte-* en globals.css; el shader los necesita como vec3 y three
// como enteros, así que aquí van literales.

import {
  DirectionalLight,
  HemisphereLight,
  Mesh,
  MeshBasicMaterial,
  MeshStandardMaterial,
  PerspectiveCamera,
  PlaneGeometry,
  Scene,
  ShaderMaterial,
  WebGLRenderer,
  type ExtrudeGeometry,
} from "three";
import { geometriaEspiral } from "@/lib/espiral-3d";

/** Estado que la intro muta cada frame y la escena solo lee. */
export type EstadoIntro = {
  velocidad: number; // 1 en reposo → 27 al sintonizar (0 con reduced motion)
  dolly: number; // 0 → 2.35: la cámara atraviesa el centro
  mx: number; // parallax del puntero, −1..1
  my: number;
  lento: boolean; // prefers-reduced-motion
};

export type Escena = { dispose(): void };

// ácido, índigo, ocre, rojo, hueso, azul eléctrico: los seis ecos
const TINTAS = [0xc7c91c, 0x26396a, 0xc36712, 0xb64924, 0xf3ead4, 0x2154c5];
const ACIDO = 0xc7c91c;
const HUESO = 0xf3ead4;
const NOCHE = 0x23224f; // la noche ultramar (fondo de la intro)
const CALIDA = 0xffb08a;
const ARCILLA = 0xb8502e; // arcilla rúbrica aclarada para el fondo saturado

const CAMARA_Z = 2.7;
const ESCALA_FRENTE = 1.3;
const ECOS = 6;
const escalaEco = (i: number, pulso: number) => 1.3 + (i + 1) * 0.52 + pulso;

const VERTEX = `
  varying vec2 vUv;
  void main(){ vUv = uv; gl_Position = vec4(position.xy, 1.0, 1.0); }`;

// El remolino: bandas espirales en polares, dos ondas que se interfieren,
// viñeta hacia el índigo oscuro y posterización a 5 niveles — registro de
// serigrafía, no de degradado.
const FRAGMENT = `
  varying vec2 vUv;
  uniform float t;
  uniform float marea;
  void main(){
    vec2 p = vUv - 0.5;
    float r = length(p) + 1e-4;
    float a = atan(p.y, p.x);
    float s1 = sin(a*3.0 + log(r)*7.0 - t*0.55*marea);
    float s2 = sin(a*5.0 - log(r)*11.0 + t*0.4*marea + sin(t*0.21)*2.0);
    float m = s1*0.6 + s2*0.4;
    vec3 acido  = vec3(0.780, 0.788, 0.110);
    vec3 indigo = vec3(0.149, 0.224, 0.416);
    vec3 ocre   = vec3(0.765, 0.404, 0.071);
    vec3 rojo   = vec3(0.714, 0.286, 0.141);
    vec3 col = mix(indigo, ocre, smoothstep(-0.9, 0.9, m));
    col = mix(col, acido, smoothstep(0.55, 0.95, s2) * 0.85);
    col = mix(col, rojo, smoothstep(0.6, 1.0, s1) * 0.6);
    col = mix(col, indigo*0.55, smoothstep(0.32, 0.85, r));
    col = floor(col * 5.0 + 0.5) / 5.0;
    gl_FragColor = vec4(col, 1.0);
  }`;

/**
 * Primero el calco (async). Devuelve un montador SÍNCRONO: así, si la intro
 * se desmonta mientras se calca, quien llama descarta la promesa y nunca
 * llega a crearse un renderer sobre el canvas.
 */
export async function prepararEscena(urlIsotipo: string) {
  const geo = await geometriaEspiral(urlIsotipo);
  return (canvas: HTMLCanvasElement, estado: EstadoIntro): Escena =>
    montar(canvas, geo, estado);
}

function montar(canvas: HTMLCanvasElement, geo: ExtrudeGeometry, estado: EstadoIntro): Escena {
  const renderer = new WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  const scene = new Scene();
  const camera = new PerspectiveCamera(44, 1, 0.1, 40);
  camera.position.set(0, 0, CAMARA_Z);

  // fondo: el warp psicodélico a pantalla completa
  const fondoU = { t: { value: 0 }, marea: { value: estado.lento ? 0 : 1 } };
  const fondoGeo = new PlaneGeometry(2, 2);
  const fondoMat = new ShaderMaterial({
    uniforms: fondoU,
    depthWrite: false,
    depthTest: false,
    vertexShader: VERTEX,
    fragmentShader: FRAGMENT,
  });
  const fondo = new Mesh(fondoGeo, fondoMat);
  fondo.renderOrder = -1;
  fondo.frustumCulled = false;
  scene.add(fondo);

  scene.add(new HemisphereLight(HUESO, NOCHE, 0.9));
  const calida = new DirectionalLight(CALIDA, 1.7);
  calida.position.set(1.6, 1.4, 2);
  scene.add(calida);
  const acida = new DirectionalLight(ACIDO, 0.8);
  acida.position.set(-2, -1, 1);
  scene.add(acida);

  // la espiral protagonista: el calco extruido, en arcilla
  const frenteMat = new MeshStandardMaterial({ color: ARCILLA, roughness: 0.5, metalness: 0.12 });
  const frente = new Mesh(geo, frenteMat);
  frente.scale.setScalar(ESCALA_FRENTE);
  scene.add(frente);

  // el túnel: ecos planos de la misma silueta en las tintas del arte
  const ecoMats: MeshBasicMaterial[] = [];
  const ecos: Mesh[] = [];
  for (let i = 0; i < ECOS; i++) {
    const mat = new MeshBasicMaterial({
      color: TINTAS[i % TINTAS.length],
      transparent: true,
      opacity: 0.85 - i * 0.11,
    });
    const m = new Mesh(geo, mat);
    m.scale.setScalar(escalaEco(i, 0));
    m.position.z = -0.55 * (i + 1);
    scene.add(m);
    ecos.push(m);
    ecoMats.push(mat);
  }

  const encuadre = () => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  window.addEventListener("resize", encuadre);
  encuadre();

  const t0 = performance.now();
  renderer.setAnimationLoop(() => {
    const t = (performance.now() - t0) / 1000;
    const { velocidad, dolly, mx, my, lento } = estado;
    fondoU.t.value = t * Math.sqrt(velocidad) + (velocidad > 1 ? t * velocidad * 0.2 : 0);
    frente.rotation.y += 0.004 * velocidad;
    frente.rotation.x = -0.28 + (lento ? 0 : Math.sin(t * 0.5) * 0.05) + my * 0.12;
    frente.rotation.z = mx * 0.06;
    frente.position.y = lento ? 0 : Math.sin(t * 0.8) * 0.03;
    ecos.forEach((m, i) => {
      // pares e impares giran en contrafase, con un pulso leve de escala
      m.rotation.z += (i % 2 ? -1 : 1) * 0.0035 * velocidad * (1 + i * 0.25);
      m.scale.setScalar(escalaEco(i, lento ? 0 : Math.sin(t * 1.1 + i * 0.9) * 0.02));
    });
    camera.position.z = CAMARA_Z - dolly;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  });

  return {
    dispose() {
      renderer.setAnimationLoop(null);
      window.removeEventListener("resize", encuadre);
      fondoGeo.dispose();
      fondoMat.dispose();
      frenteMat.dispose();
      ecoMats.forEach((m) => m.dispose());
      // `geo` no se dispone: vive cacheada en lib/espiral-3d.
      renderer.dispose();
    },
  };
}
