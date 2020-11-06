/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
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
        
        String operator;
        
        //Stores the values of an parameter fed into it (NO real value validation happening here)
        ParamValues(String paramLine){
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
            if(operator == "HASH_CREATE"){
                hashedString = paramParsedLine[3];
            }else if(operator == "HASH_REPLACE"){
                hashedString = paramParsedLine[4];
            }
        }
      
        //Constructor for temporarily storing values of artifacts in the UI
        ParamValues(String paramID, String container, String fileID, String operator, 
                     String symbol, String hashedString,
                     String lowerBound, String upperBound){
            this.paramID = paramID; 
            this.container = container; 
            this.fileID = fileID; 
            this.operator = operator; 
            this.symbol = symbol; 
            this.hashedString = hashedString; 
            this.lowerBound = lowerBound; 
            this.upperBound = upperBound; 
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
