export type ShapeName = "circle" | "triangle" | "square" | "pentagon" | "hexagon" | "diamond";

export const SHAPE_NAMES: ShapeName[] = ["circle", "triangle", "square", "pentagon", "hexagon", "diamond"];

interface PolygonDef {
  sides: number;
  rotation: number;
}

const POLYGONS: Record<string, PolygonDef> = {
  triangle: { sides: 3, rotation: -Math.PI / 2 },
  square: { sides: 4, rotation: Math.PI / 4 },
  pentagon: { sides: 5, rotation: -Math.PI / 2 },
  hexagon: { sides: 6, rotation: 0 },
  diamond: { sides: 4, rotation: 0 },
};

/**
 * Returns the vertices of the given shape centred at (cx, cy) with the given
 * radius, or null for "circle" (which callers should draw with ctx.arc).
 */
export function polygonPoints(shape: ShapeName, cx: number, cy: number, radius: number): Array<[number, number]> | null {
  const def = POLYGONS[shape];
  if (!def) return null;

  const points: Array<[number, number]> = [];
  for (let i = 0; i < def.sides; i++) {
    const angle = def.rotation + (i * 2 * Math.PI) / def.sides;
    points.push([cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)]);
  }
  return points;
}
