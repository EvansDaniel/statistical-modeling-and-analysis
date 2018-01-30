#!/bin/bash

if [[ -z $1 ]]; then
	echo "Must provide path/to/*.ipynb file as 1st argument"
	exit 1
fi

FILE=`basename $1`
if [[ `echo $FILE | cut -d"." -f2` != 'ipynb' ]]; then
	echo "Must provide path/to/*.ipynb file"
	exit 1
fi

[[ ! -e $1 ]] && echo "File $1 does not exist" && exit 1

FILE_PATH=$1

# Get path to file
IPYNB_PATH=`dirname $FILE_PATH`
# Get file name w/ extension
FILE=`basename $FILE_PATH`

# Gets name before the .ipynb extension
NAME=`echo $FILE | cut -d"." -f1`

FINAL_NAME='Evans'$NAME

FINAL_NAME_PATH=$IPYNB_PATH/$FINAL_NAME

GIT_PROJECT_DIR=`git rev-parse --show-toplevel`

# Convert # to <h*>, we don't want to overwrite the .ipynb source file
PYTHON_OUTPUT_FILE=$NAME.temp.ipynb

function cleanup {
  	echo "Removing $PYTHON_OUTPUT_FILE"
  	rm -f $PYTHON_OUTPUT_FILE
}

# Will run cleanup on exit if previous command failed
trap '[[ $? != 0 ]] && cleanup;' EXIT

python $GIT_PROJECT_DIR/convert_headers.py $FILE_PATH $PYTHON_OUTPUT_FILE

# Convert .ipynb to .rmd, -y for overwrite
ipyrmd $PYTHON_OUTPUT_FILE -o $FINAL_NAME_PATH.rmd -y

# Clean up the temporary .ipynb file created by python
cleanup

# Have to use $NAME.html because rmarkdown::render outputs 
# the HTML file in the same directory as the .rmd you give it 
# Convert .rmd to .html
Rscript -e "library(rmarkdown); rmarkdown::render('$FINAL_NAME_PATH.rmd', output_file='$FINAL_NAME.html')"

# Check if we can use GUI stuff
if [[ ! -z $DISPLAY ]]; then
	xdg-open $FINAL_NAME_PATH.html
fi