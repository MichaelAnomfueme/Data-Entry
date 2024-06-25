# Image Resizer Tool

The Image Resizer Tool is a command-line utility that allows user`s to convert and compress images. It provides options to resize images to a custom aspect ratio, compress images by reducing their quality, or perform both operations simultaneously.

## Features

- Conversion to custom aspect ratio: Users can specify a custom aspect ratio (e.g., 4:3, 16:9) to convert images accordingly.
- Compression: Users can reduce the quality of images to achieve a smaller file size.
- Progress Tracking: The tool provides a progress bar to track the conversion and compression processes.
- Output Organization: Converted and compressed images are saved in separate directories for easy access.

## Usage

The Image Resizer Tool accepts the following command-line arguments:

- `-i` or `--input`: Path to the input folder containing images.
- `-a` or `--aspect-ratio`: Custom aspect ratio to resize the images (e.g., 4:3, 16:9). Use "0:0" to skip this operation.
- `-q` or `--quality`: Compression percentage to reduce the image quality (0-100). Use 0 to skip this operation.

Examples:

To convert images in the "input" folder to a custom aspect ratio of 4:3:
```
python imageresizer.py -i input -a 4:3
```

To compress images in the "input" folder by 80% without resizing:
```
python imageresizer.py -i input -q 80
```

To convert images to a custom aspect ratio of 1:1 and compress them by 80%:
```
python imageresizer.py -i input -a 1:1 -q 80
```

## Windows Build

A Windows executable build of the Image Resizer Tool is also available. You can directly run the tool without installing Python or any dependencies. To use the Windows build, follow these steps:

1. Download the `ImageResizerTool.exe` file from the [Releases](https://github.com/your-username/ImageResizerTool/releases) section.
2. Open a command prompt or terminal and navigate to the directory where the `ImageResizerTool.exe` file is located.
3. Run the tool using the same command-line arguments mentioned in the "Usage" section.

Note: The Windows build may trigger a warning from some antivirus software due to the nature of executable files. If you encounter any issues, you can use the Python script version as an alternative.

## Folder Structure

The recommended folder structure for organizing your project is as follows:

```
ImageResizerTool/
  ├── imageresizer.py
  ├── README.md
  ├── .gitignore
  ├── converted/
  ├── compressed/
  └── ImageResizerTool.exe (Windows build)
```

- `imageresizer.py`: The main Python script that contains the image resizing and compression logic.
- `README.md`: The README file that provides an overview of the project, instructions, and other relevant information.
- `.gitignore`: The file that specifies which files and directories should be ignored by Git.
- `converted/`: The directory to store converted images.
- `compressed/`: The directory to store compressed images.
- `ImageResizerTool.exe`: The Windows executable build of the Image Resizer Tool.
