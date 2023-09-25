import skimage.io
import skimage.color
import skimage.filters
import statistics
import numpy as np
import matplotlib.pyplot as plt
import math as m
import os
from PIL import Image


def read_image(path):
    return Image.open(path)

def is_white(pixel):
    if isinstance(pixel, int):
        return pixel > 0
    else:
        return pixel[0] >= 150 and pixel[1] >= 150 and pixel[2] >= 150

def is_black(pixel):
    return not is_white(pixel)

def contains(element, array):

    for current in array:
        if element[0] == current[0] and element[1] == current[1]:
            return True

    return False

def get_neighbors(current, allpoints, process, chain):
    neighbors = []

    for point in allpoints:
        if current[0] == point[0] and current[1] == point[1]:
            continue

        if abs(current[0] - point[0]) <= 1 and abs(current[1] - point[1]) <= 1:
            if not contains(point, chain) and not contains(point, process):
                neighbors.append(point)

    return neighbors

def create_chain(allpoints, process, chain):

    chain.append(process[0])

    neighbors = get_neighbors(process[0], allpoints, process, chain)
    for neighbor in neighbors:
        process.append(neighbor)

    process.pop(0)

    pass

def find_chain(allpoints):
    chain = []
    process = []

    process.append(allpoints[0])

    while len(process) > 0:
        create_chain(allpoints, process, chain)

    return chain

def find_border_points(image, image_path):
    all_points = np.array([[0,0]])

    topLeftPixel = image.getpixel((0, 0))
    isSEM = is_black(topLeftPixel)
    isTEM = not isSEM
    im = Image.open(image_path)
    
   
    for y in range(0, im.size[1]):         #change from fixed pixel range to automatic full picture size
        for x in range(0, im.size[0]):
            pixel = image.getpixel((x, y))
            if (isSEM and is_white(pixel)) or (isTEM and is_black(pixel)):
                border_found = False
                for neighborhood_y in range(y - 1, y + 2):
                    for neighborhood_x in range(x - 1, x + 2):
                        if not border_found:
                            neighborhood_pixel = image.getpixel((neighborhood_x, neighborhood_y))
                            if (isSEM and is_black(neighborhood_pixel)) or (isTEM and is_white(neighborhood_pixel)):
                                border_found = True
                                point = np.array([[x,y]])
                                all_points = np.append(all_points, point, axis = 0)
                                #print(point)
              
    all_points = np.delete(all_points, 0, 0)

    print("Started finding real border")
    border = find_chain(all_points)
    
     
    np.savetxt(sample_name + '_borderpoints_temp1.csv', border, delimiter=',', fmt='%i') #save borderpoints as .csv file. fmt='%i' is for displaying numbers without decimals
    with open(sample_name + '_borderpoints_temp1.csv') as fin, open(sample_name + '_borderpoints_temp2.csv', 'w') as fout:
        for line in fin:
            fout.write(line.replace(',', ';')) # replace , with ; because standard setting in excel is separation of columns with ; => we now have 2 columns 
    sortedlist = np.loadtxt(sample_name + '_borderpoints_temp2.csv', dtype=str)
    sortedlist.sort()                                                            #sorts list on ascending x values
    np.savetxt(sample_name + '_Borderpoints_All_List.csv', sortedlist, fmt='%s')        #saves final list of all border points, sorted by x values, as .csv file
    
    if which_side != "none":   #only runs the following lines if picture is a zoomed in one (left, right, top or bottom)
        with open(sample_name + '_Borderpoints_All_List.csv') as fin, open(sample_name + '_borderpoints_temp3.csv', 'w') as fout:
            for line in fin:
                fout.write(line.replace(';', ' '))  #open file containing all borderpoints and replace the ; with a space. needs to be done to convert string to integer (needed to be able to determine max/min values)
        relevant_border_values = np.loadtxt(sample_name + '_borderpoints_temp3.csv', dtype=int)
        if which_side != "right": 
            relevant_border_values = np.delete(relevant_border_values, np.where((relevant_border_values[:, 0] == relevant_border_values.max(axis=0)[0])) [0], axis=0) #deletes lines where x value equals max x value 
        if which_side != "left":
            relevant_border_values = np.delete(relevant_border_values, np.where((relevant_border_values[:, 0] == relevant_border_values.min(axis=0)[0])) [0], axis=0) #deletes lines where x value equals min x value 
        if which_side != "bottom":         
            relevant_border_values = np.delete(relevant_border_values, np.where((relevant_border_values[:, 1] == relevant_border_values.max(axis=0)[1])) [0], axis=0) #deletes lines where y value equals max y value 
        if which_side != "top": 
            relevant_border_values = np.delete(relevant_border_values, np.where((relevant_border_values[:, 1] == relevant_border_values.min(axis=0)[1])) [0], axis=0) #deletes lines where y value equals min y value 

        np.savetxt(sample_name + '_Only_' + which_side + '_Side_temp1.csv', relevant_border_values, fmt='%i')
        with open(sample_name + '_Only_' + which_side + '_Side_temp1.csv') as fin, open(sample_name + '_Only_' + which_side + '_Side.csv', 'w') as fout:
            for line in fin:
                fout.write(line.replace(' ', ';')) #saves file with border values of only one side, as .csv file in 2 columns
        os.remove(sample_name + '_borderpoints_temp3.csv')
        os.remove(sample_name + '_Only_' + which_side + '_Side_temp1.csv')            
        
    os.remove(sample_name + '_borderpoints_temp1.csv')
    os.remove(sample_name + '_borderpoints_temp2.csv')
        #creates a temporary .csv file, uses that file to create a new, organised one containing all the pixel values of the border points. Then it deletes the temporary one afterwards
    
    
    print("Finished finding real border")
    return border

def plot_border_points(sample_name, image, border_points):
    edited_image = image.copy()
    for point in border_points:
        #print(point)
        edited_image.putpixel((point[0], point[1]), (255, 0, 0, 255))

    #edited_image.show()
    edited_image.save(sample_name + '_border.png')
    return

def calculate_initial_center(border_points):
    initial_center = np.average(border_points, axis=0)
    print("center X,Y is ", initial_center)
    return initial_center

def search_left(optimized_center, border_points, current_stdev):
    return search_direction(-1, 0, optimized_center, border_points, current_stdev)

def search_right(optimized_center, border_points, current_stdev):
    return search_direction(1, 0, optimized_center, border_points, current_stdev)

def search_up(optimized_center, border_points, current_stdev):
    return search_direction(0, -1, optimized_center, border_points, current_stdev)

def search_down(optimized_center, border_points, current_stdev):
    return search_direction(0, 1, optimized_center, border_points, current_stdev)

def search_direction(delta_x, delta_y, optimized_center, border_points, current_stdev):
    potential_center = (optimized_center[0] + delta_x, optimized_center[1] + delta_y )
    potential_distances = calculate_distances(potential_center, border_points)
    potential_stdev = statistics.stdev(potential_distances)

    if potential_stdev < current_stdev:
        optimized_center = potential_center

    return optimized_center

def optimize_center(initial_center, border_points):
    optimized_center = initial_center

    #print(optimized_center)

    current_distances = calculate_distances(optimized_center, border_points)
    current_stdev = statistics.stdev(current_distances)
    previous_stdev = current_stdev * 2

    print("Initial Standard Deviation ", current_stdev)
    
    if which_side == "none":
        stdev_stop = 0
    else:
        stdev_stop  =0.5
    
    while previous_stdev-current_stdev > stdev_stop:          #changed to possibly alter how accurate current_stdev is. see if-block above. full particle -> hisg precision. cut out -> low, bc it does not matter here
        print("Previous stdev was ", previous_stdev)
        print("Current stdev is ", current_stdev)

        previous_stdev = current_stdev

        optimized_center = search_left(optimized_center, border_points, current_stdev)
        optimized_center = search_right(optimized_center, border_points, current_stdev)
        optimized_center = search_up(optimized_center, border_points, current_stdev)
        optimized_center = search_down(optimized_center, border_points, current_stdev)

        current_distances = calculate_distances(optimized_center, border_points)
        current_stdev = statistics.stdev(current_distances)

    print("Final stdev is ", current_stdev)
    print("Roughness is ", current_stdev)


    mean = statistics.mean(current_distances)
    print("Mean radius is ", mean) 
    

    if which_side == 'none':   
        q = open(sample_name + "_data.txt", "w")
        L = [sample_name, "\n\nRoughness is: ", str(current_stdev), " ", unit, "\nMean radius is: ", str(mean), " ", unit, "\nRoughness/Radius = ", str((current_stdev/mean)) ,"\n\nOptimized center XY is: ", str(optimized_center), "\nResolution is: one pixel equals ", str(Q)," ", unit, "\nScale information : scale value = ", str(scale_value), "    scale length = ", str(scale_length) ]
        q.writelines(L)
        q.close()    
    else: 
        q = open(sample_name + "_data.txt", "w")
        L = [sample_name,  "\n\nResolution is: one pixel equals ", str(Q)," ", unit, "\nScale information : scale value = ", str(scale_value), "    scale length = ", str(scale_length) ]
        q.writelines(L)
        q.close()          # creates .txt file with different content data depending on original image (full particle or top/bottom or left/right)

    return optimized_center

def draw_target(sample_name, image, position, color):
    image_copy = image.copy()
    for index in range(-25, 25):
        x = int(position[0])
        y = int(position[1])
        image_copy.putpixel(((x + index), y), color)
        image_copy.putpixel((x, (y + index)), color)

    #image_copy.show()
    image_copy.save(sample_name + '_optimized_center.png')

    return image_copy

def calculate_center(image, border_points):
    initial_center = calculate_initial_center(border_points)
    edited_image = draw_target(sample_name, image, initial_center, (255, 0, 0, 255))

    optimized_center = optimize_center(initial_center, border_points)
    draw_target(sample_name, edited_image, optimized_center, (0, 0, 255, 255))
    print("Optimized center is ", optimized_center)
    return optimized_center

def plot_distance_distribution(sample_name, distances):
    x_array = []

    index = 0
    for item in distances:
        x_array.append(index)
        index = index +1
 
    plt.hist(distances, bins=50, edgecolor='black', linewidth=1.2)
    plt.xlabel('Radius ['+str(unit)+']', fontsize=16)   #changed to automatically change Radius unit depending on input 
    plt.ylabel('Number count', fontsize=16)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=16)
  
    plt.autoscale(enable=True) # changed to enable autoscaling axes 

    N = len(distances)
    print("Number of detected border points is ", N)
    
    dist = np.array(distances)
    counts, bins, bars = plt.hist(distances, bins=50, edgecolor='black', color="b", linewidth=1.2)
    
    counts_ = np.array(counts)
    counts_= np.append(counts_, "0")    #appending a 0 so counts_ and bins_ are same lenth 
    bins_ = np.array(bins)
    f = open(sample_name + "_temp.csv", "w")    
    for i in range(0, len(bins_)):
        f.write("{};{}\n".format(bins_[i], counts_[i]))     #create csv file with a-d 
    f.close()
    with open(sample_name + '_temp.csv') as fin, open(sample_name + '_distance_distribution.csv', 'w') as fout:
        for line in fin:
            fout.write(line.replace('.', ','))
    os.remove(sample_name + '_temp.csv')

    q = open(sample_name + "_data.txt", "a")        # writes more information in previous .txt file 
    
    if which_side == 'none': 
        M = ["\nNumber of detected border points is: ", str(N), "\nGreatest distance difference = ", str(np.max(dist)-np.min(dist)), " ", unit]
    else:
        if which_side == "left" or which_side == "right":          # change to document the standard deviation of the zoomed in picture, only applies if it IS a zoomed picture
            zoom_stdev = statistics.stdev(np.loadtxt(sample_name + '_Only_' + which_side + '_Side.csv', delimiter=";", usecols=(0)))
            print("Xstdev= ", zoom_stdev, which_side)
            M = ["\n\nStandard deviation (zoomed in picture, non-curved only) is ", str(zoom_stdev), " ", str(unit), "\n\nIf data shows curvature further analysis (eg in Origin) is needed"]
        elif which_side == "top" or which_side == "bottom" :
            zoom_stdev = statistics.stdev(np.loadtxt(sample_name + '_Only_' + which_side + '_Side.csv', delimiter=";", usecols=(1)))
            print("Ystdev= ", zoom_stdev, which_side)
            M = ["\n\nStandard deviation (zoomed in picture, non-curved only) is ", str(zoom_stdev), " ", str(unit), "\n\nIf data shows curvature further analysis (eg in Origin) is needed"]
    
    q.writelines(M)
    
    q.close()
    
    plt.savefig(sample_name + '_distance_distribution.png', bbox_inches='tight' ) #added bbox_inches='tight' to fit the enire plot + axis lables in picture
    return

def calculate_distances(center, border_points):
    return_value = np.empty(0)

    x1 = center[0]
    y1 = center[1]

    for border_point in border_points:
        x2 = border_point[0]
        y2 = border_point[1]
        distance = (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) * (Q)
     
        return_value = np.append(return_value, distance)

    return return_value

def calculate_angles(center, border_points):
    return_value = np.empty(0)
    length = len(border_points)

    first_vector = np.array([1, 0])
    print("Finding angles")

    for index in range(0, length):
        next_vector = np.array(border_points[index]) - np.array(center)
        angle = np.math.atan2(np.linalg.det([first_vector, next_vector]), np.dot(first_vector, next_vector))
        degrees = np.degrees(angle)

        if degrees < 0:
            degrees = 360 + degrees

        degrees = 360 - degrees

        return_value = np.append(return_value, degrees)

    return return_value

def plot_angles_and_distances(sample_name, angles, distances):
    plt.clf()                                                   
    plt.plot(angles, distances, 'o', color="b", markersize=2)
   
    plt.xlabel('Angle [degree]', fontsize=16)
    plt.ylabel('Distance ['+str(unit)+']', fontsize=16) #same changes as in plot_distance_distribution

    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=16)
    plt.xlim(0, 360)
  
    plt.ylim(np.min(distances)*0.95, np.max(distances)*1.05) #pseudo autoscaling with 5% above and below highest and lowest datapoint respectively 
  

    plt.savefig(sample_name + '_angles_and_distance.png', bbox_inches='tight') #added bbox_inches='tight' to fit the enire plot + axis lables in picture

    return


def save_data(sample_name, angles, distances):
    a = np.array(distances)
    b = np.array(angles)
    f = open(sample_name + "_angles_and_distances.csv", "w")    
       
    for i in range(0, len(a)):
        f.write("{},{}\n".format(b[i], a[i]))     #create csv file angles in first colums, distances in second 
    
    f.close()
    return

def IsoData_threshold(source):

    thold = skimage.filters.threshold_isodata(source)

    print("Threshold is ", thold)

    applied = source > thold
    colored = skimage.color.gray2rgb(applied)
    skimage.io.imsave(sample_name + "_IsoData_threshold.tif", colored)

    return thold

#######################################################################################################################################################################################################
#changed to have access to change all variables here and have automaitc changes 
scale_value = 1      # input value shown above scale bar without unit
scale_length = 202      # input pixel length of scale bar
unit = 'µm'             # input displayed unit of scale bar here ("µm", "nm", "mm" etc.)
sample_name = 'Supraparticle_threshold'   #Input file name here
which_side = 'none'                       # "left", "right", "top" or "bottom". "none" if looking at full particle. All lower case
image_path = sample_name + '.tif'        #input file extension here. No input necessary if picture is .tif format


#######################################################################################################################################################################################################
Q = (scale_value/scale_length)
source = skimage.io.imread(image_path)
threshold = IsoData_threshold(source)
image = read_image(sample_name + "_IsoData_threshold.tif")
border_points = find_border_points(image, image_path)
plot_border_points(sample_name, image, border_points)
center = calculate_center(image, border_points)
distances = calculate_distances(center, border_points)
plot_distance_distribution(sample_name, distances)
angles = calculate_angles(center, border_points)
plot_angles_and_distances(sample_name, angles, distances)
save_data(sample_name, angles, distances)
print("Threshold is ", threshold)
print ("Calculations finished")
