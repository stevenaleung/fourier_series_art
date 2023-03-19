# fourier_series_art
Line art drawn with Fourier series!

## Setup
1. Clone the repo
2. Install dependencies using pip
3. Create a csv file that contains x, y coordinates for each point in the image

### Create the coordinates csv file
1. Import the image into Inkscape
2. Use Extensions > Modify Path > Add Nodes to increase sampling rate along the path
3. Use Extensions > Export > Export XY (https://github.com/jwcliff/Inkscape_Exportxy) to output the x, y coordinates for each node

## Usage
```
python3 draw.py coordinates/hummingbird.csv
```

Output:\
<img src="https://github.com/stevenaleung/fourier_series_art/blob/main/output/hummingbird.gif" />
