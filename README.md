# Pixel-based-Roughness-Analysis-from-Microscopy-Images
Method for analysis of the roughness of spherical microparticles as well as parts of microparticles or other objects.

The python script in this repository is a modified version of Deniz Hülagüs (Username on Github: DenizHulagu) code, which can be found under:

https://github.com/BAMresearch/Roughness-Analysis-by-Electron-Microscopy

This originally code accompanies the following publication:

Hülagü, D., Tobias, C., Climent, E., Gojani, A., Rurack, K., Hodoroaba, V.-D., Generalized analysis approach of the profile roughness by electron microscopy with the example of hierarchically grown polystyrene-iron oxide silica core-shell-shell particles. Advanced Engineering Materials, 2022. DOI: 10.1002/adem.202101344  


If you use the code from this repository in your own work, please cite the following:

-	Webadress of this code repository.

-	Webadress of the original code repository from BAMresearch mentioned above.

-	The publication of Hülagü et al. mentioned above. 


# Contact information:
For questions or related topics please contact via e-mail or visit the homepage of the Mandel group for further current contact information:

-	thomas.zimmermann@fau.de

-	karl.mandel@fau.de

-	https://www.chemistry.nat.fau.eu/mandel-group/ 


# How to use the code:

- The following seven steps have to be done one time to set up the program:

  - Download the program “Anaconda Navigator (Anaconda3)” on your computer.
  
  - Download the environment data “Roughness-analysis-environment.yaml” from GitHub repository and copy it to the desktop. In the last line of the document “prefix: C:\Users\[user name]\.conda\envs\default” make sure to replace [user name] with the user name of the PC, on which you want to install the environment.
  
  - Open “CMD.exe Prompt” from “Anaconda Navigator”.
  
  - Activate Environments using the command: “conda activate default”.
  
  - Create environment using the command: “conda env create -f \Users\[user name]\Desktop\Roughness-analysis-environment.yaml”. Make sure to replace [user name] with the user name of the PC, on which you want to install the environment.
  
  - In Anaconda Navigator select the environment “Roughness-analysis-environment”. (This environment can be set to the default starting environment via File - Preferences - Default conda environment).
  
  - Download the python script “Roughness-analysis.py” from GitHub repository and copy it to a folder of your choice.
  
-	Open “Spyder (5.4.1)” from “Anaconda Navigator”.

-	Open the python script with “Spyder (5.4.1)”.

- Copy the binarized image you want to  analyze into the same folder as the python script. 

  - If you want analyze a zoomed in part of an object, make sure that after binarizing, there is a frame in the background color around the object of at least one pixel thickness.

-	In the opened python script in “Spyder (5.4.1)” scroll down to the end of the code and put in the following information (between the two lines of #):

    -	scale_value = X (input value shown above scale bar without unit)
    -	scale_lenght = Y (input pixel length of scale bar)
    -	unit = 'µm' (input the displayed unit of scale bar here ("µm", "nm", "mm" etc.)
    -	sample_name = 'Sample name'   (Input file name without file extension here)
    -	which_side = 'none'  (Choose one of the five options: 
        -	none [the full spherical particle will be analyzed]
        -	left [the left side of a structure will be analyzed; all values with the highest y-value, the lowest y-value and the highest x-value will be excluded]
        -	right [the right side of a structure will be analyzed; all values with the highest y-value, the lowest y-value and the lowest x-value will be excluded]
        -	top [the top side of a structure will be analyzed; all values with the lowest y-value, the lowest x-value and the highest x-value will be excluded]
        -	bottom [the bottom side of a structure will be analyzed; all values with the highest y-value, the lowest x-value and the highest x-value will be excluded])
    -	image_path = sample_name + '.tif' (input file extension here)
-	Press the run button.
-	The pyhton script will output 9 files. “XXXX” is a placeholder for the name of the analyzed image.
    -	Threshold image: “XXXX_IsoData_threshold.tif”
    -	Detected border as image and csv file: “XXXX_border.png” and “XXXX_Borderpoints_All_List.png”
    -	Optimized center from detected border: “XXXX_optimized_center.png”
    -	Distribution of distances as a function of angles as plot and csv file: “XXXX_angles_and_distance.png” and “XXXX_angles_and_distances.csv”
    -	Distribution of distances as histogram and csv file: “XXXX_distance_distribution.png” and “XXXX_distance_distribution.csv”
    -	Summary of the data (specified in subpoint) as txt file: “XXXX_data.txt”
        -	Mode “none” (spherical particle): Name, roughness, mean radius, roughness divided by radius, optimized center, resolution, used scale information, number of detected border points, greatest distance difference.
        -	Mode “right”, “left”, “top” or “bottom” (parts of particle or another object): Name, resolution, used scale information, Standard deviation (=roughness if object was flat), Note that further analysis is required for non-flat samples. The data can be fitted using a graphing software (e.g., Origin) and the averaged value of the deviation from the fit represents the roughness.
