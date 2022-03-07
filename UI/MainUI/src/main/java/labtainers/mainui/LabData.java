/*
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
 */
package labtainers.mainui;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Files;
import java.util.ArrayList;
import labtainers.goalsui.GoalsData;
import labtainers.resultsui.ResultsData;
import labtainers.paramsui.ParamsData;

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
    private ParamsData paramsData;
    
    static protected class NetworkData {
        public String name = "";
        public String mask = "";
        public String gateway = "";
        public int macvlan_ext;
        public int macvlan;
        public boolean tap = false;
        
        public ArrayList<String> unknownNetworkParams;
        
        NetworkData(String name){
            this.name = name;
            this.unknownNetworkParams = new ArrayList<String>();
        }
        
        NetworkData(String name, String mask, String gateway, int macvlan_ext, int macvlan, boolean tap){
            this.name = name;
            this.mask = mask;
            this.gateway = gateway;
            this.macvlan_ext = macvlan_ext;
            this.macvlan = macvlan;
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
        public ArrayList<ContainerAddHostSubData> listOfContainerAddHost;
        public boolean x11;
        public boolean no_param;
        public int clone;
        public boolean no_pull;
        public String lab_gateway = "";
        public String name_server = "";
        public boolean no_gw;
        public boolean no_resolve;
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
        public String wait_for = "";
        public String num_cpus = "";
        public String cpu_set = "";
        
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
        this.paramsData = new ParamsData(main, labPath);
        
        retrieveData(main); 
    }
    public void retrieveResultsGoalsParams(){
                //Set the list of containers the results UI will references, then parse the results.config file
                ResultsData.setContainerList(getContainerNames());
                ParamsData.setContainerList(getContainerNames());
                resultsData.retrieveData();

                //Parse the goals.config
                goalsData.retrieveData();

                paramsData.retrieveData();
    }
    
    // Parse the start.config and parse the goasl.config and results.config if the start.config exists
    private void retrieveData(MainWindow main) throws FileNotFoundException, IOException{
        File startConfig = new File(this.path+"/config/start.config");
        
        if(startConfig.exists()){
                FileReader fileReader = new FileReader(startConfig);
                String parseType = "GLOBAL_SETTINGS";

                BufferedReader bufferedReader = new BufferedReader(fileReader);
                String line = bufferedReader.readLine();
                while (line != null) {
                    line = line.trim();
                    // Check if we need to switch to Network or Container Parsing mode
                    try{
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
                    }catch(java.lang.ArrayIndexOutOfBoundsException ex){
                        System.out.println("Error in line "+line);
                        line = bufferedReader.readLine();
                        continue;
                    }
                    // Check if not a comment or empty space
                    if(!line.startsWith("#") && !line.isEmpty()){ 
                        try{
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
                                                currNetwork.gateway = line.split("GATEWAY ")[1].trim();
                                            }
                                            break;
                                        case "MACVLAN_EXT":
                                            currNetwork.macvlan_ext = Integer.parseInt(line.split("MACVLAN_EXT ")[1].trim());
                                            break;
                                        case "MACVLAN":
                                           currNetwork.macvlan = Integer.parseInt(line.split("MACVLAN ")[1].trim());
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
                                        case "NO_PARAM":
                                            currContainer.no_param = (line.split("NO_PARAM ")[1].trim()).equals("YES");
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
                                        case "NAME_SERVER":
                                            currContainer.name_server = line.split("NAME_SERVER ")[1].trim();
                                            break;
                                        case "NO_GW":
                                            currContainer.no_gw = (line.split("NO_GW ")[1].trim()).equals("YES");
                                            break;
                                        case "NO_RESOLVE":
                                            currContainer.no_resolve = (line.split("NO_RESOLVE ")[1].trim()).equals("YES");
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
                                        case "WAIT_FOR":
                                            currContainer.wait_for = (line.split("WAIT_FOR\\s+")[1].trim());
                                            break;  
                                        case "NUM_CPUS":
                                            currContainer.num_cpus = (line.split("NUM_CPUS\\s+")[1].trim());
                                            break;  
                                        case "CPU_SET":
                                            currContainer.cpu_set = (line.split("CPU_SET\\s+")[1].trim());
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
                        }catch(java.lang.ArrayIndexOutOfBoundsException exb){
                            System.out.println("Error parseType: "+parseType+" line "+line+"\n"+exb+"\n");
                            main.output("Error parseType: "+parseType+" line "+line+"\n"+exb+"\n");
                        }
                    }

                    //go to next line
                    line = bufferedReader.readLine();
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
    
    public int getNetworkCount(){
        return listOfNetworks.size();
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
    
    public String getGlobalValue(String tag){
        String retval = null;
        for(String line : global_settings_params){
             if(line.trim().startsWith(tag)){
                 retval = line.trim().split(" ")[1];
                 break;
             }
        }
        return retval;
    } 
    public ResultsData getResultsData(){
        return resultsData;
    }
    
    public GoalsData getGoalsData(){
        return goalsData;
    }

    public ParamsData getParamsData(){
        return paramsData;
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
        //goalsData = new GoalsData(data);
        // eh?
        goalsData = data;
    }

    public void setParamsData(ParamsData data){
        paramsData = new ParamsData(data);
    }
    
    public void resetContainers(){
        listOfContainers = new ArrayList<ContainerData>();
    }
    
    public void resetNetworks(){
        listOfNetworks = new ArrayList<NetworkData>();
    }
    public void setGlobalValue(String tag, String value){
        boolean gotit = false;
        int index = 0;
        for(String line : global_settings_params){
             if(line.trim().startsWith(tag)){
                 global_settings_params.set(index,   tag+" "+value);
                 gotit = true;
             }
             index++;
        }
        if(!gotit){
            String entry = tag+" "+value;
            global_settings_params.add(entry);
        }
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
        System.out.println("no_param: " + data.no_param);  
        System.out.println("clone: " + data.clone);  
        System.out.println("no_pull: " + data.no_pull);  
        System.out.println("lab_gateway: " + data.lab_gateway);  
        System.out.println("name_server: " + data.name_server);  
        System.out.println("no_gw: " + data.no_gw);  
        System.out.println("no_resolve: " + data.no_resolve);  
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
    public String writeStartConfig(boolean usetmp) throws FileNotFoundException{
        // If usetmp, save to temporary diretory and compare to current.  If they differ,
        // prompts the user to save or discard changes.
        // Return false if user cancels (does not want to exit).
        //Get path to start.config
        String startConfigPath;
        Path tempDir=null;
        if(!usetmp){
            startConfigPath = this.path+File.separator+"config"+File.separator+"start.config";
        }else{
            try{
                tempDir = Files.createTempDirectory(this.name);
            }catch(IOException ex){
                System.out.println("failed creating temporary directory" + ex);
                System.exit(1);
            }
            String dir_s = tempDir.getFileName().toString();
            //System.out.println("dir_s is "+dir_s);

            startConfigPath = File.separator+"tmp"+File.separator+dir_s+File.separator+"start.config";
        }
        PrintWriter writer = new PrintWriter(startConfigPath);
        String startConfigText = ""; 
         
        // Write Global Params
        for(String line : getGlobals()){
            startConfigText += "    "+line+"\n";
        }

        // Cycle through network objects and write
        for(NetworkData data : listOfNetworks){
            startConfigText += "NETWORK "+data.name+"\n";
            startConfigText += "     MASK "+data.mask+"\n";
            startConfigText += "     GATEWAY "+data.gateway+"\n";
            
            if(data.macvlan > 0){
                startConfigText += "     MACVLAN "+data.macvlan+"\n";
            }
            if(data.macvlan_ext > 0){
                startConfigText += "     MACVLAN_EXT" +data.macvlan_ext+"\n";
            }
            
            if(data.tap){
                startConfigText += "     TAP YES"+"\n";
            }
            for(String unknownParam : data.unknownNetworkParams){
                startConfigText += "     "+unknownParam+"\n";
            }
        }
        
        // Cycle through container objects and write 
        for(ContainerData data : listOfContainers){
            startConfigText += "CONTAINER "+data.name+"\n";
            startConfigText += "     USER "+data.user+"\n";
                
            if(data.x11){
                startConfigText += "     X11 YES\n"; 
            }
            else{
                startConfigText += "     X11 NO\n";
            }
            // Not default
            if(data.terminal_count != 1)
                startConfigText += "     TERMINALS "+data.terminal_count+"\n";
            if(!data.terminal_group.isEmpty())
                startConfigText += "     TERMINAL_GROUP "+data.terminal_group+"\n";
            if(!data.xterm_title.isEmpty())
                startConfigText += "     XTERM "+data.xterm_title+" "+data.xterm_script+"\n";
            if(!data.password.isEmpty())
                startConfigText += "     PASSWORD "+data.password+"\n";
            for(ContainerAddHostSubData addHost : data.listOfContainerAddHost){
                if(addHost.type.equals("network"))
                    startConfigText += "     ADD-HOST "+addHost.add_host_network+"\n";
                else if(addHost.type.equals("ip"))
                    startConfigText += "     ADD-HOST "+addHost.add_host_host+":"+addHost.add_host_ip+"\n";    
            }
            for(ContainerNetworkSubData network : data.listOfContainerNetworks){
                    startConfigText += "     "+network.network_name+" "+network.network_ipaddress+"\n";  
            }
            if(data.clone > 0){
                startConfigText += "     CLONE "+data.clone+"\n";
            }
            if(!data.lab_gateway.isEmpty()){
                startConfigText += "     LAB_GATEWAY "+data.lab_gateway+"\n";
            }
            if(!data.name_server.isEmpty()){
                startConfigText += "     NAME_SERVER "+data.name_server+"\n";
            }
            if(data.no_gw){
                startConfigText += "     NO_GW YES\n";
            }
            if(data.no_param){
                startConfigText += "     NO_PARAM YES\n";
            }
            if(data.no_resolve){
                startConfigText += "     NO_RESOLVE YES\n";
            }
            if(!data.base_registry.isEmpty()){
                startConfigText += "     BASE_REGISTRY "+data.base_registry+"\n";
            }
            if(!data.thumb_volume.isEmpty()){
                startConfigText += "     THUMB_VOLUME "+data.thumb_volume+"\n";
            }
            if(!data.thumb_command.isEmpty()){
                startConfigText += "     THUMB_COMMAND "+data.thumb_command+"\n";
            }
            if(!data.thumb_stop.isEmpty()){
                startConfigText += "     THUMB_STOP "+data.thumb_stop+"\n";
            }
            if(!data.publish.isEmpty()){
                startConfigText += "     PUBLISH "+data.publish+"\n";
            }
            if(data.hide){
                startConfigText += "     HIDE YES\n";
            }
            if(data.no_privilege){
                startConfigText += "     NO_PRIVILEGE YES\n";
            }
            if(data.no_pull){
                startConfigText += "     NO_PULL YES\n";
            }
            if(data.mystuff){
                startConfigText += "     MYSTUFF YES\n";
            }
            if(data.tap){
                startConfigText += "     TAP YES\n";
            }
            if(!data.mount1.isEmpty() && !data.mount2.isEmpty()){
                startConfigText += "     MOUNT "+data.mount1+":"+data.mount2+"\n";
            }
            if(!data.wait_for.isEmpty()){
                startConfigText += "     WAIT_FOR "+data.wait_for+"\n";
            }
            if(!data.num_cpus.isEmpty()){
                startConfigText += "     NUM_CPUS "+data.num_cpus+"\n";
            }
            if(!data.cpu_set.isEmpty()){
                startConfigText += "     CPU_SET "+data.cpu_set+"\n";
            }
            
        }
        
        //Write to File
        writer.print(startConfigText);
        writer.close();
        return startConfigPath;
        /*
        boolean something_changed = false;  
        if(usetmp){
            String old_file = this.path+File.separator+"config"+File.separator+"start.config";
            String new_file = startConfigPath;
            try{
                something_changed = ! CompareTextFiles.compare(old_file, new_file);
            }catch(IOException ex){
                System.out.println("Error comparing text files "+ex);
            }
        }    
        return something_changed;
        */
   }    
}

