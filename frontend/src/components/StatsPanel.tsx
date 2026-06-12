import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { StatsSnapshot } from "../types";

interface Props {
  history: StatsSnapshot[];
}

export function StatsPanel({ history }: Props) {
  const latest = history[history.length - 1];

  return (
    <div className="stats-panel">
      <h2>Population &amp; evolution</h2>

      {latest && (
        <dl className="stats-summary">
          <div>
            <dt>Tick</dt>
            <dd>{latest.tick}</dd>
          </div>
          <div>
            <dt>Population</dt>
            <dd>{latest.population}</dd>
          </div>
          <div>
            <dt>Generation</dt>
            <dd>{latest.max_generation}</dd>
          </div>
        </dl>
      )}

      <h3>Population over time</h3>
      <ResponsiveContainer width="100%" height={140}>
        <LineChart data={history}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tick" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Line type="monotone" dataKey="population" stroke="#2563eb" dot={false} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>

      <h3>Average traits over time</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={history}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tick" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="avg_size" stroke="#16a34a" dot={false} name="Size" isAnimationActive={false} />
          <Line type="monotone" dataKey="avg_speed" stroke="#dc2626" dot={false} name="Speed" isAnimationActive={false} />
          <Line type="monotone" dataKey="avg_vision" stroke="#9333ea" dot={false} name="Vision" isAnimationActive={false} />
          <Line
            type="monotone"
            dataKey="avg_metabolism"
            stroke="#ea580c"
            dot={false}
            name="Metabolism"
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="avg_fertility"
            stroke="#0891b2"
            dot={false}
            name="Fertility"
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
