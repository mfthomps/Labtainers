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
package labtainers.paramsui;
import labtainers.mainui.ToolTipHandlers;
import static labtainers.resultsui.ParamReferenceStorage.FieldType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.LineType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.SpecialTimeStampType;
import static labtainers.resultsui.ParamReferenceStorage.TimestampType_ITEMS;
import static labtainers.resultsui.ParamReferenceStorage.justFieldType;
import static labtainers.resultsui.ParamReferenceStorage.lineParamAccessible;

/**
 *
 * @author MFT
 */
public class ParamValues {
    //Values to be obtained
        String paramID, container, fileID, symbol, hashedString;
        String upperBound, lowerBound;
        String comments = "";
        String operator;
        
        //Stores the values of an parameter fed into it (NO real value validation happening here)
        ParamValues(String inputLine){
            String paramLine;
            if(inputLine.contains("\n")){
                String[] the_lines = inputLine.split("\n");
                paramLine = the_lines[the_lines.length-1];
                for(int i=0; i<the_lines.length-1; i++){
                    comments = comments+the_lines[i]+"\n";
                }
            }else{
                paramLine = inputLine; 
            }
            String operator_string;
            paramID = container= fileID = symbol = hashedString = "";
            upperBound = lowerBound = "0"; 
            operator = null;
            
          //Parsing the paramLine 
            String[] paramParsedLine = paramLine.split(" : ");

            paramID = paramParsedLine[0];
            operator_string = paramParsedLine[1];
            //operator = itemFinder(Operator_ITEMS, operator_string);
            operator = operator_string;
            fileID = paramParsedLine[2];
            if(fileID.contains(":")){
                String[] parts = fileID.split(":");
                fileID = parts[1];
                container = parts[0];
            }
            if(operator_string.contains("REPLACE")){
                symbol = paramParsedLine[3];
                if(operator_string.contains("RAND")){
                    lowerBound = paramParsedLine[4];
                    upperBound = paramParsedLine[5];
                }
            }
            if(operator.equals("HASH_CREATE")){
                hashedString = paramParsedLine[3];
            }else if(operator.equals("HASH_REPLACE")){
                hashedString = paramParsedLine[4];
            }
        }
      
        //Constructor for temporarily storing values of artifacts in the UI
        ParamValues(String paramID, String container, String fileID, String operator, 
                     String symbol, String hashedString,
                     String lowerBound, String upperBound, String comments){
            this.paramID = paramID; 
            this.container = container; 
            this.fileID = fileID; 
            this.operator = operator; 
            this.symbol = symbol; 
            this.hashedString = hashedString; 
            this.lowerBound = lowerBound; 
            this.upperBound = upperBound; 
            this.comments = comments; 
        }
        
        //Clones the original Params Values
        ParamValues(ParamValues original){
            this.paramID = original.paramID; 
            this.container = original.container; 
            this.fileID = original.fileID; 
            this.operator = original.operator; 
            this.symbol = original.symbol; 
            this.hashedString = original.hashedString; 
            this.lowerBound = original.lowerBound; 
            this.upperBound = original.upperBound; 
            this.comments = original.comments; 
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
