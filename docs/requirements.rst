Requirements
############

File requirements
-----------------

Your files should be single channel files, containing only intensity values. Internally, MultiColo will run a threshold over your input files and treat them as binary images/masks. If you need intensity calculations, you need to pass your files in as data files.

File structure
--------------

MultiColoc can work with a variety of file organization, provided a few requirements are met. As stated above, you need to have all channels split into seperate files. This can be done for instance with ImageJ.

The files for the first channel *need* to be placed in a separate folder! Files of the other channels can remain in one, however it is recommended to place them in unique folders for each channel as well.

Channel files *can* have a unique identifier for the channel in their name, but don't need to. 

Files with identifiers, same files as data files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A layout for files with identifiers could look like::

    Images/
      Channel 1/
        Capture1_ch1.tif
        Capture2_ch1.tif
        Capture3_ch1.tif
        Capture4_ch1.tif
      Channel 2/
        Capture1_ch2.tif
        Capture2_ch2.tif
        Capture3_ch2.tif
        Capture4_ch2.tif
      Channel 3/
        Capture1_ch3.tif
        Capture2_ch3.tif
        Capture3_ch3.tif
        Capture4_ch3.tif

The configurations would then be as following:

Channel 1:
    Folder: Images/Channel 1/

    Channel identifier: ch1

    Data files: Images/Channel 1/

Channel 2:
    Folder: Images/Channel 2/
    
    Channel identifier: ch2

    Data files: Images/Channel 2/

Channel 3:
    Folder: Images/Channel 2/

    Channel identifier: ch2

    Data files: Images/Channel 2/


Files with identifiers, original files as data files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A layout for files, using original files as data files, with identifiers could look like::

    Images/
      Original/
        Capture1_ch1.tif
        Capture2_ch1.tif
        Capture3_ch1.tif
        Capture4_ch1.tif
        Capture1_ch2.tif
        Capture2_ch2.tif
        Capture3_ch2.tif
        Capture4_ch2.tif
        Capture1_ch3.tif
        Capture2_ch3.tif
        Capture3_ch3.tif
        Capture4_ch3.tif
      Channel 1/
        Capture1_ch1.tif
        Capture2_ch1.tif
        Capture3_ch1.tif
        Capture4_ch1.tif
      Channel 2/
        Capture1_ch2.tif
        Capture2_ch2.tif
        Capture3_ch2.tif
        Capture4_ch2.tif
      Channel 3/
        Capture1_ch3.tif
        Capture2_ch3.tif
        Capture3_ch3.tif
        Capture4_ch3.tif

Channel 1:
    Folder: Images/Channel 1/

    Channel identifier: ch1

    Data files: Images/Original/

Channel 2:
    Folder: Images/Channel 2/

    Channel identifier: ch2

    Data files: Images/Original/

Channel 3:
    Folder: Images/Channel 2/

    Channel identifier: ch2

    Data files: Images/Original/

File lookup:
^^^^^^^^^^^^

The lookup of files functions as follows:

    1. Multi coloc will list all files in the source folder of the first channel, ending with the file type specified
    2. For all other channels:
        1. The filename from the first channel is taken
        2. The source folder is replaced with the respective source folder
        3. If present, the identifier is replaced with the identifier of the respective channel
        4. The resulting filename is checked if it exists. Otherwise a warning message is displayed
    3. If a data folder is specified, a file with the generated filename is expected to exist in the data folder

That looks awfully complicated
------------------------------

If you are not sure if your files are layed out in a correct way, you can just do a trial run in MultiColoc. Warning messages will appear, if files are not found where they are expected to be. These messeages will also give you a hint, what their expected folder and name is.