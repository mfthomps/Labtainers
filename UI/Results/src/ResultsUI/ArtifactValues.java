/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ResultsUI;

import static ResultsUI.ParamReferenceStorage.FieldType_ITEMS;
import static ResultsUI.ParamReferenceStorage.LineType_ITEMS;
import static ResultsUI.ParamReferenceStorage.SpecialTimeStampType;
import static ResultsUI.ParamReferenceStorage.TimestampType_ITEMS;
import static ResultsUI.ParamReferenceStorage.justFieldType;
import static ResultsUI.ParamReferenceStorage.lineParamAccessible;

/**
 *
 * @author Dan
 */

/* 
Errors that need to be fixed/Notes to consider: 
****The param parsing in this class is critically dependent to where the param value's corresponding index is on the artifact line. 
    If at any point this alignment is modified with less or more params, this code will need to be revised

****If the Line ID or the Field ID input contains a " : " in it, then the code will add everything after the " : " to the "line ID, or field ID".
    For the Field ID, it adds all the " : " parsed values after the field type, until it hits a Line Type(excludes the line type value)

****Currently this code will allow/read weird inputs like "CONTAINS : LINE : STUFF" in field ID or Line ID (which breaks the parsing)
*/
public class ArtifactValues {
    //Values to be obtained
        String resultTag, container, fileID, fieldID, lineID, timeStampDelimiter;
        
        ToolTipHandlers.ToolTipWrapper fieldType, lineType, timeStampType;
        
        //Stores the values of an arifactline fed into it (NO real value validation happening here)
        ArtifactValues(String artifactLine){
            resultTag = container = fileID = fieldID = lineID = timeStampDelimiter = "";
            
            fieldType = lineType = timeStampType = null;
            
          //Parsing the artifactline 
            String[] paramParsedLine = artifactLine.split(" : ");

            //Get the resultTag
            resultTag = paramParsedLine[0].split(" = ")[0];

            //Get the container, fieldID, timeStampType, and timeStampDelimiter
            handleFileRef(paramParsedLine[0].split(" = ")[1]);

          //Get Field Type and Field ID (and the lineType and lineID depending on if the field type allows it):

            //Case where "TOKEN" field Type is not explicitly stated and the paramParsedLine index is off by 1 for fieldID, lineType, lineID
            if(paramParsedLine[1].equals("ALL") || paramParsedLine[1].equals("LAST") || isInteger(paramParsedLine[1])){
                fieldType = FieldType_ITEMS[0]; //TOKEN
                fieldID = paramParsedLine[1];

                /*
                If the paramParsedLine isn't just the fileID and the fieldID (note fieldType is assumed to be "Token"),
                then that means we need to consider the other parms which are certainly* line type and line ID.
                *if the user enters a bad config file this may cause an error.
                */
                if(paramParsedLine.length > 2){
                    lineType = itemFinder(LineType_ITEMS, paramParsedLine[2]);
                    lineID = paramParsedLine[3];
                }
                else{
                    lineType = LineType_ITEMS[0]; //NONE
                    lineID ="";
                }
            }
            
            //Case where the field type IS EXPLICITY stated
            else{
                fieldType = itemFinder(FieldType_ITEMS, paramParsedLine[1]);
                //If the field type is null after looking through the field type items, then it may be under the SpecialTimeStampType array
                if(fieldType == null)
                    fieldType = itemFinder(SpecialTimeStampType, paramParsedLine[1]);
                
                //Does the field type consider other fields, if so then continue parsing for these values
                if(!justFieldType.contains(fieldType.getItem())){
                    //If the field Type doesn't bother with line Params then execute these details
                    if(!lineParamAccessible.contains(fieldType.getItem())){
                        //Everything after the field type is considered the field ID (this ensures that the fieldID potentially split by " : " will all be captured and stored)
                        fieldID = artifactLine.split(fieldType + " : ")[1];

                        //If the fieldType is equal "FILE_REGEX_TS", then overwrite the fieldType to be "FILE_REGEX" and make the timeStampType to be "LOG_TS"
                        //If the fieldType is equal "LOG_TS", then overwrite the fieldType to be "CONTAINS" and make the timeStampType to be "LOG_TS"
                        //If the fieldType is equal "LOG_RANGE", then overwrite the fieldType to be "CONTAINS" and make the timeStampType to be "LOG_RANGE"
                        switch (fieldType.getItem()) {
                            case "FILE_REGEX_TS":
                                fieldType = FieldType_ITEMS[7]; //FILE REGEX
                                timeStampType = SpecialTimeStampType[0]; //LOG_TS
                                break;
                            case "LOG_TS":
                                fieldType = FieldType_ITEMS[6]; //CONTAINS
                                timeStampType = SpecialTimeStampType[0]; // LOG_TS
                                break;
                            case "LOG_RANGE":
                                fieldType = FieldType_ITEMS[6]; //CONTAINS
                                timeStampType = SpecialTimeStampType[1]; //LOG_RANGE
                                break;
                            default:
                                break;
                        }
                        
                         lineType = LineType_ITEMS[0]; //NONE
                         lineID = "";
                    }
                    //If the field Type does bother with line Params then execute these details
                    else{
                        int properLineTypeIndex = 3; //This value may be changed if user's field ID includes " : ", offsetting the parsing indexes
                       
                        /*The Field ID may include " : ". But since the line parsing breaks the line up based on " : ", 
                        the for block below makes sure to the include the pieces that were broken up                     
                        */
                        for(int i=2; i<paramParsedLine.length && !itemExistCheck(LineType_ITEMS,paramParsedLine[i]); i++){
                            fieldID+=paramParsedLine[i];
                            if(i<(paramParsedLine.length-1) && !itemExistCheck(LineType_ITEMS,paramParsedLine[i+1])){
                                properLineTypeIndex++;                                
                                fieldID+=" : ";
                            }
                        }
                              
                        //If properLineTypeIndex < paramParsedLine.length then that means the line type and line id was written in the config file 
                        if(properLineTypeIndex < paramParsedLine.length){
                            lineType = itemFinder(LineType_ITEMS, paramParsedLine[properLineTypeIndex]);
                            //If line type is null after searching though the LineType_ITEMS then the value could possibly be a special line type
                            if(lineType == null)
                                lineType = itemFinder(SpecialTimeStampType, paramParsedLine[properLineTypeIndex]);

                            //Special LineType cases
                            if((lineType.getItem()).equals("HAVESTRING_TS")){
                                lineType = LineType_ITEMS[3]; //HAVESTRING
                                timeStampType = SpecialTimeStampType[0]; //LOG_TS
                            }
                            else if((lineType.getItem()).equals("REGEX_TS")){
                                lineType = LineType_ITEMS[4]; //REGEX
                                timeStampType = SpecialTimeStampType[0]; //LOG_TS
                            }
                            
                            
                            //accomplishes the same thing in the for-block below but more simply (Gets everything after the lineType as the lineID)
                            lineID = artifactLine.split(lineType.getItem() + " : ")[1];
                            
                            
                            /*The Line ID may include " : ". since the line parsing breaks the line up based on " : ", 
                            the for block below makes sure to the include the pieces that were broken up                     
                            */
                            /*
                            for(int i=properLineTypeIndex+1; i<paramParsedLine.length; i++){
                                lineID+=paramParsedLine[i];
                                if(i<(paramParsedLine.length-1)){                           
                                    lineID+=" : ";
                                }
                            }
                            */
                        }
                        else{
                            lineType = LineType_ITEMS[0]; //NONE
                            lineID = "";
                        }
                    }
                }
                else{
                    fieldID = "";
                    lineType = LineType_ITEMS[0]; //NONE
                    lineID = "";
                    timeStampType = TimestampType_ITEMS[0]; //File
                }
            }
        }
      
        //Constructor for temporarily storing values of artifacts in the UI
        ArtifactValues(String resultTag, String container, String fileID, ToolTipHandlers.ToolTipWrapper fieldType, String fieldID, ToolTipHandlers.ToolTipWrapper lineType, String lineID, ToolTipHandlers.ToolTipWrapper timeStampType, String timeStampDelimiter){
            this.resultTag = resultTag; 
            this.container = container;
            this.fileID = fileID; 
            this.fieldType = fieldType;
            this.fieldID = fieldID;
            this.lineType = lineType;
            this.lineID = lineID;
            this.timeStampType = timeStampType;
            this.timeStampDelimiter = timeStampDelimiter;
        }
        
        private void handleFileRef(String fileRef){
            //Case 1: <prog>.[stdin | stdout | prgout] or file_path
            if(!fileRef.contains(":")){
                container = "ALL";
                fileID = fileRef;
                timeStampType = TimestampType_ITEMS[0]; //File
            }
            //Case 2: [container_name:]<prog>.[stdin | stdout | prguot]
            else if(fileRef.contains(":") && !fileRef.contains("/")){
                container = fileRef.split(":")[0];
                fileID = fileRef.split(":")[1];
                timeStampType = TimestampType_ITEMS[0]; //File
            } 
            else{
                String[] parsedFileRef = fileRef.split(":");

                if(parsedFileRef.length == 2){
                    //Case 3: [container_name:]file_path
                   if(fileRef.indexOf(":") < fileRef.indexOf('/')){
                       container = parsedFileRef[0];
                       fileID = parsedFileRef[1];
                       timeStampType = TimestampType_ITEMS[0]; //File
                   }
                   //Case 4: file_path[:time_delimiter]
                   else{
                       fileID = parsedFileRef[0];
                       //Set the timeStamp Type either to be "Service" or "Program"
                       if(parsedFileRef[1].contains(".service")){
                           timeStampType = TimestampType_ITEMS[1]; //Service
                           timeStampDelimiter = parsedFileRef[1].replace(".service", "");
                       }
                       else{
                           timeStampType = TimestampType_ITEMS[2]; //Program
                           timeStampDelimiter = parsedFileRef[1];
                       }
                   }
                }
                //Case 5: [container_name:]file_path[:time_delimiter]
                else {
                    container = parsedFileRef[0];
                    fileID = parsedFileRef[1];
                    if(parsedFileRef[2].contains(".service")){
                        timeStampType = TimestampType_ITEMS[1]; //Serivce
                        timeStampDelimiter = parsedFileRef[2].replace(".service", "");
                    }
                    else{
                        timeStampType = TimestampType_ITEMS[2]; //Program
                        timeStampDelimiter = parsedFileRef[2];
                    }
                }
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
       
        private boolean itemExistCheck(ToolTipHandlers.ToolTipWrapper[] list,String desired){
            for(ToolTipHandlers.ToolTipWrapper item : list){
               if(item.getItem().equals(desired)){
                   return true;
               }
            }
            return false;
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
