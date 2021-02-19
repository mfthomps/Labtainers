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
import java.io.FileReader;
import java.io.IOException;
 
public class CompareTextFiles
{	
    private static boolean plainComment(String line){
        boolean retval = false;
        if(line.trim().startsWith("#") && !line.contains("DOC:")){
            retval = true;
        }
        return retval;
    }
    private static String nextLine(BufferedReader br) throws IOException{
        String line = br.readLine();
        //System.out.println("nextLine line: "+line);
        // when did java lose its evaluation precidence?
        if(line != null){
            line = line.trim().replaceAll(" +", " "); 
            while(line != null && (plainComment(line) || line.trim().length() == 0)){
                line = br.readLine();
                if(line == null)
                    break;
                line = line.trim().replaceAll(" +", " "); 
            }
        }
        return line;
    }
    public static boolean compare(String path1, String path2) throws IOException
    {	
        if(path1 == null || path2 == null){
            return false;
        }
        BufferedReader reader1 = new BufferedReader(new FileReader(path1));
        BufferedReader reader2 = new BufferedReader(new FileReader(path2));
        String line1 = nextLine(reader1);
        String line2 = nextLine(reader2);
        boolean areEqual = true;
        int lineNum = 1;
         
        while (line1 != null || line2 != null)
        {
            if((line1 == null && line2.trim().length()>0) || (line2 == null && line1.trim().length()>0))
            {
                areEqual = false;
                break;
            }
            else if((line1 != null && line2 != null) && (! line1.trim().equalsIgnoreCase(line2.trim())))
            {
                    /*
                    System.out.println("DIFFERENT");
                    System.out.println("\t"+line1);
                    System.out.println("\t"+line2);
                    */
                    areEqual = false;
                    break;
            }
            line1 = nextLine(reader1);
            line2 = nextLine(reader2);
            lineNum++;
        }
         
        if(areEqual)
        {
            //System.out.println("Two files have same content.");
        }
        else
        {
            /*
            System.out.println("Two files have different content. They differ at line "+lineNum);
            System.out.println("File1 has "+line1+" and File2 has "+line2+" at line "+lineNum);
            System.out.println("file1 "+path1+" file2: "+path2);
            */
        }
         
        reader1.close();
        reader2.close();
        return areEqual;
    }
}

