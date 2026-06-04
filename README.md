# `datahues`

A library for generating perceptually uniform colour ramps using the Oklab colour space.

## Overview

`datahues` creates smooth, visually consistent colour gradients from a start colour to an end colour. Unlike simple RGB or HSL interpolation, which can produce perceptually uneven ramps with visible banding, this library leverages the **Oklab colour space** — a perceptually uniform space where equal mathematical changes correspond to equal perceptual colour differences.

## Core Functions

### `generate_hex_list(start_hex, end_hex, n_stops=512)`

Between start and end colours, generates a list of hex colour codes representing points along a smooth colour ramp. It is assumed the user wants a discrete number (`n_stops`) of points, so no warning is given when `n_stops` is small (unlike in `generate_cmap` below). However, if these hexes are being used to create a continuous colour ramp, it is recommended to use `n_stops`>=128.

- **Parameters:** 
  - `start_hex`: Starting colour as hex code (e.g., `"#FF0000"`)
  - `end_hex`: Ending colour as hex code (e.g., `"#0000FF"`)
  - `n_stops`: Number of colour stops in the ramp (default: 512)
- **Returns:** List of hex colour codes representing the gradient

### `generate_cmap(start_hex, end_hex, n_stops=512, name="interp_ramp")`

Betweem start and end colours, creates a Matplotlib `LinearSegmentedColormap` object, forming a smooth colour ramp.

- **Parameters:**
  - `start_hex`, `end_hex`, `n_stops`: As above
  - `name`: The "name" of the colour ramp for matplotlib internal purposes (default: "interp_ramp")
- **Returns:** `LinearSegmentedColormap` object ready to use in matplotlib visualisation
- **Warning:** `n_stops < 128` may produce visible banding; use larger values for smoother results


## How It Works

The library converts colours through multiple colour spaces to achieve perceptual uniformity:

1. **Hex → RGB** — Parse hex codes into normalised [0.0, 1.0] RGB values
2. **RGB → XYZ** — Apply gamma correction and convert to CIE XYZ (D65 illuminant)
3. **XYZ → Oklab** — Convert through LMS intermediate space to Oklab (perceptually uniform)
4. **Interpolate in Oklab** — Create evenly-spaced values in perceptual space
5. **Oklab → RGB → Hex** — Reverse conversion back to hex color codes

This approach ensures that visual transitions between colours feel smooth and natural across the entire gradient.

## To Do

- #TODO git tag versioning
- #TODO test suite
- #TODO publish to pypi
- #TODO publish to conda-forge
- #TODO example (with picture!) in README
- #TODO blogpost
- #TODO set up test coverage
- #TODO github badges
