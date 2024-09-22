# GLB to GIF Converter

This tool allows you to convert 3D GLB (GL Transmission Format Binary) files into animated GIF images. It creates a smooth 360-degree rotation of the 3D model, making it easy to visualize 3D assets in a web-friendly format.

## Features

- Convert GLB files to animated GIFs
- Customizable number of frames and resolution
- Adjustable camera positioning for optimal view
- Works on headless servers (like EC2 instances)
- Smooth, constant rotation speed

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/glb-to-gif-converter.git
   cd glb-to-gif-converter
   ```

2. Install the required system packages (for Ubuntu/Debian):
   ```
   sudo apt-get update
   sudo apt-get install -y xvfb libgl1-mesa-glx
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```
python glb2gif.py input_model.glb output_animation.gif
```

Advanced usage with custom settings:
```
python glb2gif.py input_model.glb output_animation.gif --num_frames 120 --resolution 1024 768
```

Options:
- `--num_frames`: Number of frames in the output GIF (default: 60)
- `--resolution`: Width and height of the output GIF (default: 800 600)

## Examples

Convert a character model to a GIF:
```
python glb2gif.py character.glb character_rotate.gif
```

Create a high-resolution GIF with more frames:
```
python glb2gif.py product.glb product_showcase.gif --num_frames 180 --resolution 1920 1080
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyRender](https://github.com/mmatl/pyrender) for 3D rendering
- [Trimesh](https://github.com/mikedh/trimesh) for 3D model handling
- [Pillow](https://python-pillow.org/) for image processing
