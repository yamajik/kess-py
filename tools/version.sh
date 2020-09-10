#!/bin/bash

CURRENT_VERSION=`git describe --abbrev=0 --tags master || git describe --abbrev=0 --tags origin/master`

case $1 in
    upgrade)
        MAJOR=`echo ${CURRENT_VERSION} | cut -f 1 -d "."`
        MINOR=`echo ${CURRENT_VERSION} | cut -f 2 -d "."`
        MICRO=`echo ${CURRENT_VERSION} | cut -f 3 -d "."`

        case $2 in
            major)
                ((MAJOR+=1))
                MINOR=0
                MICRO=0
                ;;
            minor)
                ((MINOR+=1))
                MICRO=0
                ;;
            *)
                ((MICRO+=1))
                ;;
        esac

        UPGRADE_VERSION="${MAJOR}.${MINOR}.${MICRO}"
        echo "${UPGRADE_VERSION}"
        ;;
    *)
        echo "${CURRENT_VERSION}"
        ;;
esac
