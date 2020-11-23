# fourier_series_art

Python code to draw line art using Fourier series

## Setup

1. Clone the repo
2. Install the necessary dependencies using pip3
3. Install FFmpeg and ImageMagick (if you want to save the animations)
3. Create a csv file that contains x, y coordinates for each point in the image
	- My current workflow is to i) import the image into Inkscape, ii) use Extensions > Modify Path > Add Nodes to increase sampling rate along the path, then iii) use Extensions > Export > Export XY (https://github.com/jwcliff/Inkscape_Exportxy) to output the x, y coordinates for each node

## Usage

```
python3 drawArt.py source_material/hummingbird_coordinates.csv
```

Output:\
![Hummingbird drawn with Fourier series](https://github.com/stevenaleung/fourier_series_art/blob/develop/movies/hummingbird.gif)
