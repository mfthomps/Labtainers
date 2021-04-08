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
package labtainers.goalsui;

import java.util.List;
import static labtainers.goalsui.ParamReferenceStorage.GoalType_ITEMS;
import static labtainers.goalsui.ParamReferenceStorage.Operator_ITEMS;
import static labtainers.goalsui.ParamReferenceStorage.answerTypes;
import static labtainers.goalsui.ParamReferenceStorage.goalInput;
import static labtainers.goalsui.ParamReferenceStorage.opInput;
import static labtainers.goalsui.ParamReferenceStorage.resultTagInput;
import labtainers.mainui.ToolTipHandlers;

/**
 *
 * @author Daniel Liao
 */
public class GoalValues {
    //Values to be obtained
        String goalID, resultTag, answerTag, answerType, booleanExp, goal1, goal2, value, subgoalList, executableFile, comments;
        
        ToolTipHandlers.ToolTipWrapper goalType, operator;
        
        //Constructor for loading goals into the UI
        GoalValues(String inputLine, List<String> resultTags){
            goalID = resultTag = answerType = answerTag = booleanExp = goal1 = goal2 = value = subgoalList = executableFile = comments = "";          
            goalType = null;     
            operator = Operator_ITEMS[0];
            //by default set the result tag to the first result tag in the resultTags list (Warning: an error will occur if there is nothing the results tags list)
            resultTag = resultTags.get(0); 
            answerType = answerTypes[0];
            
            String goalLine;
            if(inputLine.contains("\n")){
                String[] the_lines = inputLine.split("\n");
                goalLine = the_lines[the_lines.length-1];
                for(int i=0; i<the_lines.length-1; i++){
                    comments = comments+the_lines[i]+"\n";
                }
            }else{
                goalLine = inputLine; 
            }
            String[] paramParsedLine = goalLine.split(" : ");
            
            //Get goal ID
            goalID = paramParsedLine[0].split(" = ")[0].trim();
            
            //System.out.println(paramParsedLine[0].split(" = ")[1]);
            
            
            
            //Get goal type
            if(paramParsedLine[0].split(" = ")[1].trim().equals("count")){
                if(paramParsedLine.length > 2)
                   goalType = GoalType_ITEMS[10]; //count_matches
                else
                    goalType = GoalType_ITEMS[9]; //count_value
            }
            else
                goalType = itemFinder(GoalType_ITEMS, paramParsedLine[0].split(" = ")[1].trim()); 
            
            if(opInput.contains(goalType.getItem())){
                operator = itemFinder(Operator_ITEMS, paramParsedLine[1]);
                if(operator == null){
                    System.out.println("Operator unknown in "+inputLine);
                }
                resultTag = paramParsedLine[2];
                
                //Overwrite the goaltype to "matchExpression" if the result tag has a parenthesis (this indicates an arithmetic expression)
                if(resultTag.contains("(")){
                    goalType = GoalType_ITEMS[12];
                    //take out outer parens in resultTag
                    if(resultTag.startsWith("(") && resultTag.endsWith(")")) 
                        resultTag = resultTag.substring(1, resultTag.length() -1);
                }

                answerTagModifier(paramParsedLine[3], resultTags);
            }
            else if(goalInput.contains(goalType.getItem())){
                goal1 = paramParsedLine[1].trim();
                goal2 = paramParsedLine[2].trim();
            }
            else if(resultTagInput.contains(goalType.getItem())){
                resultTag = paramParsedLine[1].trim();
            }
            else if("boolean".equals(goalType.getItem())){
                booleanExp = paramParsedLine[1];
            }
            else if("count_greater".equals(goalType.getItem())){
                value = paramParsedLine[1].trim();
                subgoalList = paramParsedLine[2].trim();
                //Chop off the surrounding parens since this will be readded when written
                if(subgoalList.startsWith("(") && subgoalList.endsWith(")"))
                    subgoalList = subgoalList.substring(1, subgoalList.length() -1);
            }
            else if("execute".equals(goalType.getItem())){
                executableFile = paramParsedLine[1];
                resultTag = paramParsedLine[2];
                answerTagModifier(paramParsedLine[3], resultTags);
            }
            else
                System.out.println("Goal Type doesn't match any");
        }
      
        //Constructor for temporarily storing values of artifacts in the UI
        GoalValues(String goalID, ToolTipHandlers.ToolTipWrapper goalType, ToolTipHandlers.ToolTipWrapper operator, String resultTag, String answerType, String answerTag, String booleanExp, String goal1, String goal2, String value, String subgoalList, String executableFile, String comments){  
            this.goalID = goalID;
            this.goalType = goalType;
            this.operator = operator;
            this.resultTag = resultTag;
            this.answerType = answerType;
            this.answerTag = answerTag;
            this.booleanExp = booleanExp;
            this.goal1 = goal1;
            this.goal2 = goal2;
            this.value = value;
            this.subgoalList = subgoalList;
            this.executableFile = executableFile;
            this.comments = comments;
        }
        
        //Deep copy
        GoalValues(GoalValues original){
            goalID = original.goalID;
            goalType = original.goalType;
            operator = original.operator;
            resultTag = original.resultTag;
            answerTag = original.answerTag;
            answerType = original.answerType;
            booleanExp = original.booleanExp;
            goal1 = original.goal1;
            goal2 = original.goal2;
            value = original.value;
            subgoalList = original.subgoalList;
            executableFile = original.executableFile;
            comments = original.comments;
        }
        
        //set the answertype & answertag to be displayed on the gui based on the config's answer tag
        private void answerTagModifier(String aT, List<String> resultTags){
            answerTag = "";
            try{
                if(aT.contains("answer=")){
                    answerTag = aT.split("answer=")[1];
                    //System.out.println("answer tag set to "+answerTag);
                }
                else if(resultTags.contains(aT)){
                    answerTag = aT;
                    answerType = answerTypes[1]; //Result Tags
                }  
                else if(aT.contains("result.")){
                    answerTag = aT.split("result.")[1];
                    answerType = answerTypes[1]; //Result Tags
                }
                else if(aT.contains("parameter.")){
                    answerTag = aT.split("parameter.")[1];
                    answerType = answerTypes[2]; //Parameter
                }
                else if(aT.contains("parameter_ascii.")){
                    answerTag = aT.split("parameter_ascii.")[1];
                    answerType = answerTypes[3]; //Parameter_ASCII
                }
            }catch(java.lang.ArrayIndexOutOfBoundsException ex){ 
                System.out.println("Error in goal value "+aT); 
            }
        }
        
        
        private ToolTipHandlers.ToolTipWrapper itemFinder(ToolTipHandlers.ToolTipWrapper[] list,String desired){
            for(ToolTipHandlers.ToolTipWrapper item : list){
               if(item.getItem().equals(desired)){
                   return item;
               }
            }
            return null;
        }
       
        private boolean isInteger(String s){
           try{
               Integer.parseInt(s);
               
               return true;
           }
           catch(NumberFormatException ex){
               return false;
           }
       }
}
