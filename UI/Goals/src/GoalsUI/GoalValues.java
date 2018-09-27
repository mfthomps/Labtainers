/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GoalsUI;

import static GoalsUI.ParamReferenceStorage.GoalType_ITEMS;
import static GoalsUI.ParamReferenceStorage.Operator_ITEMS;
import static GoalsUI.ParamReferenceStorage.answerTypes;
import static GoalsUI.ParamReferenceStorage.goalInput;
import static GoalsUI.ParamReferenceStorage.opInput;
import static GoalsUI.ParamReferenceStorage.resultTagInput;
import java.util.List;


/**
 *
 * @author Dan
 */

//****The param parsing in this class is limited to where the param value's corresponding index is on the goal line. 
    //If at any point this alignment is modified with less or more params, this code will need to be revised
public class GoalValues {
    //Values to be obtained
        String goalID, resultTag, answerTag, answerType, booleanExp, goal1, goal2, value, subgoalList, executableFile;
        
        ToolTipHandlers.ToolTipWrapper goalType, operator;
        
        //Constructor for loading goals into the UI
        GoalValues(String goalLine, List<String> resultTags){
            goalID = resultTag = answerType = answerTag = booleanExp = goal1 = goal2 = value = subgoalList = executableFile = "";          
            goalType = null;     
            operator = Operator_ITEMS[0];
            //by default set the result tag to the first result tag in the resultTags list (Warning: an error will occur if there is nothing the results tags list)
            resultTag = resultTags.get(0); 
            answerType = answerTypes[0];
            
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
        GoalValues(String goalID, ToolTipHandlers.ToolTipWrapper goalType, ToolTipHandlers.ToolTipWrapper operator, String resultTag, String answerType, String answerTag, String booleanExp, String goal1, String goal2, String value, String subgoalList, String executableFile){  
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
        }
        
        //set the answertype & answertag to be displayed on the gui based on the config's answer tag
        private void answerTagModifier(String aT, List<String> resultTags){
                if(aT.contains("answer=")){
                    answerTag = aT.split("answer=")[1];
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
