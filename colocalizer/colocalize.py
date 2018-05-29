"""
Module to spatially colocalize files
"""
DEBUG = False
if __name__ == '__main__':
    # Change to parent directory for imports
    # Debugging purposes!
    import os
    import sys
    import inspect

    CURRENT_DIR = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    sys.path.insert(0, PARENT_DIR)

    DEBUG = True

import os.path
import csv
import datetime
from colocalizer.helper_functions import save_binary_image, get_append_or_write, distance, angle
from structures import Options
import skimage.measure
from skimage.io import imread
import numpy as np

_callback = None
_currentrun = None


def spatial_colocalize(fileinfos, options: Options):
    """Performs spatial colocalization of the given files

    Arguments:
        fileinfos {iterable of ChannelInfo} -- [description]
        options {Options} -- [description]
    """

    assert _currentrun, "please call new_run before starting a analysis"

    data = list()

    for info in fileinfos:
        file, datafile, maskoutput, channelname = info
        _log("Loading file \"{0}\"".format(file))
        image = imread(file)
        dataimg = imread(datafile) if datafile else None

        data.append(
            # todo: turn into named touple?
            (image, dataimg, maskoutput, channelname)
        )

    images = next(zip(*data))  # first element of each tuple is the image
    # these are not the final masks!
    masks = [image > options.threshold for image in images]

    connectivity = 2 if options.diagnoalconnectivity else 1
    labeled_masks = [skimage.measure.label(
        m, connectivity=connectivity) for m in masks]

    overlapping_areas = (np.ones_like(masks[0]) == 1)  # Full true array

    for mask in masks:
        overlapping_areas = np.logical_and(overlapping_areas, mask)

    selection_masks = list()

    for index in range(0, len(masks)):
        ids = np.unique(labeled_masks[index][overlapping_areas])
        _log("{0} objects in \"{1}\"".format(len(ids), fileinfos[index][3]))

        selection_mask = np.in1d(
            labeled_masks[index], ids).reshape(images[index].shape)
        # selections masks selects features, that overlap with other features

        mask_filename = data[index][2]
        if mask_filename:  # third entry of the tuple contains a filename, if mask should be saved
            _log("Saving mask as {0}".format(mask_filename))
            save_binary_image(mask_filename, selection_mask)

        selection_masks.append(selection_mask)

    # selection mask labels
    mask_labels = [skimage.measure.label(
        mask, connectivity=connectivity) for mask in selection_masks]

    if options.csvfolder:
        _log("Calculating statistics")
        os.makedirs(os.path.dirname(options.csvfolder), exist_ok=True)

        standard_csv_lines = list()
        overlap_csv_lines = list()

        for index in range(0, len(masks)):
            _log("Working on statistics from {0}".format(data[index][3]))

            current_labels = mask_labels[index]
            regionprops = skimage.measure.regionprops(
                current_labels, intensity_image=data[index][1], cache=False)

            for region in regionprops:
                csvrow = dict()

                csvrow["channel"] = fileinfos[index][3]
                csvrow["object_id"] = region.label
                csvrow["sourcefile"] = fileinfos[index][0]

                if "area_px" in options.statistics:
                    #_log("Calculating particle areas")
                    csvrow["area_px"] = region.area

                if "intensity_mean" in options.statistics:
                    #_log("Calculating intensity avg")
                    try:
                        csvrow["intensity_mean"] = region.mean_intensity
                    except AttributeError:
                        _log("Trying to calculate intensity without data file!")
                        csvrow["intensity_mean"] = "No data image specified!"

                if "intensity_max" in options.statistics:
                    #_log("Calculating intensity max")
                    try:
                        csvrow["intensity_min"] = region.min_intensity
                        csvrow["intensity_max"] = region.max_intensity
                    except AttributeError:
                        _log("Trying to calculate intensity without data file!")
                        csvrow["intensity_min"] = "No data image specified!"
                        csvrow["intensity_max"] = "No data image specified!"

                if "com" in options.statistics:
                    csvrow["com_unweighted"] = region.centroid
                    csvrow["com_unweighted_local"] = region.local_centroid
                    try:
                        csvrow["com_weighted"] = region.weighted_centroid
                        csvrow["com_weighted_local"] = region.weighted_local_centroid
                    except AttributeError:
                        pass  # no data file specified

                if "area_overlap_px" in options.statistics:
                    # Area overlapping in all channels
                    minimal_overlapping_area = 0

                    for comparisonchannel in [i for i in range(0, len(masks)) if i != index]:
                        own_id = region.label
                        own_selection = mask_labels[index] == own_id

                        comparison_ids = np.array(
                            labeled_masks[comparisonchannel])

                        print(comparison_ids)

                        comparison_ids[np.logical_not(
                            own_selection)] = 0

                        # comparison_ids now contains ids present in both channels
                        ids_to_select = np.unique(comparison_ids)

                        # now create the final label mask, since the above solution cuts of
                        # areas not in both channels!

                        comparison_label_mask = np.in1d(
                            labeled_masks[comparisonchannel], ids_to_select).reshape(images[index].shape)

                        comparison_labels = np.array(labeled_masks[comparisonchannel])
                        comparison_labels[np.logical_not(comparison_label_mask)] = 0

                        if DEBUG:
                            print(comparison_labels)

                        # todo: implement data image
                        overlappingregions = None

                        if data[comparisonchannel][1]:
                            overlappingregions = skimage.measure.regionprops(
                                comparison_labels,
                                intensity_image=data[comparisonchannel][1],
                                cache=False)
                        else:
                            overlappingregions = skimage.measure.regionprops(
                                comparison_labels,
                                cache=False)

                        cumulative_overlap = 0

                        if DEBUG:
                            print("Comparing")
                            print(comparison_label_mask)

                        minimal_overlapping_area = np.logical_and(
                            comparison_label_mask, overlapping_areas)
                        minimal_overlapping_size = np.count_nonzero(
                            minimal_overlapping_area)

                        for overlap in overlappingregions:
                            detailedoverlapcsvrow = dict()

                            detailedoverlapcsvrow["source_channel"] = data[index][3]
                            detailedoverlapcsvrow["source_id"] = region.label
                            detailedoverlapcsvrow["comparison_channel"] = data[comparisonchannel][3]
                            detailedoverlapcsvrow["comparison_id"] = overlap.label
                            detailedoverlapcsvrow["area_in_both_channels"] = overlap.area

                            # calculate distances
                            distance_unweighted = distance(
                                region.centroid, overlap.centroid)
                            angle_unweighted = angle(
                                region.centroid, overlap.centroid)

                            distance_weighted = "No data file specified"
                            angle_weighted = "No data file specified"

                            detailedoverlapcsvrow["distance_unweighted"] = distance_unweighted
                            detailedoverlapcsvrow["angle_unweighted"] = angle_unweighted

                            try:
                                distance_weighted = distance(
                                    region.weighted_centroid, overlap.weighted_centroid)
                                angle_weighted = angle(
                                    region.weighted_centroid, overlap.weighted_centroid)
                            except AttributeError:
                                pass

                            detailedoverlapcsvrow["distance_weighted"] = distance_weighted
                            detailedoverlapcsvrow["angle_weighted"] = angle_weighted

                            cumulative_overlap += overlap.area
                            overlap_csv_lines.append(detailedoverlapcsvrow)

                        csvrow["cumulative_overlap_{0}_{1}".format(
                            data[index][3], data[comparisonchannel][3])] = cumulative_overlap

                    
                    csvrow["minimum_overlapping_area"] = minimal_overlapping_size
                standard_csv_lines.append(csvrow)

        # finally: save csv data
        standardfile = os.path.join(
            options.csvfolder, "statistics_{0:%Y-%m-%d %H-%M-%S}.csv".format(_currentrun))
        overlapfile = os.path.join(
            options.csvfolder, "overlaps_{0:%Y-%m-%d %H-%M-%S}.csv".format(_currentrun))

        _writestats(standardfile, standard_csv_lines)
        _writestats(overlapfile, overlap_csv_lines)


def new_run():
    """
    Sets the datetime for the statistic files
    """

    global _currentrun
    _currentrun = datetime.datetime.now()


def _writestats(filename, stats):
    mode = get_append_or_write(filename)
    allkeys = list()

    for line in stats:
        for key in line.keys():
            allkeys.append(key)

    with open(filename, mode) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=set(allkeys))
        if mode == 'w':
            writer.writeheader()

        for line in stats:
            writer.writerow(line)


def _log(msg):
    if _callback:
        _callback(msg)


if __name__ == '__main__':
    _callback = print

    new_run()

    spatial_colocalize([
        ('testfiles_samename/ch1/ (1).tif',
         None, None, "ch1"),
        ('testfiles_samename/ch2/ (1).tif',
         None, None, "ch2")
    ], Options(
        "stats/",
        [
            "area_px",
            "area_overlap_px",
            # "intensity_avg",
            # "intensity_max",
            "com",
        ],
        None,
        False,
        2,
        ".tif"
    ))
