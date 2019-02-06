#! /bin/bash

#
# Installation script for Scons.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2016-2018
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

# Clean install
if [ -d "src" ]; then
  echo ""
  echo "Cleaning ${INSTALL_DIR}/src directory ..."
  echo ""
  rm -rf src
fi

# Downloading file
PACKAGE_FULL_URL="${PACKAGE_URL}/${PACKAGE_NAME}"

echo ""
echo "Downloading file ${PACKAGE_FULL_URL}"
echo ""
wget --no-check-certificate ${PACKAGE_FULL_URL}

if [ "${?}" != "0" ] ; then
  echo "Error: downloading failed!"
  exit 1
fi

# Unzipping file
unzip ${PACKAGE_NAME}
if [ "${?}" != "0" ] ; then
  echo "Error: unzipping failed!"
  exit 1
fi

# Removing zip
rm -f ${PACKAGE_NAME}
if [ "${?}" != "0" ] ; then
  echo "Error: removing downloaded file failed!"
  exit 1
fi

exit 0
