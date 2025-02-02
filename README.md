# triangle-art
A small pygame-based triangle art creation software written in Python
## Roadmap

v1.0:
- [X] Drawing
  - [X] Quarter triangle, half triangle and square drawing modes
  - [X] Six active colours
  - [X] Drawing colour selection
- [X] UI update
  - [X] Buttons for triangle mode
    - [X] Icon-based buttons
  - [x] Buttons for colour selection
    - [X] Buttons to set new colours
    - [X] Tkinter-based colour selection window
  - [X] Buttons for canvas reset and zoom control
  - [ ] Position and canvas size display
  - [ ] FPS display
- [X] Efficiency
  - [X] Trim blank canvas
- [ ] File operations
  - [X] Custom .tri format
  - [ ] Custom .tri2 format (improved efficiency)
    - [ ] Direct binary values
    - [ ] Preserve view position and scale
    - [ ] Dictionary-based compression
  - [ ] PPM (.ppm) format export
- [ ] Settings
  - [X] Tkinter-based settings window
  - [X] Keyboard controls display
  - [X] pygame window size control
  - [X] FPS target modification
  - [ ] .set file for settings preservation