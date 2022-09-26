# two_scales_fusion_3d
This project consists of using MPS to resize the xy slices in Tif format, seeking to bring the information from the coarse scale to the fine scale. The files present in this project are:

- run_parallel_3D: runs MPS for each of the slices, it's the main file.
- pre_process_date: normalizes the histogram according to the quantiles (2% to 98%), since the images in the two scales have different contrasts
- generate_image: generates each of the images resized by MPS
- image_segmentation: segment the image into pore/non-pore using otsu algorithm.
- porosity_calculation: calculates porosity
  
### prerequisites
- Pillow 9.2.0
- scikit-image 0.19.3
- scikit-mps
- matplotlib

### how to run the algorithm
```
python run_parallel_3d.py
```

## how to calculate the porosity
```
python image_segmentation.py
```
```
python porosity_calculation.py
```