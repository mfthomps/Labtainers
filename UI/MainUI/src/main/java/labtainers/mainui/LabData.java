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
import labtainers.goalsui.GoalsData;
import labtainers.resultsui.ResultsData;

/**
 *
 * @author Daniel Liao
 */

public class LabData {
    private String name;
    private File path;
    private ArrayList<String> global_settings_params;
    private ArrayList<ContainerData> listOfContainers;
    private ArrayList<NetworkData> listOfNetworks;
    
    private ResultsData resultsData;
    private GoalsData goalsData;
    
    static protected class NetworkData {
        public String name = "";
        public String mask = "";
        public String gateway = "";
        public int macvlan_ext;
        public int macvlan;
        public String ip_range = "";
        public boolean tap = false;
        
        public ArrayList<String> unknownNetworkParams;
        
        NetworkData(String name){
            this.name = name;
            this.unknownNetworkParams = new ArrayList<String>();
        }
        
        NetworkData(String name, String mask, String gateway, int macvlan_ext, int macvlan, String ip_range, boolean tap){
            this.name = name;
            this.mask = mask;
            this.gateway = gateway;
            this.macvlan_ext = macvlan_ext;
            this.macvlan = macvlan;
            this.ip_range = ip_range;
            this.tap = tap;
            this.unknownNetworkParams = new ArrayList<String>();
        }
    }
    
    static protected class ContainerData{
        public String name;
        public int terminal_count = 1;
        public String terminal_group = "";
        public String xterm_title = "";
        public String xterm_script = "";
        public String user = "";
        public String password = "";
        public ArrayList<ContainerNetworkSubData> listOfContainerNetworks;
        public String script = "";
        public ArrayList<ContainerAddHostSubData> listOfContainerAddHost;
        public boolean x11;
        public int clone;
        public boolean no_pull;
        public String lab_gateway = "";
        public boolean no_gw;
        public String registry = "";
        public String base_registry = "";
        public String thumb_volume = "";
        public String thumb_command = "";
        public String thumb_stop = "";
        public String publish = "";
        public boolean hide;
        public boolean no_privilege;
        public boolean mystuff;
        public boolean tap;
        public String mount1 = "";
        public String mount2 = "";
        
        public ArrayList<String> unknownContainerParams;
        
        ContainerData(String name){
            this.name = name;
            this.listOfContainerNetworks = new ArrayList<ContainerNetworkSubData>();
            this.listOfContainerAddHost = new ArrayList<ContainerAddHostSubData>();
            this.unknownContainerParams = new ArrayList<String>();
        }
    }

    static protected class ContainerNetworkSubData{
        public String network_name;
        public String network_ipaddress; 
        
        ContainerNetworkSubData(String name, String ipaddress){
            this.network_name = name;
            this.network_ipaddress = ipaddress;
        }
    }
    
    static protected class ContainerAddHostSubData{
        public String type = "";
        public String add_host_host = "";
        public String add_host_ip = "";
        public String add_host_network = "";
        
        ContainerAddHostSubData(String type, String host, String ip, String network){
            this.type = type;
            this.add_host_host = host;
            this.add_host_ip = ip;
            this.add_host_network = network;
        }
    }
    
    LabData(MainWindow main, File labPath, String labName) throws IOException{
        this.path = labPath;
        this.name = labName;
        this.global_settings_params = new ArrayList<String>();
        this.listOfContainers = new ArrayList<ContainerData>();
        this.listOfNetworks = new ArrayList<NetworkData>();
        this.resultsData = new ResultsData(main,labPath);
        this.goalsData = new GoalsData(main, labPath);
        
        retrieveData(); 
    }
    
    // Parse the start.config and parse the goasl.config and results.config if the start.config exists
    private void retrieveData() throws FileNotFoundException, IOException{
        File startConfig = new File(this.path+"/config/start.config");
        
        if(startConfig.exists()){
            try (FileReader fileReader = new FileReader(startConfig)) {
                String parseType = "GLOBAL_SETTINGS";

                BufferedReader bufferedReader = new BufferedReader(fileReader);
                String line = bufferedReader.readLine();
                while (line != null) {
                    line = line.trim();
                    // Check if we need to switch to Network or Container Parsing mode
                    if(line.startsWith("NETWORK ")){   
                        parseType = "NETWORK";
                        listOfNetworks.add(new NetworkData(line.split("NETWORK ")[1].trim().toUpperCase()));
                        line = bufferedReader.readLine();
                        continue;
                    }
                    else if(line.startsWith("CONTAINER ")){
                        parseType = "CONTAINER";
                        listOfContainers.add(new ContainerData(line.split("CONTAINER ")[1].trim()));
                        line = bufferedReader.readLine();
                        continue;
                    }
                    // Check if not a comment or empty space
                    if(!line.startsWith("#") && !line.isEmpty()){ 
                        // Check if we're looking for gloabl_settings params, 
                        // which should be at the start before container and network info;
                        // otherwise parse the specified accepted params in the lab designer manual.
                        if(parseType.equals("GLOBAL_SETTINGS"))
                            global_settings_params.add(line);
                        else {
                            String parameter = line.split("\\s+")[0];
                            if(parseType.equals("NETWORK")){
                                NetworkData currNetwork = listOfNetworks.get(listOfNetworks .size()-1);
                                switch(parameter){
                                    case "MASK":
                                        currNetwork.mask = line.split("MASK ")[1].trim();
                                        break;
                                    case "GATEWAY":
                                        if(line.contains("GATEWAY ")){
                                            System.out.println("line is "+line);
                                            currNetwork.gateway = line.split("GATEWAY ")[1].trim();
                                        }
                                        break;
                                    case "MACVLAN_EXT":
                                        currNetwork.macvlan_ext = Integer.parseInt(line.split("MACVLAN_EXT ")[1].trim());
                                        break;
                                    case "MACVLAN":
                                       currNetwork.macvlan = Integer.parseInt(line.split("MACVLAN ")[1].trim());
                                        break;
                                    case "IP_RANGE":
                                       currNetwork.ip_range = line.split("IP_RANGE ")[1].trim();
                                        break;
                                    case "TAP":
                                        currNetwork.tap = (line.split("TAP ")[1].trim()).equals("YES");
                                        break;
                                    default:
                                        currNetwork.unknownNetworkParams.add(line);
                                        break;
                                }
                            }
                            else if(parseType.equals("CONTAINER")){                         
                                ContainerData currContainer = listOfContainers.get(listOfContainers.size()-1);
                                switch(parameter){
                                    case "TERMINALS":
                                        currContainer.terminal_count = Integer.parseInt(line.split("TERMINALS ")[1].trim());                                      
                                        break;
                                    case "TERMINAL_GROUP":
                                        currContainer.terminal_group = line.split("TERMINAL_GROUP ")[1].trim();
                                        break;
                                    case "XTERM":
                                        currContainer.xterm_title = line.split("\\s+")[1].trim();

                                        if(!currContainer.xterm_title.equals("INSTRUCTIONS"))
                                            currContainer.xterm_script = line.split("\\s+")[2].trim();
                                        break;
                                    case "USER":
                                        currContainer.user = line.split("USER ")[1].trim();
                                        break;
                                    case "PASSWORD":
                                        currContainer.password = line.split("PASSWORD ")[1].trim();
                                        break;
                                    case "SCRIPT":
                                        currContainer.script = line.split("SCRIPT ")[1].trim();
                                        break;
                                    case "ADD-HOST":
                                        String addhostParams = line.split("ADD-HOST ")[1].trim();
                                        if(addhostParams.contains(":")) //host:ip
                                            currContainer.listOfContainerAddHost.add(new ContainerAddHostSubData("ip",addhostParams.split(":")[0].trim(), addhostParams.split(":")[1].trim(), ""));
                                        else //network
                                            currContainer.listOfContainerAddHost.add(new ContainerAddHostSubData("network","", "", addhostParams));
                                        break;
                                    case "X11":
                                        currContainer.x11 = (line.split("X11 ")[1].trim()).equals("YES");
                                        break;
                                    case "CLONE":
                                        currContainer.clone = Integer.parseInt(line.split("CLONE ")[1].trim());      
                                        break;
                                    case "NO_PULL":
                                        currContainer.no_pull = (line.split("NO_PULL ")[1].trim()).equals("YES");
                                        break;
                                    case "LAB_GATEWAY":
                                        currContainer.lab_gateway = line.split("LAB_GATEWAY ")[1].trim();
                                        break;
                                    case "NO_GW":
                                        currContainer.no_gw = (line.split("NO_GW ")[1].trim()).equals("YES");
                                        break;
                                    case "REGISTRY":
                                        currContainer.registry = line.split("REGISTRY ")[1].trim();
                                        break;
                                    case "BASE_REGISTRY":
                                        currContainer.base_registry = line.split("BASE_REGISTRY ")[1].trim();
                                        break;
                                    case "THUMB_VOLUME":
                                        currContainer.thumb_volume = line.split("THUMB_VOLUME\\s+")[1].trim();
                                        break;
                                    case "THUMB_COMMAND":
                                        currContainer.thumb_command = line.split("THUMB_COMMAND\\s+")[1].trim();
                                        break;
                                    case "THUMB_STOP":
                                        currContainer.thumb_stop = line.split("THUMB_STOP\\s+")[1].trim();
                                        break;
                                    case "PUBLISH":
                                        currContainer.publish = line.split("PUBLISH\\s+")[1].trim();
                                        break;
                                    case "HIDE":
                                        currContainer.hide = (line.split("HIDE\\s+")[1].trim()).equals("YES");
                                        break;
                                    case "NO_PRIVILEGE":
                                        currContainer.no_privilege = (line.split("NO_PRIVILEGE\\s+")[1].trim()).equals("YES");
                                        break;
                                    case "MYSTUFF":
                                        currContainer.mystuff = (line.split("MYSTUFF\\s+")[1].trim()).equals("YES");
                                        break;  
                                    case "TAP":
                                        currContainer.tap = (line.split("TAP ")[1].trim()).equals("YES");
                                        break;
                                    case "MOUNT":
                                        String mountParam = line.split("MOUNT ")[1].trim();
                                        currContainer.mount1 = mountParam.split(":")[0].trim();
                                        currContainer.mount2 = mountParam.split(":")[1].trim();
                                        break;
                                    default:
                                        boolean foundMatchingNetwork = false;
                                        String networkName = line.split("\\s+")[0].toUpperCase();
                                        String ipAddrName = line.split("\\s+")[1].toUpperCase();
                                        //Check the array of network names to to see if it matches it
                                        for(int i = 0;i <listOfNetworks.size();i++){ 
                                            if(listOfNetworks.get(i).name.equals(networkName)){
                                                currContainer.listOfContainerNetworks.add(new ContainerNetworkSubData(networkName, ipAddrName));
                                                foundMatchingNetwork = true;
                                                break;
                                            }
                                        }      
                                        //if doesn't find a matching network name then this param is unknown
                                        if(!foundMatchingNetwork) {currContainer.unknownContainerParams.add(line);}
                                        break;
                                }                             
                            }   
                        }   
                    }

                    //go to next line
                    line = bufferedReader.readLine();
                }
                //Set the list of containers the results UI will references, then parse the results.config file
                ResultsData.setContainerList(getContainerNames());
                resultsData.retrieveData();

                //Parse the goals.config
                goalsData.retrieveData();
            }
        }
        else{
            System.out.println("start.config is missing");
        }
    }
    
    // GETTERS //
    
    public String getName() {
        return name;
    }
     
    public ArrayList<ContainerData> getContainers(){
        return listOfContainers;
    }
    
    public ArrayList<String> getContainerNames(){
       ArrayList<String> names = new ArrayList<String>();
       for (ContainerData container : listOfContainers) 
            names.add(container.name);
       
       return names;
    }
     
    public ArrayList<NetworkData> getNetworks(){
        return listOfNetworks;
    }
    
    public ArrayList<String> getNetworkNames(){
       ArrayList<String> names = new ArrayList<String>();
       for (NetworkData network : listOfNetworks) 
            names.add(network.name);
       
       return names;
    }
    
    public ArrayList<String> getGlobals(){
        return global_settings_params;
    }
    
    public ResultsData getResultsData(){
        return resultsData;
    }
    
    public GoalsData getGoalsData(){
        return goalsData;
    }
    
    
    // SETTERS //
    
    public void setName(String newName){
        name = newName;
    }
    
    public void setPath(File newPath){
        path = newPath;
    }
    
    public void setResultsData(ResultsData data){
        resultsData = new ResultsData(data);
    }
    
    public void setGoalsData(GoalsData data){
        goalsData = new GoalsData(data);
    }
    
    public void resetContainers(){
        listOfContainers = new ArrayList<ContainerData>();
    }
    
    public void resetNetworks(){
        listOfNetworks = new ArrayList<NetworkData>();
    }
    
    
    // DATA MANIPULATION //
    
    //Called when a user renames a network. 
    //The function will overwrite any instances of the old Network Name with the new Network Name in this state object
    public void refactorNetworkName(String oldName, String newName){
        //Rename the network in the list of networks
        for(NetworkData network : listOfNetworks){
            if(network.name.equals(oldName)){
                network.name = newName;
                break;
            }
        }
        
        //Rename the network in list of Networks and list of addHosts for each container 
        for(ContainerData container : listOfContainers){
            // check list of networks
            for(ContainerNetworkSubData networkSubData: container.listOfContainerNetworks){
                if(networkSubData.network_name.equals(oldName))
                    networkSubData.network_name = newName;
            }
            //check list of add-hosts
            for(ContainerAddHostSubData addHostSubData: container.listOfContainerAddHost){
                if(addHostSubData.add_host_network.equals(oldName))
                    addHostSubData.add_host_network = newName;
            }
        }
    }
    
    // Called when a user deletes a network
    // The function deletes any instances of the Network name being referenced in the Lab data
    public void deleteReferenceToNetwork(String networkName){
        // Delete the network in the list of networks
        for(NetworkData network : listOfNetworks){
            if(network.name.equals(networkName)){
                listOfNetworks.remove(network);
                break;
            }
        }
        
        // Delete the network in list of Networks and list of addHosts for each container 
        for(ContainerData container : listOfContainers){
            // Check list of networks 
            ArrayList<ContainerNetworkSubData> networksToRemove = new ArrayList<ContainerNetworkSubData>();
            for(ContainerNetworkSubData networkSubData: container.listOfContainerNetworks){
                if(networkSubData.network_name.equals(networkName))
                     networksToRemove.add(networkSubData);   
            }
            container.listOfContainerNetworks.removeAll(networksToRemove);
            
            // Check list of add-hosts 
            ArrayList<ContainerAddHostSubData> addHostsToRemove = new ArrayList<ContainerAddHostSubData>();
            for(ContainerAddHostSubData addHostSubData: container.listOfContainerAddHost){
                if(addHostSubData.add_host_network.equals(networkName))
                    addHostsToRemove.add(addHostSubData);   
            }
            container.listOfContainerAddHost.removeAll(addHostsToRemove);
        }
    }
    
    // Called when a user deletes a conainer
    // The function deletes any instances of the Container name being referenced in the Lab data
    public void deleteReferenceToContainer(String containerName){
        // Delete the network in the list of networks
        for(ContainerData container : listOfContainers){
            if(container.name.equals(containerName)){
                listOfContainers.remove(container);
                break;
            }
        }
        
        // Update the results data to not include the container reference
        resultsData.removeContainerReference(containerName);
    }
   
    
    // PRINT //
    
    public void printNetworkData(NetworkData data) {
        System.out.println("NETWORK----------------------");
        System.out.println("name: " + data.name);
        System.out.println("mask: " + data.mask);        
        System.out.println("gateway: " + data.gateway);
        System.out.println("macvlan_ext: " + data.macvlan_ext);        
        System.out.println("macvlan: " + data.macvlan);        
        System.out.println("ip_range: " + data.ip_range);  

        if(!data.unknownNetworkParams.isEmpty()){
            System.out.println("UNKNOWN PARAMS: ");
            for(int i = 0;i<data.unknownNetworkParams.size();i++){
                    System.out.println(data.unknownNetworkParams.get(i));  
            }        
            System.out.println("------------------------------------");
        }
        
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

        if(data.listOfContainerAddHost != null){
            for(int i = 0;i<data.listOfContainerAddHost.size();i++){
                if(data.listOfContainerAddHost.get(i).type.equals("ip")){
                    System.out.println("ADD-HOST: " + data.listOfContainerAddHost.get(i).add_host_host + " " + data.listOfContainerAddHost.get(i).add_host_ip);  
                }
                else{
                    System.out.println("ADD-HOST: " + data.listOfContainerAddHost.get(i).add_host_network);  
                } 
            }
        }
        
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
        if(!data.unknownContainerParams.isEmpty()){
            System.out.println("UNKNOWN PARAMS: ");
            for(int i = 0;i<data.unknownContainerParams.size();i++){
                    System.out.println(data.unknownContainerParams.get(i));  
            }
            System.out.println("------------------------------------");
        }
    }
    
    public void printData(){
        for(String line : global_settings_params)
            System.out.println(line);
        
        for(int i = 0;i < listOfNetworks.size();i++)
            printNetworkData(listOfNetworks.get(i));
        
        for(int i = 0;i < listOfContainers.size();i++)
            printContainerData(listOfContainers.get(i));
        
    }
}

