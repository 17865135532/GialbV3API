cd /d
#basedir=$(cd `dirname $0`; pwd)
#
#echo "basedir: ${basedir}"
#if [-d "${basedir}/TAXAuto/"];then
##if [-d "/d/TAXAuto/"];then
#  echo "文件夹存在"
#else
#  echo "文件夹不存在"
#  git clone ""
#fi
cd TAXAuto/
TAXAutoPath=$(cd `dirname $0`; pwd)
echo "TAXAuto path: ${TAXAutoPath}"
git checkout dev && git pull
#git log --pretty=oneline
git log -1