Source file
==================================

This is an example configuration file for sources to be skimmed

Note the following **metadata_1** for keys and values 
(always following YAML standards):

 - **CUSTOMIZABLE_KEY**: Indicates the key can be any value
 - **FIXED_KEY**: The must match the example string
 - **CORRECT_VALUE**: The value must be in line with the source data


Note the following **metadata_2** for keys and values
(always following YAML standards):

  - **MANDATORY**: The key/value is mandatory to exist inside the section
  - **OPTIONAL**: The key/value is optional to exist inside the section


For example: At the 3rd level, the variables are specified. The configuration
specification for variables are "[**FIXED_KEY** -- **OPTIONAL**]"; If the variable 
key *tco3_zm* is specified, the application searches for tco3 data 
on the source. When it is not specified, variable data are not searched so the
output folder [x-]_[y-] does not contain tco3 dataset files.


First example - CCMI-1
---------------------------

In this example, the data source has only one model, therefore it is
expected to have only one folder output named "CCMI-1_IPSL".

This model has 2 variables (*tco3_zm* and *vmro3_zm*) which datasets are 
located in different directories. Therefore the key *path* is the different
in both of them. Therefore, the output expected at "CCMI-1_IPSL" is 
2 type of files: 

 - tco3_zm_[YEAR]-[YEAR].nc: With tco3 skimmed data
 - vmro3_zm_[YEAR]-[YEAR].nc: With vmro3 skimmed data

Where [YEAR] are optional text output depending on how the `–split_by` 
argument is configured at the :doc:`/getting_started/cli` call.


.. code-block:: yaml

    # This is the preceded -x1- string at the output folder: '[x1]_[y-]'
    # [CUSTOMIZABLE_KEY -- MANDATORY]
    CCMI-1:

        # This is the preceded -y1- string at the output folder: '[x1]_[y1]'
        # [CUSTOMIZABLE_KEY -- MANDATORY]
        IPSL:

            # Represents the information related to tco3 data
            # [FIXED_KEY -- OPTIONAL]
            tco3_zm:

                # Variable name for tco3 array inside the dataset
                # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                name: toz

                # Reg expression, how to load the netCDF files
                # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                paths: Ccmi/mon/toz/*.nc

                # Coordinates description for tco3 data. 
                # [FIXED_KEY -- MANDATORY]:
                coordinates:

                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    time: time

                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    lat: lat

                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    lon: lon

            # Represents the information related to vmro3 data
            # [FIXED_KEY -- OPTIONAL]
            vmro3_zm:

                # Variable name for vmro3 array inside the dataset
                # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY] 
                name: vmro3

                # Reg expression, how to load the netCDF files
                # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                paths: Ccmi/mon/vmro3

                # Coordinates description for vmro3 data. 
                # [FIXED_KEY -- MANDATORY]: 

                coordinates:
                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    time: time

                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    plev: plev
                    
                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    lat: lat
                    
                    # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                    lon: lon 


Second example - ECMWF
-----------------------------------

In this example, the data source has two models, therefore it is
expected to have two folder outputs ["ECMWF_ERA-5", "ECMWF_ERA-i"].

The model ERA-5 has only information tco3 data, there is no vmro3 data.
Therefore, only one type of files is expected at "ECMWF_ERA-5": 

  - tco3_zm_[YEAR].nc: With tco3 skimmed data

This case of ERA-i indeed has 2 variables (*tco3_zm* and *vmro3_zm*) but in
this case, are located inside the same dataset files, therefore the 
key *path* should be the same for both variables. The output expected at 
"ECMWF_ERA-5" are 2 type of files: 

  - tco3_zm_[YEAR].nc: With tco3 skimmed data
  - vmro3_zm_[YEAR].nc: With vmro3 skimmed data


.. code-block:: yaml

  # This is the preceded -x2- string at the output folder: '[x2]_[y-]'
  # [CUSTOMIZABLE_KEY -- MANDATORY]
  ECMWF:

      # This is the preceded -y1- string at the output folder: '[x2]_[y1]'
      # [CUSTOMIZABLE_KEY -- MANDATORY]
      ERA-5:

          # Represents the information related to tco3 data
          # [FIXED_KEY -- OPTIONAL]
          tco3_zm:

              # Variable name for tco3 array inside the dataset
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
              name: tco3

              # Reg expression, how to load the netCDF files
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
              paths: Ecmwf/Era5

              # Coordinates description for tco3 data. 
              # [FIXED_KEY -- MANDATORY]:
              coordinates:

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lat: latitude

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lon: longitude 

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  time: time

      # This is the preceded -y2- string at the output folder: '[x2]_[y2]'
      # [CUSTOMIZABLE_KEY -- MANDATORY]
      ERA-i:

          # Represents the information related to tco3 data
          # [FIXED_KEY -- OPTIONAL]
          tco3_zm:

              # Variable name for tco3 array inside the dataset
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
              name: toz

              # Reg expression, how to load the netCDF files
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
              paths: Ecmwf/Erai

              # Coordinates description for tco3 data. 
              # [FIXED_KEY -- MANDATORY]:
              coordinates:

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  time: time

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lat: latitude

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lon: longitude 

          # Represents the information related to vmro3 data
          # [FIXED_KEY -- OPTIONAL]
          vmro3_zm:

              # Variable name for vmro3 array inside the dataset
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]         
              name: vmro3

              # Reg expression, how to load the netCDF files
              # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
              paths: Ecmwf/Erai

              # Coordinates description for vmro3 data. 
              # [FIXED_KEY -- MANDATORY]: 

              coordinates:
                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  time: time

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  plev: level

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lat: latitude

                  # [FIXED_KEY -- MANDATORY]: [CORRECT_VALUE -- MANDATORY]
                  lon: longitude

One or two files?
-----------------

Note this two examples should be located into the same file when you want the 
module to skim both examples with only one call to the command.

If need to skim the data in two different steps, you can place each example into
a different file and call each one of them separately by the module using the 
input argument:

 ``-f, --sources_file SOURCES_FILE``

