currentDir=${PWD##*/}

rm -f ./common ./interfaces


ln -s ../cppVis/common ./common
ln -s ../cppVis/interfaces ./interfaces

cd ../cppVis
rm -f ./plugins
ln -s ../$currentDir/plugins ./plugins
