"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

// Dos curvas de distancia idiolectal media por día (lectura emergente): el run
// normal y su control de ablación. La evidencia de koineización no es que la
// normal baje — es la BRECHA entre ambas. Colores: normal en violeta de
// "experimento" (--sim), ablación en gris apagado (el control, sin andamiaje).
const COLOR_NORMAL = "#5B4FCF";
const COLOR_ABLACION = "#9d7f66";

interface Props {
  normal: number[];
  ablacion: number[];
}

export default function ConvergenciaChart({ normal, ablacion }: Props) {
  const n = Math.max(normal.length, ablacion.length);
  const data = Array.from({ length: n }, (_, i) => ({
    dia: i + 1,
    normal: normal[i] != null ? +normal[i].toFixed(4) : null,
    ablacion: ablacion[i] != null ? +ablacion[i].toFixed(4) : null,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 8, right: 12, left: -8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#d8c8a3" vertical={false} />
        <XAxis
          dataKey="dia"
          tickFormatter={(v) => `D${v}`}
          tick={{ fill: "#8a7657", fontSize: 11, fontFamily: "Inter, sans-serif" }}
          tickLine={false}
          axisLine={{ stroke: "#d8c8a3" }}
          interval="preserveStartEnd"
          minTickGap={24}
        />
        <YAxis
          tick={{ fill: "#8a7657", fontSize: 11, fontFamily: "Inter, sans-serif" }}
          tickLine={false}
          axisLine={false}
          width={44}
          domain={["auto", "auto"]}
          tickFormatter={(v) => v.toFixed(2)}
        />
        <Tooltip
          formatter={(value: number, name: string) => [value?.toFixed(4), name]}
          labelFormatter={(v) => `Día ${v}`}
          contentStyle={{
            background: "#f8f1de",
            border: "1px solid #d8c8a3",
            borderRadius: 12,
            boxShadow: "0 8px 24px rgba(79,62,53,0.12)",
            fontFamily: "Inter, sans-serif",
            fontSize: 12,
          }}
          labelStyle={{ color: "#2f2517", fontWeight: 600, marginBottom: 4 }}
          cursor={{ stroke: "#c4b28b", strokeWidth: 1 }}
        />
        <Legend
          verticalAlign="top"
          height={28}
          wrapperStyle={{ fontFamily: "Inter, sans-serif", fontSize: 12 }}
        />
        <Line
          type="monotone"
          dataKey="normal"
          name="Normal (con andamiaje)"
          stroke={COLOR_NORMAL}
          strokeWidth={2.5}
          dot={false}
          activeDot={{ r: 3, strokeWidth: 0 }}
          connectNulls
        />
        <Line
          type="monotone"
          dataKey="ablacion"
          name="Ablación (control)"
          stroke={COLOR_ABLACION}
          strokeWidth={2}
          strokeDasharray="5 4"
          dot={false}
          activeDot={{ r: 3, strokeWidth: 0 }}
          connectNulls
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
