with Z specifies that I did not switch the z channel to t. If you want to start from the beginning
of the workflow, then start here. 
with T specifies that I already switched the z channel to t, and it can be directly used in 
ilastik. 
large puncta probabilities is an example pixel prediction map for atg8 EXAMPLE. 
Fiji-MaMuT file is the EXAMPLE tracking result export for atg8 EXAMPLE. It can be directly opened
with TrackMate. 


Workflow (see PDF):
-Open ImageJ and open with Z
- re-order hyperstack z-->t
- import into pixel classification and go through the steps. 
- export probabilities as hdf5 to make the pixel prediction map
- import image and probabilities into tracking with learning
- go through the tracking steps as described in the PPT
      - create the XML/HDF5 file from the original image using BigDataViewer in ImageJ
      - use this to export tracking data with the Fiji/MaMuT plugin export option in ilastik
- Open Fiji-MaMuT export file in imageJ with TrackMate
- Click 'Tracks' --> export as CSV
- import directory and CSV into the python IDE. Make sure the parameters are correct, the directory in
is satisfied, and the output file is what you want. 
- Run the program
- The exported CSV can be opened with TrackMate CSV importer
	- the CSV file MUST contain AT LEAST: 
		-TRACK_ID, POSITION_X, POSITION_Y, POSITION_T, FRAME 
		- select 'import tracks'
		- radius = 2 <--- NOT a decimal value