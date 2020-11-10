/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package labtainers.paramsui;

import labtainers.resultsui.*;
import labtainers.mainui.ToolTipHandlers;
import java.awt.Component;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import labtainers.mainui.MainWindow;
import labtainers.mainui.ToolTipHandlers.ToolTipWrapper;

/**
 *
 * @author Daniel Liao
 */
public class ParamsData {
    protected List<ParamValues> listofParams;
    static public ArrayList<String> containerList = new ArrayList<String>();
    protected int rowCount;
    MainWindow mainUI;
    public int test = 0;
    
    public ParamsData(MainWindow main, File labPath){
        listofParams = new ArrayList<ParamValues>(); 
        rowCount = 0;
        
        this.mainUI = main;
    }
    
    // Creates a deep copy of the original (shallow with containerList and mainUI)
    public ParamsData(ParamsData original){
        listofParams = new ArrayList<ParamValues>();
        //Deep copy the list of params
        for(ParamValues param : original.listofParams)
            listofParams.add(new ParamValues(param));
        
        this.rowCount = original.getRowCount();
                
        this.mainUI = original.getMainWindow();
    }
//Retrieving and Setting Data~~~~~~~~~~~~~~~~~~~~~~~~~
    
    //Parses the parameter.config to obtain all the relevant param lines, 
    //extracts the values of each param line  
    //and then loads each param line's value into the list of Params
    public void retrieveData(){
        ArrayList<String> params = getParamLines();
        
        if(params != null){
            //Fill the list of params
            for(String paramLine : params){
                listofParams.add(new ParamValues(paramLine));
                rowCount++;
            }
        }
    }
    
    //Updates the containerlist (all artifct panels refer to this list to fill in the container combobox)
    static public void setContainerList(ArrayList<String> newContainerList){
        containerList = newContainerList;
    }
    
   
//WRITING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    //Update the parameter.config file with the user's input
    public void writeParamsConfig(boolean usetmp){
         try {
            String paramID,
                       container,
                       file,
                       symbol,
                       hashedString;
            String upperBound, lowerBound;
            String comments;
            String paramsConfigText = "";
            
            ErrorHandler error = new ErrorHandler();
            ArrayList<String> paramTagList = new ArrayList<String>(); //Used for duplication checking
            
            //Iterate through each param
            for(int i=0;i < listofParams.size();i++){
                error.checkReset(); //Reset the error statuses for a new param line
                
                String paramConfigLine = listofParams.get(i).comments; 
                
                paramID = listofParams.get(i).paramID;
                paramTagList.add(paramID); 
                
                //Checks if paramID is valid or inputted
                if(paramID.matches("^[a-zA-Z0-9_]+$"))
                   paramConfigLine += (paramID + " : "); //add to param Config line
                else if(paramID.isEmpty() || paramID.equals(""))
                   error.paramIDMissing = true;
                else{
                   System.out.println("Param ID"+ paramID);
                   error.paramError = true;
                }
                String operator = listofParams.get(i).operator;
                paramConfigLine += operator + " : ";

                
              //FILEID CONFIG 
                file = listofParams.get(i).fileID;
                container = listofParams.get(i).container;
                
                if(file.isEmpty() || file.equals("")){
                    System.out.println("Bad file for param ID "+ paramID);
                    error.fileIDMissing = true;
                }
                    
                //CONTAINER (if a specific container is selected)
                if(containerList.size() > 1){
                    paramConfigLine += container+":"+file+" : ";
                }else{
                    paramConfigLine += file+" : ";
                }
                
                if(operator.contains("REPLACE")){
                    symbol = listofParams.get(i).symbol;
                    paramConfigLine += symbol;
                }
                if(operator.contains("RAND")){
                    paramConfigLine += " : "+listofParams.get(i).lowerBound+" : "+listofParams.get(i).upperBound;
                }
                if(operator.contains("HASH")){
                    paramConfigLine += " : "+listofParams.get(i).hashedString;
                }
               
                //If there's no error, put the paramConfigLine in the paramsConfigText string, 
                //Otherwise the overallPass of the user input is false
                if(error.userInputCheck(i+1)){
                    if(i < listofParams.size()-1)
                        paramConfigLine+= "\n";
                    //Add the param config line to the Params Config text
                    paramsConfigText += paramConfigLine; 
                }
                else
                    error.fail();         
            } // end for each param
            
            //Check for duplicate param IDs 
            error.checkDuplicateParamID(paramTagList);
            /*
            for(String rt : paramID)
                System.out.println(rt);
            */
            
            if(error.passStatus()){
                //Resets the parameter.config file
                File paramsConfigFile = initializeParamConfig(usetmp);

                try ( //Write the paramConfigText to the params.config
                    BufferedWriter writer = new BufferedWriter(new FileWriter(paramsConfigFile, true))) {
                    writer.write(paramsConfigText+"\n");
                }
            }
            else
                 JOptionPane.showMessageDialog(null, error.toString(), "INPUT ERROR", JOptionPane.ERROR_MESSAGE);
        } 
         catch (IOException ex) {
            Logger.getLogger(ParamsUI.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    //Checks if the parameter.config file exists and prepares the parameter.config file for the lab
    private File initializeParamConfig(boolean usetmp) throws IOException{
        //Get the filepath for the lab's parameter.config
        if(!usetmp){
            paramsConfigFile = new File(mainUI.getCurrentLab() + File.separator + "config" + File.separator + "parameter.config");
        }else{
            paramsConfigFile = new File(File.separator + "tmp" + File.separator + "parameter.config");
        } 
        if(paramsConfigFile.exists()){ 
            //Overwrite parameter.config file if it already exists
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(paramsConfigFile, false))) {
               // writer.write(baseText);
            }
            return paramsConfigFile;
        } 
        else if(paramsConfigFile.createNewFile()){ 
            //Create new parameter.config file otherwise(if it does not already exist)
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(paramsConfigFile))) {
                //writer.write(baseText);
            }
            return paramsConfigFile;
         } 
        else{ //File could not be created so return error message
            System.out.println("Parameter Config File couldn't be initialzed.");
            return null;
        }     
    } 
    
    //Handles all the error data and error checking before writing the parameter.config    
    private class ErrorHandler{
        private boolean overallPass;
        private String errorMsg;
        private boolean 
                paramError,
                fileError,

                paramIDMissing,
                fileIDMissing;
        
        
        ErrorHandler(){
            overallPass = true;
            errorMsg = "";
            checkReset();
        }
        
        void fail(){
            overallPass = false;
        } 
        
        //Resets the error status(used right before looking at new param line)
        private void checkReset(){
            paramError = false;
            fileError = false;

            paramIDMissing = false;
            fileIDMissing = false;
            
        }
        
        //Builds error message detailing the errors that appear in the user input
        boolean userInputCheck(int paramIndex){
            boolean rowPassed = true;
            String infoMsg = "Parameter Line: " + paramIndex + System.lineSeparator();

            if(paramIDMissing){
               rowPassed = false;
               infoMsg+= "-Param ID input is missing." + System.lineSeparator();
            }
            if(fileIDMissing){
               rowPassed = false;
               infoMsg+= "-File ID input is missing." + System.lineSeparator();
            }
            if(paramError){
               rowPassed = false;
               infoMsg+= "-Make sure your Param ID has only alphanumeric characters or underscores." + System.lineSeparator();
            }
            //if(fileError){
            //   rowPassed = false;
            //   infoMsg+= "-Make sure your File ID file's extentsion ends in \".stdin\", \".stdout\", or \".prgout\"." + System.lineSeparator() + " Or is a file path." + System.lineSeparator();
            //}

            
            if(!rowPassed)
                errorMsg += (infoMsg + System.lineSeparator());

            return rowPassed;
        }
        
        //Check for duplicate param ID
        void checkDuplicateParamID(ArrayList<String> paramIDs){
            ArrayList<ParamIDIndices> markedParamIDs = new ArrayList<ParamIDIndices>();
            
            //Store all the indices for each unique param ID
            for(int i=0;i<paramIDs.size();i++){
                String paramID = paramIDs.get(i);   
                //Is the paramID a duplicate? 
                //If so, add the the index number of the duplicate param ID to the corresponding param ID's list of indices
                if(isDuplicate(markedParamIDs, paramID)){
                    getDuplicate(markedParamIDs, paramID).addIndex(i);
                }
                //If not, add it to the markedParamIDs fresh 
                else
                    markedParamIDs.add(new ParamIDIndices(paramID, i));
            }
            
            //Go through every param ID and see if any of them have more than 1 index, if they do then create a custom error message for the duplicate param ID
            String duplicateErrorMsg = "";
            for(ParamIDIndices rt : markedParamIDs){
                if(rt.indices.size() > 1){
                    duplicateErrorMsg+= "Duplicate Param ID: \"" + rt.paramID + "\" on rows ";
                     
                    for(int i=0;i<rt.indices.size();i++){
                        duplicateErrorMsg+=(rt.indices.get(i)+1); //The plus 1 offset to get the 1-based row num
                        
                        if(rt.indices.size() == 2 && i == 0)
                            duplicateErrorMsg+=" and ";
                        else if(i == rt.indices.size()-1)
                            duplicateErrorMsg+=".";
                        else{
                            duplicateErrorMsg+=", ";
                            if(i == rt.indices.size()-2)
                                duplicateErrorMsg+="and ";
                        }
                    }          
                    duplicateErrorMsg+=System.lineSeparator();
                    overallPass = false;
                } 
            }
            errorMsg+=duplicateErrorMsg;  
            
        }
        
        //Stores a param ID's name and the row index they appear on
        class ParamIDIndices{
            protected String paramID;
            protected ArrayList<Integer> indices;
                    
            ParamIDIndices(String paramID, int index){
                this.paramID = paramID;
                indices = new ArrayList<Integer>();
                indices.add(index);
            }
            
            void addIndex(int index){
                indices.add(index);
            }
        }
        
        //Is the param ID already in the duplicate list?
        boolean isDuplicate(ArrayList<ParamIDIndices> markedParamIDs, String paramID){
            for(ParamIDIndices rtIndices : markedParamIDs){
                if(rtIndices.paramID.equals(paramID))
                    return true;
            }
            return false;
        }
        
        //Get the duplicate object based on the duplicate string
        ParamIDIndices getDuplicate(ArrayList<ParamIDIndices> markedParamIDs, String paramID){
            for(ParamIDIndices rtIndices : markedParamIDs){
                if(rtIndices.paramID.equals(paramID))
                    return rtIndices;
            }
            return null;
        }
            
        
        @Override
        public String toString(){
            return errorMsg;
        }
               
        boolean passStatus(){
            return overallPass;
        }
    }
    

//GENERAL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    //Gets the param lines in the parameter.config
    protected ArrayList<String> getParamLines(){
        ArrayList<String> params = new ArrayList<String>();
        
        try {
            File paramsConfig = new File(mainUI.getCurrentLab()+File.separator+"config"+File.separator+"parameter.config");

            //Get the param lines
            if(paramsConfig.exists()){
                try (FileReader fileReader = new FileReader(paramsConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader); 
                    String line = bufferedReader.readLine();
                    String param_line = ""; 
                    while (line != null) {                 
                        //just checks if the first character is: not empty, not a hash, and not whitspace)
                        param_line = param_line + line; 
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0))){
                            params.add(param_line);
                            param_line = "";
                        }else{
                            param_line=param_line+"\n"; 
                        }
                        line = bufferedReader.readLine();
                    }   
                }
                return params;
            }
            else{
                System.out.println("No parameter.config file in the loaded lab!");
                //Create the missing parameter.config file
                paramsConfig.createNewFile();
                return params;
            }
        } 
        catch (IOException e) {
            System.out.println("Issue with getting parameter.config params");
            return null;
        }     
    }
       
    //Updates the list of params
    protected void updateListofParams(JPanel PanelofParams){
       Component[] params = PanelofParams.getComponents(); //Access the list of params
                
       List<ParamValues> listofParamsTMP = new ArrayList<ParamValues>();
        
       //Iterate through each param and add it to the temp list of param values
       for (Component param : params) {
           //RESULTS TAG
           String paramID = ((ParamPanels) param).getParamIDTextField().getText();
           String file = ((ParamPanels) param).getFileTextField().getText();
           String container = (String) (((ParamPanels) param).getContainerComboBox().getSelectedItem());
           ToolTipHandlers.ToolTipWrapper operatorTT = (ToolTipHandlers.ToolTipWrapper) (((ParamPanels) param).getOperatorComboBox().getSelectedItem());
           String operator = operatorTT.getItem();
           String symbol = ((ParamPanels) param).getSymbolTextField().getText();
           String hashedString = ((ParamPanels) param).getHashedStringTextField().getText();
           String lowerBound = ((ParamPanels) param).getLowerBoundTextField().getText();
           String upperBound = ((ParamPanels) param).getUpperBoundTextField().getText();
           String comments = ((ParamPanels) param).getComments();
           
           listofParamsTMP.add(new ParamValues(paramID, container, file, operator, symbol, hashedString, lowerBound, upperBound, comments));
       }
       
       listofParams = listofParamsTMP; //overwrite the old listofParams with the temp listofParams
    }
    
    //Swaps the position of params in a list
    protected void swapParams(String type, int rowIndex){

        switch(type){
            case "UP":
                if(rowIndex > 0){
                    //System.out.println("UP: "+listofParams.get(rowIndex).paramID+" Index: "+rowIndex);
                    Collections.swap(listofParams, rowIndex, rowIndex-1);
                }
                break;
            case "DOWN":
                //System.out.println(rowCount);
                //System.out.println("RowINdex: " + rowIndex + " RowCount-1: "+ (rowCount-1));
                if(rowIndex < rowCount-1){
                    //System.out.println("DOWN: "+listofParams.get(rowIndex).paramID);
                    Collections.swap(listofParams, rowIndex, rowIndex+1);
                }
                break;
            default:
                System.out.println("swap case no register");
        }
    }
    
    //Gets a list of ParamValues from the the current state of the parameter.config file
    protected List<ParamValues> getParamValuesOfConfigFile(){
        List<ParamValues> officialListofParams = new ArrayList<ParamValues>();
        
        ArrayList<String> paramLines = getParamLines();
        
        if(paramLines != null){

            for(String paramLine : paramLines){
                ParamValues values = new ParamValues(paramLine);
                officialListofParams.add(values);
            } 
            return officialListofParams;
        }
        else
            return null;
    }
    
    //Compares the data of two lists of ParamValues. If there is a difference then return 'true', 'false' otherwise
    static boolean paramValuesDiffer(List<ParamValues> list1, List<ParamValues> list2){
        if(list1.size() != list2.size()){  
            return true;
        }
        else{
            //This is a gross implemenation of comparing each individual value between two sets of Param Values (Maybe conisder implementing the ParamValues Class as a comparable)
            for(int i=0;i<list1.size();i++){
                printlistValues(list1, list2, i);  
                if(!list1.get(i).container.equals(list2.get(i).container))
                    return true;
                else if(!list1.get(i).fileID.equals(list2.get(i).fileID))
                    return true;
            }
        }     
        return false;
    }
    
    //Used for debugging in the paramValuesDiffer(List<ParamValues> list1, List<ParamValues> list2) method
    static private void printlistValues(List<ParamValues> list1, List<ParamValues> list2, int i){
        System.out.println("Param ID: ");
                    System.out.println("UI: "+list1.get(i).paramID);
                    System.out.println("Config: "+list2.get(i).paramID);
                    System.out.println();
                
                    System.out.println("File ID: ");
                    System.out.println("UI: "+list1.get(i).fileID);
                    System.out.println("Config: "+list2.get(i).fileID);
                    System.out.println();
                    
                    System.out.println("UI: "+list1.get(i).container);
                    System.out.println("Config: "+list2.get(i).container);
                    System.out.println();
                
                
                
                
                
                
    }
    
    // Param Value objects that reference the old Container to the new Container name
    public void refactorContainerReference(String oldContainer, String newContainer){
        //Updates the listOfValues to reflect a change of a conainer name to a new name
        for(ParamValues param : listofParams){
            //System.out.println(param.container + " " + oldContainer);
            if(param.container.equals(oldContainer)){
                param.container = newContainer;
                System.out.println(param.container);
            }
        }  
        
        //Update the container list with the renamed container
        ArrayList<String> tmp = new ArrayList<String>();
        for(String container : containerList){
            if(container.equals(oldContainer))
                tmp.add(newContainer);
            else
                tmp.add(container);
        }
        containerList = tmp;
    }
    
    //Updates container list and removes Param Value objects that reference the container
    public void removeContainerReference(String container){
        // Deletes all param lines that include the container
        ArrayList<ParamValues> toRemove = new ArrayList<ParamValues>();
        for(ParamValues param : listofParams){
            if(param.container.equals(container))
                toRemove.add(param);
        }
        listofParams.removeAll(toRemove);
        
        //Update delete the container in the container list
        containerList.remove(container);
    }
    
    
//GETTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    protected List<ParamValues> getListofParams(){
        return listofParams;
    }
 
    protected ArrayList<String> getContainerList(){
        return containerList;
    }     
       
    protected int getRowCount(){
        return rowCount;
    }  
    
    protected MainWindow getMainWindow(){
        return mainUI;
    }  
    
}
