/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ResultsUI;

import static ResultsUI.ParamReferenceStorage.justFieldType;
import static ResultsUI.ParamReferenceStorage.lineParamAccessible;
import static ResultsUI.ParamReferenceStorage.timeStampDelimiterAccessible;
import ResultsUI.ToolTipHandlers.ToolTipWrapper;
import java.awt.Component;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
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

/**
 *
 * @author Dan
 */
public class ResultsData {
    List<ArtifactValues> listofArtifacts;
    ArrayList<String> containerList;
    boolean labloaded;
    String labname;
    int rowCount;
    
    ResultsData(){
        listofArtifacts = new ArrayList<>(); 
        containerList = new ArrayList<>();
        labloaded = false;
        labname = "";
        rowCount = 0;
    }
    
    ResultsData(String labname){
        listofArtifacts = new ArrayList<>(); 
        containerList = new ArrayList<>();
        labloaded = false;
        this.labname = labname;
        rowCount = 0;
        
        getData();
    }
    
//LOADING~~~~~~~~~~~~~~~~~~~~~~~~~
    
    //Checks if the lab exists and will get lab's result config data if it does
    private void getData(){
        //Check if the Folder exists
        String userHomeFolder = System.getProperty("user.home");
        File lab = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator+ labname);

        if(lab.isDirectory()){
            if(getContainers(lab) && getArtifacts())
                labloaded = true;
        }
        else
            System.out.println("Lab does not exist!");  
    }
    
    //Updates the containerlist (all artifct panels refer to this list to fill in the container combobox)
    private boolean getContainers(File lab){
        File startConfig = new File(lab+"/config/start.config");
        
        try {
            if(startConfig.exists()){
                try (FileReader fileReader = new FileReader(startConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    
                    String line = bufferedReader.readLine();
                    while (line != null) {
                        if(line.startsWith("CONTAINER")){
                            containerList.add(line.split("\\s+")[1]);
                        }
                        line = bufferedReader.readLine();
                    }
                }
                
                //Every list of containers should include "ALL" to signify when the container_name is not specified in the file ID
                if(containerList.size() > 1)
                    containerList.add("ALL");
                
                return true;
            }
            else{
                System.out.println("start.config is missing");
                return false;
            }
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(ResultsUI.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Issue with getting containers");
            return false;
        } catch (IOException ex) {
           Logger.getLogger(ResultsUI.class.getName()).log(Level.SEVERE, null, ex);
           System.out.println("Issue with getting containers");
            return false;
        }
        
    }
     
    //Parses the results.config to obtain all the relevant artifact lines, 
    //extracts the values of each artifact line  
    //and then loads each artifact line's value into the list of Artifacts
    private boolean getArtifacts(){
        ArrayList<String> artifacts = getArtifactLines();
        
        if(artifacts != null){
            //Fill the list of artifacts
            for(String artifactLine : artifacts){
                ArtifactValues values = new ArtifactValues(artifactLine);
                listofArtifacts.add(values);
                rowCount++;
            }
            return true;
        }
        else
            return false;
        
    }
    
   
//WRITING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    //Update the results.config file with the user's input
    protected void writeResultsConfig(JPanel PanelofArtifacts){
         try {
            updateListofArtifacts(PanelofArtifacts);
            String resultTag,
                       container,
                       file,
                       fieldType,
                       fieldID,
                       lineType,
                       lineID,
                       timeStampType,
                       timeStampDelimiter;
            String resultsConfigText = "";
            
            ErrorHandler error = new ErrorHandler();
            ArrayList<String> resultTagList = new ArrayList<>(); //Used for duplication checking
            
            
            //Iterate through each artifact
            for(int i=0;i < listofArtifacts.size();i++){
                error.checkReset(); //Reset the error statuses for a new artifact line
                
                String artifactConfigLine = "";
                
              //RESULTS TAG
                resultTag = listofArtifacts.get(i).resultTag;
                resultTagList.add(resultTag); 
                
                //Checks if resultTag is valid or inputted
                if(resultTag.matches("^[a-zA-Z0-9_]+$"))
                   artifactConfigLine += (resultTag + " = "); //add to artifact Config line
                else if(resultTag.isEmpty() || resultTag.equals(""))
                   error.resultTagMissing = true;
                else
                   error.resultError = true;
                
              //FILEID CONFIG 
                file = listofArtifacts.get(i).fileID;
                container = listofArtifacts.get(i).container;
                ToolTipWrapper timeStampTypeTTW = listofArtifacts.get(i).timeStampType;
                timeStampType = timeStampTypeTTW.getItem();
                timeStampDelimiter = listofArtifacts.get(i).timeStampDelimiter;
                
                if(file.isEmpty() || file.equals("")){
                    error.fileIDMissing = true;
                }
                //Checks if non-file-path file input has .stdin | .stdout | .prgout dottag
                //Note: most OS, but Windows use backslashes as a File seperator                
                else if(!file.contains("/")){
                    if(!file.contains("."))
                        error.fileError = true;
                    else{
                        String dotTag = file.substring(file.indexOf("."),file.length());
                        if(!(dotTag.equals(".stdin") || dotTag.equals(".stdout") || dotTag.equals(".prgout")))
                            error.fileError = true;
                    }
                }
                    
                //CONTAINER (if a specific container is selected)
                if(containerList.size() > 1 && !container.equals("ALL")){
                    artifactConfigLine += (container);
                    artifactConfigLine += ":"; 
                }
                
                //TIMESTAMP DELIMITER (if Serivce or Program was selected in the Timestamp combobox)
                if(timeStampDelimiterAccessible.contains(timeStampType)){
                   //Checks if the file is a file path when a user inputs a time delimiter
                   if(file.contains("/") && !(timeStampDelimiter.isEmpty() || timeStampDelimiter.equals(""))){
                       artifactConfigLine += (file+ ":" + timeStampDelimiter); 
                   
                       if((timeStampType).equals("Service"))
                            artifactConfigLine += ".service";   
                   }
                   else{
                       if(!file.contains("/"))
                           error.timeDelimiterError = true;
                       else
                           error.timeDelimiterMissing =  true;
                   }
                } 
                else
                    artifactConfigLine += file; //could be a <prog>.[stdin | stdout | prgout], file_path   
                
                
              //FIELD TYPE
                /*
                If the timeStampType is "LOG_TS" and the fieldType is "CONTAINS", then the fieldType will be "LOG_TS"
                If the timeStampType is "LOG_TS" and the fieldType is "FILE_REGEX", then the fieldType will be "FILE_REGEX_TS"
                If the timeStampType is "LOG_RANGE" and the fieldType is "CONTAINS", then the fieldType will be "LOG_RANGE"
                */
                ToolTipWrapper fieldTypeTTW = listofArtifacts.get(i).fieldType;
                fieldType = fieldTypeTTW.getItem();
                
                if(timeStampType.equals("LOG_TS")){
                    if(fieldType.equals("CONTAINS"))
                        fieldType = "LOG_TS";
                    else if(fieldType.equals("FILE_REGEX"))
                        fieldType = "FILE_REGEX_TS";
                }
                if(timeStampType.equals("LOG_RANGE")){
                    if(fieldType.equals("CONTAINS"))
                        fieldType = "LOG_RANGE";
                }
                artifactConfigLine += (" : " + fieldType); 

              //FIELD ID
                //if field type is "LINE_COUNT or CHECKSUM" then don't look into the Field TYPE and Line ID and Line Type
                if(!justFieldType.contains(fieldType)){ 
                    fieldID = listofArtifacts.get(i).fieldID;
                                       
                    //If the field type is TOKEN, check if the field ID is a number 1-9 or ALL or LAST
                    if(fieldType.equals("TOKEN") && (fieldID.equals("0") || !(fieldID.matches("^[0-9]+$") || fieldID.equals("ALL") || fieldID.equals("LAST"))))
                        error.fieldTypeTokenError = true;
                    
                    //If the field type is PARAM, check if the value is a postive number or zero
                    else if(fieldType.equals("PARAM") && !(fieldID.matches("^[0-9]+$")))
                        error.fieldTypeParamError = true;
                    
                    //Check if the user didn't inputted anthing in the Field ID
                    else if(fieldID.isEmpty() || fieldID.equals(""))
                        error.fieldIDMissing = true;
                    
                    //If all is good with the above checks, then concatenate the fieldID to the artifactLine 
                    else
                        artifactConfigLine += (" : " + fieldID); 
                    
                  //LINE_TYPE and LINE ID
                    //Is LineType and Line ID relevant based on field type? if so, then...
                    if(lineParamAccessible.contains(fieldType)){ 
                        ToolTipWrapper lineTypeTTW = listofArtifacts.get(i).lineType;
                        lineType = lineTypeTTW.getItem();
                        lineID = listofArtifacts.get(i).lineID;
                                                
                        if(!lineType.equals("NONE")){
                            //Check if there is a line ID input if the user has a line type
                            if(lineID.isEmpty() || lineID.equals(""))
                                error.lineIDMissing = true;
                            else if(lineType.equals("LINE") && (lineID.equals("0") || !(lineID.matches("^[0-9]+$")))){
                                error.lineIDError = true;
                            }
                            else if(timeStampType.equals("LOG_TS") && lineType.equals("HAVESTRING"))
                                artifactConfigLine += (" : " + "HAVESTRING_TS" + " : " + lineID);
                            else if(timeStampType.equals("LOG_TS") && lineType.equals("REGEX"))
                                artifactConfigLine += (" : " + "REGEX_TS" + " : " + lineID);
                            else
                                artifactConfigLine += (" : " + lineType + " : " + lineID);
                        }
                    }
                }
               
                //If there's no error, put the artifactConfigLine in the resultsConfigText string, 
                //Otherwise the overallPass of the user input is false
                if(error.userInputCheck(i+1)){
                    if(i < listofArtifacts.size()-1)
                        artifactConfigLine+= System.lineSeparator();
                    //Add the artifact config line to the Results Config text
                    resultsConfigText += artifactConfigLine; 
                }
                else
                    error.fail();         
            }
            
            //Check for duplicate result tags
            error.checkDuplicateResultTags(resultTagList);
            /*
            for(String rt : resultTagList)
                System.out.println(rt);
            */
            
            if(error.passStatus()){
                //Resets the results.config file
                File resultsConfigFile = initializeResultConfig();

                try ( //Write the resultsConfigText to the results.config
                    BufferedWriter writer = new BufferedWriter(new FileWriter(resultsConfigFile, true))) {
                    writer.write(resultsConfigText);
                }
            }
            else
                 JOptionPane.showMessageDialog(null, error.toString(), "INPUT ERROR", JOptionPane.ERROR_MESSAGE);
        } 
         catch (IOException ex) {
            Logger.getLogger(ResultsUI.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    //Checks if the results.config file exists and prepares the result.config file for the lab
    private File initializeResultConfig() throws IOException{
        //Get the filepath for the lab's results.config
        String userHomeFolder = System.getProperty("user.home");
        File resultsConfigFile = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator + labname + File.separator + "instr_config" + File.separator + "results.config");
        
        //May not be necessary, subject to remove the base text, perhaps there is an option for the user to add their own comments
        String baseText = 
                  "# results.config" + System.lineSeparator()
                + "#" + System.lineSeparator()
                + "# Please see the Labtainer Lab Designer User Guide" + System.lineSeparator();
        
        if(resultsConfigFile.exists()){ 
            //Overwrite results.config file if it already exists
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(resultsConfigFile, false))) {
                writer.write(baseText);
            }
            return resultsConfigFile;
        } 
        else if(resultsConfigFile.createNewFile()){ 
            //Create new results.config file otherwise(if it does not already exist)
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(resultsConfigFile))) {
                writer.write(baseText);
            }
            return resultsConfigFile;
         } 
        else{ //File could not be created so return error message
            System.out.println("Results Config File couldn't be initialzed.");
            return null;
        }     
    } 
    
    //Handles all the error data and error checking before writing the results.config    
    private class ErrorHandler{
        private boolean overallPass;
        private String errorMsg;
        private boolean 
                resultError,
                fileError,
                timeDelimiterError,
                fieldTypeTokenError,
                fieldTypeParamError,
                lineIDError,

                resultTagMissing,
                fileIDMissing,
                timeDelimiterMissing,
                fieldIDMissing,
                lineIDMissing;
        
        
        ErrorHandler(){
            overallPass = true;
            errorMsg = "";
            checkReset();
        }
        
        void fail(){
            overallPass = false;
        } 
        
        //Resets the error status(used right before looking at new artifact line)
        private void checkReset(){
            resultError = false;
            fileError = false;
            timeDelimiterError = false;
            fieldTypeTokenError = false;
            fieldTypeParamError = false;
            lineIDError = false;

            resultTagMissing = false;
            fileIDMissing = false;
            timeDelimiterMissing = false;
            fieldIDMissing = false;
            lineIDMissing = false;
            
        }
        
        //Builds error message detailing the errors that appear in the user input
        boolean userInputCheck(int artifactIndex){
            boolean rowPassed = true;
            String infoMsg = "Artifact Line: " + artifactIndex + System.lineSeparator();

            if(resultTagMissing){
               rowPassed = false;
               infoMsg+= "-Result Tag input is missing." + System.lineSeparator();
            }
            if(fileIDMissing){
               rowPassed = false;
               infoMsg+= "-File ID input is missing." + System.lineSeparator();
            }
            if(timeDelimiterMissing){
               rowPassed = false;
               infoMsg+= "-Time Delimiter input is missing." + System.lineSeparator();
            }
            if(fieldIDMissing){
               rowPassed = false;
               infoMsg+= "-Field ID input is missing." + System.lineSeparator();
            }
            if(lineIDMissing){
               rowPassed = false;
               infoMsg+= "-Line ID input is missing)." + System.lineSeparator();
            }
            if(resultError){
               rowPassed = false;
               infoMsg+= "-Make sure your Results Tag has only alphanumeric characters or underscores." + System.lineSeparator();
            }
            if(fileError){
               rowPassed = false;
               infoMsg+= "-Make sure your File ID file's extentsion ends in \".stdin\", \".stdout\", or \".prgout\"." + System.lineSeparator() + " Or is a file path." + System.lineSeparator();
            }
            if(timeDelimiterError){
               rowPassed = false;
               infoMsg+= "-Timestamp Delimiter Option is only available if your File ID is a file path." + System.lineSeparator();
            }
            if(fieldTypeTokenError){
               rowPassed = false;
               infoMsg+= "-If your Field Type is TOKEN then make sure your Field ID is a positve number(zero exclusive), \"ALL\", or \"LAST\"." + System.lineSeparator();
            }
            if(fieldTypeParamError){
               rowPassed = false;
               infoMsg+= "-If your Field Type is PARAM then make sure your Field ID is a positve number(zero inclusive)." + System.lineSeparator();
            }
            if(lineIDError){
                rowPassed = false;
                infoMsg+= "-If your Line Type is LINE then make sure your Line ID is a positve number(zero exclusive)." + System.lineSeparator();
            }

            
            if(!rowPassed)
                errorMsg += (infoMsg + System.lineSeparator());

            return rowPassed;
        }
        
        //Check for duplicate results Taga
        void checkDuplicateResultTags(ArrayList<String> resultTags){
            ArrayList<ResultTagIndices> markedResultTags = new ArrayList<>();
            
            //Store all the indices for each unique result tag
            for(int i=0;i<resultTags.size();i++){
                String resultTag = resultTags.get(i);   
                //Is the resultTag a duplicate? 
                //If so, add the the index number of the duplicate result tag to the corresponding result tag's list of indices
                if(isDuplicate(markedResultTags, resultTag)){
                    getDuplicate(markedResultTags, resultTag).addIndex(i);
                }
                //If not, add it to the markedResultTags fresh 
                else
                    markedResultTags.add(new ResultTagIndices(resultTag, i));
            }
            
            //Go through every result tag and see if any of them have more than 1 index, if they do then create a custom error message for the duplicate result tag
            String duplicateErrorMsg = "";
            for(ResultTagIndices rt : markedResultTags){
                if(rt.indices.size() > 1){
                    duplicateErrorMsg+= "Duplicate Result Tag: \"" + rt.resultTag + "\" on rows ";
                     
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
        
        //Stores a result tag's name and the row index they appear on
        class ResultTagIndices{
            protected String resultTag;
            protected ArrayList<Integer> indices;
                    
            ResultTagIndices(String resultTag, int index){
                this.resultTag = resultTag;
                indices = new ArrayList<>();
                indices.add(index);
            }
            
            void addIndex(int index){
                indices.add(index);
            }
        }
        
        //Is the result tag already in the duplicate list?
        boolean isDuplicate(ArrayList<ResultTagIndices> markedResultTags, String resultTag){
            for(ResultTagIndices rtIndices : markedResultTags){
                if(rtIndices.resultTag.equals(resultTag))
                    return true;
            }
            return false;
        }
        
        //Get the duplicate object based on the duplicate string
        ResultTagIndices getDuplicate(ArrayList<ResultTagIndices> markedResultTags, String resultTag){
            for(ResultTagIndices rtIndices : markedResultTags){
                if(rtIndices.resultTag.equals(resultTag))
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
    //Gets the artifact lines in the goals.config
    protected ArrayList<String> getArtifactLines(){
        ArrayList<String> artifacts = new ArrayList<>();
        
        try {
            String userHomeFolder = System.getProperty("user.home");
            File lab = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator+ labname);
            File resultsConfig = new File(lab+"/instr_config/results.config");

            //Get the artifact lines
            if(resultsConfig.exists()){
                try (FileReader fileReader = new FileReader(resultsConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader); 
                    String line = bufferedReader.readLine();
                    
                    while (line != null) {                 
                        //just checks if the first character is: not empty, not a hash, and not whitspace)
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0)))
                            artifacts.add(line);

                        line = bufferedReader.readLine();
                    }   
                }
                return artifacts;
            }
            else{
                System.out.println("No results.config file in the loaded lab!");
                return null;
            }
        } 
        catch (IOException e) {
            System.out.println("Issue with getting result.config artifacts");
            return null;
        }     
    }
       
    //Updates the list of artifacts
    protected void updateListofArtifacts(JPanel PanelofArtifacts){
       Component[] artifacts = PanelofArtifacts.getComponents(); //Access the list of artifacts
                
       List<ArtifactValues> listofArtifactsTMP = new ArrayList<>();
        
       //Iterate through each artifact and add it to the temp list of artifact values
       for (Component artifact : artifacts) {
           //RESULTS TAG
           String resultTag = ((ArtifactPanels) artifact).getTagTextField().getText();
           //FILEID CONFIG
           String file = ((ArtifactPanels) artifact).getFileTextField().getText();
           String container = (String) (((ArtifactPanels) artifact).getContainerComboBox().getSelectedItem());
           ToolTipHandlers.ToolTipWrapper timeStampType = (ToolTipHandlers.ToolTipWrapper) (((ArtifactPanels) artifact).getTimeStampComboBox().getSelectedItem());
           String timeStampDelimiter = ((ArtifactPanels) artifact).getTimeStampTextField().getText();
           //FieldType
           ToolTipHandlers.ToolTipWrapper fieldType = (ToolTipHandlers.ToolTipWrapper) (((ArtifactPanels) artifact).getFieldTypeComboBox().getSelectedItem());
           String fieldID = ((ArtifactPanels) artifact).getFieldIDTextField().getText();
           //LINE_TYPE and LINE ID
           ToolTipHandlers.ToolTipWrapper lineType = (ToolTipHandlers.ToolTipWrapper) (((ArtifactPanels) artifact).getLineTypeComboBox().getSelectedItem());
           String lineID = ((ArtifactPanels) artifact).getLineIDTextField().getText();
           
           listofArtifactsTMP.add(new ArtifactValues(resultTag, container, file, fieldType, fieldID, lineType, lineID, timeStampType, timeStampDelimiter));
       }
       
       listofArtifacts = listofArtifactsTMP; //overwrite the old listofArtifacts with the temp listofArtifacts
    }
    
    //Swaps the position of artifacts in a list
    protected void swapArtifacts(String type, int rowIndex){

        switch(type){
            case "UP":
                if(rowIndex > 0){
                    //System.out.println("UP: "+listofArtifacts.get(rowIndex).resultTag+" Index: "+rowIndex);
                    Collections.swap(listofArtifacts, rowIndex, rowIndex-1);
                }
                break;
            case "DOWN":
                //System.out.println(rowCount);
                //System.out.println("RowINdex: " + rowIndex + " RowCount-1: "+ (rowCount-1));
                if(rowIndex < rowCount-1){
                    //System.out.println("DOWN: "+listofArtifacts.get(rowIndex).resultTag);
                    Collections.swap(listofArtifacts, rowIndex, rowIndex+1);
                }
                break;
            default:
                System.out.println("swap case no register");
        }
    }
    
    //Gets a list of ArtifactValues from the the current state of the results.config file
    protected List<ArtifactValues> getArtifactValuesOfConfigFile(){
        List<ArtifactValues> officialListofArtifacts = new ArrayList<>();
        
        ArrayList<String> artifactLines = getArtifactLines();
        
        if(artifactLines != null){

            for(String artifactLine : artifactLines){
                ArtifactValues values = new ArtifactValues(artifactLine);
                officialListofArtifacts.add(values);
            } 
            return officialListofArtifacts;
        }
        else
            return null;
    }
    
    //Compares the data of two lists of ArtifactValues. If there is a difference then return 'true', 'false' otherwise
    static boolean artifactValuesDiffer(List<ArtifactValues> list1, List<ArtifactValues> list2){
        if(list1.size() != list2.size()){  
            return true;
        }
        else{
            //This is a gross implemenation of comparing each individual value between two sets of Artifact Values (Maybe conisder implementing the ArtifactValues Class as a comparable)
            for(int i=0;i<list1.size();i++){
                printlistValues(list1, list2, i);  
                if(!list1.get(i).container.equals(list2.get(i).container))
                    return true;
                else if(!list1.get(i).fieldID.equals(list2.get(i).fieldID))
                    return true;
                else if(!list1.get(i).fieldType.getItem().equals(list2.get(i).fieldType.getItem()))
                    return true;
                else if(!list1.get(i).fileID.equals(list2.get(i).fileID))
                    return true;
                else if(!list1.get(i).lineID.equals(list2.get(i).lineID))
                    return true;  
                else if(!list1.get(i).lineType.getItem().equals(list2.get(i).lineType.getItem()))
                    return true;
                else if(!list1.get(i).resultTag.equals(list2.get(i).resultTag))
                    return true;                
                else if(!list1.get(i).timeStampDelimiter.equals(list2.get(i).timeStampDelimiter))
                    return true;                
                else if(!list1.get(i).timeStampType.getItem().equals(list2.get(i).timeStampType.getItem()))
                    return true;                
            }
        }     
        return false;
    }
    
    //Used for debugging in the artifactValuesDiffer(List<ArtifactValues> list1, List<ArtifactValues> list2) method
    static private void printlistValues(List<ArtifactValues> list1, List<ArtifactValues> list2, int i){
        System.out.println("Result Tag: ");
                    System.out.println("UI: "+list1.get(i).resultTag);
                    System.out.println("Config: "+list2.get(i).resultTag);
                    System.out.println();
                
                    System.out.println("File ID: ");
                    System.out.println("UI: "+list1.get(i).fileID);
                    System.out.println("Config: "+list2.get(i).fileID);
                    System.out.println();
                    
                    System.out.println("Field Type: ");
                    System.out.println("UI: "+list1.get(i).fieldType);
                    System.out.println("Config: "+list2.get(i).fieldType);
                    System.out.println();
                    
                    System.out.println("Field ID: ");
                    System.out.println("UI: "+list1.get(i).fieldID);
                    System.out.println("Config: "+list2.get(i).fieldID);
                    System.out.println();
                    
                    System.out.println("Line Type: ");
                    System.out.println("UI: "+list1.get(i).lineType);
                    System.out.println("Config: "+list2.get(i).lineType);
                    System.out.println();
                    
                    System.out.println("Line ID: ");
                    System.out.println("UI: "+list1.get(i).lineID);
                    System.out.println("Config: "+list2.get(i).lineID);
                    System.out.println();
                    
                    System.out.println("TimeStamp Type: ");
                    System.out.println("UI: "+list1.get(i).timeStampType);
                    System.out.println("Config: "+list2.get(i).timeStampType);
                    System.out.println();
                    
                    System.out.println("TimeStamp Delim: ");
                    System.out.println("UI: "+list1.get(i).timeStampDelimiter);
                    System.out.println("Config: "+list2.get(i).timeStampDelimiter);
                    System.out.println();
                    
                    System.out.println("CONTAINER: ");
                    System.out.println("UI: "+list1.get(i).container);
                    System.out.println("Config: "+list2.get(i).container);
                    System.out.println();
                
                
                
                
                
                
    }
    
//GETTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    protected List<ArtifactValues> getListofArtifacts(){
        return listofArtifacts;
    }
}
