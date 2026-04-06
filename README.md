# Rocket Launch Simulation

A simple physics-based simulation of launching a rocket from Earth and observing its trajectory under gravity.  
This project helps visualize how initial velocity affects orbital motion.

## Tech Stack
- **Language**: Python  
- **Libraries**: `pygame`, `math`, `random`, `sys`  
- **Numerical Method**: Euler Integration

## Controls
| Key | Description |
|-----|------------|
| `Arrow Keys` | Adjust initial velocity and launch conditions |
| `<` / `>` | Fine adjustment |
| `1` | Toggle information display |
| `2` | Toggle vector display (current speed of the rocket)|
| `3` | Toggle distance display (distance between earth and the rocket)|

## Features
- Gravity-based motion centered on Earth
- Real-time trajectory visualization
- Vector and distance display options
- Interactive control of initial conditions
- Live physics data display:
  - Potential Energy (P.E.)
  - Kinetic Energy (K.E.)
  - Distance from Earth
  - Current speed
  - Escape velocity
- Status detection system:
  - `Crash` (collision with Earth)
  - `Orbit` (bounded trajectory)
  - `Escape` (leaving Earth's gravity)

## What I Learned
-  Without additional thrust after launch, achieving a stable orbit is difficult  
-  Most trajectories naturally form elliptical orbits  
-  Initial velocity (magnitude and direction) is critical for orbit formation  
