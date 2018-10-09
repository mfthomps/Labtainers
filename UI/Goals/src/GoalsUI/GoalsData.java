/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GoalsUI;

import static GoalsUI.ParamReferenceStorage.GoalType_ITEMS;
import static GoalsUI.ParamReferenceStorage.answerTypes;
import static GoalsUI.ParamReferenceStorage.booleanResultTypes;
import static GoalsUI.ParamReferenceStorage.goalInput;
import static GoalsUI.ParamReferenceStorage.opInput;
import static GoalsUI.ParamReferenceStorage.resultTagInput;
import GoalsUI.ToolTipHandlers.ToolTipWrapper;
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
public class GoalsData {
    private List<GoalValues> listofGoals; 
    final private List<String> resultTagList;
    final private List<String> parameters;
    final private List<String> booleanResults;
    private boolean labloaded;
    final private String labname;
    private int rowCount;
     
    GoalsData(){
        listofGoals = new ArrayList<>(); 
        resultTagList = new ArrayList<>();
        parameters = new ArrayList<>();
        booleanResults = new ArrayList<>();
        labloaded = false;
        labname = "";
        rowCount = 0;
    }
    
    GoalsData(String labname){
        listofGoals = new ArrayList<>(); 
        resultTagList = new ArrayList<>();
        parameters = new ArrayList<>();
        booleanResults = new ArrayList<>();
        labloaded = false;
        this.labname = labname;
        rowCount = 0;
        
        getData();
    }
    
    
//LOADING~~~~~~~~~~~~~~~~~~~~~~~~
    
    //Checks if the lab exists and will load lab's goals.config if it does
    private void getData(){
        //Check if the Folder exists
        String userHomeFolder = System.getProperty("user.home");
        File lab = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator+ labname);
        
        if(lab.isDirectory()){
            if(getResultTags(lab) && getGoals()){
                labloaded = true;
                getParameters(lab);
                getBooleanResults(lab);
            }
        }
        else
            System.out.println("Lab does not exist!"); 
    }
    
    //Updates the resultTagList (all goal panels refer to this list to fill in the resultTag combobox)
    private boolean getResultTags(File lab){
        File resultsConfig = new File(lab + File.separator + "instr_config" + File.separator + "results.config");
        try {
            if(resultsConfig.exists()){
                try (FileReader fileReader = new FileReader(resultsConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    
                    String line = bufferedReader.readLine();
                    while (line != null) {
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0)))
                            resultTagList.add(line.split(" = ")[0]);
                        line = bufferedReader.readLine(); 
                    }
                } 
                return true;
            }
            else{
                System.out.println("results.config is missing");
                return false;
            }
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
        catch (IOException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
            return false;
       }
    }    
    
    //Parses the goals.config to obtain all the relevant goal lines, 
    //extracts the values of each goal line and stores them into a list of "goals"(Goal Values)
    private boolean getGoals(){
        //Attempt to set the listofGoals, if it ends up being null then there was an issue accessing the goal lines, which would be paresd into Goal Values
        listofGoals = getGoalValuesOfConfigFile();
        if(listofGoals != null){
            rowCount=listofGoals.size();
            return true;
        }
        else
            return false;    
    }
    
    //Get the parameter.config IDs
    private void getParameters(File lab){        
        File parameterConfig = new File(lab + File.separator + "config" + File.separator + "parameter.config");
        try {
            if(parameterConfig.exists()){
                try (FileReader fileReader = new FileReader(parameterConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    
                    String line = bufferedReader.readLine();
                    while (line != null) {
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0)))
                            parameters.add(line.split(" : ")[0]);
                        line = bufferedReader.readLine(); 
                    }
                } 
            }
            else
                System.out.println("parameter.config is missing");
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
        } 
        catch (IOException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    //Get the result tags that are boolean result types
    private void getBooleanResults(File lab){
        File resultsConfig = new File(lab + File.separator + "instr_config" + File.separator + "results.config");
        try {
            if(resultsConfig.exists()){
                try (FileReader fileReader = new FileReader(resultsConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    
                    String line = bufferedReader.readLine();
                    while (line != null) {
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0)))
                            if(booleanResultTypes.contains(line.split(" : ")[1]))
                                booleanResults.add(line.split(" = ")[0]);
   
                        line = bufferedReader.readLine(); 
                    }
                } 
            }
            else
                System.out.println("results.config is missing");
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
        } 
        catch (IOException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
//WRITING~~~~~~~~~~~~~~~~~~~~~~~~          
        
    //Update the results.config file with the user's input
    protected void writeGoalsConfig(JPanel PanelofGoals){
         try {
            Component[] goals = PanelofGoals.getComponents(); //Access the list of goals
            String goalID,
                   goalType,
                   
                   operator,
                   resultTag,
                   answerType,
                    
                   booleanExp,
                    
                   goal1,
                   goal2,
                   
                   value,
                   subgoalList,
            
                   executableFile;
            String goalsConfigText = "";
            ErrorHandler error = new ErrorHandler();
            List<String> goalIDs = new ArrayList(); //Used for goal ID duplication check
            
            //Iterate through each goal
            for(int i=0;i < goals.length;i++){
                error.checkReset(); //Reset the error statuses for a new goal line
                
                String goalConfigLine = "";
                
                //Goal ID
                goalID = ((GoalPanels)goals[i]).getGoalIDTextField().getText();
                goalIDs.add(goalID);
                //Checks if goal ID is valid or inputted
                if(error.checkGoalID(goalID))
                   goalConfigLine += (goalID + " = "); //add to goal ID Config line
                
                //Goal Type
                ToolTipHandlers.ToolTipWrapper goalTypeTTW = (ToolTipHandlers.ToolTipWrapper)(((GoalPanels)goals[i]).getGoalTypeComboBox().getSelectedItem());
                goalType = goalTypeTTW.getItem();
                
                switch (goalType) {
                    case "matchExpression":
                        goalConfigLine += "matchany : ";
                        break;
                    case "count_value":
                    case "count_matches":
                        goalConfigLine += "count : ";
                        break;
                    default:
                        goalConfigLine += goalType+" : ";
                        break;
                }
                
                if(opInput.contains(goalType)){
                    ToolTipHandlers.ToolTipWrapper operatorTTW = (ToolTipHandlers.ToolTipWrapper)(((GoalPanels)goals[i]).getOperatorComboBox().getSelectedItem());
                    operator = operatorTTW.getItem();
                    resultTag = (String)((GoalPanels)goals[i]).getResultTagComboBox().getSelectedItem();
                    answerType = (String)((GoalPanels)goals[i]).getAnswerTypeComboBox().getSelectedItem();

                    goalConfigLine += operator+" : ";
                    goalConfigLine += resultTag+" : ";
                    goalConfigLine += answerHandler(answerType, (GoalPanels)goals[i]);
                }
                
                else if(goalInput.contains(goalType)){  
                    goal1 = ((GoalPanels)goals[i]).getGoal1TextField().getText();
                    goal2 = ((GoalPanels)goals[i]).getGoal2TextField().getText();
                    
                    ArrayList<String> listOfAboveGoals = getAboveGoals("GOAL1&2", i, goals);
                    if(error.checkGoal1(goal1, listOfAboveGoals))
                        goalConfigLine += goal1+" : ";                    
                    if(error.checkGoal2(goal2, listOfAboveGoals))
                        goalConfigLine += goal2;
                }
                
                else if(resultTagInput.contains(goalType)){  
                    resultTag = (String)((GoalPanels)goals[i]).getResultTagComboBox().getSelectedItem();
                    goalConfigLine += resultTag;
                }
                
                else if("boolean".equals(goalType)){
                    booleanExp = ((GoalPanels)goals[i]).getBooleanTextField().getText();
                    
                    if(error.checkBooleanExp(booleanExp, getAboveGoals("BOOLEAN", i, goals), booleanResults)){
                        goalConfigLine += booleanExp;
                    } 
                }
                
                else if("count_greater".equals(goalType)){
                    value = ((GoalPanels)goals[i]).getValueTextField().getText();
                    subgoalList = ((GoalPanels)goals[i]).getSubgoalTextField().getText();
                     
                    if(error.checkValueAndSubgoals(value, subgoalList, getAboveGoals("ALL", i, goals), booleanResults)){
                        goalConfigLine += value+" : ";
                        goalConfigLine += "(";
                        goalConfigLine += subgoalList;
                        goalConfigLine += ")";
                    }  
                    
                    
                        
                }
                else if("execute".equals(goalType)){
                   executableFile = ((GoalPanels)goals[i]).getExecutableFileTextField().getText();
                   resultTag = (String)((GoalPanels)goals[i]).getResultTagComboBox().getSelectedItem();
                   answerType = (String)((GoalPanels)goals[i]).getAnswerTypeComboBox().getSelectedItem();

                   goalConfigLine += executableFile+" : ";
                   goalConfigLine += resultTag+" : ";
                   goalConfigLine += answerHandler(answerType, (GoalPanels)goals[i]);
                }
                else if("matchExpression".equals(goalType)){
                   ToolTipHandlers.ToolTipWrapper operatorTTW = (ToolTipHandlers.ToolTipWrapper)(((GoalPanels)goals[i]).getOperatorComboBox().getSelectedItem());
                   operator = operatorTTW.getItem();
                   
                   //May need modification /validation
                   String rt = (String)((GoalPanels)goals[i]).getArithmeticResultTagTextField().getText();
                   resultTag="";
                   if(error.checkArithRT(rt)){ //NOTE: the checkArithRT is incomplete and simply returns 'true' 
                       resultTag += "(";
                       resultTag += rt;
                       resultTag += ")";
                   }
                   
                   answerType = (String)((GoalPanels)goals[i]).getAnswerTypeComboBox().getSelectedItem();

                   goalConfigLine += operator+" : ";
                   goalConfigLine += resultTag+" : ";
                   goalConfigLine += answerHandler(answerType, (GoalPanels)goals[i]);
                }    
                

                //If there's no error, put the goalConfigLine in the resultsConfigText string, 
                //Otherwise the overallPass of the user input is false
                if(error.userInputCheck(i+1)){
                    if(i < goals.length-1)
                        goalConfigLine+= System.lineSeparator();
                    //Add the goal config line to the Results Config text
                    goalsConfigText += goalConfigLine; 
                }
                else
                    error.fail();         
            }
            
            //Check for duplicate goal IDs
            error.checkDuplicateGoalIDs(goalIDs, booleanResults);
            
            
            if(error.passStatus()){
                //Resets the results.config file
                File goalsConfigFile = initializeGoalsConfig();

                try ( //Write the resultsConfigText to the results.config
                    BufferedWriter writer = new BufferedWriter(new FileWriter(goalsConfigFile, true))) {
                    writer.write(goalsConfigText);
                }
            }
            else
                 JOptionPane.showMessageDialog(null, error.toString(), "INPUT ERROR", JOptionPane.ERROR_MESSAGE);
        } 
         catch (IOException ex) {
            Logger.getLogger(GoalsUI.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    //Builds the string bit to be added in the goals.config that describes the answer for a goal
    private String answerHandler(String answerType, GoalPanels goal){
        String answer = "";
        
        if(answerType.equals(answerTypes[0])){ //Literal
            answer += "answer=";
            answer += goal.getAnswerTagTextField().getText();
        }
        else if(answerType.equals(answerTypes[1])){ //Result Tag
            answer += "result.";
            answer += (String)(goal.getResultTag2ComboBox().getSelectedItem());                        
        }
        else if(answerType.equals(answerTypes[2])){ //Parameter
            answer += "parameter.";   
            answer += (String)(goal.getParameterComboBox().getSelectedItem());   
        }
        else if(answerType.equals(answerTypes[3])){ //Parameter ASCII
            answer += "parameter_ascii.";    
            answer += (String)(goal.getParameterComboBox().getSelectedItem());
        }
        else
            System.out.println("Issue writing answer in the goals.config");
        
        return answer;
    } 
    
    //Checks if the goals.config file exists and prepares the goals.config file for the lab
    private File initializeGoalsConfig() throws IOException{
        //Get the filepath for the lab's goals.config
        String userHomeFolder = System.getProperty("user.home");
        File goalsConfigFile = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator + labname + File.separator + "instr_config" + File.separator + "goals.config");
        
        //May not be necessary, subject to remove the base text, perhaps there is an option for the user to add their own comments
        String baseText = 
                  "# goals.config" + System.lineSeparator()
                + "#" + System.lineSeparator()
                + "# Please see the Labtainer Lab Designer User Guide" + System.lineSeparator();
        
        if(goalsConfigFile.exists()){ 
            //Overwrite goals.config file if it already exists
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(goalsConfigFile, false))) {
                writer.write(baseText);
            }
            return goalsConfigFile;
        } 
        else if(goalsConfigFile.createNewFile()){ 
            //Create new goals.config file otherwise(if it does not already exist)
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(goalsConfigFile))) {
                writer.write(baseText);
            }
            return goalsConfigFile;
        } 
        else{ //File could not be created so return error message
            System.out.println("Goals Config File couldn't be initialzed.");
            return null;
        }     
    } 

    //Handles all the error data and error checking before writing the goals.config    
    protected class ErrorHandler{
        private boolean overallPass;
        private String errorMsg;
        boolean
                goalError,
                goalIDMissing,
                
                goal1Error,
                goal1Missing,
                goal2Error,
                goal2Missing,
                
                booleanExpCharError,
                booleanExpTagError,
                booleanExpNotError,
                booleanExpStartError,
                booleanExpEndError,
                booleanParensError,
                booleanAlternateError,
                booleanMissing,
                
                arithRTCharError,
                arithRTMissing,
                
                valueError,
                valueMissing,
                subgoalError,
                subgoalMissing;

        ErrorHandler(){
            overallPass = true;
            errorMsg = "";
            checkReset();
        }
        
        void fail(){
            overallPass = false;
        } 
        
        //Rests the error status(used right before looking at new goal line)
        private void checkReset(){
            goalError = false;
            goalIDMissing = false;

            goal1Error = false;
            goal1Missing = false;
            goal2Error = false;
            goal2Missing = false;

            booleanExpCharError = false;
            booleanExpTagError = false;
            booleanExpNotError = false;
            booleanExpStartError = false;
            booleanExpEndError = false;
            booleanParensError = false;
            booleanAlternateError = false;
            booleanMissing = false;

            arithRTCharError = false;
            arithRTMissing = false;

            valueError = false;
            valueMissing = false;
            subgoalError = false;
            subgoalMissing = false;
        }
        
        
        
        //Builds error message detailing the errors that appear in the user input
        boolean userInputCheck(int goalIndex){
            boolean rowPassed = true;
            String infoMsg = "Goal Line: " + goalIndex + System.lineSeparator();

            if(goalError){
                rowPassed = false;
                infoMsg+= "-Make sure your Goal ID has only alphanumeric characters or underscores." + System.lineSeparator();
            }
            if(goalIDMissing){
                rowPassed = false;
                infoMsg+= "-Goal ID input is missing." + System.lineSeparator();
            }


            if(goal1Error){
                rowPassed = false;
                infoMsg+= "-Make sure that Goal 1 is a 'matchany' goal above this line or a results boolean." + System.lineSeparator();
            }
            if(goal1Missing){
                rowPassed = false;
                infoMsg+= "-Goal 1 input is missing." + System.lineSeparator();
            }
            if(goal2Error){
                rowPassed = false;
                infoMsg+= "-Make sure that Goal 2 is a 'matchany' goal above this line or a results boolean." + System.lineSeparator();
            }
            if(goal2Missing){
                rowPassed = false;
                infoMsg+= "-Goal 2 input is missing." + System.lineSeparator();
            }


            if(booleanExpCharError || booleanExpTagError){
                rowPassed = false;
                infoMsg+= "-Make sure Boolean Expression contains only result booleans, non-matchacross goal IDs above this goal line," + System.lineSeparator() +
                          "parentheses, and boolean operators(and, or, and_not, or_not, not)." + System.lineSeparator();
            }
             if(booleanExpNotError){
                rowPassed = false;
                infoMsg+= "-The 'not' boolean operator can only appear at the beginning of a boolean expression." + System.lineSeparator();
            }
            if(booleanExpStartError || booleanExpEndError || booleanParensError || booleanAlternateError){
                rowPassed = false;
                infoMsg+= "-Make sure your expression is formatted correctly: Proper Parentheses and making sure an item precedes and follows " + System.lineSeparator()
                        + "a boolean operator." + System.lineSeparator();
            }
            if(booleanMissing){
                rowPassed = false;
                infoMsg+= "-Boolean input is missing." + System.lineSeparator();
            }


            if(arithRTCharError){
                rowPassed = false;
                infoMsg+= "-Make sure Arithmetic Result Tag is formatted correctly." + System.lineSeparator();
            }
            if(arithRTMissing){
                rowPassed = false;
                infoMsg+= "-Arithmetic Result Tag input is missing." + System.lineSeparator();
            }


            if(valueError){
                rowPassed = false;
                infoMsg+= "-Value can only be a positive number(includes zero) less than the number of subgoal items." + System.lineSeparator();
            }
            if(valueMissing){
                rowPassed = false;
                infoMsg+= "-Value input is missing." + System.lineSeparator();
            }
            if(subgoalError){
                rowPassed = false;
                infoMsg+= "-Make sure your Subgoal list is seperated by commas(', ') and only contains goals from above this goal line" + System.lineSeparator()
                        + "and/or result booleans." + System.lineSeparator();
            }
            if(subgoalMissing){
                rowPassed = false;
                infoMsg+= "-Subgoal List input is missing." + System.lineSeparator();
            }

            if(!rowPassed)
                errorMsg += (infoMsg + System.lineSeparator());

            return rowPassed;
        }
        
        //Checks is goal ID is missing or has invalid characters(valid: alphanumeric, and underscores)
        boolean checkGoalID(String goalID){
            if(goalID.isEmpty() || goalID.equals("")){
               goalIDMissing = true;
               return false;
            }
            else if(!goalID.matches("^[a-zA-Z0-9_-]+$")){
               goalError = true;
               return false;
            }
            else
                return true;
        }
        
        
        //Checks if goal 1 is either an above goal or a boolean results
        boolean checkGoal1(String goal1, List<String> listOfAboveGoals){
            if(goal1.isEmpty() || goal1.equals("")){
               goal1Missing = true;
               return false;
            }
            else if(!listOfAboveGoals.contains(goal1) && !booleanResults.contains(goal1)){
                goal1Error = true;
                return false;
            }
            else
                return true;
        }
        
        //Checks if goal 2 is either an above goal or a boolean results
        boolean checkGoal2(String goal2, List<String> listOfAboveGoals){
            if(goal2.isEmpty() || goal2.equals("")){
               goal2Missing = true;
               return false;
            }
            else if(!listOfAboveGoals.contains(goal2) && !booleanResults.contains(goal2)){
                goal2Error = true;
                return false;
            }
            else
                return true;
        }
        
        //Checks if boolean expression is valid: (The checking may have some overlap thta may need to be recoded)
        boolean checkBooleanExp(String booleanExp, List<String> nonMAAGoals, List<String> booleanResults) {
            String[] booleanOperators = {"and", "or", "and_not", "or_not"};
            
            if(booleanExp.isEmpty() || booleanExp.equals("")){
               booleanMissing = true;
               return false;
            }
            
            //Does the boolean exp contain invalid chars (char not: alphnumeric, undescore, hyphen, whitespace, parenthesis)
            if(!booleanExp.matches("^[a-zA-Z0-9_() -]+$")){
                booleanExpCharError = true; 
                return false;
            }
        
        //Reformat the boolean expression string to identitfy things that shouldn't be there   
            //Replace all " not" with %
            booleanExp = " "+booleanExp; 
            //The line above is necessary because when 'not' is used in the beginning there may or may not be a space before it. 
            //Adding the space includes the non-space-preceeded case.
            booleanExp = booleanExp.replaceAll(" not ", "%");
            
            booleanExp = booleanExp.trim();
            
            //System.out.println("OG: "+booleanExp);
            //System.out.println();
            //System.out.println("GOALS:");
            
            //Replace all non Matchacross Goals with an asterisk symbol
            for(String toReplace : nonMAAGoals){
                booleanExp = symbolReplace(booleanExp, toReplace, "*");
            }
            
            //System.out.println();
            //System.out.println("RESULT BOOLEANS:");
            //Replace all non boolean results with an asterisk symbol
            for(String toReplace : booleanResults){
                booleanExp = symbolReplace(booleanExp, toReplace, "*");
            }
            
            //System.out.println();
            //System.out.println("BOOLEAN OPERATORS:");
            //Replace all boolean operators  with a pound symbol
            for(String toReplace : booleanOperators){
                booleanExp = symbolReplace(booleanExp, toReplace, "#");
            }
                 
            //System.out.println(booleanExp);
            
            booleanExp = booleanExp.replaceAll("\\s+","");//removes white space

            //If the boolean expression had a "not " in it, did it not occur at the beginning and/or more than once
            if(booleanExp.contains("%") && (!booleanExp.startsWith("%") || (booleanExp.indexOf("%") != booleanExp.lastIndexOf("%")))){
                booleanExpNotError = true;
                return false;
            }
            //Does the reformatted Boolean Expression string pick up alphnumeric(with underscore) substring that doesn't belong in either nonMAAGoals or booleanResults
            if(!booleanExp.matches("^[%*#()]+$")){
                
                booleanExpTagError = true; 
                return false;
            }
            //Does it start with an operator or a close parens
            else if(booleanExp.startsWith("#") || booleanExp.startsWith(")")){
                booleanExpStartError = true; 
                return false;
            }
            //Does it end with an operator or an open parens
            else if(booleanExp.endsWith("#") || booleanExp.endsWith("(")){
                booleanExpEndError = true; 
                return false;
            }
            //Does the boolean expression have bad parens
            else if(parensHandler(booleanExp)){
                booleanParensError = true;
                return false;
            }
            //Does it at least have one operator not preceeded and not followed by a nonMAA goal/boolean result
            else if(alternatationCheck(booleanExp)){
                booleanAlternateError = true;
                return false;
            }                            
            
            return true;
        }
        
        //Replaces the a substring in the a string with another string
        String symbolReplace(String booleanExp, String toReplace, String replaceWith){
            int tRIndex = booleanExp.indexOf(toReplace);
                while(tRIndex != -1){
                    int indexAfterWord = tRIndex+toReplace.length();
                    int indexBeforeWord = tRIndex-1;
                    //System.out.println(toReplace+": ");
                    //System.out.println("tRIndex: "+tRIndex);
                    //System.out.println("indexAfterWord: "+indexAfterWord);
                    
                    
                    //IF the word to replace is at the beginning:  "toReplace and_not other" -> "* and_not other"
                    if(tRIndex == 0 && booleanExp.charAt(indexAfterWord) == ' '){
                        booleanExp = booleanExp.substring(0, indexAfterWord).replaceFirst(toReplace, replaceWith)+
                                     booleanExp.substring(indexAfterWord, booleanExp.length());
                    }
                    //IF the word to replace is at the end: "other and_not toRepalce" -> "other and_not *"
                    else if(tRIndex == booleanExp.length()-toReplace.length() && 
                            booleanExp.charAt(booleanExp.length()-toReplace.length()-1) == ' '){
                        booleanExp = booleanExp.substring(0, tRIndex) + 
                                     booleanExp.substring(tRIndex, booleanExp.length()).replaceFirst(toReplace, replaceWith);
                    } 
                    /*
                    IF the word to replace is in the middle: "other and toReplace and another" -> "other and * and another"
                                                             "(other and toReplace) and another" -> "(other and *) and another"
                                                             "(toReplace and other) and another" -> "(* and other) and another"
                                                             "(toReplace) and another" -> "(*) and another"
                    */
                    else if((booleanExp.charAt(indexBeforeWord) == ' ' || booleanExp.charAt(indexBeforeWord) == '(') &&
                            (booleanExp.charAt(indexAfterWord) == ' ' || booleanExp.charAt(indexAfterWord) == ')')){
                        booleanExp = booleanExp.substring(0, tRIndex)+
                                     booleanExp.substring(tRIndex, indexAfterWord).replaceFirst(toReplace, replaceWith)+
                                     booleanExp.substring(indexAfterWord, booleanExp.length());
                    }
                    
                    //System.out.println(booleanExp);
                    //System.out.println();
                    
                    indexAfterWord = tRIndex+replaceWith.length(); //The indexAfterWord is shifted since the word has been deleted and replaced
                    if(indexAfterWord<booleanExp.length())
                        tRIndex = booleanExp.indexOf(toReplace, indexAfterWord);
                    else
                        break;
                }  
                
                return booleanExp;
        }
        
        
        //Checks if number of open parens and close parens is the same, then
        //checks if each open parens is followed by either by another open paren or a booleanResults/goalID 
        //and if each close parens is followed by either by another close paren or a booleanResults/goalID 
        //TRUE == error; FALSE == valid
        boolean parensHandler(String booleanExp){            
            //need  to check if number of open parens and close parens is equal <--- TODO (check character count method)
            if(characterCounter(booleanExp, '(') != characterCounter(booleanExp, ')')){
                return true;
            }
              
            for(int i=0;i<booleanExp.length()-1;i++){
                //checks if each open parens is followed by either by another open paren or a booleanResults/goalID 
                if( booleanExp.charAt(i) == '(' && !(booleanExp.charAt(i+1) == '(' || booleanExp.charAt(i+1) == '*')) 
                    return true;

                //checks if each close parens is followed by either by another close paren or a booleanResults/goalID 
                if( booleanExp.charAt(booleanExp.length()-1-i) == ')' && !(booleanExp.charAt(booleanExp.length()-2-i) == ')' || booleanExp.charAt(booleanExp.length()-2-i) == '*')) 
                    return true;
                
            }
            
            return false;
        }
        
        //Counts the number of times a character appears in a string
        int characterCounter(String str, char c) {
            int counter = 0;
            for( int i=0; i<str.length(); i++ ) {
                if( str.charAt(i) == c ) {
                    counter++;
                } 
            }
            return counter;
        }
        
        //Checks if each operator is preceeded and followed by a nonMAA goal/boolean result (symbolically) '*' = nonMAA goal/booolean result '#' = boolean operator
        //TRUE == error; FALSE == valid
        boolean alternatationCheck(String booleanExp){
            //Take out all chars besides '*', '#' for easier checking
            booleanExp = booleanExp.replaceAll("%", "");
            booleanExp = booleanExp.replaceAll("\\(", "");
            booleanExp = booleanExp.replaceAll("\\)", "");
            
            for(int i=0;i<booleanExp.length()-2;i+=2){
                if(booleanExp.charAt(i) == '*' && booleanExp.charAt(i+1) != '#')
                    return true;
            }
            
            return false;
        }
        
        
        //Checks if the subgoals are either boolean results or previous goals
         //Checks if the value is a positve number (including zero)
        //Checks if the number of subgoals is less than or equal to the value (invalid)
        boolean checkValueAndSubgoals(String value, String subgoalList, List<String> aboveGoals, List<String> booleanResults){            
            boolean pass = true;
            
            if(subgoalList.isEmpty() || subgoalList.equals("")){
               subgoalMissing = true;
               pass = false;
            }
            if(value.isEmpty() || value.equals("")){
                valueMissing = true;
                pass = false;
            }
            
            if(!subgoalMissing && !valueMissing){
                String[] subgoals = subgoalList.split(", ");
                for(String subgoal : subgoals){
                    subgoal = subgoal.replaceAll("\\s+", "");
                    if(!aboveGoals.contains(subgoal) && !booleanResults.contains(subgoal)){
                        subgoalError = true;
                        pass = false;
                    }
                } 
                
                if(!value.matches("^[0-9]+$") || subgoals.length <= Integer.parseInt(value)){                
                    valueError = true;
                    pass = false;
                }
                
                
            }
            return pass;
        }
        
        //Checks if the result tag has any arithmetic errors (NEEDS REVISION) ***Incomplete
        boolean checkArithRT(String arithRT){
            if(arithRT.isEmpty() || arithRT.equals("")){
               arithRTMissing = true;
               return false;
            }
//            for(String rt : resultTagList)
//                arithRT.replaceAll(rt, "0");
//            arithRT.replaceAll("\\s+","");//removes white space
//            
//            if(!arithRT.matches("^[-+0*/&0-9()]+$")){
//                arithRTCharError = true;
//                return false;
//            }
            
            return true;
        }
        
        
        
        
        
        //Check if there are goalID duplicates (this includes checking duplicates with boolean results)
        void checkDuplicateGoalIDs(List<String> goalIDs, List<String> booleanResults){
            ArrayList<GoalIDIndices> goalIDSet = new ArrayList<>();
            
            //Store all the indices for each unique goal ID
            for(int i=0;i<goalIDs.size();i++){
                String goalID = goalIDs.get(i);   
                //Is the goal ID a duplicate? 
                //If so, add the the index number of the duplicate result tag to the corresponding result tag's list of indices
                if(isDuplicate(goalIDSet, goalID))
                    getDuplicate(goalIDSet, goalID).addIndex(i);

                //If not, add it to the goalIDSet fresh 
                else
                    goalIDSet.add(new GoalIDIndices(goalID, i));
            }
            
            //Check if goalIDs have booleanResults
            for(int i=0; i<goalIDSet.size();i++){
                GoalIDIndices goalID = goalIDSet.get(i);
                for(int j=0; j<booleanResults.size();j++){
                    String booleanRT = booleanResults.get(j);
                    if(booleanRT.equals(goalID.goalID))
                       goalID.isResultTagBoolean = true;
                }
            }
            
            //Go through every goal ID and see if any of them have more than 1 index, if they do then create a custom error message for the duplicate result tag
            //also check if goal Id appears as a boolean results, if so create a custom message
            String duplicateErrorMsg = "";
            for(GoalIDIndices goal : goalIDSet){
                if(goal.indices.size() > 1){
                    duplicateErrorMsg+= "Duplicate Goal ID: \"" + goal.goalID + "\" on rows ";
                     
                    for(int i=0;i<goal.indices.size();i++){
                        duplicateErrorMsg+=(goal.indices.get(i)+1); //The plus 1 offset to get the 1-based row num
                        
                        if(goal.indices.size() == 2 && i == 0)
                            duplicateErrorMsg+=" and ";
                        else if(i == goal.indices.size()-1)
                            duplicateErrorMsg+=".";
                        else{
                            duplicateErrorMsg+=", ";
                            if(i == goal.indices.size()-2)
                                duplicateErrorMsg+="and ";
                        }
                    }
                    
                    duplicateErrorMsg+=System.lineSeparator();
                    overallPass = false;
                } 
                
                if(goal.isResultTagBoolean){
                   duplicateErrorMsg+= "Goal ID: \"" + goal.goalID + "\" is already a results boolean."; 
                   duplicateErrorMsg+=System.lineSeparator();
                   overallPass = false;
                }
            
            
            }
            errorMsg+=duplicateErrorMsg;  
        }
        
        //Stores a goalID's name and the row index they appear on and also if they appear as a result boolean
        class GoalIDIndices{
            protected String goalID;
            protected boolean isResultTagBoolean;
            protected List<Integer> indices;
                    
            GoalIDIndices(String goalID, int index){
                this.goalID = goalID;
                indices = new ArrayList<>();
                indices.add(index);
                isResultTagBoolean = false;
            }
            
            void addIndex(int index){
                indices.add(index);
            }
        }
        
        //Is the goal ID already in the duplicate list?
        boolean isDuplicate(List<GoalIDIndices> goalIDSet, String goalID){
            for(GoalIDIndices goalIndices : goalIDSet){
                if(goalIndices.goalID.equals(goalID))
                    return true;
            }
            return false;
        }
        
        //Get the duplicate object based on the duplicate string
        GoalIDIndices getDuplicate(List<GoalIDIndices> goalIDSet, String goalID){
            for(GoalIDIndices goalIndices : goalIDSet){
                if(goalIndices.goalID.equals(goalID))
                    return goalIndices;
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
    //Gets a list of GoalValues from the the current state of the goals.config file
    protected ArrayList<GoalValues> getGoalValuesOfConfigFile(){
        ArrayList<GoalValues> officialListofGoals = new ArrayList<>();

        ArrayList<String> goalLines = getGoalLines();
        if(goalLines != null){
            for(String goalLine : goalLines){
                GoalValues values = new GoalValues(goalLine, resultTagList);
                officialListofGoals.add(values);
            } 
            return officialListofGoals;
        }
        else
            return null;
    }
    
    //Get the list of goal lines from the goals.config that need to be parsed
    private ArrayList<String> getGoalLines(){
        ArrayList<String> goals = new ArrayList<>();
        
        try {
            String userHomeFolder = System.getProperty("user.home");
            File lab = new File(userHomeFolder + File.separator + "labtainer" + File.separator + "trunk" + File.separator + "labs" + File.separator+ labname);
            File goalsConfig = new File(lab+"/instr_config/goals.config");

            //Get the artifact lines
            if(goalsConfig.exists()){
                try (FileReader fileReader = new FileReader(goalsConfig)) {
                    BufferedReader bufferedReader = new BufferedReader(fileReader); 
                    
                    String line = bufferedReader.readLine();                    
                    while (line != null) {                 
                        //just checks if the first character is: not empty, not a hash, and not whitspace)
                        if(!line.isEmpty() && line.charAt(0) != '#' && !Character.isWhitespace(line.charAt(0)))
                            goals.add(line);

                        line = bufferedReader.readLine();
                    }   
                }
                return goals;
            }
            else{
                System.out.println("No goals.config file in the loaded lab!");
                return null;
            }
        } 
        catch (IOException e) {
            System.out.println("Issue with getting goals.config goals");
            return null;
        }     
    }
    
    
    //Updates the list of goals
    protected void updateListofGoals(JPanel PanelofGoals){
        Component[] goals = PanelofGoals.getComponents(); //Access the list of goals
                
        ArrayList<GoalValues> listofGoalsTMP = new ArrayList<>();
        
        //Iterate through each goal panel in the UI and add its values to the temp list of goal values
        for (Component goal : goals) {
            //Goal ID
            String goalID = ((GoalPanels) goal).getGoalIDTextField().getText();
            //GoalType
            ToolTipWrapper goalType = (ToolTipWrapper)((GoalPanels) goal).getGoalTypeComboBox().getSelectedItem();
            
            
            //Operator
            ToolTipWrapper operator = (ToolTipWrapper)((GoalPanels) goal).getOperatorComboBox().getSelectedItem();
            String resultTag = "";
            if(goalType.equals(GoalType_ITEMS[12])){ //matchExpression              
                resultTag = ((GoalPanels) goal).getArithmeticResultTagTextField().getText();
            }
            else{
                //Result Tag
                resultTag = (String)((GoalPanels) goal).getResultTagComboBox().getSelectedItem();
            }
            //Answer Type
            String answerType = (String)((GoalPanels) goal).getAnswerTypeComboBox().getSelectedItem();
            //Answer Tag
            String answerTag = "";
            if(answerType.equals(answerTypes[0])) //Literal
                answerTag = ((GoalPanels) goal).getAnswerTagTextField().getText();
            else if(answerType.equals(answerTypes[1])) //Result Tag
                answerTag = (String)(((GoalPanels) goal).getResultTag2ComboBox().getSelectedItem());            
            else if(answerType.equals(answerTypes[2]) || answerType.equals(answerTypes[3])) //Parameter and Parameter ASCII
                answerTag = (String)(((GoalPanels) goal).getParameterComboBox().getSelectedItem()); 

            
            
            //Boolean Expression
            String booleanExp = ((GoalPanels) goal).getBooleanTextField().getText();
            
            
            //Goal 1
            String goal1 = ((GoalPanels) goal).getGoal1TextField().getText();
            //Goal 2
            String goal2 = ((GoalPanels) goal).getGoal2TextField().getText();
            
            
            //Value
            String value = ((GoalPanels) goal).getValueTextField().getText();
            //Subgoal List
            String subgoalList = ((GoalPanels) goal).getSubgoalTextField().getText();
            
            
            //Executable File
            String executableFile = ((GoalPanels) goal).getExecutableFileTextField().getText();

            listofGoalsTMP.add(new GoalValues(goalID, goalType, operator, resultTag, answerType, answerTag, booleanExp, goal1, goal2, value, subgoalList, executableFile));
       }
       listofGoals = listofGoalsTMP; //overwrite the old listofGoals with the temp listofGoals
    }
     
    //Swaps goal order in the list of goals and then redraws them
    protected void swapGoals(String type, int rowIndex){
        switch(type){
            case "UP":
                if(rowIndex > 0){
                    //System.out.println("UP: "+listofGoals.get(rowIndex).resultTag+" Index: "+rowIndex);
                    Collections.swap(listofGoals, rowIndex, rowIndex-1);
                }
                break;
            case "DOWN":
                if(rowIndex < rowCount-1){
                    //System.out.println("DOWN: "+listofGoals.get(rowIndex).resultTag);
                    Collections.swap(listofGoals, rowIndex, rowIndex+1);
                }
                break;
            default:
                System.out.println("swap case not registered");
        }
    }
     
        
    //Compares the data of two lists of ArtifactValues. If there is a difference then return 'true', 'false' otherwise
    static boolean goalValuesDiffer(List<GoalValues> list1, List<GoalValues> list2){
        if(list1 == null || list2 == null || list1.size() != list2.size()) 
            return true;
        else{
            //This is a gross implemenation of copmaring each individual value between two sets of Goal Values (Maybe conisder implementing the GoalValues Class as a comparable)
            for(int i=0;i<list1.size();i++){
                goalValuesDifferDEBUG(list1, list2, i);    
                               
                if(!list1.get(i).goalID.equals(list2.get(i).goalID))
                    return true;
                else if(!list1.get(i).goalType.equals(list2.get(i).goalType))
                    return true;
                else if(!list1.get(i).operator.equals(list2.get(i).operator))
                    return true;
                else if(!list1.get(i).resultTag.equals(list2.get(i).resultTag))
                    return true;
                else if(!list1.get(i).answerType.equals(list2.get(i).answerType))
                    return true;
                else if(!list1.get(i).answerTag.equals(list2.get(i).answerTag))
                    return true;
                else if(!list1.get(i).booleanExp.equals(list2.get(i).booleanExp))
                    return true;
                else if(!list1.get(i).goal1.equals(list2.get(i).goal1))
                    return true;
                else if(!list1.get(i).goal2.equals(list2.get(i).goal2))
                    return true;
                else if(!list1.get(i).value.equals(list2.get(i).value))
                    return true;
                else if(!list1.get(i).subgoalList.equals(list2.get(i).subgoalList))
                    return true;
                else if(!list1.get(i).executableFile.equals(list2.get(i).executableFile))
                    return true;
            }
        }
        return false;
    }
       
    //Gets a list of the goal IDs before a certain row
    private ArrayList<String> getAboveGoals(String type, int rowIndex, Component[] goals){
        ArrayList<String> aboveGoals = new ArrayList<>();
        for(int i=0;i<rowIndex;i++){
            ToolTipHandlers.ToolTipWrapper goalTypeTTW = (ToolTipWrapper)(((GoalPanels)goals[i]).getGoalTypeComboBox().getSelectedItem());
            String goalType = goalTypeTTW.getItem();
            
            String goalID = ((GoalPanels)goals[i]).getGoalIDTextField().getText();
            
            switch(type){
                case "ALL": 
                    aboveGoals.add(goalID);
                    break;
                case "GOAL1&2": //Only matchany and boolean
                    if(goalType.equals("matchany") || goalType.equals("boolean"))
                        aboveGoals.add(goalID);
                    break;
                case "BOOLEAN": //Non Match across
                    if(!goalType.equals("matchacross"))
                        aboveGoals.add(goalID);
                    break;
                default:
                    System.out.println("GetAboveGoals type is invalid");      
            }   
        }
        return aboveGoals;
    }
    
    //Resets the list of goals and the row count
    protected void resetData(){
        listofGoals = new ArrayList<>(); 
        rowCount = listofGoals.size();
    }
    
//RowCount setters    
    void increaseRowCount(){
        rowCount++;
    }
    
    void decreaseRowCount(){
        rowCount--;
    }
    
//Getters
    boolean isLoaded(){
        return labloaded;
    }
    
    int getRowCount(){
        return rowCount;
    }
    
    List<GoalValues> getListofGoals(){
        return listofGoals;
    }
    
    List<String> getResultTagList(){
        return resultTagList;
    }
    
    List<String> getParameters(){
        return parameters;
    }
    
    List<String> getBooleanResults(){
        return booleanResults;
    }
    
//Debug
    static private void goalValuesDifferDEBUG(List<GoalValues> list1, List<GoalValues> list2, int i){
        System.out.println("GOAL: "+i);
                System.out.println();
                System.out.println("Goal ID");
                System.out.println(list1.get(i).goalID + " : " + list2.get(i).goalID);
                System.out.println();
                System.out.println("Goal Type");
                System.out.println(list1.get(i).goalType + " : " + list2.get(i).goalType);
                System.out.println();
                System.out.println("Opertor");
                System.out.println(list1.get(i).operator + " : " + list2.get(i).operator);
                System.out.println();
                System.out.println("Result Tag");
                System.out.println(list1.get(i).resultTag + " : " + list2.get(i).resultTag);
                System.out.println();
                System.out.println("Answer Tag");
                System.out.println(list1.get(i).answerTag + " : " + list2.get(i).answerTag);
                System.out.println();
                System.out.println("Boolean Expression");
                System.out.println(list1.get(i).booleanExp + " : " + list2.get(i).booleanExp);
                System.out.println();
                System.out.println("Goal 1");
                System.out.println(list1.get(i).goal1 + " : " + list2.get(i).goal1);
                System.out.println();
                System.out.println("Goal 2");
                System.out.println(list1.get(i).goal2 + " : " + list2.get(i).goal2);
                System.out.println();
                System.out.println("Value");
                System.out.println(list1.get(i).value + " : " + list2.get(i).value);
                System.out.println();
                System.out.println("Subgoal List");
                System.out.println(list1.get(i).subgoalList + " : " + list2.get(i).subgoalList);
                System.out.println();
                System.out.println("Goal ID");
                System.out.println(list1.get(i).executableFile + " : " + list2.get(i).executableFile);
    }
    
}
