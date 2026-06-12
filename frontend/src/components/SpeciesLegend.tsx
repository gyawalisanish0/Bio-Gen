import type { Species } from "../types";
import { polygonPoints } from "../shapes";

const ICON_SIZE = 18;
const CENTER = ICON_SIZE / 2;
const RADIUS = ICON_SIZE / 2 - 2;

interface Props {
  species: Species[];
}

export function SpeciesLegend({ species }: Props) {
  if (species.length === 0) return null;

  return (
    <div className="species-legend">
      <h3>Species</h3>
      <ul className="species-legend-list">
        {species.map((s) => (
          <li key={s.id} className="species-legend-item">
            <svg width={ICON_SIZE} height={ICON_SIZE} viewBox={`0 0 ${ICON_SIZE} ${ICON_SIZE}`}>
              <SpeciesIcon species={s} />
            </svg>
            <span>Species {s.id + 1}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SpeciesIcon({ species }: { species: Species }) {
  const fill = `hsl(${species.hue}, 75%, 50%)`;
  const points = polygonPoints(species.shape, CENTER, CENTER, RADIUS);

  if (!points) {
    return <circle cx={CENTER} cy={CENTER} r={RADIUS} fill={fill} stroke="rgba(0, 0, 0, 0.4)" />;
  }

  return <polygon points={points.map(([x, y]) => `${x},${y}`).join(" ")} fill={fill} stroke="rgba(0, 0, 0, 0.4)" />;
}
