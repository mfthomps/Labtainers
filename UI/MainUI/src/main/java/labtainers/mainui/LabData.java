/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package labtainers.mainui;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 *
 * @author Daniel Liao
 */

public class LabData {
    private String name;
    private File path;
    private ArrayList<ContainerData> listOfContainers;
    private ArrayList<NetworkData> listOfNetworks;
    
    static protected class NetworkData {
        public String name = "";
        public String mask = "";
        public String gateway = "";
        public int macvlan_ext;
        public int macvlan;
        public String ip_range = "";
        
        NetworkData(String name){
            this.name = name;
        }
    }
    
    static protected class ContainerData{
        public String name;
        public int terminal_count;
        public String terminal_group;
        public String xterm_title;
        public String xterm_script;
        public String user;
        public String password;
        public ArrayList<ContainerNetworkSubData> listOfContainerNetworks;
        public String script;
        public String add_host_host;
        public String add_host_ip;
        public String add_host_network;
        public boolean x11;
        public int clone;
        public boolean no_pull;
        public String lab_gateway;
        public boolean no_gw;
        public String registry;
        public String base_registry;
        public String thumb_volume;
        public String thumb_command;
        public String thumb_stop;
        public String publish;
        public boolean hide;
        public boolean no_privilege;
        public boolean mystuff;
        
        ContainerData(String name){
            this.name = name;
            this.listOfContainerNetworks = new ArrayList();
        } 
    }

    static protected class ContainerNetworkSubData{
        public String network_name;
        public String network_ipaddress; 
        
        ContainerNetworkSubData(String name, String ipaddress){
            this.network_name = name;
            this.network_ipaddress = ipaddress;
        }
        

        
        ContainerNetworkSubData(){
            
        }
    }
    
    LabData(){
        
    }
    
    LabData(File labPath, String labName){
        this.path = labPath;
        this.name = labName;
        this.listOfContainers = new ArrayList();
        this.listOfNetworks = new ArrayList();
        
        //System.out.println("Lab Path: "+labPath);
        //System.out.println("Lab Name: "+labName);
        
        retrieveData();
    }
    
    
    
    boolean retrieveData(){
        File startConfig = new File(this.path+"/config/start.config");
        
        try {
            if(startConfig.exists()){
                try (FileReader fileReader = new FileReader(startConfig)) {
                    String parseType = "NETWORK";
                    
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    String line = bufferedReader.readLine();
                    while (line != null) {
                        // Check if we need to switch to Network or Container Parsing mode
                        if(line.startsWith("NETWORK")){   
                            parseType = "NETWORK";
                            listOfNetworks.add(new NetworkData(line.split("\\s+")[1]));
                        }
                        else if(line.startsWith("CONTAINER")){
                            parseType = "CONTAINER";
                            listOfContainers.add(new ContainerData(line.split("\\s+")[1]));
                        }
                        line = line.trim(); //trim the line for parsing
                        // If not a comment or empty space
                        if(!line.startsWith("#") && !line.isEmpty()){
                            
                            String parameter = line.split("\\s+")[0];
                            if(parseType.equals("NETWORK")){
                                switch(parameter){
                                    case "MASK":
                                        listOfNetworks.get(listOfNetworks .size()-1).mask = line.split("MASK ")[1];
                                        break;
                                    case "GATEWAY":
                                        listOfNetworks.get(listOfNetworks.size()-1).gateway = line.split("GATEWAY ")[1];
                                        break;
                                    case "MACVLAN_EXT":
                                        listOfNetworks.get(listOfNetworks.size()-1).macvlan_ext = Integer.parseInt(line.split("MACVLAN_EXT ")[1]);
                                        break;
                                    case "MACVLAN":
                                        listOfNetworks.get(listOfNetworks.size()-1).macvlan = Integer.parseInt(line.split("MACVLAN ")[1]);
                                        break;
                                    case "IP_RANGE":
                                        listOfNetworks.get(listOfNetworks.size()-1).ip_range = line.split("IP_RANGE ")[1];
                                        break;
                                }
                          }
                          else if(parseType.equals("CONTAINER")){
                              switch(parameter){
                                  case "TERMINALS":
                                        listOfContainers.get(listOfContainers.size()-1).terminal_count = Integer.parseInt(line.split("\\s+")[1]);                                      
                                      break;
                                  case "TERMINAL_GROUP":
                                      listOfContainers.get(listOfContainers.size()-1).terminal_group = line.split("TERMINAL_GROUP ")[1];
                                      break;
                                  case "XTERM":
                                      listOfContainers.get(listOfContainers.size()-1).xterm_title = line.split("\\s+")[1];
                                      listOfContainers.get(listOfContainers.size()-1).xterm_script = line.split("\\s+")[1];
                                      break;
                                  case "USER":
                                      listOfContainers.get(listOfContainers.size()-1).user = line.split("\\s+")[1];
                                      break;
                                  case "PASSWORD":
                                      listOfContainers.get(listOfContainers.size()-1).password = line.split("\\s+")[1];
                                      break;
                                  case "SCRIPT":
                                      listOfContainers.get(listOfContainers.size()-1).script = line.split("\\s+")[1];
                                      break;
                                  case "ADD-HOST":
                                      if(line.split("\\s+")[1].contains(":")){ //host:ip
                                          String tmp = line.split("\\s+")[1];
                                          listOfContainers.get(listOfContainers.size()-1).add_host_host = tmp.split(":")[0];
                                          listOfContainers.get(listOfContainers.size()-1).add_host_ip = tmp.split(":")[1];
                                      }
                                      else { //network
                                          listOfContainers.get(listOfContainers.size()-1).add_host_network =  line.split("\\s+")[1];    
                                      }
                                      
                                      break;
                                  case "X11":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).x11 = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).x11 = false;
                                      }
                                      break;
                                  case "CLONE":
                                      listOfContainers.get(listOfContainers.size()-1).clone = Integer.parseInt(line.split("\\s+")[1]);      
                                      break;
                                  case "NO_PULL":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).no_pull = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).no_pull = false;
                                      }
                                      break;
                                  case "LAB_GATEWAY":
                                      listOfContainers.get(listOfContainers.size()-1).lab_gateway = line.split("\\s+")[1];
                                      break;
                                  case "NO_GW":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).no_gw = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).no_gw = false;
                                      }
                                      break;
                                  case "REGISTRY":
                                      listOfContainers.get(listOfContainers.size()-1).registry = line.split("\\s+")[1];
                                      break;
                                  case "BASE_REGISTRY":
                                      listOfContainers.get(listOfContainers.size()-1).base_registry = line.split("\\s+")[1];
                                      break;
                                  case "THUMB_VOLUME":
                                      listOfContainers.get(listOfContainers.size()-1).thumb_volume = line.split("THUMB_VOLUME\\s+")[1];
                                      break;
                                  case "THUMB_COMMAND":
                                      listOfContainers.get(listOfContainers.size()-1).thumb_command = line.split("THUMB_COMMAND\\s+")[1];
                                      break;
                                  case "THUMB_STOP":
                                      listOfContainers.get(listOfContainers.size()-1).thumb_stop = line.split("THUMB_STOP\\s+")[1];
                                      break;
                                  case "PUBLISH":
                                      listOfContainers.get(listOfContainers.size()-1).publish = line.split("PUBLISH\\s+")[1];
                                      break;
                                  case "HIDE":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).hide = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).hide = false;
                                      }
                                      break;
                                  case "NO_PRIVILEGE":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).no_privilege = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).no_privilege = false;
                                      }
                                      break;
                                  case "MYSTUFF":
                                      if(line.split("\\s+")[1].equals("YES")){
                                          listOfContainers.get(listOfContainers.size()-1).mystuff = true;
                                      }
                                      else{
                                          listOfContainers.get(listOfContainers.size()-1).mystuff = false;
                                      }
                                      break;                                                   
                              }
                              //Check the array of network names to check it 
                              for(int i = 0;i <listOfNetworks.size();i++){
                                  if(listOfNetworks.get(i).name.equals(line.split("\\s+")[0])){
                                      listOfContainers.get(listOfContainers.size()-1).listOfContainerNetworks.add(new ContainerNetworkSubData(line.split("\\s+")[0], line.split("\\s+")[1]));
                                  }
                              }
                          }
                                                    
                        }                                 
                        
                        line = bufferedReader.readLine();
                    }
                }
                return true;
            }
            else{
                System.out.println("start.config is missing");
                return false;
            }
        } 
        catch (FileNotFoundException ex) {
            System.out.println("Issue with getting containers");
            return false;
        } catch (IOException ex) {
            System.out.println("Issue with getting containers");
            return false;
        }
    }

    public String getName() {
        return name;
    }
    
     
    public ArrayList<ContainerData> getContainers(){
        return listOfContainers;
    }
    
    public ArrayList<NetworkData> getNetworks(){
        return listOfNetworks;
    }
    
    public void printNetworkData(NetworkData data) {
        System.out.println("NETWORK----------------------");
        System.out.println("name: " + data.name);
        System.out.println("mask: " + data.mask);        
        System.out.println("gateway: " + data.gateway);
        System.out.println("macvlan_ext: " + data.macvlan_ext);        
        System.out.println("macvlan: " + data.macvlan);        
        System.out.println("ip_range: " + data.ip_range);          
    }
    
    public void printContainerData(ContainerData data) {
        System.out.println("CONTAINER----------------------");
        System.out.println("name: " + data.name);
        System.out.println("terminal_count: " + data.terminal_count);        
        System.out.println("terminal_group: " + data.terminal_group);
        System.out.println("xterm_title: " + data.xterm_title);        
        System.out.println("xterm_script: " + data.xterm_script);        
        System.out.println("user: " + data.user);  
        
        System.out.println("password: " + data.password);   
        System.out.println("script: " + data.script);  
        System.out.println("add_host_host: " + data.add_host_host);  
        System.out.println("add_host_ip: " + data.add_host_ip);  
        System.out.println("add_host_network: " + data.add_host_network);  
        System.out.println("x11: " + data.x11);  
        System.out.println("clone: " + data.clone);  
        System.out.println("no_pull: " + data.no_pull);  
        System.out.println("lab_gateway: " + data.lab_gateway);  
        System.out.println("no_gw: " + data.no_gw);  
        System.out.println("registry: " + data.registry);  
        System.out.println("base_registry: " + data.base_registry);  
        System.out.println("thumb_volume: " + data.thumb_volume);  
        System.out.println("thumb_command: " + data.thumb_command);  
        System.out.println("thumb_stop: " + data.thumb_stop);  
        System.out.println("publish: " + data.publish);  
        System.out.println("hide: " + data.hide);  
        System.out.println("no_privilege: " + data.no_privilege);  
        System.out.println("mystuff: " + data.mystuff);
        if(data.listOfContainerNetworks != null){
            for(int i = 0;i<data.listOfContainerNetworks.size();i++){
                System.out.println(data.listOfContainerNetworks.get(i).network_name + " " + data.listOfContainerNetworks.get(i).network_ipaddress);  
            }
        }

    }
    

    public void printData(){
        for(int i = 0;i < listOfNetworks.size();i++){
            printNetworkData(listOfNetworks.get(i));
        }
        for(int i = 0;i < listOfContainers.size();i++){
            printContainerData(listOfContainers.get(i));
        }
    }
}

