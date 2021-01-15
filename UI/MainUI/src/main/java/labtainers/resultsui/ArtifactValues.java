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
package labtainers.resultsui;
import java.util.Arrays;
import labtainers.mainui.ToolTipHandlers;
import static labtainers.resultsui.ParamReferenceStorage.FieldType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.LineType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.SpecialTimeStampType;
import static labtainers.resultsui.ParamReferenceStorage.TimestampType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.justFieldType;
import static labtainers.resultsui.ParamReferenceStorage.lineParamAccessible;

/**
 *
 * @author Daniel Liao
 */
public class ArtifactValues {
    //Values to be obtained
        String resultTag, container, fileID, fieldID, lineID, timeStampDelimiter;
        String comments = "";
        
        ToolTipHandlers.ToolTipWrapper fieldType, lineType, timeStampType;
        
        //Stores the values of an arifactline fed into it (NO real value validation happening here)
        ArtifactValues(String inputLine){
            String artifactLine;
            if(inputLine.contains("\n")){
                String[] the_lines = inputLine.split("\n");
                artifactLine = the_lines[the_lines.length-1];
                for(int i=0; i<the_lines.length-1; i++){
                    comments = comments+the_lines[i]+"\n";
                }
            }else{
                artifactLine = inputLine; 
            }
            resultTag = container = fileID = fieldID = lineID = timeStampDelimiter = "";
            
            fieldType = lineType = timeStampType = null;
            
          //Parsing the artifactline 
            String[] paramParsedLine = artifactLine.split(" : ");
            Arrays.stream(paramParsedLine).map(String::trim).toArray(unused -> paramParsedLine);

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
                if(fieldType == null){
                    System.out.println("could not get field type for "+paramParsedLine[1]);
                    return;
                }
                
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
                            case "RANGE_REGEX":
                                fieldType = FieldType_ITEMS[7]; //FILE_REGEX
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
        ArtifactValues(String resultTag, String container, String fileID, ToolTipHandlers.ToolTipWrapper fieldType, String fieldID, ToolTipHandlers.ToolTipWrapper lineType, String lineID, ToolTipHandlers.ToolTipWrapper timeStampType, String timeStampDelimiter, String comments){
            this.resultTag = resultTag; 
            this.container = container;
            this.fileID = fileID; 
            this.fieldType = fieldType;
            this.fieldID = fieldID;
            this.lineType = lineType;
            this.lineID = lineID;
            this.timeStampType = timeStampType;
            this.timeStampDelimiter = timeStampDelimiter;
            this.comments = comments;
        }
        
        //Clones the original Artifact Values
        ArtifactValues(ArtifactValues original){
            this.resultTag =  original.resultTag; 
            this.container = original.container;
            this.fileID = original.fileID; 
            this.fieldType = original.fieldType;
            this.fieldID = original.fieldID;
            this.lineType = original.lineType;
            this.lineID = original.lineID;
            this.timeStampType = original.timeStampType;
            this.timeStampDelimiter = original.timeStampDelimiter;
            this.comments = original.comments;
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
                   }
                }
                //Case 5: [container_name:]file_path[:time_delimiter]
                else {
                    container = parsedFileRef[0];
                    fileID = parsedFileRef[1];
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
