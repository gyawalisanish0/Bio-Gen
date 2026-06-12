import type { Genome } from "./types";

/**
 * Mirrors backend/app/config.py TRAIT_BOUNDS. Kept in sync manually since the
 * frontend only needs the (min, max) range for visualization/UI scaling.
 */
export const TRAIT_BOUNDS: Record<keyof Genome, [number, number]> = {
  size: [0.5, 2.0],
  speed: [0.5, 2.5],
  vision: [1.0, 5.0],
  metabolism: [0.5, 2.0],
  fertility: [0.5, 2.0],
};
