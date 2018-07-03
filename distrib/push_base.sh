#!/bin/bash
pull_push(){
   registry=mfthomps
   test_registry=testregistry:5000
   docker pull $registry/$1 
   docker tag $registry/$1 $test_registry/$1
   docker push $test_registry/$1
}
pull_push labtainer.base
pull_push labtainer.network
pull_push labtainer.firefox
pull_push labtainer.wireshark
pull_push labtainer.java
pull_push labtainer.centos
pull_push labtainer.centos.xtra
pull_push labtainer.lamp
pull_push labtainer.lamp.xtra
pull_push labtainer.kali
pull_push labtainer.metasploitable

